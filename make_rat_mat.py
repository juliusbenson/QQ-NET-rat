"""
Turns rat data niftis into a "SNR100_p5_trial6_avg.mat"-style .mat file to load in QQ_NET_test_simul.py
"""

import numpy as np
from nibabel.nifti1 import Nifti1Image
from scipy.io import savemat
from pathlib import Path
from os import makedirs

ratMgeNiiPath = '/home/jsb/temp/quantitative/QSMxT/RAT1117/JuliusBenson_FXS_RAT1117_24_1_1.nii'
ratQSMPath = '/home/jsb/temp/quantitative/QSMxT/BIDS/derivatives/qsmxt/sub-01/anat/sub-01_acq-nifti_Chimap.nii'
ratMaskPath = '/home/jsb/temp/quantitative/QSMxT/RAT1117/BET_mask.nii.gz'

ratMgeNii   = Nifti1Image.from_filename(ratMgeNiiPath)
ratQsmNii   = Nifti1Image.from_filename(ratQSMPath)
ratMaskNii  = Nifti1Image.from_filename(ratMaskPath)

ratMgeData  = np.asarray(ratMgeNii.dataobj).squeeze()
ratQsmData  = np.asarray(ratQsmNii.dataobj).squeeze()
ratMaskData = np.asarray(ratMaskNii.dataobj).squeeze()

# rat MGE data needs to be normalized to first echo. first echo should be all 1's

def normalize_mge(mge_data):
    first_echo = mge_data[..., 0]
    normalized_mge = mge_data / first_echo[..., np.newaxis]
    return normalized_mge

ratMgeNorm = normalize_mge(ratMgeData)

# The .mat file has a variable "Output_test"
# It is formatted as a 4D array.
# The final dimension is the number of echoes, then the QSM at the end
# We have 8 echoes, so the final dimension will be 9 (8 echoes + 1 QSM)

ratOutputTest = np.concatenate((ratMgeNorm, ratQsmData[..., np.newaxis]), axis=-1)

# ratOutputTest also needs to be masked
ratOutputTest = ratOutputTest * ratMaskData[..., np.newaxis]

# The .mat file also has a variable "Target_test" whose 4th dimension is 5 long
# This is supposed to hold the ground truth [S0, R2, chi_nb, v, Y], but I don't have that
# So I'll just fill it with 5 copies of the mask

Target_test = np.stack([ratMaskData] * 5, axis=-1)

# Diagnostic
Nifti1Image.to_filename(Nifti1Image(dataobj=ratOutputTest, affine=np.eye(4)), 'ratOutputTest.nii')
Nifti1Image.to_filename(Nifti1Image(dataobj=Target_test, affine=np.eye(4)), 'ratTargetTest.nii')
Nifti1Image.to_filename(Nifti1Image(dataobj=ratMaskData, affine=np.eye(4)), 'ratMaskData.nii')

resultDir = Path('./result')
makedirs(resultDir,exist_ok=True)
outDir = Path('./data')
makedirs(outDir,exist_ok=True)

savemat(outDir / 'SNR100_p5_trial0_avg.mat', {'Output_test': ratOutputTest, 'Target_test': Target_test, 'Mask': ratMaskData})