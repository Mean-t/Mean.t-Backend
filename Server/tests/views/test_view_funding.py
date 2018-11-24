import re
import pytest

from tests.data_fixtures import funding
from app.models import Funding

# type hinting
from flask import Response
from typing import Dict, List


class TestViewFunding:
    def test_view_funding_list(self, flask_client, funding) -> None:
        res: Response = flask_client.get("/api/v1/funding")

        # default response check
        assert "application/json" == res.headers["Content-Type"]
        assert 201 == res.status_code

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

    def test_view_specific_funding(self, flask_client, funding: Funding) -> None:
        res: Response = flask_client.get('/api/v1/funding/{}'.format(funding.funding_id))

        # default response check
        assert "application/json" == res.headers["Content-Type"]
        assert 201 == res.status_code

        # HATEOAS check
        links: Dict[str] = res.data["links"]

        assert self.funding_instance_link == links["self"]
        assert self.funding_instance_link + "/order" == links["order"]

        # data check
        assert isinstance(dict, res.data)

        res_data: Dict[str] = res.data

        assert funding.email == res_data["email"]
        assert funding.host == res_data["host"]
        assert funding.title == res_data["title"]
        assert isinstance(res_data["tag"], list)
        assert [tag.title for tag in funding.tag] == res_data["tag"]
        assert funding.body == res_data["body"]
        assert funding.title_img_path == res_data["title_image"]
        assert funding.cover_img_path == res_data["cover_image"]
        assert funding.header_img_paths.split("%") == res_data["header_image_paths"]
