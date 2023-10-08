# shastra (**Sh**arma's **astr**o **a**rchive)

A package for the analysis tools for astro research that arose from the code used for the publication [HI-Rich but low star formation galaxies in MaNGA: physical properties and comparison to control samples](https://academic.oup.com/mnras/article-abstract/526/1/1573/7264872?redirectedFrom=fulltext). You need to install it to run the example notebook *HIRichLowSFRGalaxies_example.ipynb*. The goal is to make it faster to do statistical analysis and data visualization for astro research projects, specifically the one that involves multiple control samples.

Report any bugs, suggestions, or thoughts to Anubhav Sharma at [anubhavprasadsharma@gmail.com](mailto:anubhavprasadsharma@gmail.com).

## Table of Contents
- [Installation](#installation)
- [Documentation](#documentation)
  - [Data](#data)
  - [Column](#column)
  - [Sample](#sample)
  - [Research](#research)
- [Acknowledgement](#acknowledgement)

## Installation

To install the `shastra` package, you can use `pip`, Python's package manager. In your terminal, you can use the following command:

```bash
python3 -m pip install git+https://github.com/sharmanubhav/shastra.git
```

If you are using in Jupyter Notebook, use the following command. Using Python 3 (ipykernel) or a virtual environment is recommended if there are problems with installation.

```notebook
import sys
!{sys.executable} -m pip install git+https://github.com/sharmanubhav/shastra.git
```

## Documentation

### Data

The `Data` class is used for managing scientific data from FITS files.

#### Attributes

- `table` (astropy.table.Table): An Astropy Table containing the data.
- `primaryKey` (str): The primary key column name.
- `primaryKeyList` (list): A list of primary key values.

#### Methods

##### `__init__(self, dataPath: str, primaryKey: str = "")`

Constructor for the Data class.

- `dataPath` (str): The path to the FITS data file.
- `primaryKey` (str, optional): The primary key column name.

Raises:
- `FileNotFoundError`: If the specified file does not exist.

##### `from_table(cls, table: Table, primaryKey: str = "")`

Create a Data object from an existing Astropy Table and primary key.

- `table` (Table): The Astropy Table containing the data.
- `primaryKey` (str, optional): The primary key column name.

Returns:
- `Data`: A new instance of the Data class.

##### `__str__(self)`

Return a string representation of the Data object.

Returns:
- `str`: A string representation of the Data object.

### Column

The `Column` class represents a column within a Data object and supports various operations.

#### Attributes

- `data` (Data): The Data object that this column belongs to.
- `columnName` (str): The name of the column in the Data object.
- `result`: The result column.

#### Methods

##### `__init__(self, data: Data, columnName: str, result=None)`

Constructor for the Column class.

- `data` (Data): The Data object that this column belongs to.
- `columnName` (str): The name of the column in the Data object.

Returns:
- `Column`: A new instance of the Column class.

##### `newColumnName(self, operation: str, otherColumn=None)`

Get an updated column name for the current operation.

- `operation` (str): The operation symbol (e.g., '+', '-', '*', '/', '**').
- `otherColumn` (str, optional): The name of another column for binary operations.

Returns:
- `str`: The updated column name.

##### `updatedData(self, newColumnName: str, result)`

Update the Column's data attribute with a new column and set the new column name.

- `newColumnName` (str): The name for the new column.
- `result` (astropy.table.Column): The result column to update the data attribute.

Binary operations (+, -, *, /, **):

##### `__add__(self, other)`

Add another Column or a scalar to this column.

- `other` (Column, int, float): The column or scalar to add.

Returns:
- `Column`: A new Column containing the result of the addition.

##### `__sub__(self, other)`

Subtract another Column or a scalar from this column.

- `other` (Column, int, float): The column or scalar to subtract.

Returns:
- `Column`: A new Column containing the result of the subtraction.

##### `__mul__(self, other)`

Multiply this column by another Column or a scalar.

- `other` (Column, int, float): The column or scalar to multiply by.

Returns:
- `Column`: A new Column containing the result of the multiplication.

##### `__truediv__(self, other)`

Divide this column by another Column or a scalar.

- `other` (Column, int, float): The column or scalar to divide by.

Returns:
- `Column`: A new Column containing the result of the division.

##### `__pow__(self, other)`

Raise this column to the power of another Column or a scalar.

- `other` (Column, int, float): The column or scalar to raise to the power of.

Returns:
- `Column`: A new Column containing the result of the exponentiation.

Inequality operations (<, <=, >, >=, ==, !=):

##### `__lt__(self, other)`

Check if this column is less than another Column or a scalar.

- `other` (Column, int, float): The column or scalar to compare with.

Returns:
- `Data`: A new Data object containing rows where the comparison is True.

##### `__le__(self, other)`

Check if this column is less than or equal to another Column or a scalar.

- `other` (Column, int, float): The column or scalar to compare with.

Returns:
- `Data`: A new Data object containing rows where the comparison is True.

##### `__gt__(self, other)`

Check if this column is greater than another Column or a scalar.

- `other` (Column, int, float): The column or scalar to compare with.

Returns:
- `Data`: A new Data object containing rows where the comparison is True.

##### `__ge__(self, other)`

Check if this column is greater than or equal to another Column or a scalar.

- `other` (Column, int, float): The column or scalar to compare with.

Returns:
- `Data`: A new Data object containing rows where the comparison is True.

##### `__eq__(self, other)`

Check if this column is equal to another Column or a scalar.

- `other` (Column, int, float): The column or scalar to compare with.

Returns:
- `Data`: A new Data object containing rows where the comparison is True.

##### `__ne__(self, other)`

Check if this column is not equal to another Column or a scalar.

- `other` (Column, int, float): The column or scalar to compare with.

Returns:
- `Data`: A new Data object containing rows where the comparison is True.

##### `__str__(self)`

Return a string representation of the Column object.

Returns:
- `str`: A string representation of the Column object.

### Sample

The `Sample` class represents a sample of data.

#### Attributes

- `name` (str): The name of the sample.
- `ids` (List[str]): A list of identifiers associated with the sample, typically the primaryKey of Data.

#### Methods

None.

### Research

The `Research` class is used for conducting research and statistical analysis on data.

#### Attributes

- `data` (Data): The data for the research.
- `mainSample` (Sample): The main sample associated with this research.
- `controls` (List[Sample]): A list of control samples (default is an empty list).
- `parameters` (Dict[str, Column]): A dictionary of parameters and their associated data columns that you are interested in this research.

#### Methods

##### `getValue(self, sample: Sample, parameterName: str)`

Given a parameter name and a sample, it gets the parameter values associated with the sample.

- `sample` (Sample): The sample for which to retrieve the parameter values.
- `parameterName` (str): The name of the parameter.

Returns:
- `list`: A list of parameter values for the given sample.

##### `printValue(self, sample: Sample, parameterName: str)`

Print the values of a parameter for a given sample.

- `sample` (Sample): The sample for which to print the parameter values.
- `parameterName` (str): The name of the parameter.

##### `interval(self, arr, bootstrapN=10000)`

Compute the interval for a given array using bootstrap resampling.

- `arr` (list or np.ndarray): The input array for which to compute the interval.
- `bootstrapN` (int): The number of bootstrap samples to generate (default is 10,000).

Returns:
- `list`: A list containing the standard deviations of the mean, median, and standard deviation of the resampled data.

##### `printStatistics(self, sample: Sample, parameterName: str)`

Print statistics (mean, median, and standard deviation) for a given sample and parameter.

- `sample` (Sample): The sample for which to print statistics.
- `parameterName` (str): The name of the parameter.

##### `printCorrelation(self, sample1: Sample, sample2: Sample, parameterName: str)`

Print correlation statistics (KS Test and Anderson-Darling Test) between two samples for a given parameter.

- `sample1` (Sample): The first sample for comparison.
- `sample2` (Sample): The second sample for comparison.
- `parameterName` (str): The name of the parameter.

##### `printStatisticsAll(self, parameterName: str)`

Print statistics (mean, median, and standard deviation) for all samples, including controls, for a given parameter.

- `parameterName` (str): The name of the parameter.

##### `printCorrelationAll(self, parameterName: str)`

Print correlation statistics (KS Test and Anderson-Darling Test) between the main sample and all control samples for a given parameter.

- `parameterName` (str): The name of the parameter.

##### `plotSingleHistogram(self, sample: Sample, parameterName: str, toSave=False, filename="", xLabel="", yLabel="Count", **kwargs)`

Plot a histogram for a single sample and a single parameter.

- `sample` (Sample): The sample for which to plot the histogram.
- `parameterName` (str): The name of the parameter.
- `toSave` (bool): Whether to save the plot as an image (default is False).
- `filename` (str): The filename to use if saving the plot (default is ""). If not specified, the parameterName is used.
- `xLabel` (str): The label for the x-axis (default is ""). If not specified, parameterName is used.
- `yLabel` (str): The label for the y-axis (default is "Count").
- `**kwargs`: Additional keyword arguments for customizing the histogram.

##### `plotStackedHistogram(self, parameterName, toSave=False, filename="", xLabel="", yLabel="Count", mainSampleBins=15, mainSampleRange=None, **kwargs)`

Plot a stacked histogram for the main sample and control samples for a given parameter.

- `parameterName` (str): The name of the parameter.
- `toSave` (bool): Whether to save the plot as an image (default is False).
- `filename` (str): The filename to use if saving the plot (default is ""). If not specified, the parameterName is used.
- `xLabel` (str): The label for the x-axis (default is ""). If not specified, parameterName is used.
- `yLabel` (str): The label for the y-axis (default is "Count").
- `mainSampleBins` (int): The number of bins for the main sample's histogram (default is 15).
- `mainSampleRange` (tuple): The range for the main sample's histogram (default is None).
- `**kwargs`: Additional keyword arguments for customizing the histograms.

##### `plotAllStackedHistograms(self, toSave=False, **kwargs)`

Plot stacked histograms for all parameters.

- `toSave` (bool): Whether to save the plots as images (default is False).
- `**kwargs`: Additional keyword arguments for customizing the histograms.

##### `__str__(self)`

Return a string representation of the Research object.

Returns:
- `str`: A string representation of the Research object.

## Acknowledgement
Shastra acknowledges the support and guidance of Prof. Karen L. Masters and Dr. David V. Stark during the research of publication [HI-rich but low star formation galaxies in MaNGA: physical properties and comparison to control samples](https://academic.oup.com/mnras/article-abstract/526/1/1573/7264872?redirectedFrom=fulltext) which resulted in this code. This package also utilized assistance of ChatGPT, a powerful language model created by OpenAI, which provided assistance for in-depth documentation and implementation of some trivial functions.

## Citation
```
@misc{shastra,
  author = {Anubhav Sharma},
  title = {SHarma's ASTRo Archive},
  year = {2023},
  howpublished = {\url{https://github.com/sharmanubhav/shastra}}
}
```
---