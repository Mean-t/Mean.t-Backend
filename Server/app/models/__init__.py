from typing import List, Tuple
from datetime import datetime
from sqlalchemy import Table, ForeignKeyConstraint, Index
from app.extensions import db



class Funding(db.Model):
    __tablename__ = 'funding'

    email = db.Column(db.String(50), primary_key=True, nullable=False)  # type: str
    code = db.Column(db.String(10), primary_key=True, nullable=False)  # type: str
    title = db.Column(db.String(45), nullable=False)  # type: str
    body = db.Column(db.String(1600), nullable=False)  # type: str
    expiration = db.Column(db.DateTime, nullable=False)  # type: datetime
    title_img_path = db.Column(db.String(100), nullable=False)  # type: str
    cover_img_path = db.Column(db.String(100), nullable=False)  # type: str
    header_img_path = db.Column(db.String(500), nullable=False)  # type: str

    tag = db.relationship('Tag', secondary='tag_has_funding', backref='fundings')  # type: List[Tag]


class Idea(db.Model):
    __tablename__ = 'idea'

    email = db.Column(db.String(50), primary_key=True, nullable=False)  # type: str
    code = db.Column(db.String(10), primary_key=True, nullable=False)  # type: str
    title = db.Column(db.String(45), nullable=False)  # type: str
    body = db.Column(db.String(1600), nullable=False)  # type: str

    tag = db.relationship('Tag', secondary='idea_has_tag', backref='ideas')  # type: List[Tag]


t_idea_has_tag = db.Table(
    'idea_has_tag',
    db.Column('idea_email', db.String(50), primary_key=True, nullable=False),
    db.Column('idea_code', db.String(10), primary_key=True, nullable=False),
    db.Column('tag_title', db.ForeignKey('tag.title', ondelete='CASCADE', onupdate='CASCADE'),
              primary_key=True, nullable=False, index=True),
    db.ForeignKeyConstraint(('idea_email', 'idea_code'), ['idea.email', 'idea.code'], onupdate='CASCADE'),
    db.Index('fk_idea_has_tag_idea1_idx', 'idea_email', 'idea_code')
)  # type: Table


class Order(db.Model):
    __tablename__ = 'order'
    __table_args__ = (
        db.ForeignKeyConstraint(('funding_email', 'funding_code'), ['funding.email', 'funding.code']),
        db.Index('fk_order_funding1_idx', 'funding_email', 'funding_code')
    )  # type: Tuple[ForeignKeyConstraint, Index]

    code = db.Column(db.String(10), primary_key=True, nullable=False)  # type: str
    email = db.Column(db.String(50), primary_key=True, nullable=False)  # type: str
    funding_email = db.Column(db.String(50), primary_key=True, nullable=False)  # type: str
    funding_code = db.Column(db.String(10), primary_key=True, nullable=False)  # type: str

    funding = db.relationship('Funding',
                              primaryjoin='and_(Order.funding_email == Funding.email, \
                                          Order.funding_code == Funding.code)',
                              backref='orders')  # type: Funding


class Tag(db.Model):
    __tablename__ = 'tag'

    title = db.Column(db.String(45), primary_key=True)  # type: str


t_tag_has_funding = db.Table(
    'tag_has_funding',
    db.Column('tag_title', db.ForeignKey('tag.title', onupdate='CASCADE'),
              primary_key=True, nullable=False, index=True),
    db.Column('funding_email', db.String(50), primary_key=True, nullable=False),
    db.Column('funding_code', db.String(10), primary_key=True, nullable=False),
    db.ForeignKeyConstraint(('funding_email', 'funding_code'), ['funding.email', 'funding.code'],
                            ondelete='CASCADE', onupdate='CASCADE'),
    db.Index('fk_tag_has_funding_funding1_idx', 'funding_email', 'funding_code')
)  # type: Table
