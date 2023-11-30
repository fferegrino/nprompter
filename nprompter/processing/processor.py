import logging
import shutil
from pathlib import Path
from typing import Dict, Optional, Union

import pkg_resources
from jinja2 import Environment, PackageLoader, select_autoescape
from slugify import slugify

import nprompter
from nprompter.api.notion_client import NotionClient


class HtmlNotionProcessor:
    def __init__(
        self, notion_client: NotionClient, output_folder: Union[str, Path], configuration: Optional[Dict] = None
    ):
        self.notion_client = notion_client
        self.output_folder = Path(output_folder)
        self.env = Environment(
            loader=PackageLoader("nprompter", package_path="web/templates"), autoescape=select_autoescape()
        )
        self.assets_folder = Path(pkg_resources.resource_filename("nprompter", "web/assets/"))
        self.user_assets_folder = (
            Path(configuration["build"]["web_assets_folder"])
            if configuration["build"].get("web_assets_folder")
            else None
        )

        self.script_template = self.env.get_template("script.html")
        self.index_template = self.env.get_template("index.html")
        self.logger = logging.getLogger("NotionProcessor")
        self.configuration = configuration or {}
        self.custom_css = []

    def prepare_folder(self, configuration: Dict):
        if not self.output_folder.exists():
            self.output_folder.mkdir(parents=True)

        js_template = self.env.get_template("settings.js")
        css_template = self.env.get_template("nprompter.css")

        with open(self.output_folder / "settings.js", "w", encoding="utf8") as writeable:
            writeable.write(js_template.render(**configuration))

        with open(self.output_folder / "nprompter.css", "w", encoding="utf8") as writeable:
            writeable.write(css_template.render(**configuration))

        shutil.copytree(self.assets_folder, self.output_folder, dirs_exist_ok=True)
        if self.user_assets_folder and self.user_assets_folder.exists():
            shutil.copytree(self.user_assets_folder, self.output_folder, dirs_exist_ok=True)

    def add_extra_style(self, path: Path):
        self.custom_css.append(path.name)
        shutil.copy(path, self.output_folder)

    def process_databases(self, database_id: str, config: Dict):
        db = self._process_single_database(database_id, config)

        content = self.index_template.render(databases=[db], version=nprompter.__version__, custom_css=self.custom_css)
        with open(self.output_folder / "index.html", "w", encoding="utf8") as writeable:
            writeable.write(content)

    def _process_single_database(self, database_id: str, config: Dict):
        database = self.notion_client.get_database(database_id)
        pages = self.notion_client.get_pages(
            database_id=database_id,
            property_filter=config["build"]["filter"]["property"],
            property_value=config["build"]["filter"]["value"],
        )
        # Create database folder
        (self.output_folder / database_id).mkdir(exist_ok=True)
        database_dict = {"title": database["title"][0]["plain_text"], "scripts": []}

        sort_property = config["build"]["sort"]["property"]
        sort_property_definition = database["properties"][sort_property]
        sort_property_type = sort_property_definition["type"]
        if sort_property_type in ["title", "rich_text"]:
            pages = sorted(
                pages,
                key=lambda x: x["properties"][sort_property][sort_property_type][0]["plain_text"],
            )

        for page in pages:
            database_dict["scripts"].append(self.process_page(database_id, page))
        return database_dict

    def process_page(self, database_id: str, page: dict):
        title = page["properties"]["Name"]["title"][0]["text"]["content"]
        title_slug = slugify(title)
        blocks = self.notion_client.get_blocks(page["id"])
        block_contents = self.process_blocks(blocks)
        content = self.script_template.render(
            elements=block_contents, title=title, version=nprompter.__version__, custom_css=self.custom_css
        )

        file_name = Path(self.output_folder, database_id, f"{title_slug}.html")
        with open(file_name, "w", encoding="utf8") as writeable:
            writeable.write(content)

        from_root_path = f"{database_id}/{title_slug}.html"
        return {"title": title, "path": from_root_path}

    def process_blocks(self, blocks):
        block_contents = []

        bulleted_list_item = False
        numbered_list_item = False
        for block in blocks:
            block_type = block["type"]

            # Control for lists
            if block_type == "bulleted_list_item" and not bulleted_list_item:
                block_contents.append("<ul>")
                bulleted_list_item = True
            elif block_type != "bulleted_list_item" and bulleted_list_item:
                block_contents.append("</ul>")

            if block_type == "numbered_list_item" and not numbered_list_item:
                block_contents.append("<ol>")
                numbered_list_item = True
            elif block_type != "numbered_list_item" and numbered_list_item:
                block_contents.append("</ol>")

            if block_type == "paragraph":
                if data := self.process_paragraph(block, "paragraph", "p"):
                    block_contents.append(data)
            elif block_type == "quote" or block_type == "callout":
                if data := self.process_paragraph(block, block_type, "blockquote"):
                    block_contents.append(data)
            elif block_type == "bulleted_list_item" or block_type == "numbered_list_item":
                if data := self.process_paragraph(block, block_type, "li"):
                    block_contents.append(data)
            elif block_type.startswith("heading_"):
                size = block_type[-1]
                if data := self.process_paragraph(block, block_type, f"h{size}"):
                    block_contents.append(data)
            elif block_type == "equation":
                expression = block["equation"]["expression"]
                block_contents.append(f"<p>${expression}$</p>")
            elif block_type == "divider":
                if self.configuration["processor"]["skip_on_break"]:
                    self.logger.info("Found divider, stopping block processing")
                    break
                else:
                    block_contents.append("<hr />")
            elif block_type == "code":
                if self.configuration["processor"]["render_code"] == "skip":
                    self.logger.info("Found code block, don't render")
                elif self.configuration["processor"]["render_code"] == "placeholder":
                    block_contents.append("<p>⚠ Code block ⚠</p>")
                elif self.configuration["processor"]["render_code"] == "render":
                    block_contents.append("<pre>")
                    block_contents.append(block["code"]["rich_text"][0]["plain_text"])
                    block_contents.append("</pre>")
                else:
                    self.logger.warning("Invalid configuration for render_code")
            else:
                block_contents.append(f"<p>⚠ {block['type']} ⚠</p>")
                block_contents.append(f"<!-- Block of type {block['type']} is not currently supported by Nprompter -->")
                self.logger.warning(f"Block of type {block['type']} is not currently supported by Nprompter")

        return block_contents

    def process_paragraph(self, block, block_type, tag_name):
        notion_color = block[block_type].get("color", "default")
        base_classes = [block_type, f"notion-{notion_color}"]
        if notion_color != "default" and self.configuration["processor"]["hide_colors"]:
            base_classes.append("notion-hide")
        contents = block[block_type].get("text", block[block_type].get("rich_text", []))
        paragraph_content_tags = []
        for content in contents:
            if text := content.get("text"):
                text_content = text["content"].replace("\n", "<br />")
                annotations = content["annotations"]
                annotations_tags = ["bold", "italic", "strikethrough", "underline", "code"]
                classes = " ".join(base_classes + [tag for tag in annotations_tags if annotations.get(tag)])
                tag = f'<span class="{classes}">{text_content}</span>'
                paragraph_content_tags.append(tag)
            elif equation := content.get("equation"):
                paragraph_content_tags.append(f'${equation["expression"]}$')
        if paragraph_content_tags:
            paragraph_content = "".join(paragraph_content_tags)
            return f"<{tag_name}>{paragraph_content}</{tag_name}>"
        return None
