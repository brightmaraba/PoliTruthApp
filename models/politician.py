politician_list = []


def get_last_id():
    if politician_list:
        last_politician = last_politician[-1]
    else:
        return 1
    return last_politician.id + 1


class Politician:
    def __init__(self, name):
        self.id = get_last_id()
        self.name = name
        self.is_publish = False

    @property
    def data(self):
        return {
            'id': self.id,
            'name': self.name
        }
