import pandas as pd
from actymath.indexers import SliceNIndexer

from .base import Column
from actymath import ActyMathError

""" Defining time periods. """


class t(Column):
    """ Time period count starting at zero. """

    parameters = {}
    column_name = "t"

    @classmethod
    def calculate(cls, calc):
        return pd.Series(range(calc.shape[0]))


class n(Column):
    """ Remaining term (n) periods. """

    parameters = {"term_id": "Term identifier (int)", "n": "Term in periods (int)"}
    column_name = "n{term_id}"

    @classmethod
    def calculate(cls, calc, **kwargs):
        """ n is the remaining term. """
        return pd.Series(range(kwargs["n"], -1, -1))
