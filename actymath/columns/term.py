import pandas as pd
import numpy as np
from actymath import ActyMathError

from .base import Column

""" Actuarial formulae for term limited life insurance. """


class a_due_x_n(Column):
    """ PV of annuity due (paid in advance) for term n. """

    parameters = {"life": "Life identifier (int)", "term_id": "Term identifier (int)"}
    column_name = "a_due(x{life})[n{term_id}]"
    dependencies = ["N(x{life})", "D(x{life})", "n{term_id}"]
    default = 0

    @classmethod
    def calculate(cls, calc, **kwargs):
        location = int(calc[f"n{kwargs['term_id']}"].get(0))
        return (
            (
                calc[f"N(x{kwargs['life']})"]
                - calc[f"N(x{kwargs['life']})"].get(location)
            )
            / calc[f"D(x{kwargs['life']})"]
        )[: location + 1]


class a_x_n(Column):
    """ PV of annuity (paid in arrears) for term n. """

    parameters = {"life": "Life identifier (int)", "term_id": "Term identifier (int)"}
    column_name = "a(x{life})[n{term_id}]"
    dependencies = ["N(x{life})", "D(x{life})", "n{term_id}"]
    default = 0

    @classmethod
    def calculate(cls, calc, **kwargs):
        location = int(calc[f"n{kwargs['term_id']}"].get(0))
        return (
            (
                calc[f"N(x{kwargs['life']})"].shift(-1)
                - calc[f"N(x{kwargs['life']})"].get(location + 1)
            )
            / calc[f"D(x{kwargs['life']})"]
        )[: location + 1]


class A_x_n(Column):
    """ PV of a term assurance (paid in arrears) for term n. """

    parameters = {"life": "Life identifier (int)", "term_id": "Term identifier (int)"}
    column_name = "A(x{life})[n{term_id}]"
    dependencies = ["M(x{life})", "D(x{life})", "n{term_id}"]
    default = 0

    @classmethod
    def calculate(cls, calc, **kwargs):
        location = int(calc[f"n{kwargs['term_id']}"].get(0))
        return (
            (
                calc[f"M(x{kwargs['life']})"]
                - calc[f"M(x{kwargs['life']})"].get(location)
            )
            / calc[f"D(x{kwargs['life']})"]
        )[: location + 1]


class E_x_n(Column):
    """ PV of a pure endowment for term n. """

    parameters = {"life": "Life identifier (int)", "term_id": "Term identifier (int)"}
    column_name = "E(x{life})[n{term_id}]"
    dependencies = ["D(x{life})", "n{term_id}"]
    default = 0

    @classmethod
    def calculate(cls, calc, **kwargs):
        location = int(calc[f"n{kwargs['term_id']}"].get(0))
        return (
            calc[f"D(x{kwargs['life']})"].get(location) / calc[f"D(x{kwargs['life']})"]
        )[: location + 1]


class EA_x_n(Column):
    """ PV of an endowment assurance (paid in arrears) for term n. """

    parameters = {"life": "Life identifier (int)", "term_id": "Term identifier (int)"}
    column_name = "EA(x{life})[n{term_id}]"
    dependencies = ["M(x{life})", "D(x{life})", "n{term_id}"]
    default = 0

    @classmethod
    def calculate(cls, calc, **kwargs):
        location = int(calc[f"n{kwargs['term_id']}"].get(0))
        return (
            (
                calc[f"M(x{kwargs['life']})"]
                - calc[f"M(x{kwargs['life']})"].get(location)
                + calc[f"D(x{kwargs['life']})"].get(location)
            )
            / calc[f"D(x{kwargs['life']})"]
        )[: location + 1]


