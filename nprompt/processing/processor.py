from nprompt.api.notion_client import NotionClient


class HtmlNotionProcessor:
    def __init__(self, notion_client: NotionClient):
        self.notion_client = notion_client

    def process_database(self, database_id: str):
        database = self.notion_client.get_database(database_id)
        pages = self.notion_client.get_pages(database_id, "Ready")
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
                    tag = f'<span class="{classes}">{text_content}<span>'
                    paragraph_content_tags.append(tag)
            paragraph_content = "".join(paragraph_content_tags)

            block_contents.append(f"<p>{paragraph_content}</p>")
