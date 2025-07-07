##

import numpy as np
import matplotlib.pyplot as plt
import nibabel as nib
import cv2 as cv
import os
import glob


id_patient = 3

# Indicate the path where MR volumes and optical images are located
Patient_ID_array = np.array(["P_025", "P_029", "P_031", "P_033", "P_055", "P_058", "P_059", "P_060", "P_066", "P_068", "P_070" ])
main_path = "/home/caredda/Videos/Optical_MRI_data/" + Patient_ID_array[id_patient]


path_neuronavigation_optics = main_path + "/optics/Condition_Neuronavigation/"

# Saving directory
output_dir = main_path +  "/results_registration_landmarks/"
if not os.path.exists(output_dir):
    os.mkdir(output_dir)



# Set filenames
filename_Optics_img = main_path + "/optics/initial_img.png"
filename_Optics_mask = main_path + "/optics/mask.png"

l = glob.glob(path_neuronavigation_optics+"*")
filename_neuronavigation_optics = []
for i in range(1,len(l)+1):
    filename_neuronavigation_optics.append(path_neuronavigation_optics+str(i)+".tif")

#Get Optics resolution
if not os.path.isfile(main_path + "/optics/resolution.txt"):
    BGR_resolution = 0.064
else:
    BGR_resolution = np.loadtxt(main_path + "/optics/resolution.txt")


##
initial_img = cv.imread(filename_Optics_img)


Optics_x_point = np.zeros(len(filename_neuronavigation_optics))
Optics_y_point = np.zeros(len(filename_neuronavigation_optics))

for i in range(len(filename_neuronavigation_optics)):
    plt.close('all')
    plt.figure()
    im= cv.imread(filename_neuronavigation_optics[i])
    plt.title("Click left on the left image where the neuronavigation tool is pointing. Validate with middle mouse button")
    plt.subplot(121)
    plt.imshow(cv.cvtColor(im, cv.COLOR_BGR2RGB),zorder=2)
    plt.subplot(122)
    plt.imshow(cv.cvtColor(initial_img, cv.COLOR_BGR2RGB),zorder=2)
    yroi = plt.ginput(0,0)
    a = yroi.pop()
    Optics_x_point[i] = a[0]
    Optics_y_point[i] = a[1]


plt.close('all')


print("Create Optics landmarks")

# #Optics data
# landmarks_Optics = np.zeros((initial_img.shape[0],initial_img.shape[1],1), dtype=np.int16)
# #landmarks
# for i in range(0,len(Optics_x_point)):
#     landmarks_Optics[int(Optics_y_point[i]),int(Optics_x_point[i]),0] = i+1
#
#
# #Create nii img
# landmarks_Optics = nib.Nifti1Image(landmarks_Optics, np.eye(4))
# # landmarks_Optics.header.set_xyzt_units(MRI_img.header.get_xyzt_units())
# landmarks_Optics.header.set_zooms((BGR_resolution,BGR_resolution,BGR_resolution))
# # #save nii image
# nib.save(landmarks_Optics,output_dir+"landmarks_Optics.nii")

#Save optical landmarks point
np.savetxt(output_dir+"Optical_col_landmarks.txt",Optics_x_point)
np.savetxt(output_dir+"Optical_row_landmarks.txt",Optics_y_point)