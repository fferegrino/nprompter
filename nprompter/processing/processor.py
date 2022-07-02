import shutil
from pathlib import Path
from typing import Union
import logging
import pkg_resources
from jinja2 import PackageLoader, select_autoescape, Environment

from nprompter.api.notion_client import NotionClient
from slugify import slugify


class HtmlNotionProcessor:
    def __init__(self, notion_client: NotionClient, output_folder: Union[str, Path]):
        self.notion_client = notion_client
        self.output_folder = Path(output_folder)
        env = Environment(
            loader=PackageLoader("nprompter", package_path="web/templates"), autoescape=select_autoescape()
        )
        self.assets_folder = Path(pkg_resources.resource_filename("nprompter", "web/assets/"))
        self.script_template = env.get_template("script.html")
        self.index_template = env.get_template("index.html")
        self.logger = logging.getLogger("NotionProcessor")

    def prepare_folder(self):
        if not self.output_folder.exists():
            self.output_folder.mkdir(parents=True)
        shutil.copytree(self.assets_folder, self.output_folder, dirs_exist_ok=True)

    def process_database(self, database_id: str):
        db = self._process_single_database(database_id)

        content = self.index_template.render(databases=[db])
        with open(self.output_folder / "index.html", "w", encoding="utf8") as writeable:
            writeable.write(content)

    def _process_single_database(self, database_id):
        database = self.notion_client.get_database(database_id)
        pages = self.notion_client.get_pages(database_id, "Ready")
        # Create database folder
        (self.output_folder / database_id).mkdir(exist_ok=True)
        database_dict = {"title": database["title"][0]["plain_text"], "scripts": []}
        for page in pages:
            database_dict["scripts"].append(self.process_page(database_id, page))
        return database_dict

    def process_page(self, database_id: str, page: dict):
        title = page["properties"]["Name"]["title"][0]["text"]["content"]
        title_slug = slugify(title)
        blocks = self.notion_client.get_blocks(page["id"])
        block_contents = self.process_blocks(blocks)
        content = self.script_template.render(elements=block_contents, title=title)

        file_name = Path(self.output_folder, database_id, f"{title_slug}.html")
        with open(file_name, "w", encoding="utf8") as writeable:
            writeable.write(content)

        from_root_path = f"{database_id}/{title_slug}.html"
        return {"title": title, "path": from_root_path}

    processable_blocks = {"paragraph", *[f"heading_{idx}" for idx in range(1, 7)]}

    def process_blocks(self, blocks):
        block_contents = []
        for block in blocks:
            block_type = block["type"]
            if block_type == "paragraph":
                if data := self.process_paragraph(block, "paragraph", "p"):
                    block_contents.append(data)
            elif block_type.startswith("heading_"):
                size = block_type[-1]
                if data := self.process_paragraph(block, block_type, f"h{size}"):
                    block_contents.append(data)
            else:
                self.logger.warning(f"Block of type {block['type']} is not currently supported by Nprompter")
                # breakpoint()
                continue

        return block_contents

    def process_paragraph(self, block, block_type, tag_name):
        contents = block[block_type].get("text", block[block_type].get("rich_text", []))
        paragraph_content_tags = []
        for content in contents:
            if text := content.get("text"):
                text_content = text["content"]
                annotations = content["annotations"]
                annotations_tags = ["bold", "italic", "strikethrough", "underline"]
                classes = " ".join([block_type] + [tag for tag in annotations_tags if annotations.get(tag)])
                tag = f'<span class="{classes}">{text_content}</span>'
                paragraph_content_tags.append(tag)
        if paragraph_content_tags:
            paragraph_content = "".join(paragraph_content_tags)
            return f"<{tag_name}>{paragraph_content}</{tag_name}>"
        return None
