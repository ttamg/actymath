import pandas as pd
from actymath import Calc, columns
from actymath.calc import register
from actymath.tables import A1967_70_Exams


def get_qx():
    table = A1967_70_Exams()
    q30 = table.qx(30, select=True)
    return q30


def test_register_created_correctly():
    """ the register should create at import time """
    assert "x{life}" in register.keys()
    assert register["x{life}"] == columns.Age


def test_calc_is_dataframe():
    calc = Calc()
    assert isinstance(calc, pd.DataFrame)


def test_calc_add_life():
    calc = Calc()
    result = calc.add_life(age=30, qx=get_qx())
    assert result == "x1"
    assert "x1" in calc.columns
    assert "q(x1)" in calc.columns
    assert calc["x1"].iloc[0] == 30