class NP_x_n(Column):
    """ Net Premium a term assurance for term n. """

    parameters = {"life": "Life identifier (int)", "term_id": "Term identifier (int)"}
    column_name = "NP(x{life})[n{term_id}]"
    dependencies = ["EA(x{life})[n{term_id}]", "a_due(x{life})[n{term_id}]"]
    default = 0

    @classmethod
    def calculate(cls, calc, **kwargs):
        return (
            calc[f"EA(x{kwargs['life']})[n{kwargs['term_id']}]"]
            / calc[f"a_due(x{kwargs['life']})[n{kwargs['term_id']}]"]
        ).replace([np.inf, -np.inf], np.nan)


class Ia_due_x_n(Column):
    """ PV of arithmetically increasing annuity due (paid in advance) for term n. """

    parameters = {"life": "Life identifier (int)", "term_id": "Term identifier (int)"}
    column_name = "Ia_due(x{life})[n{term_id}]"
    dependencies = ["S(x{life})", "D(x{life})", "n{term_id}"]
    default = 0

    @classmethod
    def calculate(cls, calc, **kwargs):
        location = int(calc[f"n{kwargs['term_id']}"].get(0))
        return (
            (
                calc[f"S(x{kwargs['life']})"]
                - calc[f"S(x{kwargs['life']})"].get(location)
            )
            / calc[f"D(x{kwargs['life']})"]
        )[: location + 1]


class Ia_x_n(Column):
    """ PV of arithmetically increasing annuity (paid in arrears) for term n. """

    parameters = {"life": "Life identifier (int)", "term_id": "Term identifier (int)"}
    column_name = "Ia(x{life})[n{term_id}]"
    dependencies = ["S(x{life})", "D(x{life})", "n{term_id}"]
    default = 0

    @classmethod
    def calculate(cls, calc, **kwargs):
        location = int(calc[f"n{kwargs['term_id']}"].get(0))
        return (
            (
                calc[f"S(x{kwargs['life']})"].shift(-1)
                - calc[f"S(x{kwargs['life']})"].get(location + 1)
            )
            / calc[f"D(x{kwargs['life']})"]
        )[: location + 1]


class IA_x_n(Column):
    """ PV of arithmetically increasing term assurance (paid in arrears) for term n. """

    parameters = {"life": "Life identifier (int)", "term_id": "Term identifier (int)"}
    column_name = "IA(x{life})[n{term_id}]"
    dependencies = ["R(x{life})", "D(x{life})", "n{term_id}"]
    default = 0

    @classmethod
    def calculate(cls, calc, **kwargs):
        location = int(calc[f"n{kwargs['term_id']}"].get(0))
        return (
            (
                calc[f"R(x{kwargs['life']})"]
                - calc[f"R(x{kwargs['life']})"].get(location)
            )
            / calc[f"D(x{kwargs['life']})"]
        )[: location + 1]


class IE_x_n(Column):
    """ PV of arithmetically increasing pure endowment (paid in arrears) for term n. """

    parameters = {"life": "Life identifier (int)", "term_id": "Term identifier (int)"}
    column_name = "IE(x{life})[n{term_id}]"
    dependencies = ["D(x{life})", "n{term_id}"]
    default = 0

    @classmethod
    def calculate(cls, calc, **kwargs):
        location = int(calc[f"n{kwargs['term_id']}"].get(0))
        return (
            calc[f"D(x{kwargs['life']})"].get(location)
            * location
            / calc[f"D(x{kwargs['life']})"]
        )[: location + 1]


class IAE_x_n(Column):
    """ PV of arithmetically increasing endowment assurance (paid in arrears) for term n. """

    parameters = {"life": "Life identifier (int)", "term_id": "Term identifier (int)"}
    column_name = "IEA(x{life})[n{term_id}]"
    dependencies = ["IE(x{life})[n{term_id}]", "IA(x{life})[n{term_id}]"]
    default = 0

    @classmethod
    def calculate(cls, calc, **kwargs):
        location = int(calc[f"n{kwargs['term_id']}"].get(0))
        return (
            calc[f"IE(x{kwargs['life']})[n{kwargs['term_id']}]"]
            + calc[f"IA(x{kwargs['life']})[n{kwargs['term_id']}]"]
        )