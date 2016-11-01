import itertools
import reprlib
import numpy as np
import abc
from .lazy import *

class TimeSeriesInterface(abc.ABC):
    """
    This is the interface for a Timeseries. 
    """

    @abc.abstractmethod
    def __getitem__(self, i):
    	"""
    	returns the ith item of the time series.
    	"""

    @abc.abstractmethod
    def __contains__(self, value):
    	"""
    	returns True if the value is contained in the time series, False otherwise.
    	"""

    @abc.abstractmethod
    def __iter__(self):
    	"""
    	time series must be iterable over values.
    	"""

    @abc.abstractmethod
    def __repr__(self):
        """
        returns a string representation of the object
        """

    @abc.abstractmethod
    def itertimes(self):
    	"""
    	returns an iterator over the times of the timeseries
    	"""

    def iteritems(self):
        """
        Returns an Iterator over values, time pair
        """
        return iter(self.timeseries)

class SizedContainerTimeSeriesInterface(TimeSeriesInterface):
    """
    This is the interface for a Timeseries which can hold values and times in storage. 
    """

    def __iter__(self):
        """
        Returns an Iterator over values
        """
        return iter(self._values)

    def itertimes(self):
        """
        Returns an Iterator over times
        """
        return iter(self._times)


    def __getitem__(self, i):
        """ 
        Returns the ith value of the TimeSeries object
        
        Parameter
        ---------

        i: int

        Notes
        -----

        - If the user asks for the index of an item which is not contained in that list, an IndexError will be raised.
        This is due to the fact that the underlying data structure is a Python list.
        """

        return self._values[i]

    def __setitem__(self, i, value):
        """ 
        Sets the value of the ith item TimeSeries object to the value `value`

        Notes
        -----

        - !!!! The setitem method does not change the time associated with the ith item !!!!

        - If the user asks for the index of an item which is not contained in that list, an IndexError will be raised.
        This is due to the fact that the underlying data structure is a Python list.
        """
        self._values[i] = value
        self.timeseries[i] = (self._times[i], value)

    def __contains__(self, value):
        """
        Returns a boolean value indicating if the instance contains a certain value
        """
        return (value in self._values)

    def __len__(self):
        """ 
        Returns the length of the TimeSeries object, which corresponds to the length of the timeseries attribute
        """
        return len(self.timeseries)

    def __repr__(self):
        '''
        This function returns the formal string representation of a TimeSeries object. We define the formal string
        representations by:

        Type(len=XX, timeseries=XX) 

        Notes
        -----

        - If the TimeSeries contains more than 5 elements, we only print the first 5 elements.
        '''
        class_name = type(self).__name__
        length = len(self.timeseries)
        if length <= 5:
            return '{}(len = {}; timeseries = {})'.format(class_name, length, self.timeseries)
        else:
            components = reprlib.repr(list(itertools.islice(self.timeseries,0,5)))
            components = components[:components.find(']')]
            return '{}(timeseries = {}, ...]; len = {})'.format(class_name, length, components)

    def __str__(self):
        '''
        This function returns the informal string representation of a TimeSeries object which only correponds to the
        string representation of the `timeseries` attribute.

        Notes
        -----

        - If the TimeSeries contains more than 5 elements, we only print the first 5 elements.
        '''

        length = len(self.timeseries)
        if length <= 5:
            return str(self.timeseries)
        else:
            components = reprlib.repr(list(itertools.islice(self.timeseries,0,5)))
            components = components[:components.find(']')]
            return '{}, ...]'.format(components)

    def values(self):
        """
        Returns a numpy array of the values of a timeseries
        """
        return np.array(self._values)

    def itervalues(self):
        """
        Returns an iterator of the numpy array of the values of a timeseries
        """
        return iter(self.values())

    def times(self):
        """
        Returns a numpy array of the times of a timeseries
        """
        return np.array(self._times)

    def items(self):
        """
        Returns an iterator of the numpy array of the times of a timeseries
        """
        return self.timeseries

    def __abs__(self):
        """
        Returns the 2-norm of the timeseries values
        """
        return math.sqrt(sum(x * x for x in self.values()))

    def __bool__(self):
        """
        Returns a boolean value indicating if the 2-norm of the timeseries values is zero
        """
        return bool(abs(self))

    def __neg__(self):
        """
        Returns a timeseries instance with each value being the negative of the original
        """
        return TimeSeries([-x for x in self._values], self._times)

    def __pos__(self):
        """
        Returns a timeseries instance with each value preserving the original sign
        """
        return TimeSeries(self._values, self._times)
       
    @property
    @lazy
    def lazy(self):
        return self

    def mean(self):
        if(len(self._values) == 0):
            raise ValueError("List must have at least 1 value.")
        return np.mean(self._values)
        
    def std(self):
        if(len(self._values) == 0):
            raise ValueError("List must have at least 1 value.")
        return np.std(self._values)

    @staticmethod
    def _check_match_helper(self , rhs):
        """
        Helper function to check if two timeseries have matching times
        
        Parameter
        ----------------
        rhs: a TimeSeries instance with the exact same time indeces; otherwise a ValueError will be raised
        """
        if (not self.hastime) or (not rhs.hastime):
            raise NotImplemented
        if not self._times==rhs._times:
            raise ValueError(str(self)+' and '+str(rhs)+' must have the same time points')

    def __add__(self, rhs):
        """
        Element-wise addition of two timeseries instances
        
        Parameter
        ----------------
        rhs: a TimeSeries instance with the exact same time indeces; if rhs is not a TimeSeries, a TypeError will be raised; if the rhs does not have matching time indeces, a ValueError will be raised
        """
        if isinstance(rhs, TimeSeries):
            TimeSeries._check_match_helper(self, rhs)
            pairs = zip(self._values, rhs._values)
            return TimeSeries([a + b for a, b in pairs], [x for x in self._times])
        else:
            raise TypeError(str(rhs)+' must be a TimeSeries instance')

    def __sub__(self, rhs):
        """
        Element-wise subtraction of two timeseries instances
        
        Parameter
        ----------------
        rhs: a TimeSeries instance with the exact same time indeces; if rhs is not a TimeSeries, a TypeError will be raised; if the rhs does not have matching time indeces, a ValueError will be raised
        """
        if isinstance(rhs, TimeSeries):
            TimeSeries._check_match_helper(self, rhs)
            pairs = zip(self._values, rhs._values)
            return TimeSeries([a - b for a, b in pairs], [x for x in self._times])
        else:
            raise TypeError(str(rhs)+' must be a TimeSeries instance')

    def __mul__(self, rhs):
        """
        Element-wise multiplication of two timeseries instances
        
        Parameter
        ----------------
        rhs: a TimeSeries instance with the exact same time indeces; if rhs is not a TimeSeries, a TypeError will be raised; if the rhs does not have matching time indeces, a ValueError will be raised
        """
        if isinstance(rhs, TimeSeries):
            TimeSeries._check_match_helper(self, rhs)
            pairs = zip(self._values, rhs._values)
            return TimeSeries([a * b for a, b in pairs], [x for x in self._times])
        else:
            raise TypeError(str(rhs)+' must be a TimeSeries instance')

    def __eq__(self, rhs):
        """
        Check if two timeseries instances are the same
        
        Parameter
        ----------------
        rhs: a TimeSeries instance with the exact same time indeces; if rhs is not a TimeSeries, a TypeError will be raised; if the rhs does not have matching time indeces, a ValueError will be raised
        """
        if isinstance(rhs, TimeSeries):
            TimeSeries._check_match_helper(self, rhs)
            pairs = zip(self._values, rhs._values)
            return all([a==b for a, b in pairs])
        else:
            raise TypeError(str(rhs)+' must be a TimeSeries instance')

class StreamTimeSeriesInterface(TimeSeriesInterface):
   @abc.abstractmethod
    def produce(self, chunk=1):
        """
        produces a set of 'chunk' ew elements into the timeseries whenever it is called
        """
    def online_mean(self):
        """
        Returns a new Streaming Time Series with tuples (time/index, value, online_mean)
        """
    def online_dev(self):
