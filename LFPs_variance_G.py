import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def get_variance_across_each_time_point(LFP_data):
    return np.var(LFP_data, axis=1)

# find the local minimums and global minimum, using derivative
def find_minima(dataset):
    # find the derivative of the dataset
    derivative = np.diff(dataset)
    # find the points where the derivative changes sign
    sign_change = np.diff(np.sign(derivative))
    # find the local minima
    minima = np.where(sign_change > 0)[0] + 1
    # find the global minima, the point with largest change in derivative
    min1 = np.argmax(np.abs(derivative))+1
    # get the minimum point after min1
    min2 = np.argmin(dataset[min1:])+ min1+1
    return  min1, min2

G_range = np.arange(0.001, 0.07, 0.001) # You decide the range of G values
all_ts = {}

for i in range(len(G_range)):
	all_ts[f'G_{G_range[i]}'] = LFP_data[i]

variance_list = np.zeros(len(G_range))
for i in range(len(G_range)):
    variance_list[i] = np.max(get_variance_across_each_time_point(all_ts[f'G_{G_range[i]}']))

# Visualize the variance graph
plt.figure(figsize=(10, 5))
plt.plot(G_range, variance_list, marker='o')
plt.xlabel('G')
plt.ylabel('Variance of LFPs')
plt.title('Variance of LFPs across different G values')
plt.show()

# After the variance list:
df_gc_gm = pd.DataFrame()
for i in range(len(variance_list.index)):
    dataset = variance_list.iloc[i, :].values
    local_min, global_min = find_minima(dataset)
    print(f"local_min: {local_min}, global_min: {global_min}")
    # Visualize in the line graph, with the minima marked
    plt.plot(dataset)
    plt.plot(local_min, dataset[local_min], 'ro', label='local minima')
    plt.plot(global_min, dataset[global_min], 'go', label = 'global minima')
    plt.legend()
    plt.show()
    G_range = np.round(np.arange(0.001, 0.07, 0.001), 3)
    print(f"local_min: {G_range[local_min]}, global_min: {G_range[global_min]}")
    # for each case, add the local_min and global_min to the df_gc_gm
    df_gc_gm = pd.concat([df_gc_gm, pd.DataFrame({'caseid': df.iloc[i, 0], 'local_min': G_range[local_min], 'global_min': G_range[global_min]})], ignore_index=True)