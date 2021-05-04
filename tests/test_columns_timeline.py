import pandas as pd
import pytest
from actymath import Calc
from actymath.tables import A1967_70_Exams

# A1967-70 table - Actuarial Green tables for testing
table = A1967_70_Exams()
q45 = table.qx(45, select=True)

# Create calc
calc = Calc()
calc.add_life(45, q45)
calc.add_i(rate=0.04)  # Will use 4% tables


def test_t():
    calc.populate("t")
    assert calc["t"].iloc[0] == 0
    assert calc["t"].iloc[25] == 25


def test_n():
    calc.add_term(n=10)
    calc.add_term(n=20)
    assert calc["n1"].iloc[0] == 10
    assert calc["n1"].iloc[10] == 0
    assert pd.isnull(calc["n1"].iloc[11])
    assert calc["n2"].iloc[0] == 20
    assert calc["n2"].iloc[10] == 10
