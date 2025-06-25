import os
from tvb.simulator.lab import *
import numpy as np
import seaborn
import matplotlib.pyplot as plt
LOG = get_logger('demo')
import pickle as cPickle
from tvb.simulator.models.stefanescu_jirsa import ReducedSetHindmarshRose
import argparse
from os.path import join as pjoin
import pandas as pd
import scipy.io

parser = argparse.ArgumentParser(description='pass parameters')
parser.add_argument('--Group',type=str, required=True, help='group')
parser.add_argument('--Caseid',type=str, required=True, help='caseid')
parser.add_argument('--Go',type=float, required=True, help='Go')
parser.add_argument('--K21',type=float, required=True, help='K21')
args = parser.parse_args()

# Define the path:
data_dir = '/YOUR_DATA_DIR'
connectome_dir = pjoin(data_dir, 'YOUR_ZIP_DIR')
file = pjoin(connectome_dir, args.Group, args.Caseid+'.zip')

def tvb_K21_fitting(k21, Go, file):
    connectivity.speed = np.array([10.])
    sim = simulator.Simulator(
        model=ReducedSetHindmarshRose(K21=np.array([k21])), # K21
        connectivity=connectivity.Connectivity.from_file(file),                      
        coupling=coupling.Linear(a=np.array([Go])),
        simulation_length=1e3*416,
        integrator=integrators.HeunStochastic(dt=0.01220703125, noise=noise.Additive(nsig=np.array([1.0]), ntau=0.0,
                                                                                    random_stream=np.random.RandomState(seed=42))),
        monitors=(
        monitors.TemporalAverage(period=1.),
        monitors.Bold(hrf_kernel = equations.Gamma(), period=2000.),
        monitors.ProgressLogger(period=1e2)
        ))
    sim.configure()
    (tavg_time, tavg_data), (raw_time, raw_data), _ = sim.run()
    raw_data_mean = np.mean(raw_data,3)
    # Write it into the csv file based on regions
    df = pd.DataFrame(raw_data_mean[:,0,:], columns = ['aCNG-L', 'aCNG-R','mCNG-L','mCNG-R','pCNG-L','pCNG-R', 'HIP-L','HIP-R','PHG-L','PHG-R','AMY-L','AMY-R', 'sTEMp-L','sTEMP-R','mTEMp-L','mTEMp-R'])
    return df

if __name__ == "__main__":
    df = tvb_K21_fitting(args.K21, args.Go, file)
    if not os.path.exists(pjoin('/YOUR_PATH',args.Group)):
        os.makedirs(pjoin('/YOUR_PATH',args.Group))
    df.to_csv(pjoin('/YOUR_PATH', args.Group,args.Caseid+"_"+str(args.K21)+".csv"), index=False)