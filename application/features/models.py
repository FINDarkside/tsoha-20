from application import db
from application.models import Base

class Feature(Base):
    user_id = db.Column(db.Integer, nullable=True)
    title = db.Column(db.String(144), nullable=False)
    description = db.Column(db.String(144), nullable=False)

    def __init__(self, title, description, userId):
        self.title = title
        self.description = description
        self.user_id = userId


class Like(Base):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=True)
    feature_id = db.Column(db.Integer, db.ForeignKey(
        'feature.id'), nullable=False)

    def __init__(self, title, description, userId):
        self.title = title
        self.description = description
        self.user_id = userId
