from typing import List

from annotation.param import Param


class Jsdoc:

    def __init__(self):
        self.params = list()
        self.name = ''

    def add_param(self, param: Param):
        self.params.append(param)

    def set_name(self, name: str):
        self.name = name

    def set_type(self, type_: str):
        self.type_ = type_

    def set_line_number(self, line_number: int):
        self.line_number = line_number

    def __str__(self):
        repr = "/**\n"
        for param in self.params:
            repr = repr + str(param) + "\n"

        repr = repr + "* @return {{{}}}".format(self.type_) + "\n"
        repr = repr + "*/\n"
        return repr


    def get_params(self) -> List[Param]:
        return self.params

    def get_name(self) -> str:
        return self.name

    def get_line_number(self) -> int:
        return self.line_number

    def get_type(self) -> str:
        return self.type_