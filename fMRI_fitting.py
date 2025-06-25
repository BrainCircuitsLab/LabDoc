import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.io


# Load the empirical data. If you only have time series, you need to generate a correlation matrix. 
# An example, load the correlation matrix as mat_fisher_z here.
file_path_z = '/YOUR_PATH_Empirical_FC.mat' 
mat_fisher_z = scipy.io.loadmat(file_path_z)
# Get the upper part of of the matrix along diagonal:
emp_tril = np.tril(np.array(mat_fisher_z['ROICorrelation_FisherZ']), -1)
emp_vec = emp_tril[np.nonzero(emp_tril)].flatten()

# The range of G
G_list = np.arange(START, END, STEPSIZE)

# Initialize lists to store values
g_values = []
corr_values = []

# Read the data
for g in g_list:
    g = np.round(g, 1)
    sim_data = pd.read_csv(f"./sim_data_K21_2820A_{g}.csv")
    # calculate the functional connectivity of the simulated data
    sim_fc = sim_data.iloc[:,1:].corr(method='pearson')
    # flattern the simulated data
    sim_tril = np.tril(np.array(sim_fc), -1)
    sim_vec = sim_tril[np.nonzero(sim_tril)].flatten()
    # do correlation analysis between the empirical data and the simulated data
    corr = np.corrcoef(emp_vec, sim_vec)[0,1]
    # append values to lists
    g_values.append(g)
    corr_values.append(corr)

# Create DataFrame from lists
G_corr = pd.DataFrame({
    'G': g_values,
    'corr': corr_values
})

# Find the position of the max correlation value
max_corr_pos = G_corr['corr'].idxmax()
max_corr_value = G_corr['corr'].max()
max_corr_G = G_corr['G'].iloc[max_corr_pos]
print(f"The maximum correlation value is {max_corr_value} at G = {max_corr_G}")

# Visualize the correlation values
plt.figure(figsize=(10,5))
plt.plot(G_corr['G'], G_corr['corr'])
plt.xlabel('G')
plt.ylabel('Correlation')
plt.title('Correlation between Empirical and Simulated Data')
plt.show()