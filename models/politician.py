politician_list = []


def get_last_id():
    if politician_list:
        last_politician = politician_list[-1]
    else:
        return 1
    return last_politician.id + 1


class Politician:

    def __init__(self, name, position, description, age, gender,
                bio_data, c_vitae, county, constituency, ward):
        self.id = get_last_id()
        self.name = name
        self.position = position
        self.description = description
        self.age = age
        self.gender = gender
        self.bio_data = bio_data
        self.c_vitae = c_vitae
        self.county = county
        self.constituency = constituency
        self.ward = ward
        self.is_publish = False

    @property
    def data(self):
        return {
            'id': self.id,
            'name': self.name,
            'position': self.position,
            'description': self.description,
            'age': self.age,
            'gender': self.gender,
            'bio_data': self.bio_data,
            'c_vitae': self.c_vitae,
            'county': self.county,
            'constituency': self.constituency,
            'ward': self.ward
        }
