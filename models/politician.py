from extensions import db


class Politician(db.Model):
    __tablename__ = 'politician'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(100), nullable=False)
    bio_data = db.Column(db.String(1000), nullable=False)
    c_vitae = db.Column(db.String(10000), nullable=False)
    county = db.Column(db.String(100), nullable=False)
    constituency =  db.Column(db.String(100), nullable=False)
    ward = db.Column(db.String(100), nullable=False)
    is_publish = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))

    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))

    @classmethod
    def get_all_published(cls):
        return cls.query.filter_by(is_publish=True).all()

    @classmethod
    def get_by_id(cls, politician_id):
        return cls.query.filter_by(id=politician_id).first()

    @classmethod
    def get_all_by_user(cls, user_id, visibilty='public'):
        if visibilty == 'public':
            return cls.query.filter_by(user_id=user_id, is_publish=True).all()
        elif visibilty == 'private':
            return cls.query.filter_by(user_id=user_id, is_publish=False).all()
        else:
            return cls.query.filter_by(user_id=user_id).all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
