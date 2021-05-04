from abc import ABC, abstractclassmethod

import pandas as pd
import parse
from actymath import ActyMathError, columns


class Column:
    """ An abstract class for columns to populate """

    default = None  # A default value to use if the value is missing
    parameters = {}  # Required kwargs parameters for populating this Column.
    column_name = "overwrite_me({kwarg})"
    dependencies = []  # List of column names required for calculation

    @classmethod
    def column(cls, **kwargs):
        """ Returns the string Column name to create in DataFrame. """
        return cls.column_name.format(**kwargs)

    @classmethod
    def parse_column(cls, column):
        """
        Reverses the column name into the column_name and kwargs.
        Returns them as a tuple (column_name, dict of kwargs).
        """
        result = parse.parse(cls.column_name, column, case_sensitive=True)
        if result:
            return (cls.column_name, result.named)

    @classmethod
    def calculate(cls, calc: pd.DataFrame, **kwargs):
        """
        Pandas calculation using dataframe columns.
        Must return a Pandas Series.
        This series will be inserted in the column with the column name.
        """
        raise ActyMathError(f"Calculate method for {cls} not yet implemented.")

    @classmethod
    def populate(cls, calc, force=False, **kwargs):
        """ Populates this object and any dependencies in the Grid DataFrame. """

        # Validate that the required parameters are provided
        for param in cls.parameters.keys():
            if param not in kwargs:
                raise ActyMathError(
                    f"Missing parameter ({param}) to populate ({cls}) - {cls.parameters[param]}."
                )

        # If column already exists then skip
        if cls.column(**kwargs) in calc.columns and force is False:
            return

        # First check dependencies exist and if not, then create them, first
        for column_name in cls.dependencies:
            column = column_name.format(**kwargs)
            if column not in calc.columns or force is True:
                calc.populate(column, force=force)
                # try:
                #     class_ = calc.register[column_name]
                #     class_.populate(calc, force=force, **kwargs)
                # except Exception as e:
                #     raise ActyMathError(
                #         f"Unable to populate dependency column ({column_name}) - does the class for this column exist? - {e}"
                #     )

        # Calculate pandas series and insert in a new column
        new_column = cls.column(**kwargs)
        calc[new_column] = cls.calculate(calc, **kwargs)
        if cls.default is not None:
            calc[new_column].fillna(0, inplace=True)

        return new_column
