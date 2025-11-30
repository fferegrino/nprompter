from typing import Dict, List, Tuple

import requests


def build_filter_query(properties: List[Tuple[str, str, str]]) -> Dict:
    """
    Builds a query to filter for pages with the properties specified as triplets

    :param properties: A list of triplets containing (property, condition, value)
    :return:
    """

    or_conditions = [
        {"property": property_name, "status": {condition: value}} for property_name, condition, value in properties
    ]

    return {"filter": {"or": or_conditions}}


class NotionClient:
    def __init__(self, notion_api_key: str, notion_version: str):
        self.headers = {
            "Authorization": f"Bearer {notion_api_key}",
            "Notion-Version": notion_version,
        }

    def get_data_source_from_database(self, database_id: str) -> Dict:
        database = requests.get(
            f"https://api.notion.com/v1/databases/{database_id}",
            headers=self.headers,
        ).json()

        if data_sources := database.get("data_sources"):
            if len(data_sources) > 1:
                # TODO: Handle multiple data sources
                pass
            data_source_id = data_sources[0]["id"]
        else:
            raise ValueError(f"Database {database_id} has no data sources")

        data_source = requests.get(
            f"https://api.notion.com/v1/data_sources/{data_source_id}",
            headers=self.headers,
        ).json()
        if data_source.get("object") == "error":
            raise ValueError(f"{data_source['code']} - {data_source['message']}")
        return data_source

    def get_pages(self, data_source_id: str, property_filter: str, property_value: str) -> List[Dict]:
        query = build_filter_query([(property_filter, "equals", property_value)])
        database = requests.post(
            f"https://api.notion.com/v1/data_sources/{data_source_id}/query",
            json=query,
            headers=self.headers,
        ).json()

        if database.get("object") == "error":
            raise ValueError(f"{database['code']} - {database['message']}")

        return database["results"]

    def get_blocks(self, page_id: str) -> List[Dict]:
        blocks = []
        page = requests.get(
            f"https://api.notion.com/v1/blocks/{page_id}/children",
            headers=self.headers,
        ).json()
        blocks.extend(page["results"])

        while start_cursor := page.get("next_cursor", None):
            page = requests.get(
                f"https://api.notion.com/v1/blocks/{page_id}/children",
                params={"start_cursor": start_cursor},
                headers=self.headers,
            ).json()
            blocks.extend(page["results"])
        return blocks
