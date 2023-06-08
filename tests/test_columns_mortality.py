import pytest

from actymath import Calc
from actymath.exceptions import ActyMathError
from actymath.tables import A1967_70_Exams

# A1967-70 table - Actuarial Green tables for testing
table = A1967_70_Exams()
q0 = table.qx(0, select=True)

# Create calc
calc = Calc()
calc.add_life(0, q0)
calc.add_i(rate=0.04)  # Will use 4% tables


def test_qx1():
    assert calc["q(x1)"].iloc[0] == pytest.approx(0.00058, abs=0.00001)
    assert calc["q(x1)"].iloc[4] == pytest.approx(0.00053, abs=0.00001)


def test_px1():
    calc.populate("p(x1)")
    assert calc["p(x1)"].iloc[0] == pytest.approx(1 - 0.0005800)
    assert calc["p(x1)"].iloc[4] == pytest.approx(1 - 0.00053000)


def test_lx1():
    calc.populate("l(x1)")
    assert calc["l(x1)"].iloc[0] == pytest.approx(34481.408)
    assert calc["l(x1)"].iloc[4] == pytest.approx(34398.727)
    assert calc["l(x1)"].iloc[54] == pytest.approx(31926.430)


def test_dx1():
    calc.populate("d(x1)")
    assert calc["d(x1)"].iloc[0] == pytest.approx(19.999)
    assert calc["d(x1)"].iloc[4] == pytest.approx(18.231)
    assert calc["d(x1)"].iloc[54] == pytest.approx(241.227)


def test_dx2_raises_error():
    with pytest.raises(ActyMathError):
        calc.populate("d(x2)")


# def test_e_x():
#     calc.populate("e(x1)")
#     print(calc["e(x1)"][:20])
#     assert calc["e(x1)"].iloc[0] == pytest.approx(73.321, abs=0.001)
#     assert calc["e(x1)"].iloc[4] == pytest.approx(69.493, abs=0.001)
#     assert calc["e(x1)"].iloc[54] == pytest.approx(22.099, abs=0.001)
