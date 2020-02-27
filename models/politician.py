politician_list = []


def get_last_id():
    if politician_list:
        last_politician = politician_list[-1]
    else:
        return 1
    return last_politician.id + 1


class Politician:
    def __init__(self, name, gender, age, party, position, county, constituency, ward,
                 bio_data, c_vitae, description):
        self.id = get_last_id()
        self.name = name
        self.gender = gender
        self.age = age
        self.party = party
        self.position = position
        self.county = county
        self.constituency = constituency
        self.ward = ward
        self.bio_data = bio_data
        self.c_vitae = c_vitae
        self.description = description
        self.is_publish = False


    def data(self):
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'age': self.age,
            'party': self.party,
            'position': self.position,
            'county': self.county,
            'constituency': self.constituency,
            'ward': self.ward,
            'bio_data': self.bio_data,
            'c_vitae': self.c_vitae,
            'description': self.description
        }
