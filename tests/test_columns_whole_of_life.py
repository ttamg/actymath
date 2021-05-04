import pytest
from actymath import Calc
from actymath.tables import A1967_70_Exams

# A1967-70 table - Actuarial Green tables for testing
table = A1967_70_Exams()
q0 = table.qx(0, select=True)

# Create calc
calc = Calc()
calc.add_life(0, q0)
calc.add_i(rate=0.04)  # Will use 4% tables

# Set the l(x) with the right base for the tables
calc.populate("l(x1)")


def test_a_due_x1():
    calc.populate("a_due(x1)")
    assert calc["a_due(x1)"].iloc[0] == pytest.approx(24.240, abs=0.001)
    assert calc["a_due(x1)"].iloc[54] == pytest.approx(14.672, abs=0.001)


def test_a_x1():
    calc.populate("a(x1)")
    assert calc["a(x1)"].iloc[53] == pytest.approx(
        14.672 * 3840.1664 / 4020.9326, abs=0.001
    )


def test_A_x1():
    calc.populate("A(x1)")
    assert calc["A(x1)"].iloc[0] == pytest.approx(0.06769, abs=0.00001)
    assert calc["A(x1)"].iloc[54] == pytest.approx(0.43569, abs=0.00001)


def test_NP_x1():
    calc.populate("NP(x1)")
    assert calc["NP(x1)"].iloc[0] == pytest.approx(0.00279, abs=0.00001)
    assert calc["NP(x1)"].iloc[54] == pytest.approx(0.02970, abs=0.00001)


def test_Ia_due_x1():
    calc.populate("Ia_due(x1)")
    assert calc["Ia_due(x1)"].iloc[54] == pytest.approx(
        627007.87 / 3840.1664, rel=0.0001
    )  # ultimate


def test_Ia_x1():
    calc.populate("Ia(x1)")
    assert calc["Ia(x1)"].iloc[54] == pytest.approx(
        570664.95 / 3840.1664, rel=0.0001
    )  # ultimate


def test_IA_x1():
    calc.populate("IA(x1)")
    assert calc["IA(x1)"].iloc[54] == pytest.approx(
        32227.231 / 3840.1664, rel=0.0001
    )  # ultimate
