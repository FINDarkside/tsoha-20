from application import db
from application.models import Base
from sqlalchemy import func, select, event
from sqlalchemy.orm import column_property
from sqlalchemy.sql import and_, text
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
    category_id = db.Column(db.Integer, db.ForeignKey(
        FeatureCategory.id), index=True)
    category = db.relationship("FeatureCategory", foreign_keys=[
                               category_id], lazy='joined')

    def __init__(self, title, description, userId):
        self.title = title
        self.description = description
        self.user_id = userId
        self.category_id = FeatureCategory.get_first().id

    @property
    def authorized_to_modify(self):
        return current_user.is_admin or current_user.id == self.user_id

    @property
    def current_user_liked(self):
        count = db.session.query(Like).filter_by(
            user_id=current_user.id, feature_id=self.id).count()
        return count > 0

    @staticmethod
    def count_by_category(category_id):
        return Feature.query.filter_by(category_id=category_id).count()

    @staticmethod
    def get_paginated(page_num, page_size, category_id):
        skip_count = (page_num - 1) * page_size
        current_user_id = -1 if not current_user.is_authenticated else current_user.id
        stmt = text(""" 
                    SELECT Feature.*,
                        (SELECT COUNT(*)
                           FROM "like"
                           WHERE feature_id=Feature.id) AS like_count,
                        (SELECT COUNT(*)
                            FROM "like"
                            WHERE feature_id=Feature.id AND user_id=:current_user ) AS current_user_liked
                    FROM Feature
                    WHERE category_id=:category_id
                    ORDER BY like_count DESC
                    LIMIT :page_size
                    OFFSET :skip_count
                    """).params(current_user=current_user_id, category_id=category_id, skip_count=skip_count, page_size=page_size)
        res = db.engine.execute(stmt)
        response = []
        keys = res.keys()
        for row in res:
            # When no Features match query, there will still be one row with bunch of None values
            if(row[0] is None):
                break
            feature = {}
            for i, key in enumerate(keys):
                feature[key] = row[i]
            feature["authorized_to_modify"] = current_user.is_admin or feature.user_id == current_user.id
            response.append(feature)

        return response


Feature.like_count = column_property(
    select([func.count(Like.id)]).
    where(Like.feature_id == Feature.id)
)
