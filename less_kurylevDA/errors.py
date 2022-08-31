"""������"""


class IncorrectDataRecivedError(Exception):
    """����������  - ������������ ������ �������� �� ������"""
    def __str__(self):
        return '������� ������������ ��������� �� ��������� ����������.'


class ServerError(Exception):
    """���������� - ������ �������"""
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return self.text


class NonDictInputError(Exception):
    """���������� - �������� ������� �� �������"""
    def __str__(self):
        return '�������� ������� ������ ���� �������.'


class ReqFieldMissingError(Exception):
    """������ - ����������� ������������ ���� � �������� �������"""
    def __init__(self, missing_field):
        self.missing_field = missing_field

    def __str__(self):
        return f'� �������� ������� ����������� ������������ ���� {self.missing_field}.'