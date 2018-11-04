import pytest
import uuid

from app.models import Idea, Tag


@pytest.fixture(scope="function")
def idea(session):
    new_tag = Tag(title="raincoat")
    session.add(new_tag)

    new_idea = Idea(email="artoria@artoria.us",
                    code=str(uuid.uuid4()).upper().replace("-", "")[:10],
                    title="raincoat",
                    tag=[new_tag],
                    body="I have an idea about raincoat")

    session.add(new_idea)
    session.commit()

    return new_idea
