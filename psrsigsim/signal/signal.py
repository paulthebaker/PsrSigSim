
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import numpy as np
from scipy import stats

from ..utils.utils import make_quant

__all__ = ["Signal", "BaseSignal"]

class BaseSignal(object):
    """base class for signals, subclass from this

    Required Args:
        fcent [float]: central radio frequency

        bandwidth [float]: radio bandwidth of signal

    Optional Args:
        sample_rate [float]: sample rate of data, default: ``None``
            If no ``sample_rate`` is given the observation will default to
            the Nyquist frequency. Sub-Nyquist sampling is allowed, but a
            warning will be generated.

        dtype [type]: data type of array, default: ``np.float32``
            supported types are: ``np.float32`` and ``np.int8``
    """

    _sigtype = "Signal"
    _Nchan = None
    
    _draw_max = None
    _draw_norm = 1

    def __init__(self,
                 fcent, bandwidth,
                 sample_rate=None,
                 dtype=np.float32):

        self._fcent = fcent
        self._bw = bandwidth
        self._samprate = sample_rate
        if dype is np.float32 or np.int8:
            self._dtype = dtype
        else:
            msg = "data type {} not supported".format(dtype)
            raise ValueError(msg)

    def __repr__(self):
        return self.sigtype+"({0}, bw={1})".format(self.fcent, self.bw)

    def __add__(self, b):
        """overload ``+`` to concatinate signals"""
        raise NotImplementedError()

    def _set_draw_norm(self):
        """this only works for amplitude signals, intensity signals
        (like FilterBank) need to redefine this explicitly"""
        if self.dtype is np.float32:
            self._draw_max = 200
            self._draw_norm = 1
        if self.dtype is np.int8:
            gauss_limit = stats.norm.ppf(0.999)
            self._draw_max = np.iinfo(np.int8).max
            self._draw_norm = self._draw_max/gauss_limit

    def init_data(self, Nsamp):
        """initialize a data array to store the signal
        Required Args:
            Nsamp (int): number of data samples
        """
        self._data = np.empty((self.Nchan, Nsamp), dtype=self.dtype)

    def to_RF(self):
        """convert signal to RFSignal
        must be implemented in subclass!"""
        raise NotImplementedError()

    def to_Baseband(self):
        """convert signal to BasebandSignal
        must be implemented in subclass!"""
        raise NotImplementedError()

    def to_FilterBank(self, subbw):
        """convert signal to FilterBankSignal
        must be implemented in subclass!"""
        raise NotImplementedError()

    @property
    def data(self):
        return self._data

    @property
    def sigtype(self):
        return self._sigtype

    @property
    def Nchan(self):
        return self._Nchan

    @property
    def fcent(self):
        return self._fcent

    @property
    def bw(self):
        return self._bw

    @property
    def tobs(self):
        if hasattr(self, '_tobs'):
            return self._tobs
        else:
            return None

    @property
    def samprate(self):
        return self._samprate

    @property
    def dtype(self):
        return self._dtype

def Signal():
    """helper function to instantiate signals
    """
    pass
