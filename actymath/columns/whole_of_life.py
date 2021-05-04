import pandas as pd

from .base import Column


""" Actuarial formulae for whole remainder of life. """


class a_due_x(Column):
    """ PV of annuity due (paid in advance) for remainder of life. """

    parameters = {"life": "Life identifier (int)"}
    column_name = "a_due(x{life})"
    dependencies = ["N(x{life})", "D(x{life})"]

    @classmethod
    def calculate(cls, calc, **kwargs):
        return calc[f"N(x{kwargs['life']})"] / calc[f"D(x{kwargs['life']})"]


class a_x(Column):
    """ PV of annuity (paid in arrears) for remainder of life. """

    parameters = {"life": "Life identifier (int)"}
    column_name = "a(x{life})"
    dependencies = ["N(x{life})", "D(x{life})"]

    @classmethod
    def calculate(cls, calc, **kwargs):
        return calc[f"N(x{kwargs['life']})"].shift(-1) / calc[f"D(x{kwargs['life']})"]


class A_x(Column):
    """ PV of whole of life assurance paid in arrears. """

    parameters = {"life": "Life identifier (int)"}
    column_name = "A(x{life})"
    dependencies = ["M(x{life})", "D(x{life})"]

    @classmethod
    def calculate(cls, calc, **kwargs):
        return calc[f"M(x{kwargs['life']})"] / calc[f"D(x{kwargs['life']})"]


class NP_x(Column):
    """ Net premium for whole of life assurance. """

    parameters = {"life": "Life identifier (int)"}
    column_name = "NP(x{life})"
    dependencies = ["A(x{life})", "a_due(x{life})"]

    @classmethod
    def calculate(cls, calc, **kwargs):
        return calc[f"A(x{kwargs['life']})"] / calc[f"a_due(x{kwargs['life']})"]


class Ia_due_x(Column):
    """ PV of arithmetically increasing annuity due (paid in advance) for remainder of life. """

    parameters = {"life": "Life identifier (int)"}
    column_name = "Ia_due(x{life})"
    dependencies = ["S(x{life})", "D(x{life})"]

    @classmethod
    def calculate(cls, calc, **kwargs):
        return calc[f"S(x{kwargs['life']})"] / calc[f"D(x{kwargs['life']})"]


class Ia_x(Column):
    """ PV of arithmetically increasing annuity (paid in arrears) for remainder of life. """

    parameters = {"life": "Life identifier (int)"}
    column_name = "Ia(x{life})"
    dependencies = ["S(x{life})", "D(x{life})"]

    @classmethod
    def calculate(cls, calc, **kwargs):
        return calc[f"S(x{kwargs['life']})"].shift(-1) / calc[f"D(x{kwargs['life']})"]


class IA_x(Column):
    """ PV of arithmetically increasing whole of life assurance paid in arrears. """

    parameters = {"life": "Life identifier (int)"}
    column_name = "IA(x{life})"
    dependencies = ["R(x{life})", "D(x{life})"]

    @classmethod
    def calculate(cls, calc, **kwargs):
        return calc[f"R(x{kwargs['life']})"] / calc[f"D(x{kwargs['life']})"]