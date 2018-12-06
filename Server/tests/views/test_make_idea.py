import re
import pytest

from app.models import Idea

# type hinting
from flask import Response
from typing import Dict


class TestShareIdea:
    def test_verify(self, flask_client, session):
        res: Response = flask_client.post("/api/v1/idea/new/verify", data=dict(
            email="artoria@artoria.us",
            host="lewis kim"
        ))

        # default response check
        assert "application/json" == res.headers["Content-Type"]
        assert 201 == res.status_code

        # HATEOAS check
        links: Dict[str] = res.data["links"]

        assert "/api/v1/idea/new" == links["continue"]

    def test_share(self, flask_client, idea_base):
        res: Response = flask_client.post("/api/v1/idea/new", data=dict(
            title="bulletproof raincoat",
            body="how about bulletproof raincoat?",
        ), content_type='application/json',  headers={'Authorization': idea_base.code})

        # default response check
        assert "application/json" == res.content_type
        assert 201 == res.status_code

        # HATEOAS check
        links: Dict[str] = res.data["links"]

        idea_instance_url_regex: re.Match = re.compile(r"[/]api[/]v1[/]idea[/]\d")
        assert re.match(idea_instance_url_regex, links["location"])
