import importlib
import os
import socketserver
import webbrowser
from http.server import SimpleHTTPRequestHandler
from pathlib import Path
from typing import Any, Optional

import tomli
import typer
from jinja2 import TemplateError
from requests import RequestException

import nprompter
import nprompter.web
from nprompter.api.notion_client import NotionClient
from nprompter.cli.defaults import DEFAULT_OUTPUT_PATH, DEFAULT_PORT
from nprompter.cli.helpers import get_config
from nprompter.cli.output import (
    VerbosityLevel,
    debug,
    error,
    info,
    parse_verbosity,
    progress,
    set_verbosity,
    success,
    verbose,
    warning,
)
from nprompter.processing.processor import HtmlNotionProcessor

app = typer.Typer(add_completion=False)


def _build_phase_error(phase: str, exc: Exception) -> None:
    """Log a build failure with phase context and exception type (not only when --verbose)."""
    error(f"{phase}: {type(exc).__name__}: {exc}", err=exc)


@app.command()
def build(
    database_id: str = typer.Argument(default=None, help="The Notion's database to process"),
    notion_api_key: str = typer.Argument(None, envvar="NOTION_API_KEY", help="The Notion API key to use"),
    output: Optional[Path] = typer.Option(
        DEFAULT_OUTPUT_PATH, "--output", "-o", help="Where the output should be written"
    ),
    property_filter: Optional[str] = typer.Option(
        None, "--filter", "-f", help="The name of the Notion's page property to filter by"
    ),
    property_value: Optional[str] = typer.Option(
        None, "--value", help="The value of the Notion's page property to filter by"
    ),
    sort_property: Optional[str] = typer.Option(
        None, "--sort", "-s", help="The name of the Notion's page property to sort documents by"
    ),
    configuration_file: Optional[Path] = typer.Option(
        None, "--config", "-c", help="A path to an appearance configuration file"
    ),
    custom_css: Optional[Path] = typer.Option(None, "--extra-css", help="A path to extra css configuration"),
    download_database: bool = typer.Option(
        True, "--download/--no-download", help="Whether to sync with the Notion's database"
    ),
    quiet: bool = typer.Option(False, "--quiet", "-q", help="Suppress all output except errors"),
    verbose_count: int = typer.Option(
        0, "--verbose", "-v", count=True, help="Increase verbosity (use -v, -vv, or -vvv)"
    ),
):
    """
    Fetch a Notion database and create the teleprompter's pages from it
    """
    # Set verbosity level
    verbosity = parse_verbosity(quiet, verbose_count)
    set_verbosity(verbosity)

    debug(f"Starting build with verbosity level: {verbosity.name}")
    debug(f"Output directory: {output}")
    debug(f"Configuration file: {configuration_file}")

    try:
        config_dict = get_config(configuration_file)
    except tomli.TOMLDecodeError as e:
        _build_phase_error("Configuration file has invalid TOML syntax", e)
        raise typer.Exit(code=1)
    except OSError as e:
        _build_phase_error("Could not read the configuration file", e)
        raise typer.Exit(code=1)

    try:
        if property_filter is not None:
            config_dict["build"]["filter"]["property"] = property_filter
            verbose(f"Using filter property: {property_filter}")
        if property_value is not None:
            config_dict["build"]["filter"]["value"] = property_value
            verbose(f"Using filter value: {property_value}")
        if sort_property is not None:
            config_dict["build"]["sort"]["property"] = sort_property
            verbose(f"Using sort property: {sort_property}")
        if database_id is not None:
            config_dict["build"]["database_id"] = database_id
            verbose(f"Processing database: {database_id}")
        if output is not None:
            config_dict["build"]["output"] = str(output)
        if custom_css is not None:
            config_dict["build"]["custom_css"] = str(custom_css)
            verbose(f"Using custom CSS: {custom_css}")
    except KeyError as e:
        _build_phase_error(
            "Configuration is missing a required section or key (expected [build] with filter and sort)",
            e,
        )
        raise typer.Exit(code=1)

    notion_version = os.getenv("NOTION_VERSION", nprompter.__notion_version__)
    debug(f"Using Notion API version: {notion_version}")

    try:
        progress("Connecting to Notion API...")
        notion_client = NotionClient(notion_api_key=notion_api_key, notion_version=notion_version)
        processor = HtmlNotionProcessor(notion_client, output_folder=output, configuration=config_dict)
    except KeyError as e:
        _build_phase_error("Configuration is missing keys required to initialize the processor", e)
        raise typer.Exit(code=1)

    try:
        progress("Preparing output folder...")
        processor.prepare_folder(config_dict)
        verbose(f"Output folder prepared: {output}")
    except OSError as e:
        _build_phase_error("Could not create the output folder or write static assets", e)
        raise typer.Exit(code=1)
    except TemplateError as e:
        _build_phase_error("Template rendering failed while preparing the output folder", e)
        raise typer.Exit(code=1)

    if "custom_css" in config_dict["build"]:
        try:
            progress("Adding custom CSS...")
            processor.add_extra_style(custom_css)
        except OSError as e:
            _build_phase_error("Could not copy the custom CSS file into the output folder", e)
            raise typer.Exit(code=1)

    try:
        if "databases" in config_dict["build"]:
            progress("Processing multiple databases...")
            processor.process_databases(config_dict)
            success("Successfully processed all databases")
        elif download_database:
            db_id = config_dict["build"]["database_id"]
            progress(f"Processing database: {db_id}")
            processor.process_database(db_id, config=config_dict, index_at_root=True)
            success(f"Successfully processed database: {db_id}")
        else:
            info("Skipping database download (--no-download flag set)")
    except RequestException as e:
        _build_phase_error("Network or HTTP error while calling the Notion API", e)
        raise typer.Exit(code=1)
    except ValueError as e:
        _build_phase_error("Notion API returned an error or the response could not be parsed", e)
        raise typer.Exit(code=1)
    except (KeyError, IndexError) as e:
        _build_phase_error("Could not interpret Notion page or database data (structure mismatch)", e)
        raise typer.Exit(code=1)
    except OSError as e:
        _build_phase_error("Could not write generated HTML files", e)
        raise typer.Exit(code=1)
    except TemplateError as e:
        _build_phase_error("Template rendering failed while generating pages", e)
        raise typer.Exit(code=1)


