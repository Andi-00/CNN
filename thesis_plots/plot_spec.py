## Code to generate the 10^4 parameters, strains and spectrograms

import sys
import os

from gwpy.timeseries import TimeSeries

import matplotlib.pyplot as plt
import numpy as np

from few.trajectory.inspiral import EMRIInspiral
from few.amplitude.romannet import RomanAmplitude
from few.amplitude.interp2dcubicspline import Interp2DAmplitude
from few.waveform import FastSchwarzschildEccentricFlux, SlowSchwarzschildEccentricFlux, GenerateEMRIWaveform
from few.utils.utility import (get_overlap,
                               get_mismatch,
                               get_fundamental_frequencies,
                               get_separatrix,
                               get_mu_at_t,
                               get_p_at_t,
                               get_kerr_geo_constants_of_motion,
                               xI_to_Y,
                               Y_to_xI)

from few.utils.ylm import GetYlms
from few.utils.modeselector import ModeSelector
from few.summation.interpolatedmodesum import CubicSplineInterpolant
from few.waveform import SchwarzschildEccentricWaveformBase
from few.summation.interpolatedmodesum import InterpolatedModeSum
from few.summation.directmodesum import DirectModeSum
from few.utils.constants import *
from few.summation.aakwave import AAKSummation
from few.waveform import Pn5AAKWaveform, AAKWaveformBase



use_gpu = False

# keyword arguments for inspiral generator (RunSchwarzEccFluxInspiral)
inspiral_kwargs={
        "DENSE_STEPPING": 0,  # we want a sparsely sampled trajectory
        "max_init_len": int(1e3),  # all of the trajectories will be well under len = 1000
    }

# keyword arguments for inspiral generator (RomanAmplitude)
amplitude_kwargs = {
    "max_init_len": int(1e3),  # all of the trajectories will be well under len = 1000
    "use_gpu": use_gpu  # GPU is available in this class
}

# keyword arguments for Ylm generator (GetYlms)
Ylm_kwargs = {
    "assume_positive_m": False  # if we assume positive m, it will generate negative m for all m>0
}

# keyword arguments for summation generator (InterpolatedModeSum)
sum_kwargs = {
    "use_gpu": use_gpu,  # GPU is availabel for this type of summation
    "pad_output": False,
}

# THE FOLLOWING THREAD COMMANDS DO NOT WORK ON THE M1 CHIP, BUT CAN BE USED WITH OLDER MODELS
# EVENTUALLY WE WILL PROBABLY REMOVE OMP WHICH NOW PARALLELIZES WITHIN ONE WAVEFORM AND LEAVE IT TO
# THE USER TO PARALLELIZE FOR MANY WAVEFORMS ON THEIR OWN.

# set omp threads one of two ways
# num_threads = 4

# this is the general way to set it for all computations
# from few.utils.utility import omp_set_num_threads
# omp_set_num_threads(num_threads)

few = FastSchwarzschildEccentricFlux(
    inspiral_kwargs=inspiral_kwargs,
    amplitude_kwargs=amplitude_kwargs,
    Ylm_kwargs=Ylm_kwargs,
    sum_kwargs=sum_kwargs,
    use_gpu=use_gpu,
    # num_threads=num_threads,  # 2nd way for specific classes
)



gen_wave = GenerateEMRIWaveform("Pn5AAKWaveform")

# parameters
T = 0.05 # years
dt = 5  # seconds

M = 1e4  # solar mass
mu = 1  # solar mass

dist = 1.0  # distance in Gpc

p0 = 12.0
e0 = 0.2
x0 = 0.99  # will be ignored in Schwarzschild waveform

qS = 1E-6  # polar sky angle
phiS = 0.0  # azimuthal viewing angle


# spin related variables
a = 0.6  # will be ignored in Schwarzschild waveform
qK = 1E-6  # polar spin angle
phiK = 0.0  # azimuthal viewing angle


