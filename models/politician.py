politician_list = []


def get_last_id():
    if politician_list:
        last_politician = politician_list[-1]
    else:
        return 1
    return last_politician.id + 1


class Politician:
    def __init__(self, name, position, description, gender, age, county,
                    constituency, ward, bio_data, c_vitae):
        self.id = get_last_id()
        self.name = name
        self.position = position
        self.description
        self.gender = gender
        self.age = age
        self.county
        self.constituency
        self.ward
        self.bio_data
        self.c_vitae
        self.is_publish = False

    @property
    def data(self):
        return {
            'id': self.id,
            'name': self.name,
            'position': self.position,
            'description': self.description,
            'gender': self.gender,
            'age': self.age,
            'county': self.county,
            'constituency': self.constituency,
            'ward': self.ward,
            'bio_data': self.bio_data,
            'c_vitae': self.c_vitae
        }
