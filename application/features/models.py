from application import db
from application.models import Base
from sqlalchemy import func


class Feature(Base):
    user_id = db.Column(db.Integer, nullable=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)

    def __init__(self, title, description, userId):
        self.title = title
        self.description = description
        self.user_id = userId

    @property
    def like_count(self):
        return db.session.query(Feature.id).outerjoin(Like).filter_by(feature_id=self.id).count()


class Like(Base):
    user_id = db.Column(db.Integer, db.ForeignKey(
        'account.id'), nullable=True)
    feature_id = db.Column(db.Integer, db.ForeignKey(
        'feature.id'), nullable=False)

    def __init__(self, feature_id, user_id):
        self.feature_id = feature_id
        self.user_id = user_id
