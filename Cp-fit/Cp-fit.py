import os
import re
import sys

import numpy as np
import matplotlib.pyplot as plt

import scipy.constants as cons
from scipy.optimize import curve_fit
from scipy import integrate

def main():

    def parse_data(filepath): 
        raw = np.genfromtxt(filepath)
        tdata, hcdata = [], []
        for t, hc in raw:
            tdata.append(t)
            hcdata.append(hc)
    
        return (tdata, hcdata)
        
    def debyeIntegral(t, args):
        T, m = args
        return 9*R*((T/m)**3)*(t**4)*np.exp(t)/(np.exp(t)-1)**2
    
    def func(T, m):
        return (integrate.quad(debyeIntegral, 0, m/T, [T, m])[0])
 
    def data_filter(filepath):
        tdata, hcdata = parse_data(filepath)
        fit_t, fit_hc = [], []
        for i in range(len(tdata)):
            if tdata[i] >= 20 and tdata[i] <= 200:
                fit_t.append(tdata[i])
                fit_hc.append(hcdata[i])

        return (fit_t, fit_hc)

    filepath = "Cv"

    fit1_upper_temperature = 3.1 # in Kelvin ... 0.0 = ignore
    fit2_upper_temperature = 0.0 # in Kelvin ... 0.0 = ignore
     
    R = cons.R

    tdata, hcdata = data_filter(filepath)
 
    vfunc = np.vectorize(func, excluded=set([1]))
    
    popt, pcov = curve_fit(vfunc, tdata , hcdata, p0=(205,), bounds=(0, np.inf))

    print("popt=", popt)
    print("pcov=", pcov)
       
    # fres = sum(residuals**2)
    
    # if fit2_upper_temperature == 0.0:
    #     print("Fit with a Debye and 2 Einstein Modes")
    # else:
    #     print("Fit from 0 -", fit2_upper_temperature, "K with a Debye and 2 Einstein Modes")
        
    
    # print("N Debye:                ", (atomsPerUnit-(d+e)/(3*R)), "±", (error[2]/+error[3])/(3*R))
    # print("Debye Temperature:      ", m, "±", error[0] , "K")
    
    plt.clf()
    plt.plot(tdata, hcdata, 'o', markersize=7)
    for p0_content in range(150, 450, 5):
        popt, pcov = curve_fit(vfunc, tdata , hcdata, p0=(p0_content,), bounds=(0, np.inf))
        plt.plot(tdata, [func(T, popt) for T in tdata])
        print("plot when popt = {}, pcov = {}".format(popt, pcov))
    plt.show()

if __name__ == "__main__":
    main()
