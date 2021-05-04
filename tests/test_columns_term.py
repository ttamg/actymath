import pandas as pd
import pytest
from actymath import Calc
from actymath.tables import A1967_70_Exams

# A1967-70 table - Actuarial Green tables for testing
table = A1967_70_Exams()
q45 = table.qx(45, select=True)  # Select
q54 = table.qx(54, select=False)  # Ultimate

# Create calc
calc = Calc()
calc.add_life(45, q45)
calc.add_i(rate=0.04)  # Will use 4% tables
calc.add_term(n=10)  # Will use the x+n = 55 tables in Green tables for tests

# Set the l(x) with the right base for the tables
calc.populate("l(x1)")


calc54 = Calc()  # 54 year old
calc54.add_life(54, q54)
calc54.add_i(rate=0.04)  # Will use 4% tables
calc54.add_term(n=10)
calc54.populate("l(x1)")


def test_a_due_x1_n1():
    calc.populate("a_due(x1)[n1]")
    assert calc["a_due(x1)[n1]"].iloc[0] == pytest.approx(8.317, abs=0.001)  # Select
    assert calc["a_due(x1)[n1]"].iloc[5] == pytest.approx(4.582, abs=0.001)  # Ultimate
    assert calc["a_due(x1)[n1]"].iloc[10] == 0
    assert calc["a_due(x1)[n1]"].iloc[12] == 0  # Will stop after end of term


def test_a_x1_n1():
    calc.populate("a(x1)[n1]")
    assert calc["a(x1)[n1]"].iloc[5] == pytest.approx(
        (68970.076 - 48838.184) / 4597.0607, abs=0.001
    )  # Ultimate
    assert calc["a(x1)[n1]"].iloc[10] == 0.0
    assert calc["a(x1)[n1]"].iloc[12] == 0


def test_EA_x1_n1():
    calc.populate("EA(x1)[n1]")
    # print(calc["EA(x1)[n1]"][:15])
    assert calc["EA(x1)[n1]"].iloc[0] == pytest.approx(0.68013, abs=0.00001)  # Select
    assert calc["EA(x1)[n1]"].iloc[5] == pytest.approx(0.82376, abs=0.00001)  # Ultimate
    assert calc["EA(x1)[n1]"].iloc[10] == 1.0
    assert calc["EA(x1)[n1]"].iloc[12] == 0


def test_NP_x1_n1():
    calc.populate("NP(x1)[n1]")
    assert calc["NP(x1)[n1]"].iloc[0] == pytest.approx(0.08178, abs=0.00001)  # Select
    assert calc["NP(x1)[n1]"].iloc[5] == pytest.approx(0.17978, abs=0.00001)  # Ultimate
    assert calc["NP(x1)[n1]"].iloc[10] == 0
    assert calc["NP(x1)[n1]"].iloc[12] == 0


def test_E_x1_n1_and_A_x1_n1():
    """ Should sum up to the EA total in the tables """
    calc.populate("EA(x1)[n1]")
    calc.populate("E(x1)[n1]")
    calc.populate("A(x1)[n1]")
    for index in (0, 5, 10):
        assert calc["EA(x1)[n1]"].iloc[index] == pytest.approx(
            calc["E(x1)[n1]"].iloc[index] + calc["A(x1)[n1]"].iloc[index]
        )
    assert calc["E(x1)[n1]"].iloc[10] == 1.0
    assert calc["A(x1)[n1]"].iloc[10] == 0
    assert calc["E(x1)[n1]"].iloc[12] == 0
    assert calc["A(x1)[n1]"].iloc[12] == 0


def test_Ia_due_x_n():
    calc54.populate("Ia_due(x1)[n1]")
    assert calc54["Ia_due(x1)[n1]"].iloc[0] == pytest.approx(
        (627007.87 - 216287.48) / 3840.1664, rel=0.0001
    )  # ultimate
    assert calc54["Ia_due(x1)[n1]"].iloc[11] == 0


def test_Ia_x_n():
    calc54.populate("Ia(x1)[n1]")
    assert calc54["Ia(x1)[n1]"].iloc[0] == pytest.approx(
        (570664.95 - 190986.55) / 3840.1664, rel=0.0001
    )  # ultimate
    assert calc54["Ia(x1)[n1]"].iloc[11] == 0


def test_IA_x_n():
    calc54.populate("IA(x1)[n1]")
    assert calc54["IA(x1)[n1]"].iloc[0] == pytest.approx(
        (32227.231 - 16982.186) / 3840.1664, rel=0.0001
    )  # ultimate
    assert calc54["IA(x1)[n1]"].iloc[11] == 0


def test_IE_x_n():
    calc54.populate("IE(x1)[n1]")
    assert calc54["IE(x1)[n1]"].iloc[0] == pytest.approx(
        (2279.50 * 10) / 3840.1664, rel=0.0001
    )  # ultimate
    assert calc54["IE(x1)[n1]"].iloc[11] == 0


def test_IEA_x_n():
    calc54.populate("IEA(x1)[n1]")
    assert calc54["IEA(x1)[n1]"].iloc[0] == pytest.approx(
        (32227.231 - 16982.186 + 2279.50 * 10) / 3840.1664, rel=0.0001
    )  # ultimate
    assert calc54["IEA(x1)[n1]"].iloc[11] == 0
