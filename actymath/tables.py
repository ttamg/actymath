import csv
import os
from abc import ABC, abstractmethod

DATA_PATH = os.path.dirname(__file__) + "/table_data"


def convert_lx_to_qx(lx_list: list):
    """ Converts a list of lx values to a qx list. """
    q_values = []
    for i, l in enumerate(lx_list[:-1]):
        q_values.append(1 - lx_list[i + 1] / l)
    return q_values


class MortalityTableError(Exception):
    pass


class MortalityTable(ABC):
    """ Abstract mortality table """

    def __init__(self):
        self.data = []
        self.age_index = {}

    @abstractmethod
    def qx(self, age, **kwargs):
        """ returns a list of q values starting with the age requested """


class OneDimensionTableMixIn:
    """
    Simple one dimensional mortality table.
    """

    table_type = "qx"  # data is either 'qx' or 'lx'

    def qx(self, age):
        """ Returns a list of the future q(x) for the age. """
        if age not in self.age_index.keys():
            raise MortalityTableError(f"Age {age} not found in the table")
        index = self.age_index[age]
        values = [x[0] for x in self.data[index:]]

        if self.table_type == "qx":
            return values

        elif self.table_type == "lx":
            return convert_lx_to_qx(values)

        else:
            raise MortalityTableError(
                f"Unknown table type {self.table_type}.  Check mortality table class is defined correctly."
            )


class TwoDimensionHorizontalTableMixIn:
    """
    Two dimensional mortality table with select mortality along a row,
    and then ultimate mortality down the right hand column.
    """

    def qx(self, age, select=True):
        """
        Returns a list of the future q(x) for the age.
        Uses select mortality when select=True, ultimate mortality otherwise.
        """
        if age not in self.age_index.keys():
            raise MortalityTableError(f"Age {age} not found in the table")

        if select:
            index = self.age_index[age]
            values = self.data[index]  # Select mortality
            values.extend([x[self.ultimate_col] for x in self.data[index + 1 :]])

        else:
            index = self.age_index[age] - self.ultimate_col
            values = [x[self.ultimate_col] for x in self.data[index:]]

        if self.table_type == "qx":
            return values

        elif self.table_type == "lx":
            return convert_lx_to_qx(values)

        else:
            raise MortalityTableError(
                f"Unknown table type {self.table_type}.  Check mortality table class is defined correctly."
            )


class TwoDimensionDiagonalTableMixIn:
    """
    Two dimensional mortality table that starts left and then rolls down
    the right column for ultimate mortality values
    """

    def qx(self, age, select=True):
        """
        Returns a list of the future q(x) for the age.
        Uses select mortality when select=True, ultimate mortality otherwise.
        """
        if age not in self.age_index.keys():
            raise MortalityTableError(f"Age {age} not found in the table")

        if select:
            values = []
            index = self.age_index[age]
            for i in range(self.ultimate_col):
                values.append(self.data[index + i][i])
            values.extend(
                [x[self.ultimate_col] for x in self.data[index + self.ultimate_col :]]
            )

        else:
            index = self.age_index[age]
            values = [x[self.ultimate_col] for x in self.data[index:]]

        if self.table_type == "qx":
            return values

        elif self.table_type == "lx":
            return convert_lx_to_qx(values)

        else:
            raise MortalityTableError(
                f"Unknown table type {self.table_type}.  Check mortality table class is defined correctly."
            )


class CSVMortalityTable(MortalityTable):
    """
    Loads a mortality table from CSV file
    Two dimensional tables are loaded into multiple columns.
    Specify table data type as 'qx' or 'lx'.
    Constructor will build lx, dx and qx data when it loads.
    """

    path = DATA_PATH
    filename = None
    age_column = ""  # The name of the column where age sits
    table_type = "qx"  # data is either 'qx' or 'lx'
    value_columns = []  # The name of the value columns in the order to be read

    def __init__(self, filename=None, path=None):
        super().__init__()
        if path is not None:
            self.path = path
        if filename is not None:
            self.filename = filename

        with open(f"{self.path}/{self.filename}") as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                self.age_index[float(row[self.age_column])] = i
                self.data.append(
                    [float(row[x]) if row[x] else None for x in self.value_columns]
                )

        self.ultimate_col = len(self.value_columns) - 1  # Index for last column


class TestTable(OneDimensionTableMixIn, CSVMortalityTable):
    """ A test mortality table. """

    filename = "test.csv"
    age_column = "Age x"
    table_type = "qx"
    value_columns = ["q x"]


class TestTable2(OneDimensionTableMixIn, CSVMortalityTable):
    """ A test mortality table using lx. """

    filename = "test_lx.csv"
    age_column = "Age x"
    table_type = "lx"
    value_columns = ["l x"]


class AMC00(TwoDimensionDiagonalTableMixIn, CSVMortalityTable):
    """UK AMC00 mortality table.
    https://www.actuaries.org.uk/learn-and-develop/continuous-mortality-investigation/cmi-mortality-and-morbidity-tables/00-series-tables
    """

    filename = "amc00.csv"
    age_column = "Age x"
    table_type = "qx"
    value_columns = ["Duration 0", "Duration 1", "Durations 2+"]


class A1967_70_Exams(TwoDimensionHorizontalTableMixIn, CSVMortalityTable):
    """UK A1967-70 mortality table used in actuarial examinations.
    https://www.actuaries.org.uk/learn-and-develop/continuous-mortality-investigation/cmi-mortality-and-morbidity-tables/mortality-rates-older-mortality-tables
    """

    filename = "a1967-70_exam.csv"
    age_column = "x"
    table_type = "lx"
    value_columns = ["l[x]", "l([x]+1)", "l(x+2)"]


class A1967_70(TwoDimensionDiagonalTableMixIn, CSVMortalityTable):
    """UK A1967-70 mortality table provided by the CMI usese Qx in diagonal select pattern.
    https://www.actuaries.org.uk/learn-and-develop/continuous-mortality-investigation/cmi-mortality-and-morbidity-tables/mortality-rates-older-mortality-tables
    """

    filename = "a1967-70.csv"
    age_column = "Age x"
    table_type = "qx"
    value_columns = ["Duration 0", "Duration 1", "Durations 2+"]
