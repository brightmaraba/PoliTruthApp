from extensions import db

politician_list = []


def get_last_id():
    if politician_list:
        last_politician = politician_list[-1]
    else:
        return 1
    return last_politician.id + 1


class Politician(db.Model):
    __tablename__ = 'politicians'

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