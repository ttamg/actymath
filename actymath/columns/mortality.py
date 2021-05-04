import pandas as pd

from .base import Column
from actymath import ActyMathError
from actymath.indexers import SliceToEndIndexer


""" Base mortality functions. """

indexer_to_end = SliceToEndIndexer()


class Age(Column):
    """ Age of a life. """

    parameters = {
        "life": "Life identifier (int)",
        "age": "Age at start of the life (int).",
    }
    column_name = "x{life}"

    @classmethod
    def calculate(cls, calc, **kwargs):
        return pd.Series(range(kwargs["age"], calc.shape[0] + kwargs["age"]))


class q_x(Column):
    """ Mortality q(x) of a life. """

    parameters = {
        "life": "Life identifier (int)",
        "qx": "List of mortality rates for this life starting at life age at time zero (list of float).",
    }

    column_name = "q(x{life})"

    @classmethod
    def calculate(cls, calc, **kwargs):
        return pd.Series(kwargs["qx"])


class p_x(Column):
    """ Probability p(x) of surviving until next period. """

    parameters = {
        "life": "Life identifier (int)",
    }
    column_name = "p(x{life})"
    dependencies = ["q(x{life})"]

    @classmethod
    def calculate(cls, calc, **kwargs):
        return 1 - calc[f"q(x{kwargs['life']})"]


class l_x(Column):
    """ Number of lives l(x) from original population alive at this age. """

    parameters = {
        "life": "Life identifier (int)",
    }
    column_name = "l(x{life})"
    dependencies = ["q(x{life})"]

    # TODO: Set up initial lx value in parameter

    @classmethod
    def calculate(cls, calc, **kwargs):
        if "base" in kwargs:  # Optional starting value for lx
            base = kwargs["base"]
        else:
            base = 34481.408
        values = []
        values.append(base)
        for i, index in enumerate(calc.index):
            values.append(values[i] * (1 - calc[f"q(x{kwargs['life']})"].iloc[index]))
        return pd.Series(values)


class d_x(Column):
    """ Number of deaths d(x) from original population in this period. """

    parameters = {
        "life": "Life identifier (int)",
    }
    column_name = "d(x{life})"
    dependencies = ["l(x{life})"]

    @classmethod
    def calculate(cls, calc, **kwargs):
        return calc[f"l(x{kwargs['life']})"] - calc[f"l(x{kwargs['life']})"].shift(-1)


# TODO: NOT EFFICIENT OR CORRECT YET
# class e_x(Column):
#     """ Expectation of life e(x). """

#     parameters = {
#         "life": "Life identifier (int)",
#     }
#     column_name = "e(x{life})"
#     dependencies = ["l(x{life})", "d(x{life})", "t"]

#     @classmethod
#     def calculate(cls, calc, **kwargs):
#         Idx = (calc[f"d(x{kwargs['life']})"] * calc["t"]).rolling(indexer_to_end).sum()
#         return Idx / calc[f"l(x{kwargs['life']})"]
