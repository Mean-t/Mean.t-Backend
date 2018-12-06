import re
import pytest

from tests.data_fixtures import funding
from app.models import Funding

# type hinting
from flask import Response
from typing import Dict, List


class TestSearch:
    def test_search(self, flask_client, funding) -> None:
        res: Response = flask_client.get("/api/v1/funding/search")

        # default response check
        assert "application/json" == res.headers["Content-Type"]
        assert 200 == res.status_code

        # data check
        assert isinstance(list, res.data["fundings"])
        assert isinstance(dict, res.data["fundings"][0])

        funding_list: List[Dict[str]] = res.data["fundings"]
        funding_instance: Dict[str] = funding_list[0]

        assert funding_instance["email"] == funding.email
        assert funding_instance["title"] == funding.title
        assert funding_instance["tag"] == [tag.title for tag in funding.tag]

        # instance HATEOAS check
        assert isinstance(funding_instance["links"], dict)

        links: Dict[str] = funding_instance["links"]

        link_regex = re.compile(r"[/]api[/]v1[/]funding[/]\d")
        assert re.match(link_regex, links["self"])

    def test_view_specific_funding(self, flask_client, funding) -> None:
        funding_instance_link: str = flask_client.get("/api/v1/funding/search").data["fundings"][0]["links"]["self"]
        res: Response = flask_client.get(funding_instance_link)

        # default response check
        assert "application/json" == res.headers["Content-Type"]
        assert 200 == res.status_code

        # HATEOAS check
        links: Dict[str] = res.data["links"]

        assert funding_instance_link == links["self"]
        assert funding_instance_link + "/order/verify" == links["order"]

        # data check
        assert isinstance(dict, res.data)

        funding_data: Dict[str] = res.data

        assert funding_data["email"] == funding.email
        assert funding_data["host"] == funding.host
        assert funding_data["title"] == funding.title
        assert funding_data["tag"] == [tag.title for tag in funding.tag]
        assert funding_data["body"] == funding.body
        assert funding_data["title_img_path"] == funding.title_image
        assert funding_data["cover_img_path"] == funding.cover_image
        assert funding_data["header_img_paths"] == funding.header_image_paths.split("%")
