import pandas as pd

from .base import Column
from actymath.indexers import SliceToEndIndexer

""" Commutation functions. """

# Indexers to perform Pandas slice operations
indexer_to_end = SliceToEndIndexer()


class Cx(Column):
    """ Commutation factor Cx. """

    parameters = {"life": "Life identifier (int)"}
    column_name = "C(x{life})"
    dependencies = ["v^t", "d(x{life})"]

    @classmethod
    def calculate(cls, calc, **kwargs):
        return calc["v^t"].shift(-1) * calc[f"d(x{kwargs['life']})"]


class Dx(Column):
    """ Commutation factor Dx. """

    parameters = {"life": "Life identifier (int)"}
    column_name = "D(x{life})"
    dependencies = ["v^t", "l(x{life})"]

    @classmethod
    def calculate(cls, calc, **kwargs):
        return calc["v^t"] * calc[f"l(x{kwargs['life']})"]


class Mx(Column):
    """ Commutation factor Mx. """

    parameters = {"life": "Life identifier (int)"}
    column_name = "M(x{life})"
    dependencies = ["C(x{life})"]

    @classmethod
    def calculate(cls, calc, **kwargs):
        return calc[f"C(x{kwargs['life']})"].rolling(indexer_to_end).sum()


class Nx(Column):
    """ Commutation factor Nx. """

    parameters = {"life": "Life identifier (int)"}
    column_name = "N(x{life})"
    dependencies = ["D(x{life})"]

    @classmethod
    def calculate(cls, calc, **kwargs):
        return calc[f"D(x{kwargs['life']})"].rolling(indexer_to_end).sum()


class Rx(Column):
    """ Commutation factor Rx. """

    parameters = {"life": "Life identifier (int)"}
    column_name = "R(x{life})"
    dependencies = ["M(x{life})"]

    @classmethod
    def calculate(cls, calc, **kwargs):
        return calc[f"M(x{kwargs['life']})"].rolling(indexer_to_end).sum()


class Sx(Column):
    """ Commutation factor Sx. """

    parameters = {"life": "Life identifier (int)"}
    column_name = "S(x{life})"
    dependencies = ["N(x{life})"]

    @classmethod
    def calculate(cls, calc, **kwargs):
        return calc[f"N(x{kwargs['life']})"].rolling(indexer_to_end).sum()


""" Commutation value at fixed term """