@app.command()
def serve(
    port: int = typer.Argument(DEFAULT_PORT),
    content_directory: Path = typer.Argument(DEFAULT_OUTPUT_PATH),
    browser: bool = typer.Option(True, help="Whether to open a web browser pointing to the server's address"),
    quiet: bool = typer.Option(False, "--quiet", "-q", help="Suppress all output except errors"),
    verbose_count: int = typer.Option(
        0, "--verbose", "-v", count=True, help="Increase verbosity (use -v, -vv, or -vvv)"
    ),
):
    """
    Start a basic web server to display the teleprompter's pages.
    This a good option for a small scale deployment.
    """
    # Set verbosity level
    verbosity = parse_verbosity(quiet, verbose_count)
    set_verbosity(verbosity)

    debug(f"Starting server with verbosity level: {verbosity.name}")
    debug(f"Port: {port}")
    debug(f"Content directory: {content_directory}")

    if not content_directory.exists():
        error(f"Content directory does not exist: {content_directory}")
        raise typer.Exit(code=1)

    class CustomHandler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(content_directory), **kwargs)

        def log_message(self, format: str, *args: Any) -> None:
            # Only log HTTP requests in verbose mode
            if verbosity >= VerbosityLevel.VERBOSE:
                debug(f"HTTP {format % args}")

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", port), CustomHandler) as httpd:
        location = f"http://localhost:{port}"
        info(f"Serving at {location}")
        verbose(f"Content directory: {content_directory}")
        if browser:
            verbose("Opening browser...")
            webbrowser.open(location)
        else:
            verbose("Browser opening disabled")
        info("Press Ctrl+C to stop the server")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            info("\nServer stopped")


@app.command()
def create_config(
    override: bool = typer.Option(False, "--override", help="Override existing configuration file"),
    quiet: bool = typer.Option(False, "--quiet", "-q", help="Suppress all output except errors"),
    verbose_count: int = typer.Option(
        0, "--verbose", "-v", count=True, help="Increase verbosity (use -v, -vv, or -vvv)"
    ),
):
    """
    Create a default configuration file.
    """
    # Set verbosity level
    verbosity = parse_verbosity(quiet, verbose_count)
    set_verbosity(verbosity)

    config_path = nprompter.cli.defaults.DEFAULT_CONFIG_PATH
    debug(f"Creating config file: {config_path}")

    config = importlib.resources.read_text(nprompter.web, nprompter.cli.defaults.DEFAULT_CONFIG_PATH)

    if not os.path.exists(config_path) or override:
        with open(config_path, "w") as writable:
            writable.write(config)
        success(f"Configuration file created: {config_path}")
        verbose(f"File location: {os.path.abspath(config_path)}")
    else:
        warning(f"The file {config_path} already exists. " "Use the --override flag to replace it.")
        raise typer.Exit(code=1)
