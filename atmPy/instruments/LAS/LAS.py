# -*- coding: utf-8 -*-
"""
Created on Mon Nov 10 11:43:10 2014

@author: htelg
"""

import numpy as np
import pandas as pd
import datetime
from StringIO import StringIO as io
import pylab as plt
from scipy.interpolate import UnivariateSpline
import warnings
from matplotlib.colors import LogNorm
import hagmods as hm

def readFromFakeXLS(fname):
    """reads and shapes a XLS file produced by the LAS instrument"""
    fr = pd.read_csv(fname, sep = '\t')
    newcolname = [fr.columns[e] + ' ' +str(fr.values[0][e]) for e,i in enumerate(fr.columns)]
    fr.columns = newcolname
    fr = fr.drop(fr.index[0])
    bla = pd.Series(fr['Date -'].values +' '+ fr['Time -'].values)
    fr.index = bla.map(lambda x: datetime.datetime.strptime(x, '%m/%d/%Y %I:%M:%S.%f %p'))
    fr = fr.drop(['Date -','Time -'], axis = 1)
    return fr
    
def removeHousekeeping(frame):
    """Limits the frame to the collumns which have the number concentrations in them"""
    frame = frame.copy()
    k = frame.keys()
    k = k[:int(np.argwhere(k == 'Flow sccm'))+1]
    frame = frame.drop(k, axis = 1)
    return frame
    
def getBinCenters(frame, binedges = False, log = False):
    """LAS gives the bin edges, this calculates the bin centers.
    if log is True, the center will be with respect to the log10 ... log(d_{n+1})-log(d_{n})
    if binedges is True, frame is not really a frame but the binedges (array with dtype=float)
    Make sure you are running "removeHousekeeping" first"""
    frame = frame.copy()
    
    if binedges:
        if log:
            binCenters = 10**((np.log10(frame[:-1]) + np.log10(frame[1:]))/2.)
        else:
            
            binCenters = (frame[:-1] + frame[1:])/2.
    else:
        binCenters = np.zeros(frame.keys().shape)
        for e,i in enumerate(frame.keys()):
            bin_s,bin_e = i.split(' ')
            bin_s = float(bin_s)
            bin_e = float(bin_e)
            normTo = bin_e - bin_s
            frame[i] = frame[i].divide(normTo)
            if log:
                binCenters[e] = 10**((np.log10(bin_e) + np.log10(bin_s))/2.)
            else:
                binCenters[e] = (bin_e + bin_s)/2.
    return binCenters
    
def frameToXYZ(frame,binCenters, timeDelta = False):
    """This creates a three same shaped arrays, so it can be plotted using pcolor, contour ...
    Inputs:
        \t frame - has to be run through "removeHousekeeping"
        \t binCenters - can be obtained using "getBinCenters" 
        \t timeDelta - time offset in hours"""
#    binCenters = getBinCenters(frame)
    frame = frame.copy()
    histArray = frame.values.astype(np.float)
    histArray[np.isnan(histArray)] = 0   
    BINS_center = np.meshgrid(np.zeros(frame.index.values.shape[0]),binCenters)[1].transpose()
    timeMesh = np.zeros(frame.shape, dtype = "datetime64[ms]").transpose()
    for e,i in enumerate(timeMesh):
        timeMesh[e] = frame.index.values
        if timeDelta:
            timeMesh[e] += timeDelta
    return timeMesh.transpose().astype(datetime.datetime),BINS_center,histArray
    
def getTimeIntervalFromFrame(frame,start,end):
    """cutes out a particular time interval from frame.
    e.g.: getTimeIntervalFromFrame(frame,'2014-10-31 18:10:00','2014-10-31 18:10:00')"""
    frame = frame.copy()
    if start:
        frame = frame.truncate(before = start)

    if end:
        frame = frame.truncate(after = end)
    
    return frame
    
def frame2singleDistribution(frame):
    frame = frame.copy()
    singleHist = np.zeros(frame.shape[1])
    for i in xrange(frame.shape[1]):
#                 print i
        singleHist[i] = np.nansum(frame.values[:,i])
    singleHist /= frame.shape[0]
    return singleHist
    
def _string2Dataframe(data):
    sb = io(data)
    dataFrame = pd.read_csv(sb, sep = ' ', names = ('d','amp')).sort('d')
    return dataFrame
    
