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


def test_Cx1():
    calc.populate("C(x1)")
    assert calc["C(x1)"].iloc[0] == pytest.approx(19.230016, abs=0.001)
    assert calc["C(x1)"].iloc[54] == pytest.approx(27.899252)


def test_Dx1():
    calc.populate("D(x1)")
    assert calc["D(x1)"].iloc[0] == pytest.approx(34481.408)
    assert calc["D(x1)"].iloc[54] == pytest.approx(3840.1664)


def test_Mx1():
    calc.populate("M(x1)")
    assert calc["M(x1)"].iloc[0] == pytest.approx(2333.9667)
    assert calc["M(x1)"].iloc[54] == pytest.approx(1673.131)


def test_Nx1():
    calc.populate("N(x1)")
    assert calc["N(x1)"].iloc[0] == pytest.approx(835833.48)
    assert calc["N(x1)"].iloc[54] == pytest.approx(56342.918)


def test_Rx1():
    calc.populate("R(x1)")
    assert calc["R(x1)"].iloc[0] == pytest.approx(141556.8)
    assert calc["R(x1)"].iloc[54] == pytest.approx(32227.231, abs=0.1)


def test_Sx1():
    calc.populate("S(x1)")
    assert calc["S(x1)"].iloc[0] == pytest.approx(18051194)
    assert calc["S(x1)"].iloc[54] == pytest.approx(627007.87)
