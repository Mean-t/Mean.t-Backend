from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required

from app.extensions import db
from app.docs.sample import *
from app.views import BaseResource
from app.models import Funding


class FundingInstance(BaseResource):
    @swag_from(SAMPLE_POST)
    @jwt_required
    def get(self, funding_id: int):
        funding: Funding = Funding.query.filter_by(funding_id=funding_id).first()

        return self.unicode_safe_json_dumps({
            'id': funding.funding_id,
            'title': funding.title,
            'body': funding.body,
            'expiration': funding.expiration,
            'title_img': funding.title_img_path,
            'cover_img': funding.cover_img_path,
            'header_imgs': funding.header_img_paths.split("%"),
            'host': funding.host,
            'tag': [t.title for t in funding.tag],
            'idea': [[i.idea_id, i.title] for i in funding.ideas]
        })

    @swag_from(SAMPLE_POST)
    @jwt_required
    def patch(self, funding_id: int):
        acceptable_key = ["title", "body", "title_img_path", "cover_img_path", "header_img_path"]

        patch_data: dict = {k: v for k, v in request.json.items() if k in acceptable_key}
        patch_data.update({"updated_at": self.now()})

        Funding.query.filter_by(funding_id=funding_id).update(**patch_data)
        db.session.commit()

        return self.unicode_safe_json_dumps(status_code=204)

    @swag_from(SAMPLE_POST)
    @jwt_required
    def delete(self, funding_id: int):
        Funding.query.filter_by(funding_id=funding_id).delete()

        return self.unicode_safe_json_dumps(status_code=204)


