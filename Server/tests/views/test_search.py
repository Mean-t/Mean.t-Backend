import re
import pytest

from tests.data_fixtures import funding
from app.models import Funding

# type hinting
from flask import Response
from typing import Dict, List


class TestSearch:
    funding_data: Funding
    funding_instance_link: str

    def test_search(self, flask_client, funding) -> None:
        res: Response = flask_client.get("/api/v1/funding/search")

        # default response check
        assert "application/json" == res.headers["Content-Type"]
        assert 200 == res.status_code

        # HATEOAS check
        links: Dict[str] = res.data["links"]

        assert "/api/v1/funding" == links["funding"]

        # data check
        assert isinstance(list, res.data["fundings"])
        assert isinstance(dict, res.data["fundings"][0])

        funding_list: List[Dict[str]] = res.data["fundings"]
        funding_instance: Dict[str] = funding_list[0]

        assert "artoria@artoria.us" == funding_instance["email"]
        assert "raincoat" == funding_instance["title"]
        assert isinstance(funding_instance["tag"], list)
        assert "raincoat" == funding_instance["tag"][0]

        # instance HATEOAS check
        assert isinstance(funding_instance["links"], dict)

        links: Dict[str] = funding_instance["links"]

        link_regex = re.compile(r"[/]api[/]v1[/]funding[/]\d")
        assert re.match(link_regex, links["self"])

        self.funding_instance_link: str = links["self"]
        self.funding_data = funding

    def test_view_specific_funding(self, flask_client) -> None:
        res: Response = flask_client.get(self.funding_instance_link)

        # default response check
        assert "application/json" == res.headers["Content-Type"]
        assert 201 == res.status_code

        # HATEOAS check
        links: Dict[str] = res.data["links"]

        assert self.funding_instance_link == links["self"]
        assert self.funding_instance_link + "/order" == links["order"]

        # data check
        assert isinstance(dict, res.data)

        funding: Dict[str] = res.data

        assert self.funding_data.email == funding["email"]
        assert self.funding_data.host == funding["host"]
        assert self.funding_data.title == funding["title"]
        assert isinstance(funding["tag"], list)
        assert [tag.title for tag in self.funding_data.tag] == funding["tag"]
        assert self.funding_data.body == funding["body"]
        assert self.funding_data.title_img_path == funding["title_image"]
        assert self.funding_data.cover_img_path == funding["cover_image"]
        assert self.funding_data.header_img_paths.split("%") == funding["header_image_paths"]
