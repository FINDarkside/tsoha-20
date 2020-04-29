from application import db
from application.models import Base
from sqlalchemy import func, select, event
from sqlalchemy.orm import column_property
from sqlalchemy.sql import and_
from flask_login import current_user
from application.categories.models import FeatureCategory


class Like(Base):
    user_id = db.Column(db.Integer, db.ForeignKey(
        'account.id'), nullable=False, index=True)
    feature_id = db.Column(db.Integer, db.ForeignKey(
        'feature.id'), nullable=False, index=True)

    def __init__(self, feature_id, user_id):
        self.feature_id = feature_id
        self.user_id = user_id

class Feature(Base):
    user_id = db.Column(db.Integer, nullable=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey(FeatureCategory.id), index=True)
    category = db.relationship("FeatureCategory", foreign_keys=[category_id], lazy='joined')

    def __init__(self, title, description, userId):
        self.title = title
        self.description = description
        self.user_id = userId
        self.category_id = 1

    @property
    def authorized_to_modify(self):
        return current_user.is_admin or current_user.id == self.user_id

    @property
    def current_user_liked(self):
        count = db.session.query(Like).filter_by(
            user_id=current_user.id, feature_id=self.id).count()
        return count > 0


Feature.like_count = column_property(
    select([func.count(Like.id)]).
    where(Like.feature_id == Feature.id)
)
