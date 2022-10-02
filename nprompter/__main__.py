import importlib
import os
import socketserver
import webbrowser
from http.server import SimpleHTTPRequestHandler
from pathlib import Path
from typing import Any, Optional, Union

import typer

import nprompter
import nprompter.web
from nprompter.api.notion_client import NotionClient
from nprompter.cli.helpers import get_config
from nprompter.processing.processor import HtmlNotionProcessor

app = typer.Typer(add_completion=False)

DEFAULT_PATH = ".content"


@app.command()
def build(
    database_id: str,
    content_directory: Union[str, None] = DEFAULT_PATH,
    property_filter: Optional[str] = "Status",
    property_value: Optional[str] = "Ready",
    config: Optional[Path] = typer.Option("config.toml"),
    custom_css: Optional[Path] = typer.Option(None),
    just_assets: bool = False,
):
    notion_api_key = os.environ["NOTION_API_KEY"]
    notion_version = os.getenv("NOTION_VERSION", nprompter.__notion_version__)

    notion_client = NotionClient(notion_api_key=notion_api_key, notion_version=notion_version)
    processor = HtmlNotionProcessor(notion_client, output_folder=content_directory)

    config_dict = get_config(config)
    processor.prepare_folder(config_dict)

    if custom_css:
        processor.add_extra_style(custom_css)

    if not just_assets:
        processor.process_databases(database_id, property_filter, property_value)


@app.command()
def serve(port: int = 8889, content_directory: Union[str, None] = DEFAULT_PATH):
    class CustomHandler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=content_directory, **kwargs)

        def log_message(self, format: str, *args: Any) -> None:
            pass

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", port), CustomHandler) as httpd:
        location = f"http://localhost:{port}"
        print(f"Serving at {location}")
        webbrowser.open(location)
        httpd.serve_forever()


@app.command()
def create_config(override: bool = False):
    config = importlib.resources.read_text(nprompter.web, "config.toml")

    if not os.path.exists("config.toml") or override:
        with open("config.toml", "w") as writable:
            writable.write(config)
    else:
        print("The file config.toml already exists, call this program with the --override flag to override")
