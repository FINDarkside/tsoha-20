from application import db
from application.models import Base
from sqlalchemy import func, select
from sqlalchemy.orm import column_property
from sqlalchemy.sql import and_
from flask_login import current_user


class Like(Base):
    user_id = db.Column(db.Integer, db.ForeignKey(
        'account.id'), nullable=True)
    feature_id = db.Column(db.Integer, db.ForeignKey(
        'feature.id'), nullable=False)

    def __init__(self, feature_id, user_id):
        self.feature_id = feature_id
        self.user_id = user_id


class Feature(Base):
    user_id = db.Column(db.Integer, nullable=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)

    def __init__(self, title, description, userId):
        self.title = title
        self.description = description
        self.user_id = userId

    @property
    def authorized_to_modify(self):
        return current_user.is_admin or current_user.id == self.user_id


Feature.like_count = column_property(
    select([func.count(Like.id)]).
    where(Like.feature_id == Feature.id)
)
