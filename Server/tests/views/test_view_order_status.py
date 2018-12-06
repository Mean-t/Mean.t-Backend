import re
import pytest

from tests.data_fixtures import order
from app.models import Order

# type hinting
from flask import Response
from typing import Dict


class TestViewOrderStatus:
    def test_check_order(self, flask_client, order: Order):
        res: Response = flask_client.get('/api/v1/tracker/order?email={email}&code={code}'.format(
            email=order.email,
            code=order.code
        ))

        # default response check
        assert "application/json" == res.content_type
        assert 200 == res.status_code

        # data check
        data: Dict[str] = res.data

        assert order.payee == data["payee"]
        assert order.destination == data["destination"]
        assert order.code == data["code"]

        status_regex = re.compile(r"[0-9]{2}")
        assert re.match(status_regex, data["status"])
