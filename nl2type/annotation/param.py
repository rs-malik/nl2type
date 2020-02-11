class Param:

    def __init__(self, name: str, type_: str):
        self.name = name
        self.type_ = type_

    @property
    def get_name(self):
        return self.name

    @property
    def get_type(self):
        return self.type_

    def __str__(self):
        return "* @param {{{}}} {}".format(self.type_, self.name)
