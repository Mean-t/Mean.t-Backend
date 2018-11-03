from typing import List, Tuple
from datetime import datetime
from sqlalchemy import Table, ForeignKeyConstraint, Index
from app.extensions import db


class Tag(db.Model):
    __tablename__ = 'tag'

    title: str = db.Column(db.String(45), primary_key=True)


t_tag_has_funding: Table = db.Table(
    'tag_has_funding',
    db.Column('tag_title', db.ForeignKey('tag.title', onupdate='CASCADE'),
              primary_key=True, nullable=False, index=True),
    db.Column('funding_email', db.String(50), primary_key=True, nullable=False),
    db.Column('funding_code', db.String(10), primary_key=True, nullable=False),
    db.ForeignKeyConstraint(('funding_email', 'funding_code'), ['funding.email', 'funding.code'],
                            ondelete='CASCADE', onupdate='CASCADE'),
    db.Index('fk_tag_has_funding_funding1_idx', 'funding_email', 'funding_code')
)

t_idea_has_tag: Table = db.Table(
    'idea_has_tag',
    db.Column('idea_email', db.String(50), primary_key=True, nullable=False),
    db.Column('idea_code', db.String(10), primary_key=True, nullable=False),
    db.Column('tag_title', db.ForeignKey('tag.title', ondelete='CASCADE', onupdate='CASCADE'),
              primary_key=True, nullable=False, index=True),
    db.ForeignKeyConstraint(('idea_email', 'idea_code'), ['idea.email', 'idea.code'], onupdate='CASCADE'),
    db.Index('fk_idea_has_tag_idea1_idx', 'idea_email', 'idea_code')
)


class Funding(db.Model):
    __tablename__ = 'funding'

    funding_id = db.Column(db.Integer, nullable=False)
    email: str = db.Column(db.String(50), primary_key=True, nullable=False)
    host: str = db.Column(db.String(10), nullable=False)
    code: str = db.Column(db.String(10), primary_key=True, nullable=False)
    title: str = db.Column(db.String(45))
    body: str = db.Column(db.String(1600))
    expiration: datetime = db.Column(db.DateTime)
    title_img_path: str = db.Column(db.String(100))
    cover_img_path: str = db.Column(db.String(100))
    header_img_path: str = db.Column(db.String(500))

    tag = db.relationship('Tag', secondary='tag_has_funding', backref='fundings')  # type: List[Tag]


class Idea(db.Model):
    __tablename__ = 'idea'

    idea_id = db.Column(db.Integer, nullable=False)
    email: str = db.Column(db.String(50), primary_key=True, nullable=False)
    code: str = db.Column(db.String(10), primary_key=True, nullable=False)
    title: str = db.Column(db.String(45))
    body: str = db.Column(db.String(1600))

    tag: List[Tag] = db.relationship('Tag', secondary='idea_has_tag', backref='ideas')


t_idea_has_funding: Table = db.Table(
    'idea_has_funding',
    db.Column('idea_email', db.String(50), primary_key=True, nullable=False),
    db.Column('idea_code', db.String(10), primary_key=True, nullable=False),
    db.Column('funding_email', db.String(50), primary_key=True, nullable=False),
    db.Column('funding_code', db.String(10), primary_key=True, nullable=False),
    db.ForeignKeyConstraint(('funding_email', 'funding_code'), ['funding.email', 'funding.code']),
    db.ForeignKeyConstraint(('idea_email', 'idea_code'), ['idea.email', 'idea.code']),
    db.Index('fk_idea_has_funding_idea1_idx', 'idea_email', 'idea_code'),
    db.Index('fk_idea_has_funding_funding1_idx', 'funding_email', 'funding_code')
)


class Order(db.Model):
    __tablename__ = 'order'
    __table_args__: Tuple[ForeignKeyConstraint, Index] = (
        db.ForeignKeyConstraint(('funding_email', 'funding_code'), ['funding.email', 'funding.code']),
        db.Index('fk_order_funding1_idx', 'funding_email', 'funding_code')
    )

    code: str = db.Column(db.String(10), primary_key=True, nullable=False)
    email: str = db.Column(db.String(50), primary_key=True, nullable=False)
    payee: str = db.Column(db.String(10), nullable=False)
    destination: str = db.Column(db.String(50), nullable=False)
    funding_email: str = db.Column(db.String(50), primary_key=True, nullable=False)
    funding_code = db.Column(db.String(10), primary_key=True, nullable=False)

    funding: Funding = db.relationship('Funding',
                                       primaryjoin='and_(Order.funding_email == Funding.email, \
                                          Order.funding_code == Funding.code)',
                                       backref='orders')
