from __future__ import annotations

from typing import List, Tuple, Type
from datetime import datetime
from sqlalchemy import ForeignKeyConstraint, Table, Index
from enum import Enum

from app.extensions import db


class FundingStatusEnum(Enum):
    ready = 1
    success = 2
    manufacture = 3
    complete = 4


class OrderStatusEnum(Enum):
    cancel = 1
    standby = 2
    ready = 3
    manufacture = 4
    delivery = 5
    arrive = 6


class Funding(db.Model):
    __tablename__ = 'funding'

    funding_id: int = db.Column(db.Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    email: str = db.Column(db.String(50), primary_key=True, nullable=False)
    code: str = db.Column(db.String(10), primary_key=True, nullable=False)
    title: str = db.Column(db.String(45))
    body: str = db.Column(db.String(1600))
    expiration: datetime = db.Column(db.DateTime)
    title_img_path: str = db.Column(db.String(100))
    cover_img_path: str = db.Column(db.String(100))
    header_img_paths: str = db.Column(db.String(500))
    host: str = db.Column(db.String(10))
    created_at: datetime = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    updated_at: datetime = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())

    ideas: List[Idea] = db.relationship('Idea', secondary='funding_has_idea', backref='fundings')
    tag: List[Tag] = db.relationship('Tag', secondary='funding_has_tag', backref='fundings')


class FundingStatus(Funding):
    __tablename__ = 'funding_status'
    __table_args__: Tuple[ForeignKeyConstraint] = (
        db.ForeignKeyConstraint(('funding_funding_id', 'funding_email', 'funding_code'),
                                ['funding.funding_id', 'funding.email', 'funding.code'],
                                ondelete='CASCADE', onupdate='CASCADE'),
    )

    funding_funding_id: int = db.Column(db.Integer, primary_key=True, nullable=False)
    funding_email: str = db.Column(db.String(50), primary_key=True, nullable=False)
    funding_code: str = db.Column(db.String(10), primary_key=True, nullable=False)
    balance: int = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    participants_num: int = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    status: Type[Enum] = db.Column(db.Enum(FundingStatusEnum))


t_funding_has_idea: Table = db.Table(
    'funding_has_idea',
    db.Column('funding_funding_id', db.Integer, primary_key=True, nullable=False),
    db.Column('funding_email', db.String(50), primary_key=True, nullable=False),
    db.Column('funding_code', db.String(10), primary_key=True, nullable=False),
    db.Column('idea_idea_id', db.Integer, primary_key=True, nullable=False),
    db.Column('idea_email', db.String(50), primary_key=True, nullable=False),
    db.Column('idea_code', db.String(10), primary_key=True, nullable=False),
    db.ForeignKeyConstraint(('funding_funding_id', 'funding_email', 'funding_code'),
                            ['funding.funding_id', 'funding.email', 'funding.code'],
                            ondelete='CASCADE', onupdate='CASCADE'),
    db.ForeignKeyConstraint(('idea_idea_id', 'idea_email', 'idea_code'),
                            ['idea.idea_id', 'idea.email', 'idea.code'],
                            onupdate='CASCADE'),
    db.Index('fk_funding_has_idea_idea1_idx', 'idea_idea_id', 'idea_email', 'idea_code'),
    db.Index('fk_funding_has_idea_funding1_idx', 'funding_funding_id', 'funding_email', 'funding_code')
)

t_funding_has_tag: Table = db.Table(
    'funding_has_tag',
    db.Column('funding_funding_id', db.Integer, primary_key=True, nullable=False),
    db.Column('funding_email', db.String(50), primary_key=True, nullable=False),
    db.Column('funding_code', db.String(10), primary_key=True, nullable=False),
    db.Column('tag_title', db.ForeignKey('tag.title'), primary_key=True, nullable=False, index=True),
    db.ForeignKeyConstraint(('funding_funding_id', 'funding_email', 'funding_code'),
                            ['funding.funding_id', 'funding.email', 'funding.code'], onupdate='CASCADE'),
    db.Index('fk_funding_has_tag_funding1_idx', 'funding_funding_id', 'funding_email', 'funding_code')
)


class Idea(db.Model):
    __tablename__ = 'idea'

    idea_id: int = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    email: str = db.Column(db.String(50), primary_key=True, nullable=False)
    code: str = db.Column(db.String(10), primary_key=True, nullable=False)
    title: str = db.Column(db.String(45))
    body: str = db.Column(db.String(1600))
    created_at: datetime = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    updated_at: datetime = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())

    tag: List[Tag] = db.relationship('Tag', secondary='idea_has_tag', backref='ideas')


t_idea_has_ta: Table = db.Table(
    'idea_has_tag',
    db.Column('idea_idea_id', db.Integer, primary_key=True, nullable=False),
    db.Column('idea_email', db.String(50), primary_key=True, nullable=False),
    db.Column('idea_code', db.String(10), primary_key=True, nullable=False),
    db.Column('tag_title', db.ForeignKey('tag.title'), primary_key=True, nullable=False, index=True),
    db.ForeignKeyConstraint(('idea_idea_id', 'idea_email', 'idea_code'),
                            ['idea.idea_id', 'idea.email', 'idea.code'],
                            onupdate='CASCADE'),
    db.Index('fk_idea_has_tag_idea1_idx', 'idea_idea_id', 'idea_email', 'idea_code')
)


class Order(db.Model):
    __tablename__ = 'order'
    __table_args__: Tuple[ForeignKeyConstraint, Index] = (
        db.ForeignKeyConstraint(('funding_funding_id', 'funding_email', 'funding_code'),
                                ['funding.funding_id', 'funding.email', 'funding.code']),
        db.Index('fk_order_funding1_idx', 'funding_funding_id', 'funding_email', 'funding_code')
    )

    code: str = db.Column(db.String(10), primary_key=True, nullable=False)
    email: str = db.Column(db.String(50), primary_key=True, nullable=False)
    payee: str = db.Column(db.String(10), nullable=False)
    destination: str = db.Column(db.String(50), nullable=False)
    status: Type[Enum] = db.Column(db.Enum(OrderStatusEnum), nullable=False, server_default=db.FetchedValue())
    ordered_at: str = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    funding_funding_id: int = db.Column(db.Integer, primary_key=True, nullable=False)
    funding_email: str = db.Column(db.String(50), primary_key=True, nullable=False)
    funding_code: str = db.Column(db.String(10), primary_key=True, nullable=False)

    funding: Funding = db.relationship('Funding',
                                               primaryjoin='and_(Order.funding_funding_id == Funding.funding_id, '
                                                           'Order.funding_email == Funding.email, '
                                                           'Order.funding_code == Funding.code)', backref='orders')


class Tag(db.Model):
    __tablename__ = 'tag'

    title: str = db.Column(db.String(45), primary_key=True)
