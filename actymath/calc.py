import numpy as np
import pandas as pd

from .indexers import SliceNIndexer, SliceToEndIndexer
from actymath import columns, ActyMathError


# A dictionary mapping all column names to Column classes - created on the fly at import time
register = dict(
    [
        (cls.column_name, cls)
        for name, cls in columns.__dict__.items()
        if isinstance(cls, type)
    ]
)


class Calc(pd.DataFrame):
    """
    A modified pandas Dataframe with some additional properties
    and methods for creating and actuarial calculation.
    """

    @property
    def _constructor(self):
        return Calc

    _metadata = ["life_count", "term_count", "register"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.life_count = 0
        self.term_count = 0
        self.register = register

    def add_life(self, age: int, qx: list):
        """
        Add a life and their mortality to the Calc.

        Params:
        - age (int) - Age of life at the start
        - qx (list) - list of q(x) values for this life starting at starting age

        Returns:
        - Life identifier / column name
        """
        self.life_count += 1
        column = columns.q_x.populate(calc=self, life=self.life_count, qx=qx)
        column = columns.Age.populate(calc=self, life=self.life_count, age=age)
        return column

    def add_term(self, n: int):
        """
        Add a term (n) to the Calc.

        Params:
        - n (int) - Term in periods.

        Returns:
        - Term identifier / column name
        """
        self.term_count += 1
        column = columns.n.populate(calc=self, term_id=self.term_count, n=n)
        return column

    def add_i(self, rate: float):
        """
        Add the fixed interest rate to the Calc.

        Params:
        - rate (float) - the interest rate per period, fixed through the term.
        """
        self["i"] = rate

    @property
    def formulae(self):
        """ Returns a dictionary of the potential column names registered and description of the column (from the docstring). """
        return {k: v.__doc__ for k, v in self.register.items()}

    def populate(self, column: str, force=False):
        """
        Populates a particular column in the Calc dataframe, including any dependencies.

        Params:
        - column (str) - the name of the column to fetch and calculate
        - force (bool) - optional if set to True will force a recalculation of all dependent columns.  Default is False.
        """
        if column in self.register:
            # Fetch class directly
            class_ = self.register[column]
            class_.populate(calc=self, force=force)
            return
        else:
            # Parse name and kwargs from the column names
            for class_ in self.register.values():
                result = class_.parse_column(column)
                if result is not None:
                    kwargs = result[1]
                    class_.populate(calc=self, force=force, **kwargs)
                    return

        raise ActyMathError(
            f"Unable to populate column ({column}) - does the class for this column exist?"
        )