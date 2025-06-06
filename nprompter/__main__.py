import importlib
import os
import socketserver
import webbrowser
from http.server import SimpleHTTPRequestHandler
from pathlib import Path
from typing import Any, Optional

import typer

import nprompter
import nprompter.web
from nprompter.api.notion_client import NotionClient
from nprompter.cli.defaults import DEFAULT_OUTPUT_PATH, DEFAULT_PORT
from nprompter.cli.helpers import get_config
from nprompter.processing.processor import HtmlNotionProcessor

app = typer.Typer(add_completion=False)


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
        None, "--value", "-v", help="The value of the Notion's page property to filter by"
    ),
    sort_property: Optional[str] = typer.Option(
        None, "--sort", "-s", help="The name of the Notion's page property to sort documents by"
    ),
    configuration_file: Optional[Path] = typer.Option(
        None, "--config", "-c", help="A path to an appearance configuration file"
    ),
    custom_css: Optional[Path] = typer.Option(None, "--extra-css", "-s", help="A path to extra css configuration"),
    download_database: bool = typer.Option(
        True, "--download/--no-download", help="Whether to sync with the Notion's database"
    ),
):
    """
    Fetch a Notion database and create the teleprompter's pages from it
    """

    config_dict = get_config(configuration_file)

    if property_filter is not None:
        config_dict["build"]["filter"]["property"] = property_filter
    if property_value is not None:
        config_dict["build"]["filter"]["value"] = property_value
    if sort_property is not None:
        config_dict["build"]["sort"]["property"] = sort_property
    if database_id is not None:
        config_dict["build"]["database_id"] = database_id
    if output is not None:
        config_dict["build"]["output"] = str(output)
    if custom_css is not None:
        config_dict["build"]["custom_css"] = str(output)

    notion_version = os.getenv("NOTION_VERSION", nprompter.__notion_version__)

    notion_client = NotionClient(notion_api_key=notion_api_key, notion_version=notion_version)
    processor = HtmlNotionProcessor(notion_client, output_folder=output, configuration=config_dict)

    processor.prepare_folder(config_dict)

    if "custom_css" in config_dict["build"]:
        processor.add_extra_style(custom_css)

    if "databases" in config_dict["build"]:
        processor.process_databases(config_dict)
    elif download_database:
        processor.process_database(config_dict["build"]["database_id"], config=config_dict, index_at_root=True)


@app.command()
def serve(
    port: int = typer.Argument(DEFAULT_PORT),
    content_directory: Path = typer.Argument(DEFAULT_OUTPUT_PATH),
    browser: bool = typer.Option(True, help="Whether to open a web browser pointing to the server's address"),
):
    """
    Start a basic web server to display the teleprompter's pages.
    This a good option for a small scale deployment.
    """

    class CustomHandler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(content_directory), **kwargs)

        def log_message(self, format: str, *args: Any) -> None:
            pass

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", port), CustomHandler) as httpd:
        location = f"http://localhost:{port}"
        print(f"Serving at {location}")
        if browser:
            webbrowser.open(location)
        httpd.serve_forever()


@app.command()
def create_config(override: bool = False):
    config = importlib.resources.read_text(nprompter.web, nprompter.cli.defaults.DEFAULT_CONFIG_PATH)

    if not os.path.exists(nprompter.cli.defaults.DEFAULT_CONFIG_PATH) or override:
        with open(nprompter.cli.defaults.DEFAULT_CONFIG_PATH, "w") as writable:
            writable.write(config)
    else:
        print(
            f"The file {nprompter.cli.defaults.DEFAULT_CONFIG_PATH} "
            "already exists, call this program with the --override flag to override"
        )
