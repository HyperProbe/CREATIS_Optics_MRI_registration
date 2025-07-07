
import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv
import os
import glob


id_patient = 3

# Indicate the path where MR volumes and optical images are located
Patient_ID_array = np.array(["P_025", "P_031", "P_033", "P_040", "P_054", "P_055", "P_058", "P_059", "P_060", "P_064", "P_066", "P_068"])
CHU = np.array(["CHU_Sainté","HCL","HCL","HCL","CHU_Sainté", "HCL","HCL","HCL","HCL","HCL","HCL","HCL"])


main_path = "/home/caredda/Videos/Optical_MRI_data/" + Patient_ID_array[id_patient]

# Saving directory
output_dir = main_path +  "/results/"


#Load images
# mri = cv.imread(output_dir+"MRI_proj_enhanced.png",cv.IMREAD_ANYCOLOR)
mri = cv.imread(output_dir+"MRI_projection.png",cv.IMREAD_ANYCOLOR)
optics = cv.imread(output_dir+"RGB_registered_on_MRI.png")

#Create merged image
alpha = 0.7
merged = cv.cvtColor(mri,cv.COLOR_GRAY2BGR)
for r in range(optics.shape[0]):
    for c in range(optics.shape[1]):
        if(optics[r,c,:].sum() != 0):
            merged[r,c,:] = alpha*optics[r,c,:] + (1-alpha)*merged[r,c,:]


plt.close('all')


# Create two subplots
ft = 18
fig, (ax1, ax2, ax3) = plt.subplots(1, 3)

#Draw images
ax1.set_title("Landmarks on registered optical image",fontsize=ft)
ax1.imshow(cv.cvtColor(optics,cv.COLOR_BGR2RGB))
ax1.set_axis_off()

ax2.set_title("Landmarks on MRI projection",fontsize=ft)
ax2.set_axis_off()
ax2.imshow(mri,cmap='plasma')

ax3.set_axis_off()
ax3.imshow(cv.cvtColor(merged,cv.COLOR_BGR2RGB))


# Initialize lists to store the points
points_optics = []
points_mri = []

# Function to be called when a mouse click event occurs
def onclick(event):
    # Check if the click happened in ax1
    if event.inaxes == ax1:
        x, y = event.xdata, event.ydata
        points_optics.append((x, y))
        ax1.plot(x, y, 'ro')  # Draw a red dot at the selected point
        fig.canvas.draw()

    # Check if the click happened in ax2
    elif event.inaxes == ax2:
        x, y = event.xdata, event.ydata
        points_mri.append((x, y))
        ax2.plot(x, y, 'bo')  # Draw a blue dot at the selected point
        fig.canvas.draw()

# Connect the event to the figure
cid = fig.canvas.mpl_connect('button_press_event', onclick)


# Display the plot
plt.show()


## Save verification landmarks
points_optics = np.asarray(points_optics)
points_mri = np.asarray(points_mri)

if not os.path.exists(output_dir+"verification_landmarks"):
    os.mkdir(output_dir+"verification_landmarks")

np.savetxt(output_dir+"verification_landmarks/optics.txt",points_optics)
np.savetxt(output_dir+"verification_landmarks/mri.txt",points_mri)

## Test
ft = 18

points_optics = np.loadtxt(output_dir+"verification_landmarks/optics.txt").astype(int)
points_mri = np.loadtxt(output_dir+"verification_landmarks/mri.txt").astype(int)


plt.figure()
plt.subplot(121)
plt.title("Landmarks on registered optical image",fontsize=ft)

plt.imshow(cv.cvtColor(optics,cv.COLOR_BGR2RGB))
plt.axis('off')
for i in range(points_optics.shape[0]):
    plt.plot(points_optics[i,0],points_optics[i,1],'r*')

plt.subplot(122)
plt.title("Landmarks on MRI projection",fontsize=ft)
plt.imshow(mri)
plt.axis('off')

for i in range(points_mri.shape[0]):
    plt.plot(points_mri[i,0],points_mri[i,1],'go')
for i in range(points_optics.shape[0]):
    plt.plot(points_optics[i,0],points_optics[i,1],'r*')
plt.show()