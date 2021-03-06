import pytest
import uuid
from datetime import datetime, timedelta

from app.models import Idea, Tag, Funding, Order


@pytest.fixture(scope="function")
def idea_base(session) -> Idea:
    new_tag: Tag = Tag(title="raincoat")
    session.add(new_tag)

    new_idea: Idea = Idea(email="artoria@artoria.us",
                          code=str(uuid.uuid4()).upper().replace("-", "")[:10])

    session.add(new_idea)
    session.commit()

    return new_idea


@pytest.fixture(scope="function")
def idea(session) -> Idea:
    new_tag: Tag = Tag(title="raincoat")
    session.add(new_tag)

    new_idea: Idea = Idea(email="artoria@artoria.us",
                          code=str(uuid.uuid4()).upper().replace("-", "")[:10],
                          title="raincoat",
                          tag=[new_tag],
                          body="I have an idea about raincoat")

    session.add(new_idea)
    session.commit()

    return new_idea


@pytest.fixture(scope="function")
def funding_base(session, idea) -> Funding:
    new_funding: Funding = Funding(email="artoria@artoria.us",
                                   host="lewis kim",
                                   code=str(uuid.uuid4()).upper().replace("-", "")[:10])
    session.add(new_funding)
    session.commit()

    return new_funding


@pytest.fixture(scope="function")
def funding(session, idea) -> Funding:
    new_funding: Funding = Funding(email="artoria@artoria.us",
                                   host="lewis kim",
                                   code=str(uuid.uuid4()).upper().replace("-", "")[:10],
                                   title="bulletproof raincoat",
                                   tag=[idea.tag],
                                   body="ability of withstand .50 BMG",
                                   expiration=datetime.date(datetime.now() + timedelta(days=10)),
                                   goal=1000000000,
                                   idea_ideas=[idea],
                                   title_img_path="/static/wef2r243.jpg",
                                   cover_img_path="/static/wef2r243.jpg",
                                   header_img_paths="/static/wef2r243.jpg%/static/wef2r243.jpg%/static/wef2r243.jpg"
                                   )
    session.add(new_funding)
    session.commit()

    return new_funding


@pytest.fixture(scope="function")
def order_base(session, funding) -> Order:
    new_order: Order = Order(code=str(uuid.uuid4()).upper().replace("-", "")[:10],
                             email="artoria@artoria.us",
                             payee="lewis kim",
                             destination="Apple Campus, Cupertino, CA 95014 U.S.A",
                             funding_funding=funding)
    session.add(new_order)
    session.commit()

    return new_order


@pytest.fixture(scope="function")
def order(session, funding) -> Order:
    new_order: Order = Order(code=str(uuid.uuid4()).upper().replace("-", "")[:10],
                             email="artoria@artoria.us",
                             payee="lewis kim",
                             destination="Apple Campus, Cupertino, CA 95014 U.S.A",
                             funding_funding=funding)
    session.add(new_order)
    session.commit()

    return new_order
