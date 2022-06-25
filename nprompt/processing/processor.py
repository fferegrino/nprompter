from nprompt.api.notion_client import NotionClient


class HtmlNotionProcessor:

    def __init__(self, notion_client: NotionClient):
        self.notion_client=notion_client

    def process_database(self, database_id: str):
        database = self.notion_client.get_database(database_id)
        pages = self.notion_client.get_pages(database_id, 'Ready')


        blocks = self.notion_client.get_blocks(pages[0]['id'])

        for block in blocks:
            print(block['type'])
        pass