from .base import Column
from actymath import ActyMathError


class i(Column):
    """ Fixed interest rate """

    column_name = "i"

    @classmethod
    def calculate(cls, calc, **kwargs):
        raise ActyMathError(f"{cls} calculation method not yet implemented ")


class v(Column):
    """ Discount factor v^t to discount for interest rates to first index period """

    column_name = "v^t"
    dependencies = [
        "i",
    ]

    @classmethod
    def calculate(cls, calc, **kwargs):
        return (1 + calc["i"]) ** (-calc.index)
