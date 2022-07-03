import os
import socketserver
import webbrowser
from http.server import SimpleHTTPRequestHandler
from typing import Any, Optional, Union

import typer

import nprompter
from nprompter.api.notion_client import NotionClient
from nprompter.processing.processor import HtmlNotionProcessor

app = typer.Typer(add_completion=False)

DEFAULT_PATH = ".content"


@app.command()
def build(
    database_id: str,
    content_directory: Union[str, None] = DEFAULT_PATH,
    property_filter: Optional[str] = "Status",
    property_value: Optional[str] = "Ready",
    just_assets: bool = False,
):
    notion_api_key = os.environ["NOTION_API_KEY"]
    notion_version = os.getenv("NOTION_VERSION", nprompter.__notion_version__)

    notion_client = NotionClient(notion_api_key=notion_api_key, notion_version=notion_version)
    processor = HtmlNotionProcessor(notion_client, output_folder=content_directory)

    processor.prepare_folder()

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
