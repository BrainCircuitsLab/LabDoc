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
import cPickle

# Set the argument parse part to pass the parameters to the script.
parser = argparse.ArgumentParser(description='pass parameters') 
parser.add_argument('--Group',type=str, required=True, help='group')
parser.add_argument('--Caseid',type=str, required=True, help='caseid')
parser.add_argument('--G',type=float, required=True, help='G')
args = parser.parse_args()

# Simulation script
def tvb_simulation_branch(file, g):
    """
    Parameters
    ------------
    file: zip
        structural connectivity zip file
    g: float
        Global coupling value to the script.
    """
    speed = 10.
    data = []
    oscillator = ReducedSetHindmarshRose()
    white_matter = connectivity.Connectivity.from_file(file)
    oscillator.variables_of_interest = ["xi"]
    white_matter.speed = np.array([speed])
    white_matter_coupling = coupling.Linear(a=np.array(g))
    #heunint = integrators.HeunStochastic(dt=2 ** -6)
    heunint = integrators.HeunStochastic(dt=0.01220703125, noise=noise.Additive(nsig=np.array([0.00001])))
    # Initialise some Monitors with period in physical time
    mon_raw = monitors.Raw()
    mon_tavg = monitors.TemporalAverage(period=1.)
    mon_log = monitors.ProgressLogger(period=1e2)
    what_to_watch = (mon_raw, mon_tavg, mon_log)
    # Initialise a Simulator -- Model, Connectivity, Integrator, and Monitors.
    sim = simulator.Simulator(model=oscillator, connectivity=white_matter,
                          coupling=white_matter_coupling,
                          integrator=heunint, monitors=what_to_watch)
    sim.configure()

# Perform the simulation
    raw_data = []
    raw_time = []
    tavg_data = []
    tavg_time = []

    for raw, tavg, *rest in sim(simulation_length=1000):
        if not raw is None:
            raw_time.append(raw[0])
            raw_data.append(raw[1])

        if not tavg is None:
            tavg_time.append(tavg[0])
            tavg_data.append(tavg[1])

# Make the lists numpy.arrays for easier use.
    RAW = np.array(raw_data)
    data.append(RAW[:, 0, :, 0])
    t = raw_time

    sim_state_fname = 'sim_state.pickle'

    with open(sim_state_fname, 'wb') as file_descr:
        cPickle.dump({
            'history': sim.history.buffer,
            'current_step': sim.current_step,
            'current_state': sim.current_state,
            'rng': sim.integrator.noise.random_stream.get_state()},file_descr)
    file_descr.close()
    del sim

    sim = simulator.Simulator(model=oscillator, connectivity=white_matter,
                              coupling=white_matter_coupling,
                              integrator=heunint, monitors=what_to_watch)
    sim.configure()

    with open(sim_state_fname, 'rb') as file_descr:
        while True:
            try:
                state = cPickle.load(file_descr)
                sim.history.buffer = state['history']
                sim.current_step = state['current_step']
                sim.current_state = state['current_state']
                sim.integrator.noise.random_stream.set_state(state['rng'])
            except:
                break

    raw_data_branch = []
    raw_time_branch = []
    tavg_data_branch = []
    tavg_time_branch = []

    for raw, tavg, *rest in sim():
        if not raw is None:
            raw_time_branch.append(raw[0])
            raw_data_branch.append(raw[1])

        if not tavg is None:
            tavg_time_branch.append(tavg[0])
            tavg_data_branch.append(tavg[1])

    RAW_branch = np.array(raw_data_branch)
    t = raw_time_branch
    # Save the simulation based on brain regions
    df = pd.DataFrame(RAW_branch[:,0,:,0], columns = ['aCNG-L', 'aCNG-R','mCNG-L','mCNG-R','pCNG-L','pCNG-R', 'HIP-L','HIP-R','PHG-L','PHG-R','AMY-L','AMY-R', 'sTEMp-L','sTEMP-R','mTEMp-L','mTEMp-R'])
    return df


if __name__ == "__main__":
	# Define input path of structural connectomes zip file you need to use
	input_path = '/YOUR_PATH'+'.zip'
	# Define output path for saving the simulation results
	output_path = '/OUTPUT_PATH' + '/'
	# Make sure the directory exists
	Path(output_path).mkdir(parents=True, exist_ok=True)
	# Get the simulation results and save them.
	df = tvb_simulation_branch(input_path, args.G)
	output_name = args.Group + "_" + args.Caseid + "_" + str(args.G) + ".xlsx"
	output = output_path + output_name
	df.to_excel(output)
	print(f"{args.Group} of {args.Caseid} in {args.G} has finished")