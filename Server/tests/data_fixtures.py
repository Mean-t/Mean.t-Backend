import pytest
import uuid

from app.models import Idea


@pytest.fixture(scope="function")
def idea(session):
    new_idea = Idea(email="artoria@artoria.us",
                    code=str(uuid.uuid4()).upper().replace("-", "")[:10],
                    title="raincoat",
                    body="I have an idea about raincoat")

    session.add(new_idea)

    return new_idea
