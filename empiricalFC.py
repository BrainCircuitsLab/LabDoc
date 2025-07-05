import scipy.io
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import io
import numpy as np

# change the file_path to yours
file_path = '/Users/yilewang/workspaces/data4project/lateralization/ts_fmri/fmri_AAL_16/AD-TS/0306A/ROISignals_0306A.mat' 

regions = ['aCNG-L', 'aCNG-R','mCNG-L','mCNG-R','pCNG-L','pCNG-R', 'HIP-L','HIP-R','PHG-L','PHG-R','AMY-L','AMY-R', 'sTEMp-L','sTEMP-R','mTEMp-L','mTEMp-R']

mat = scipy.io.loadmat(file_path)
all = mat['ROISignals']

# filename = '/mnt/c/Users/wayne/Desktop/Functional TS/Region_Labels_90ROIs.txt'
# list_ = open(filename).read().split()
# region = list_[1::2]

# fc = np.ones((88,88))
# for i in range(88):
#     for j in range(88):
#         fc[i,j] = np.corrcoef(all[:,i], all[:,j])

df = pd.DataFrame(all, columns = range(16))
fc = df.corr(method='pearson') # the correlation matrix we have

fig = plt.figure(figsize=(15,12),dpi = 300)
sns.heatmap(pd.DataFrame(fc), cmap = "coolwarm", annot=False, vmin=-1, vmax=1, xticklabels=regions, yticklabels=regions)