def read_Calibration_fromString(data):
    '''unit of diameter must be nm
    e.g.:
data = """140 88
150 102
173 175
200 295
233 480
270 740
315 880
365 1130
420 1350
490 1930
570 3050
660 4200
770 5100
890 6300
1040 8000
1200 8300
1400 10000
1600 11500
1880 16000
2180 21000
2500 28000
3000 37000"""
    '''
    
    dataFrame = _string2Dataframe(data)
    calibrationInstance = calibration(dataFrame)
    return calibrationInstance
    
def save_Calibration(calibrationInstance, fname):
    """should be saved hier cd ~/data/POPS_calibrations/"""
    calibrationInstance.data.to_csv(fname, index = False)
    return

def plot_distMap_LAS(fr_d,binEdgensLAS_d):
    binCenters = getBinCenters(binEdgensLAS_d , binedges= True, log = True)
    TIME_LAS,D_LAS,DNDP_LAS = frameToXYZ(fr_d, binCenters)
    f,a = plt.subplots()
    pcIm = a.pcolormesh(TIME_LAS,D_LAS,
                 DNDP_LAS,
                 norm = LogNorm(),#vmin = 3,vmax = distZoom.data.values.max()),#vmin = 1e-5),
    #              cmap=plt.cm.RdYlBu_r,
    #              cmap = plt.cm.terrain_r,
                  cmap = hm.get_colorMap_intensity(),#plt.cm.hot_r, #PuBuGn,
    #            shading='gouraud',
                 )
    a.semilogy()
    a.set_ylim((150,2500))
    a.set_ylabel('Diameter (nm)')
    a.set_xlabel('Time')
    a.set_title('LAS')
    cb = f.colorbar(pcIm)
    cb.set_label("Particle number (cm$^{-3}\,$s$^{-1}$)")
    f.autofmt_xdate()
#    a.yaxis.set_minor_formatter(FormatStrFormatter("%i"))
#    a.yaxis.set_major_formatter(FormatStrFormatter("%i"))

    
class calibration:
    def __init__(self,dataTabel):
        self.data = dataTabel
        self.calibrationFunction = self.get_calibrationFunctionSpline()
        
        
    def save_csv(self,fname):
        save_Calibration(self,fname)
        return
        
    def get_calibrationFunctionSpline(self, fitOrder = 1):# = 1, noOfPts = 500, plot = False):
        """
        Performes a spline fit/smoothening (scipy.interpolate.UnivariateSpline) of d over amp (yes this way not the other way around).
    
        Returns (generates): creates a function self.spline which can later be used to calculate d from amp 
    
        Optional Parameters:
        \t s: int - oder of the spline function
        \t noOfPts: int - length of generated graph
        \t plot: boolean - if result is supposed to be plotted
        """       
        # The following two step method is necessary to get a smooth curve. 
        #When I only do the second step on the cal_curve I get some wired whiggles
        ##### First Step
        if (self.data.amp.values[1:]-self.data.amp.values[:-1]).min() < 0:
            warnings.warn('The data represent a non injective function! This will not work. plot the calibration to see what I meen')  
        
        fitOrder = 1
        sf = UnivariateSpline(self.data.d.values, self.data.amp.values, s=fitOrder)
        d = np.logspace(np.log10(self.data.d.values.min()), np.log10(self.data.d.values.max()), 500)
        amp = sf(d)
    
        ##### second step
        cal_function = UnivariateSpline(amp, d, s=fitOrder)
        return cal_function
        
    def plot_calibration(self):
        """Plots the calibration function and data
        Arguments
        ------------
            cal: calibration instance
        
        Returns
        ------------
            figure
            axes
            calibration data graph
            calibration function graph
        """
        cal_function = self.calibrationFunction
        amp = np.logspace(np.log10(self.data.amp.min()), np.log10(self.data.amp.max()), 500)
        d = cal_function(amp)
    
        f,a = plt.subplots()
        
        cal_data, = a.plot(self.data.d,  self.data.amp, 'o',label = 'data',)
        cal_func, = a.plot(d,amp, label = 'function')
        
        a.loglog()
    
        a.set_xlim(0.9*self.data.d.min(), 1.1*self.data.d.max())
        a.set_xlabel('Diameter (nm)')#($\mu$m)')
    
        a.set_ylim(0.9*self.data.amp.min(), 1.1*self.data.amp.max()) 
        a.set_ylabel('Amplitude (digitizer bins)')
    
        a.set_title('Calibration curve')
        a.legend(loc = 2)
        return f,a,cal_data, cal_func