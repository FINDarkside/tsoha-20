from application import db


class Feature(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())
    user_id = db.Column(db.Integer, nullable=True)
    title = db.Column(db.String(144), nullable=False)
    description = db.Column(db.String(144), nullable=False)

    def __init__(self, title, description, userId):
        self.title = title
        self.description = description
        self.user_id = userId
