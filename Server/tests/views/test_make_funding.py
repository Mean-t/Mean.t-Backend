import re
import pytest
from datetime import datetime, timedelta

from tests.data_fixtures import idea, funding_base
from app.models import Funding

# type hinting
from flask import Response
from typing import Dict


class TestMakeFunding:
    def test_verify(self, flask_client):
        res: Response = flask_client.post("/api/v1/funding/new/verify", data=dict(
            email="artoria@artoria.us",
            host="lewis kim"
        ))

        # default response check
        assert "application/json" == res.headers["Content-Type"]
        assert 201 == res.status_code

        # HATEOAS check
        links: Dict[str] = res.data["links"]

        assert "api/v1/funding/new/verify" == links["makeFunding.verify"]
        assert "/api/v1/funding/new" == links["makeFunding.new"]

    def test_new(self, flask_client, idea, funding_base):
        from io import BytesIO

        res: Response = flask_client.post("/api/v1/funding/new", data=dict(
            title="bulletproof raincoat!",
            body="ability of withstand .50 BMG",
            expiration=datetime.date(datetime.now() + timedelta(days=10)),
            goal=1000000000,
            referenced_ideas=[1],
            tag=["raincoat", "safe", "bulletproof"],
            title_image=BytesIO(b"asdfqwerzxcv", "raincoat_title_img.png"),
            cover_image=BytesIO(b"qwerzxcvasdf", "raincoat_cove.jpg"),
            header_images={BytesIO(b"zxcvqwerasdf", "1.jpg"),
                           BytesIO(b"zxcvqwerasdf", "2.jpg"),
                           BytesIO(b"zxcvqwerasdf", "3.jpg")}

        ), content_type='multipart/form-data',  headers={'Authorization': funding_base.code})

        # default response check
        assert "application/json" == res.content_type
        assert 201 == res.status_code

        # HATEOAS check
        links: Dict[str] = res.data["links"]

        assert "/api/v1/funding/new" == links["makeFunding.new"]

        idea_instance_url_regex: re.Match = re.compile(r"[/]api[/]v1[/]funding[/]\d")
        assert re.match(idea_instance_url_regex, links["funding.item.instance"])
