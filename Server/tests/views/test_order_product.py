import re
import pytest

from tests.data_fixtures import order
from app.models import Order

# type hinting
from flask import Response
from typing import Dict


class TestOrderProduct:
    test_mail = "artoria@artoria.us"
    test_name = test_payee = "lewis kim"
    test_destination_address = "Apple Campus, Cupertino, CA 95014 U.S.A"

    def test_verify(self, flask_client, session):
        res: Response = flask_client.post("/api/v1/funding/1/order/verify", data=dict(
            email=self.test_mail,
            payee=self.test_name
        ))

        # default response check
        assert "application/json" == res.headers["Content-Type"]
        assert 201 == res.status_code

        # HATEOAS check
        links: Dict[str] = res.data["links"]

        assert "/api/v1/funding/1/order" == links["continue"]

    def test_order(self, flask_client, order_base):
        res: Response = flask_client.post("/api/v1/funding/1/order", data=dict(
            payee=self.test_payee,
            destination=self.test_destination_address
        ), content_type='application/json',  headers={'Authorization': order_base.code})

        # default response check
        assert "application/json" == res.content_type
        assert 201 == res.status_code

        # HATEOAS check
        links: Dict[str] = res.data["links"]

        assert "/api/v1/tracker/order?email={0}&code={1}".format(order_base.email, order_base.code) == links["orderStatus"]
