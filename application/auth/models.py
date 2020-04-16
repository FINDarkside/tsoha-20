from application import db
from application.models import Base
from sqlalchemy.sql import text


class User(Base):

    __tablename__ = "account"

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    @staticmethod
    def find_users_with_most_features():
        stmt = text("SELECT Account.id, Account.username, COUNT(*) AS feature_count FROM Account"
                    " LEFT JOIN Feature ON Feature.user_id = Account.id"
                    " GROUP BY Account.id"
                    " ORDER BY feature_count DESC"
                    " LIMIT 10")
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append({
                "id": row[0],
                "username": row[1],
                "feature_count": row[2]
            })
        return response
