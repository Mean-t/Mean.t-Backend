import re
import pytest

# type hinting
from flask import Response
from typing import Dict, List


class TestViewIdea:
    def test_view_idea_list(self, flask_client, idea) -> None:
        res: Response = flask_client.get("/api/v1/idea")

        # default response check
        assert "application/json" == res.headers["Content-Type"]
        assert 201 == res.status_code

        # HATEOAS check
        links: Dict[str] = res.data["links"]

        assert "/api/v1/idea" == links["idea"]

        # data check
        assert isinstance(list, res.data["ideas"])
        assert isinstance(dict, res.data["ideas"][0])

        ideas: List[Dict[str]] = res.data["ideas"]
        idea_instance: Dict[str] = ideas[0]

        assert "artoria@artoria.us" == idea_instance["email"]
        assert "raincoat" == idea_instance["title"]
        assert isinstance(idea_instance["tag"], list)
        assert "raincoat" == idea_instance["tag"][0]

        # instance HATEOAS check
        assert isinstance(idea_instance["links"], dict)

        links: Dict[str] = idea_instance["links"]

        link_regex = re.compile(r"[/]api[/]v1[/]idea[/]\d")
        assert re.match(link_regex, links["self"])

        self.idea_instance_link: str = links["self"]

    def test_view_specific_idea(self, flask_client) -> None:
        res: Response = flask_client.get(self.idea_instance_link)

        # default response check
        assert "application/json" == res.headers["Content-Type"]
        assert 201 == res.status_code

        # HATEOAS check
        links: Dict[str] = res.data["links"]

        assert self.idea_instance_link == links["self"]

        # data check
        assert isinstance(dict, res.data)

        idea: Dict[str] = res.data

        assert "artoria@artoria.us" == idea["email"]
        assert "raincoat" == idea["title"]
        assert isinstance(idea["tag"], list)
        assert "raincoat" == idea["tag"][0]
