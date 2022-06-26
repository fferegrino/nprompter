import click
from typing import Any, Union
import os

import typer
from nprompter.api.notion_client import NotionClient
from nprompter.processing.processor import HtmlNotionProcessor


app = typer.Typer(add_completion=False)
def cli():
    pass

DEFAULT_PATH = ".content"


@app.command()
def build(database_id: str, content_directory: Union[str, None] = DEFAULT_PATH):
    notion_api_key = os.environ["NOTION_API_KEY"]
    notion_version = os.environ["NOTION_VERSION"]

    notion_client = NotionClient(notion_api_key=notion_api_key, notion_version=notion_version)
    processor = HtmlNotionProcessor(notion_client, output_folder=content_directory)
    processor.process_database(database_id)
