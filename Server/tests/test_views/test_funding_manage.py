import re
import pytest

from tests.data_fixtures import funding

# type hinting
from flask import Response
from typing import Dict


class TestFundingManage:
    def test_funding_status(self, flask_client, funding):
        res: Response = flask_client.get('/api/v1/funding/{0}/status'.format(funding.funding_id),
                                         headers={"Authorization": funding.code})

        # default response check
        assert "application/json" == res.content_type
        assert 200 == res.status_code

        # data check
