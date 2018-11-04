import re
import pytest

from app.models import Order

# type hinting
from flask import Response
from typing import Dict


class TestOrderProduct:
    test_mail = "artoria@artoria.us"
    test_name = "lewis kim"
    test_payee = "arthur pandragon"
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

        assert "api/v1/funding/1/order/verify" == links["orderProduct.verify"]
        assert "/api/v1/funding/1/order" == links["orderProduct.order"]

        self.verification_code = session.query(Order).first().code

    def test_order(self, flask_client):
        res: Response = flask_client.post("/api/v1/funding/1/order", data=dict(
            payee=self.test_payee,
            destination=self.test_destination_address
        ), content_type='application/json',  headers={'Authorization': self.verification_code})

        # default response check
        assert "application/json" == res.content_type
        assert 201 == res.status_code

        # HATEOAS check
        links: Dict[str] = res.data["links"]

        assert "/api/v1/funding/1/order" == links["orderProduct.order"]
        assert "/api/v1/tracker/order" == links["statusTracker.order.status"]

    def test_check_order(self, flask_client):
        res: Response = flask_client.get('/api/v1/tracker/order?email={email}&code={code}'.format(
            email=self.test_mail,
            code=self.verification_code
        ))

        # default response check
        assert "application/json" == res.content_type
        assert 201 == res.status_code

        # HATEOAS check
        links: Dict[str] = res.data["links"]

        assert "/api/v1/tracker/order" == links["statusTracker.order.status"]

        funding_regex = re.compile(r"[/]api[/]funding[/]\d")
        assert re.match(funding_regex, links["funding.item.instance"])

        # data check
        data: Dict[str] = res.data

        assert self.test_payee == data["payee"]
        assert self.test_destination_address == data["destination"]
        assert self.verification_code == data["code"]

        status_regex = re.compile(r"[0-9]{2}")
        assert re.match(status_regex, data["status"])