# Phases in r, theta and phi
Phi_phi0 = 0
Phi_theta0 = 0
Phi_r0 = 0

# Generate the random parameters for the EMRIs
# The parameters include M, mu / d, a, e0 and p0

def gen_parameters(N):
    n = np.random.uniform(4, 7, N)
    M = 10 ** n
    dm = np.random.uniform(1, 1E2, N)
    a = np.random.uniform(0, 1, N)
    e0 = np.random.uniform(0.1, 0.7, N)
    p0 = np.random.uniform(10, 16, N)

    parameters = np.array([np.array([M[i], dm[i], a[i], e0[i], p0[i]]) for i in range(N)])

    return parameters

# Generate the strain h from the parameters par and returns it
def gen_strain(par):
    M = par[:, 0]
    mu = np.ones_like(M)
    d = par[:, 1]
    a = par[:, 2]
    e0 = par[:, 3]
    p0 = par[:, 4]

    h = [gen_wave(M[i], mu[i], a[i], p0[i], e0[i], x0, d[i], qS, phiS, qK, phiK, Phi_phi0, Phi_theta0, Phi_r0, T=T, dt=dt) for i in range(len(d))]

    return h

# Generate the spectrograms of the given strains
def gen_specs(hs):

    specs = []

    for h in hs:
        
        # Fill the strain array with zeros, so that all have the same length
        # independant of the signal duration
        hp = np.pad(h.real, (0, 315582 - len(h)))

        ts = TimeSeries(hp, dt = dt)

        data = ts.spectrogram(2E4) ** (1/2)


        specs.append(data)

    return specs

# Save the spectrogram files as csv data
def save_files(files, loc, n = 0):
    for i in range(len(files)):
        np.savetxt("./thesis_plots/plots/spec_{}.png".format(i), np.array(files[i]), delimiter = ",")




# Save the parameters in a csv file
p0 = np.genfromtxt("/hpcwork/cg457676/data/parameters/parameters_0.csv", delimiter = ",")[49]
p1 = np.genfromtxt("/hpcwork/cg457676/data/parameters/parameters_0.csv", delimiter = ",")[49]
p2 = np.genfromtxt("/hpcwork/cg457676/data/parameters/parameters_0.csv", delimiter = ",")[49]
p3 = np.genfromtxt("/hpcwork/cg457676/data/parameters/parameters_0.csv", delimiter = ",")[49]
p4 = np.genfromtxt("/hpcwork/cg457676/data/parameters/parameters_0.csv", delimiter = ",")[49]
p5 = np.genfromtxt("/hpcwork/cg457676/data/parameters/parameters_0.csv", delimiter = ",")[49]

par = np.array([p0, p1, p2, p3, p4, p5])

nums = [[0, 1], [0, 2], [0, 4], [1, 4], [2, 4]]
m = [31.36, 2.3, -12, -0.10, -3.25]
c = [-0.043, 0.012, -0.058, 0.044, 0.097]
z = [0.3, 0.2, 0.2, 20, 0.4]

for i in range(len(m)):
    x, y = nums[i][0], nums[i][1]

    dx = z[i] / 2
    dy = m[i] * dx + c[i]

    if x != 0: par[i + 1][x] += dx
    else : par[i + 1][x] *= 10 ** (dx)

    par[i + 1][y] += dy



h = gen_strain(par)

specs = gen_specs(h)

np.savetxt("./thesis_plots/plots/chapter_5/spec_val.csv", np.array(specs[-1]), delimiter = ",")

i = 0

for spec in specs:

    plot = spec.imshow(norm='log', vmin = np.max(specs) * 1E-6)
    ax = plot.gca()
    ax.set_yscale('log')
    ax.set_ylim(1E-4, 1E-1)
    ax.colorbar(
    label=r'Gravitational-wave amplitude [strain/$\sqrt{\mathrm{Hz}}$]')
    plot.savefig("./thesis_plots/plots/chapter_5/specs/spec_{}.png".format(i))
    
    i += 1



