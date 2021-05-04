import pytest
from actymath.tables import (
    MortalityTableError,
    TestTable,
    TestTable2,
    AMC00,
    A1967_70_Exams,
    A1967_70,
)


def test_qx_read_correctly():
    """ TestTable uses a one dimensional table structure. """
    table = TestTable()
    assert table.qx(30)[0] == 0.000531


def test_qx_read_invalid_age_raises_error():
    table = TestTable()
    with pytest.raises(MortalityTableError):
        assert table.qx(5)[0] == 0.000531


def test_lx_table_converts_to_qx_when_read():
    """ TestTable2 is one dimensional and specified using l(x) values not q(x) values. """
    table = TestTable2()
    assert table.qx(20)[0] == pytest.approx(1 - (66000 / 70000))


def test_A1967_70_horizontal_read_correctly():
    """ The examps A1967-70 table uses Lx and horizontal layout """
    table = A1967_70_Exams()
    # select mortality
    q30 = table.qx(30)
    assert q30[0] == pytest.approx(0.00043767, abs=0.00000001)  # Select mortality
    assert q30[4] == pytest.approx(0.00079004, abs=0.00000001)  # Ultimate mortality
    # ultimate mortality
    q30 = table.qx(30, select=False)
    assert q30[0] == pytest.approx(0.00065368, abs=0.00000001)  # Ultimate mortality
    assert q30[4] == pytest.approx(0.00079004, abs=0.00000001)  # Ultimate mortality


def test_A1967_70_diagonal_read_correctly():
    """ The CMI A1967-70 table uses diagonal qx layout """
    table = A1967_70()
    # select mortality
    q30 = table.qx(30)
    assert q30[0] == pytest.approx(0.00043767, abs=0.00000001)  # Select mortality
    assert q30[4] == pytest.approx(0.00079004, abs=0.00000001)  # Ultimate mortality
    # ultimate mortality
    q30 = table.qx(30, select=False)
    assert q30[0] == pytest.approx(0.00065368, abs=0.00000001)  # Ultimate mortality
    assert q30[4] == pytest.approx(0.00079004, abs=0.00000001)  # Ultimate mortality
