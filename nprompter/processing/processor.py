from pathlib import Path

from jinja2 import PackageLoader, select_autoescape, Environment

from nprompter.api.notion_client import NotionClient
from slugify import slugify


class HtmlNotionProcessor:
    def __init__(self, notion_client: NotionClient):
        self.notion_client = notion_client
        self.output_folder = Path(".content")
        env = Environment(loader=PackageLoader("nprompter"), autoescape=select_autoescape())
        self.script_template = env.get_template("script.html")

        if not self.output_folder.exists():
            self.output_folder.mkdir(parents=True)

    def process_database(self, database_id: str):
        database = self.notion_client.get_database(database_id)
        pages = self.notion_client.get_pages(database_id, "Ready")

        title = pages[0]["properties"]["Name"]["title"][0]["text"]["content"]
        title_slug = slugify(title)

        blocks = self.notion_client.get_blocks(pages[0]["id"])

        block_contents = []
        for block in blocks:
            if block["type"] != "paragraph":
                continue

            paragraph_content_tags = []
            for content in block["paragraph"]["text"]:
                if text := content.get("text"):
                    text_content = text["content"]
                    annotations = content["annotations"]
                    annotations_tags = ["bold", "italic", "strikethrough", "underline"]
                    classes = " ".join(["paragraph"] + [tag for tag in annotations_tags if annotations.get(tag)])
                    tag = f'<span class="{classes}">{text_content}</span>'
                    paragraph_content_tags.append(tag)
            paragraph_content = "".join(paragraph_content_tags)

            block_contents.append(f"<p>{paragraph_content}</p>")

        content = self.script_template.render(elements=block_contents, title=title)

        file_name = Path(self.output_folder, f"{title_slug}.html")
        with open(file_name, "w", encoding="utf8") as writeable:
            writeable.write(content)
