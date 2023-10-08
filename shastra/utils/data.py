from astropy.table import Table, Column
from astropy.io import fits
from astropy.table import Table
import numpy as np

class Data:
    def __init__(self, dataPath: str, primaryKey: str = ""):
        """
        Constructor for the Data class.

        Args:
            dataPath (str): The path to the FITS data file.
            primaryKey (str, optional): The primary key column name.

        Raises:
            FileNotFoundError: If the specified file does not exist.
        """
        try:
            dataFile = fits.open(dataPath, memmap=True)
            self.table = Table(dataFile[1].data)
            if primaryKey == "":
                primaryKey = self.table.columns[0].name
            primaryKeyColumn = self.table[primaryKey]
            self.primaryKey = primaryKey
            self.primaryKeyList = [x.strip() for x in list(np.array(primaryKeyColumn))]
        except FileNotFoundError:
            raise FileNotFoundError("File Not Found: The specified file does not exist.")

    @classmethod
    def from_table(cls, table: Table, primaryKey: str = ""):
        """
        Create a Data object from an existing Astropy Table and primary key.

        Args:
            table (Table): The Astropy Table containing the data.
            primaryKey (str, optional): The primary key column name.

        Returns:
            Data: A new instance of the Data class.
        """
        data = cls.__new__(cls)
        data.table = table
        data.primaryKey = primaryKey
        data.primaryKeyList = [x.strip() for x in list(np.array(table[primaryKey]))]
        return data

    def __str__(self):
        """
        Return a string representation of the Data object.

        Returns:
            str: A string representation of the Data object.
        """
        return f"<Data> \n (Primary Key: {self.primaryKey}) \n {self.table}"

