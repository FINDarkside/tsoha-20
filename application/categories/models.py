from application import db
from application.models import Base
from sqlalchemy import func, select, event
from sqlalchemy.orm import column_property
from sqlalchemy.sql import and_
from flask_login import current_user


class FeatureCategory(Base):
    name = db.Column(db.String, nullable=False)

    def __init__(self, name):
        self.name = name


def init_categories(*args, **kwargs):
    # FIXME: Read password from env variable or remove this completely!
    db.session.add(FeatureCategory("open"))
    db.session.add(FeatureCategory("done"))
    db.session.commit()


event.listen(FeatureCategory.__table__, 'after_create', init_categories)
