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

        assert "api/v1/idea/new/verify" == links["shareIdea.verify"]
        assert "/api/v1/idea/new" == links["shareIdea.new"]

        self.verification_code = session.query(Idea).first().code

    def test_share(self, flask_client):
        res: Response = flask_client.post("/api/v1/idea/new", data=dict(
            title="bulletproof raincoat",
            body="how about bulletproof raincoat?",
        ), content_type='application/json',  headers={'Authorization': self.verification_code})

        # default response check
        assert "application/json" == res.content_type
        assert 201 == res.status_code

        # HATEOAS check
        links: Dict[str] = res.data["links"]

        assert "/api/v1/idea/new" == links["shareIdea.new"]

        idea_instance_url_regex: re.Match = re.compile(r"[/]api[/]v1[/]idea[/]\d")
        assert re.match(idea_instance_url_regex, links["idea.item.instance"])

        r: re.Match = re.compile(r"[/]\d")
        self.my_funding_id: int = int(re.search(r, links["viewIdea.instance"].group()[1:]))

    def test_shared_check(self, flask_client):
        res: Response = flask_client.get('/api/v1/idea/{}'.format(self.my_funding_id))

        # default response check
        assert "application/json" == res.content_type
        assert 201 == res.status_code

        # HATEOAS check
        links: Dict[str] = res.data["links"]

        idea_instance_url_regex: re.Match = re.compile(r"[/]api[/]v1[/]idea[/]\d")
        assert re.match(idea_instance_url_regex, links["self"])

        # data check
        data: Dict[str] = res.data

        assert "bulletproof raincoat" == data["title"]
        assert "how about bulletproof raincoat?" == data["body"]
