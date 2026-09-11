from pathlib import Path

# import nibabel as nib
import numpy as np
from scipy.io import loadmat
from nibabel.nifti1 import Nifti1Image

matPath = Path("./result/SNR100_NET_p5_trial0_overlap30.mat")
outputDir = Path(".")
outputDir.mkdir(exist_ok=True)

matData: dict[str, np.ndarray] = loadmat(matPath)

mask3: np.ndarray = matData["Mask3"]
target3: np.ndarray = matData["Target3"]
targetTest: np.ndarray = matData["Target_test"]

print(mask3.shape)       # (128, 128, 20)
print(target3.shape)     # (128, 128, 20, 5)
print(targetTest.shape)  # (5, 128, 128, 20)

affine: np.ndarray = np.eye(4)

# nib.save(
#     nib.Nifti1Image(mask3.astype(np.float32), affine),
#     outputDir / "Mask3.nii.gz",
# )

# nib.save(
#     nib.Nifti1Image(target3.astype(np.float32), affine),
#     outputDir / "Target3.nii.gz",
# )

# targetTestNifti: np.ndarray = np.moveaxis(targetTest, 0, -1)  # (128, 128, 20, 5)

# nib.save(
#     nib.Nifti1Image(targetTestNifti.astype(np.float32), affine),
#     outputDir / "Target_test.nii.gz",
# )

# Disaggregate
# [S0,R2,Y,v,chinb]

S0      = targetTest[0]
R2      = targetTest[1]
Y       = targetTest[2]
v       = targetTest[3]
chinb   = targetTest[4]

Nifti1Image(S0   ,affine).to_filename(outputDir / "S0")
Nifti1Image(R2   ,affine).to_filename(outputDir / "R2")
Nifti1Image(Y    ,affine).to_filename(outputDir / "Y")
Nifti1Image(v    ,affine).to_filename(outputDir / "v")
Nifti1Image(chinb,affine).to_filename(outputDir / "chinb")