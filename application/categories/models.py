from application import db
from application.models import Base
from sqlalchemy import func, select, event
from sqlalchemy.orm import column_property
from sqlalchemy.sql import and_, text


class FeatureCategory(Base):
    name = db.Column(db.String, nullable=False)
    feature = db.relationship("Feature", cascade="all,delete")

    def __init__(self, name):
        self.name = name

    @staticmethod
    def get_all():
        return FeatureCategory.query.order_by(FeatureCategory.id).all()

    @staticmethod
    def get_first():
        return FeatureCategory.query.order_by(FeatureCategory.id).first()

    @staticmethod
    def feature_count_by_category():
        stmt = text("""SELECT feature_category.name, COUNT(Feature.id) AS feature_count FROM feature_category
                        LEFT JOIN Feature ON Feature.category_id = feature_category.id
                        GROUP BY feature_category.id
                        ORDER BY feature_count DESC""")
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append({
                "name": row[0],
                "feature_count": row[1]
            })
        return response


def init_categories(*args, **kwargs):
    # FIXME: Read password from env variable or remove this completely!
    db.session.add(FeatureCategory("Suggestions"))
    db.session.add(FeatureCategory("Done"))
    db.session.add(FeatureCategory("Rejected"))
    db.session.commit()


event.listen(FeatureCategory.__table__, "after_create", init_categories)
