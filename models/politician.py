#This is a model file to define Politician
#Developer Details
__author__ = "Brian Koech"
__copyright__ = "Copyright 2020, LibranConsult LLC"
__credits__ = []
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Brian Koech"
__email__ = "librankoech@gmail.com"
__status__ = "Prototype"

#Empty list to hold data
politician_list = []

#Iterate Function
def get_last__id():
    if politician_list:
        last_politician = politician_list[-1]
    else:
        return 1
    return last_politician.id + 1

#Class Politician models the politicians parameters
class Politician:
    def __init__(self, name, gender, age, party, position, county, constituency, ward,
                    bio_data, c_vitae, description, is_published):
        self.id = get_last__id(),
        self.name = name,
        self.gender = gender,
        self.age = age,
        self.party = party,
        self.position = position,
        self.county = county,
        self.constituency = constituency,
        self.ward = ward,
        self.bio_data = bio_data,
        self.c_vitae = c_vitae,
        self.description = description,
        self.is_publish = False

#Data method for returning the data as a dictionary object
    @property
    def data(self):
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'age': self.age,
            'party': self.party,
            'postition': self.position,
            'county': self.county,
            'constituency': self.constituency,
            'ward':self.ward,
            'bio_data': self.bio_data,
            'c_vitae': self.c_vitae,
            'description': self.description
        }