class Column:
    def __init__(self, data: Data, columnName: str, result=None):
        """
        Constructor for the Column class.

        Args:
            data (Data): The Data object that this column belongs to.
            columnName (str): The name of the column in the Data object.

        Returns:
            Column: A new instance of the Column class.
        """
        self.data = data  # Extract the Astropy Table from the Data object
        self.columnName = columnName
        self.result = result if result is not None else data.table[columnName]

    def newColumnName(self, operation: str, otherColumn=None):
        """
        Get an updated column name for the current operation.

        Args:
            operation (str): The operation symbol (e.g., '+', '-', '*', '/', '**').
            otherColumn (str, optional): The name of another column for binary operations.

        Returns:
            str: The updated column name.
        """
        if otherColumn:
            return f"{self.columnName} {operation} {otherColumn}"
        else:
            return f"{self.columnName} {operation}"

    def updatedData(self, newColumnName: str, result):
        """
        Update the Column's data attribute with a new column and set the new column name.

        Args:
            newColumnName (str): The name for the new column.
            result (astropy.table.Column): The result column to update the data attribute.
        """
        updated_data = self.data
        updated_data.table = Table(self.data.table)
        updated_data.table[newColumnName] = result
        self.data = updated_data
        self.columnName = newColumnName

    # Binary operations (+, -, *, /, **)

    def __add__(self, other):
        """
        Add another Column or a scalar to this column.

        Args:
            other (Column, int, float): The column or scalar to add.

        Returns:
            Column: A new Column containing the result of the addition.
        """
        if isinstance(other, Column):
            result = self.data.table[self.columnName] + other.data.table[other.columnName]
            newColumnName = self.newColumnName('+', other.columnName)
        elif isinstance(other, (int, float)):
            result = self.data.table[self.columnName] + other
            newColumnName = self.newColumnName('+', str(other))
        else:
            raise TypeError("Unsupported operand type for +")
        
        self.updatedData(newColumnName, result)
        return Column(self.data, newColumnName, result)

    def __sub__(self, other):
        """
        Subtract another Column or a scalar from this column.

        Args:
            other (Column, int, float): The column or scalar to subtract.

        Returns:
            Column: A new Column containing the result of the subtraction.
        """
        if isinstance(other, Column):
            result = self.data.table[self.columnName] - other.data.table[other.columnName]
            newColumnName = self.newColumnName('-', other.columnName)
        elif isinstance(other, (int, float)):
            result = self.data.table[self.columnName] - other
            newColumnName = self.newColumnName('-', str(other))
        else:
            raise TypeError("Unsupported operand type for -")
        
        self.updatedData(newColumnName, result)
        return Column(self.data, newColumnName, result)

    def __mul__(self, other):
        """
        Multiply this column by another Column or a scalar.

        Args:
            other (Column, int, float): The column or scalar to multiply by.

        Returns:
            Column: A new Column containing the result of the multiplication.
        """
        if isinstance(other, Column):
            result = self.data.table[self.columnName] * other.data.table[other.columnName]
            newColumnName = self.newColumnName('*', other.columnName)
        elif isinstance(other, (int, float)):
            result = self.data.table[self.columnName] * other
            newColumnName = self.newColumnName('*', str(other))
        else:
            raise TypeError("Unsupported operand type for *")
        
        self.updatedData(newColumnName, result)
        return Column(self.data, newColumnName, result)

    def __truediv__(self, other):
        """
        Divide this column by another Column or a scalar.

        Args:
            other (Column, int, float): The column or scalar to divide by.

        Returns:
            Column: A new Column containing the result of the division.
        """
        if isinstance(other, Column):
            if np.any(other.data.table[other.columnName] == 0):
                raise ValueError("Division by zero encountered.")
            result = self.data.table[self.columnName] / other.data.table[other.columnName]
            newColumnName = self.newColumnName('/', other.columnName)
        elif isinstance(other, (int, float)):
            if other == 0:
                raise ValueError("Division by zero encountered.")
            result = self.data.table[self.columnName] / other
            newColumnName = self.newColumnName('/', str(other))
        else:
            raise TypeError("Unsupported operand type for /")
        
        self.updatedData(newColumnName, result)
        return Column(self.data, newColumnName, result)

    def __pow__(self, other):
        """
        Raise this column to the power of another Column or a scalar.

        Args:
            other (Column, int, float): The column or scalar to raise to the power of.

        Returns:
            Column: A new Column containing the result of the exponentiation.
        """
        if isinstance(other, Column):
            result = self.data.table[self.columnName] ** other.data.table[other.columnName]
            newColumnName = self.newColumnName('**', other.columnName)
        elif isinstance(other, (int, float)):
            result = self.data.table[self.columnName] ** other
            newColumnName = self.newColumnName('**', str(other))
        else:
            raise TypeError("Unsupported operand type for **")
        
        self.updatedData(newColumnName, result)
        return Column(self.data, newColumnName, result)
        
    # Inequality operations (<, <=, >, >=, ==, !=)
    def __lt__(self, other):
        """
        Check if this column is less than another Column or a scalar.

        Args:
            other (Column, int, float): The column or scalar to compare with.

        Returns:
            Data: A new Data object containing rows where the comparison is True.
        """
        if isinstance(other, Column):
            result = self.data.table[self.columnName] < other.data.table[other.columnName]
        elif isinstance(other, (int, float)):
            result = self.data.table[self.columnName] < other
        else:
            raise TypeError("Unsupported operand type for <")
        
        mask = np.array(result, dtype=bool)
        filtered_data = self.data.table[mask]
        return Data.from_table(filtered_data, primaryKey=self.data.primaryKey)

    def __le__(self, other):
        """
        Check if this column is less than or equal to another Column or a scalar.

        Args:
            other (Column, int, float): The column or scalar to compare with.

        Returns:
            Data: A new Data object containing rows where the comparison is True.
        """
        if isinstance(other, Column):
            result = self.data.table[self.columnName] <= other.data.table[other.columnName]
        elif isinstance(other, (int, float)):
            result = self.data.table[self.columnName] <= other
        else:
            raise TypeError("Unsupported operand type for <=")
        
        mask = np.array(result, dtype=bool)
        filtered_data = self.data.table[mask]
        return Data.from_table(filtered_data, primaryKey=self.data.primaryKey)

    def __gt__(self, other):
        """
        Check if this column is greater than another Column or a scalar.

        Args:
            other (Column, int, float): The column or scalar to compare with.

        Returns:
            Data: A new Data object containing rows where the comparison is True.
        """
        if isinstance(other, Column):
            result = self.data.table[self.columnName] > other.data.table[other.columnName]
        elif isinstance(other, (int, float)):
            result = self.data.table[self.columnName] > other
        else:
            raise TypeError("Unsupported operand type for >")
        
        mask = np.array(result, dtype=bool)
        filtered_data = self.data.table[mask]
        return Data.from_table(filtered_data, primaryKey=self.data.primaryKey)

    def __ge__(self, other):
        """
        Check if this column is greater than or equal to another Column or a scalar.

        Args:
            other (Column, int, float): The column or scalar to compare with.

        Returns:
            Data: A new Data object containing rows where the comparison is True.
        """
        if isinstance(other, Column):
            result = self.data.table[self.columnName] >= other.data.table[other.columnName]
        elif isinstance(other, (int, float)):
            result = self.data.table[self.columnName] >= other
        else:
            raise TypeError("Unsupported operand type for >=")
        
        mask = np.array(result, dtype=bool)
        filtered_data = self.data.table[mask]
        return Data.from_table(filtered_data, primaryKey=self.data.primaryKey)

    def __eq__(self, other):
        """
        Check if this column is equal to another Column or a scalar.

        Args:
            other (Column, int, float): The column or scalar to compare with.

        Returns:
            Data: A new Data object containing rows where the comparison is True.
        """
        if isinstance(other, Column):
            result = self.data.table[self.columnName] == other.data.table[other.columnName]
        elif isinstance(other, (int, float)):
            result = self.data.table[self.columnName] == other
        else:
            raise TypeError("Unsupported operand type for ==")
        
        mask = np.array(result, dtype=bool)
        filtered_data = self.data.table[mask]
        return Data.from_table(filtered_data, primaryKey=self.data.primaryKey)

    def __ne__(self, other):
        """
        Check if this column is not equal to another Column or a scalar.

        Args:
            other (Column, int, float): The column or scalar to compare with.

        Returns:
            Data: A new Data object containing rows where the comparison is True.
        """
        if isinstance(other, Column):
            result = self.data.table[self.columnName] != other.data.table[other.columnName]
        elif isinstance(other, (int, float)):
            result = self.data.table[self.columnName] != other
        else:
            raise TypeError("Unsupported operand type for !=")
        
        mask = np.array(result, dtype=bool)
        filtered_data = self.data.table[mask]
        return Data.from_table(filtered_data, primaryKey=self.data.primaryKey)

    def __str__(self):
        """
        Return a string representation of the Column object.

        Returns:
            str: A string representation of the Column object.
        """
        return f"<Column> \n Name: {self.columnName} \n Result: {self.result}"


