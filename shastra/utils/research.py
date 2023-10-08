import numpy as np
from astropy.stats import bootstrap
from astropy.utils import NumpyRNGContext
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib as mpl
from typing import List, Dict
from .data import Data, Column
from matplotlib.ticker import AutoMinorLocator

class Sample:
    def __init__(self, name: str = "Sample", ids: List[str] = []):
        """
        Initialize a Sample object.

        Args:
            name (str): The name of the sample (default is "Sample").
            ids (List[str]): A list of identifiers associated with the sample, typically the primaryKey of Daa.
        """
        self.name = name 
        self.ids = ids

    def __str__(self):
        """
        Return a string representation of the Sample object.
        """
        return f"<Sample> \n \tName: {self.name} \n \t IDs: {', '.join(self.ids)} \n"

class Research:
    def __init__(self, data: Data , mainSample: Sample, controls: List[Sample]=[], parameters: Dict[str, Column]={}):
        """
        Initialize a Research object.

        Args:
            data (Data): The data for the research.
            mainSample (Sample): The main sample associated with this research.
            controls (List[Sample]): A list of control samples (default is an empty list).
            parameters (Dict[str, Column]): A dictionary of parameters and their associated data columns that you are interested in this research.
        """
        self.data = data
        self.mainSample = mainSample
        self.controls = controls
        self.parameters = parameters

    def getValue(self, sample: Sample, parameterName: str):
        """
        Given a parameter name and a sample, it gets the parameter values associated with the sample.

        Args:
            sample (Sample): The sample for which to retrieve the parameter values.
            parameterName (str): The name of the parameter.

        Returns:
            list: A list of parameter values for the given sample.
        """
        indices = []
        primaryKeyList = self.data.primaryKeyList
        parameterColumn = self.data.table[self.parameters[parameterName].columnName]
        parameterList = list(np.array(parameterColumn))
        if sample.name == self.mainSample.name:
            sampleList = self.mainSample.ids
        else:
            for controls in self.controls:
                if sample.name == controls.name:
                    sampleList = controls.ids
        for index, primaryKey in enumerate(primaryKeyList):
            if primaryKey in sampleList:
                indices.append(index)
        value = [parameterList[x] for x in indices]
        return value

    def printValue(self, sample: Sample, parameterName: str):
        """
        Print the values of a parameter for a given sample.

        Args:
            sample (Sample): The sample for which to print the parameter values.
            parameterName (str): The name of the parameter.
        """
        print(parameterName + " for " + sample.name)
        print(self.getValue(sample, parameterName))

    def interval(self, arr, bootstrapN=10000):
        """
        Compute the interval for a given array using bootstrap resampling.

        Args:
            arr (list or np.ndarray): The input array for which to compute the interval.
            bootstrapN (int): The number of bootstrap samples to generate (default is 10,000).

        Returns:
            list: A list containing the standard deviations of the mean, median, and standard deviation of the resampled data.
        """
        arr = np.array(arr)
        test_statistic = lambda x: (np.nanmean(x), np.nanmedian(x), np.nanstd(x))
        with NumpyRNGContext(1):
            bootresult = bootstrap(arr, bootstrapN, bootfunc=test_statistic)
        return [np.nanstd(bootresult[:, 0]), np.nanstd(bootresult[:, 1]), np.nanstd(bootresult[:, 2])]

    def printStatistics(self, sample: Sample, parameterName: str):
        """
        Print statistics (mean, median, and standard deviation) for a given sample and parameter.

        Args:
            sample (Sample): The sample for which to print statistics.
            parameterName (str): The name of the parameter.
        """
        value = self.getValue(sample, parameterName)
        error = self.interval(value)
        print("-" * 80)
        print(sample.name + " statistics for " + parameterName)
        print("Mean: ", np.nanmean(value), "+-", error[0])
        print("Median: ", np.nanmedian(value), "+-", error[1])
        print("Standard Deviation: ", np.nanstd(value), "+-", error[2])
        print("-" * 80)

    def printCorrelation(self, sample1: Sample, sample2: Sample, parameterName: str):
        """
        Print correlation statistics (KS Test and Anderson-Darling Test) between two samples for a given parameter.

        Args:
            sample1 (Sample): The first sample for comparison.
            sample2 (Sample): The second sample for comparison.
            parameterName (str): The name of the parameter.
        """
        value1 = self.getValue(sample1, parameterName)
        value2 = self.getValue(sample2, parameterName)
        print("-" * 80)
        print("KS Test between " + sample1.name + " and " + sample2.name)
        print(stats.ks_2samp(value2, value1))
        print("-" * 50)
        print("AD Test between " + sample1.name + " and " + sample2.name)
        print(stats.anderson_ksamp(np.array([value2, value1])))
        print("-" * 80)

    def printStatisticsAll(self, parameterName: str):
        """
        Print statistics (mean, median, and standard deviation) for all samples, including controls, for a given parameter.

        Args:
            parameterName (str): The name of the parameter.
        """
        self.printStatistics(self.mainSample, parameterName)
        for controls in self.controls:
            self.printStatistics(controls, parameterName)
    
    def printCorrelationAll(self, parameterName: str):
        """
        Print correlation statistics (KS Test and Anderson-Darling Test) between the main sample and all control samples for a given parameter.

        Args:
            parameterName (str): The name of the parameter.
        """
        for controls in self.controls:
            self.printCorrelation(self.mainSample, controls, parameterName)

    def plotSingleHistogram(self, sample: Sample, parameterName: str, toSave=False, filename="", xLabel="", yLabel="Count", **kwargs):
        """
        Plot a histogram for a single sample and a single parameter.

        Args:
            sample (Sample): The sample for which to plot the histogram.
            parameterName (str): The name of the parameter.
            toSave (bool): Whether to save the plot as an image (default is False).
            filename (str): The filename to use if saving the plot (default is ""). If not specified, the parameterName is used.
            xLabel (str): The label for the x-axis (default is ""). If not specified, parameterName is used.
            yLabel (str): The label for the y-axis (default is "Count").
            **kwargs: Additional keyword arguments for customizing the histogram.
        """
        if xLabel == "": 
            xLabel = parameterName
        mpl.rcParams['font.size'] = 14
        fig, ax = plt.subplots()
        plt.xlabel(xLabel)
        plt.ylabel(yLabel)
        value = self.getValue(sample, parameterName)
        plt.hist(value, label=sample.name, **kwargs)
        plt.legend()
        ax.xaxis.set_minor_locator(AutoMinorLocator())
        ax.tick_params(which='minor', length=2, color='k')
        ax.yaxis.set_minor_locator(AutoMinorLocator())
        ax.tick_params(which='minor', length=2, color='k')
        if toSave:
            if filename == "":
                filename = parameterName.replace(" ", "_")
            plt.savefig(filename, bbox_inches='tight')
        plt.show()

    def plotStackedHistogram(self, parameterName, toSave=False, filename="", xLabel="", yLabel="Count", mainSampleBins=15, mainSampleRange=None, **kwargs):
        """
        Plot a stacked histogram for the main sample and control samples for a given parameter.

        Args:
            parameterName (str): The name of the parameter.
            toSave (bool): Whether to save the plot as an image (default is False).
            filename (str): The filename to use if saving the plot (default is ""). If not specified, the parameterName is used.
            xLabel (str): The label for the x-axis (default is ""). If not specified, parameterName is used.
            yLabel (str): The label for the y-axis (default is "Count").
            mainSampleBins (int): The number of bins for the main sample's histogram (default is 15).
            mainSampleRange (tuple): The range for the main sample's histogram (default is None).
            **kwargs: Additional keyword arguments for customizing the histograms.
        """
        if xLabel == "": 
            xLabel = parameterName
        mpl.rcParams['font.size'] = 14
        fig, ax = plt.subplots()
        plt.xlabel(xLabel)
        plt.ylabel(yLabel)
        value = self.getValue(self.mainSample, parameterName)
        plt.hist(value, label=self.mainSample.name, ec="black", histtype='step', range=mainSampleRange, fc=(0.5, 0.5, 0.5, 0.6), bins=mainSampleBins)
        for controls in self.controls:
            value = self.getValue(controls, parameterName)
            plt.hist(value, label=controls.name, histtype='stepfilled', **kwargs)
        plt.legend()
        ax.xaxis.set_minor_locator(AutoMinorLocator())
        ax.tick_params(which='minor', length=2, color='k')
        ax.yaxis.set_minor_locator(AutoMinorLocator())
        ax.tick_params(which='minor', length=2, color='k')
        if toSave:
            if filename == "":
                filename = parameterName.replace(" ", "_")
            plt.savefig(filename, bbox_inches='tight')
        plt.show()

    def plotAllStackedHistograms(self, toSave=False, **kwargs):
        """
        Plot stacked histograms for all parameters.

        Args:
            toSave (bool): Whether to save the plots as images (default is False).
            **kwargs: Additional keyword arguments for customizing the histograms.
        """
        for parameters in self.parameters:
            self.plotHistogram(parameters, toSave=toSave, **kwargs)

    def __str__(self):
        """
        Return a string representation of the Research object.
        """
        return f"<Research> \n \tData: {self.data}\n \t Main Sample: {self.mainSample}\n \t Controls: {', '.join(map(str, self.controls))}  \n ------------ \n"