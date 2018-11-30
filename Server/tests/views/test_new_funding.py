import re
import pytest
from datetime import datetime, timedelta

from app.models import Funding

# type hinting
from flask import Response
from typing import Dict


class TestNewFunding:
    def test_verify(self, flask_client, session):
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

        self.verification_code = session.query(Funding).first().code

    def test_new(self, flask_client, idea):
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

        ), content_type='multipart/form-data',  headers={'Authorization':self.verification_code})

        # default response check
        assert "application/json" == res.content_type
        assert 201 == res.status_code

        # HATEOAS check
        links: Dict[str] = res.data["links"]

        assert "/api/v1/funding/new" == links["makeFunding.new"]

        idea_instance_url_regex = re.compile(r"[/]api[/]v1[/]funding[/]\d")
        assert re.match(idea_instance_url_regex, links["funding.item.instance"])

        r = re.compile(r"[/]\d")
        self.my_funding_id = re.search(r, links["funding.item.instance"].group()[1:])

    def test_upload_check(self, flask_client):
        res: Response = flask_client.get('/api/v1/funding/{}'.format(self.my_funding_id))

        # default response check
        assert "application/json" == res.content_type
        assert 201 == res.status_code

        # HATEOAS check
        links: Dict[str] = res.data["links"]

        idea_instance_url_regex = re.compile(r"[/]api[/]v1[/]funding[/]\d")
        assert re.match(idea_instance_url_regex, links["self"])

        # data check
        data: Dict[str] = res.data

        assert "bulletproof raincoat!" == data["title"]
        assert "ability of withstand .50 BMG" == data["body"]
        assert str(datetime.date(datetime.now() + timedelta(days=10))) == data["expiration"]
        assert 1000000000 == data["goal"]
        assert isinstance(list, data["tag"])
        assert isinstance(list, data["referenced_ideas"])
        static_url_regex = re.compile(r"[/]static[/][a-zA-Z0-9]+[.][pngjpg]+")
        assert re.match(static_url_regex, data["title_image_path"])
        assert re.match(static_url_regex, data["cover_image_path"])
        assert re.match(static_url_regex, data["header_image_paths"][0])