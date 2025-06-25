# If you need to install tvb-library first:
# ! pip install tvb-library
from tvb.simulator.models.stefanescu_jirsa import ReducedSetHindmarshRose #import the local model from TVB library
from tvb.simulator.lab import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from pathlib import Path
import argparse

# Set the argument parse part to pass the parameters to the script.
parser = argparse.ArgumentParser(description='pass parameters') 
parser.add_argument('--Group',type=str, required=True, help='group')
parser.add_argument('--Caseid',type=str, required=True, help='caseid')
parser.add_argument('--G',type=float, required=True, help='G')
args = parser.parse_args()

# The main simulation function. 
def tvb_simulation(file, g):
    '''
    Parameters
    ------------
    file: zip
        structural connectivity zip file
    g: float
        Global coupling value to the script.
    '''
    connectivity.speed = np.array([10.])# conduction velocity
    # simulation parameters
    sim = simulator.Simulator(
        model=ReducedSetHindmarshRose(),# local model
        connectivity=connectivity.Connectivity.from_file(file), # file path of tvb connectome zip file
        coupling=coupling.Linear(a=np.array([g])), # Global coupling
        simulation_length=1e3*416, # Length of the simulation
        integrator=integrators.HeunStochastic(dt=0.01220703125, noise=noise.Additive(nsig=np.array([1.0]), ntau=0.0, random_stream=np.random.RandomState(seed=42))),# Define noise 
        monitors=(
        monitors.TemporalAverage(period=1.),
        monitors.Bold(hrf_kernel = equations.Gamma(), period=2000.),
        monitors.ProgressLogger(period=1e2))
    ).configure() # Using Gamma Kernal to simulate BOLD signal
    (tavg_time, tavg_data), (raw_time, raw_data),_ = sim.run()
    # Save the simulation based on brain regions
    df = pd.DataFrame(raw_data[:, 0, :, 0], columns = ['aCNG-L', 'aCNG-R','mCNG-L','mCNG-R','pCNG-L','pCNG-R', 'HIP-L','HIP-R','PHG-L','PHG-R','AMY-L','AMY-R', 'sTEMp-L','sTEMP-R','mTEMp-L','mTEMp-R'])
    return df

if __name__ == "__main__":
	# Define input path of structural connectomes zip file you need to use
	input_path = '/YOUR_PATH'+'.zip'
	# Define output path for saving the simulation results
	output_path = '/OUTPUT_PATH' + '/'
	# Make sure the directory exists
	Path(output_path).mkdir(parents=True, exist_ok=True)
	# Get the simulation results and save them.
	df = tvb_simulation(input_path, args.G)
	output_name = args.Group + "_" + args.Caseid + "_" + str(args.G) + ".xlsx"
	output = output_path + output_name
	df.to_excel(output)
	print(f"{args.Group} of {args.Caseid} in {args.G} has finished")