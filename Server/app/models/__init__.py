from sqlalchemy import Column, DateTime, ForeignKey, ForeignKeyConstraint, Index, String, Table
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Funding(db.Model):
    __tablename__ = 'funding'

    email = db.Column(db.String(50), primary_key=True, nullable=False)
    code = db.Column(db.String(10), primary_key=True, nullable=False)
    title = db.Column(db.String(45), nullable=False)
    body = db.Column(db.String(1600), nullable=False)
    expiration = db.Column(db.DateTime, nullable=False)
    title_img_path = db.Column(db.String(100), nullable=False)
    cover_img_path = db.Column(db.String(100), nullable=False)
    header_img_path = db.Column(db.String(500), nullable=False)

    tag = db.relationship('Tag', secondary='tag_has_funding', backref='fundings')


class Idea(db.Model):
    __tablename__ = 'idea'

    email = db.Column(db.String(50), primary_key=True, nullable=False)
    code = db.Column(db.String(10), primary_key=True, nullable=False)
    title = db.Column(db.String(45), nullable=False)
    body = db.Column(db.String(1600), nullable=False)

    tag = db.relationship('Tag', secondary='idea_has_tag', backref='ideas')


t_idea_has_tag = db.Table(
    'idea_has_tag',
    db.Column('idea_email', db.String(50), primary_key=True, nullable=False),
    db.Column('idea_code', db.String(10), primary_key=True, nullable=False),
    db.Column('tag_title', db.ForeignKey('tag.title', ondelete='CASCADE', onupdate='CASCADE'),
              primary_key=True, nullable=False, index=True),
    db.ForeignKeyConstraint(('idea_email', 'idea_code'), ['idea.email', 'idea.code'], onupdate='CASCADE'),
    db.Index('fk_idea_has_tag_idea1_idx', 'idea_email', 'idea_code')
)


class Order(db.Model):
    __tablename__ = 'order'
    __table_args__ = (
        db.ForeignKeyConstraint(('funding_email', 'funding_code'), ['funding.email', 'funding.code']),
        db.Index('fk_order_funding1_idx', 'funding_email', 'funding_code')
    )

    code = db.Column(db.String(10), primary_key=True, nullable=False)
    email = db.Column(db.String(50), primary_key=True, nullable=False)
    funding_email = db.Column(db.String(50), primary_key=True, nullable=False)
    funding_code = db.Column(db.String(10), primary_key=True, nullable=False)

    funding = db.relationship('Funding',
                              primaryjoin='and_(Order.funding_email == Funding.email, \
                                          Order.funding_code == Funding.code)',
                              backref='orders')


class Tag(db.Model):
    __tablename__ = 'tag'

    title = db.Column(db.String(45), primary_key=True)


t_tag_has_funding = db.Table(
    'tag_has_funding',
    db.Column('tag_title', db.ForeignKey('tag.title', onupdate='CASCADE'),
              primary_key=True, nullable=False, index=True),
    db.Column('funding_email', db.String(50), primary_key=True, nullable=False),
    db.Column('funding_code', db.String(10), primary_key=True, nullable=False),
    db.ForeignKeyConstraint(('funding_email', 'funding_code'), ['funding.email', 'funding.code'],
                            ondelete='CASCADE', onupdate='CASCADE'),
    db.Index('fk_tag_has_funding_funding1_idx', 'funding_email', 'funding_code')
)
