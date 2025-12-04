#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 14:57:11 2023

@author: C. Caredda
"""



import itk.itkSimilarity2DTransformPython
import itk.itkElastixRegistrationMethodPython
import itk.elxParameterObjectPython

from module.ITK import *
from math import sqrt
import os
#from opticalSegmentation import *
from skimage.transform import pyramid_reduce
from scipy.ndimage import center_of_mass
from scipy.ndimage import binary_erosion, binary_dilation, generate_binary_structure, iterate_structure

import itertools
import subprocess
from subprocess import call
import nibabel as nib
import matplotlib.pyplot as plt

from scipy import ndimage
import cv2 as cv
import shutil
from skimage import measure
import pyvista as pv



import itk
import numpy as np

def itk_metric_value_fixed_space(metric_type, fixed_img, moving_img):
    """
    Compute an ITK metric value between two images (same geometry).
    metric_type must be one of:
        itk.MeanSquaresImageToImageMetricv4
        itk.NormalizedCorrelationImageToImageMetricv4
        itk.MattesMutualInformationImageToImageMetricv4
    """
    metric = metric_type[type(fixed_img), type(moving_img)].New()
    transform = itk.TranslationTransform[itk.D, fixed_img.GetImageDimension()].New()
    interpolator = itk.LinearInterpolateImageFunction[type(fixed_img), itk.D].New()

    
    metric.SetFixedImage(fixed_img)
    metric.SetMovingImage(moving_img)
    metric.SetFixedImageRegion(fixed_img.GetLargestPossibleRegion())
    metric.SetTransform(transform)
    metric.SetInterpolator(interpolator)

    # Required for MI
    if metric_type == itk.MattesMutualInformationImageToImageMetricv4:
        metric.SetNumberOfHistogramBins(64)

    metric.Initialize()

    params = itk.OptimizerParameters[itk.D]()
    params.SetSize(2)
    params.SetElement(0, 0)

    return float(metric.GetValue(params))


def is_RGB_optical_image(filename):
    img = cv.imread(filename,cv.IMREAD_ANYCOLOR)

    if img.ndim>2:
        out_flag = True
        suffix_out_optics = ""
    else:
        out_flag = False
        suffix_out_optics = "_HSI"
    
    return out_flag,suffix_out_optics


def dice_coefficient(mask1, mask2):
    # Ensure the masks are binary
    mask1 = np.asarray(mask1).astype(np.bool_)
    mask2 = np.asarray(mask2).astype(np.bool_)
    
    intersection = np.sum(mask1 & mask2)
    size_sum = np.sum(mask1) + np.sum(mask2)
    
    if size_sum == 0:
        # Avoid division by zero: if both masks are empty, define DICE as 1
        return 1.0
    
    dice = 2.0 * intersection / size_sum
    return dice

def overlap_coefficient(A, B):
    # A and B: binary NumPy arrays (0/1 or False/True)
    
    intersection = np.count_nonzero(A & B)
    size_A = np.count_nonzero(A)
    size_B = np.count_nonzero(B)
    
    if size_A == 0 or size_B == 0:
        return 0.0  # no overlap possible
    
    return float(intersection / min(size_A, size_B))




def merge_two_colored_img(in1_BGR, in2_BGR, mask, weight ):
    
    out = np.zeros(in1_BGR.shape)

    for row in range(in1_BGR.shape[0]):
        for col in range(in1_BGR.shape[1]):
            if mask[row,col]==0:
                out[row,col,:] = in1_BGR[row,col,:]
            else:
                out[row,col,:] = in1_BGR[row,col,:]*weight + in2_BGR[row,col,:]*(1-weight)
    return out.astype(np.uint8)


def apply_colormap_with_mask(in_BGR, in_grayscale, mask, colormap, weight):
    

    # Apply a colormap to grayscale
    if colormap == "":
        display = cv.cvtColor(in_grayscale,cv.COLOR_GRAY2BGR)
    else:
        display = cv.applyColorMap(in_grayscale, colormap)

    out =  merge_two_colored_img(in_BGR, display, mask, weight )
    
    return out


def adapt_img_size_after_roation(input_img, target_img, kp_target_img):

    #Update center of rotation
    (h, w) = input_img.shape[:2]
    (cX, cY) = (int(w / 2), int(h / 2))

    # Crop rotated img or add zero to match initial image size
    nb_cols_before = kp_target_img[0]-cX
    nb_rows_before = kp_target_img[1]-cY

    # print(nb_cols_before, nb_rows_before)

    #Handle columns before the image
    if nb_cols_before>0:
        #Create the columns of zeros
        column_of_zeros = np.zeros((input_img.shape[0], nb_cols_before))

        # Add the column of zeros before the image
        input_img = np.concatenate((column_of_zeros, input_img), axis=1)
    else:
        input_img = input_img[:,np.abs(nb_cols_before):]

    #Handle rows before the image
    if nb_rows_before>0:
        #Create the rows of zeros
        row_of_zeros = np.zeros((nb_rows_before, input_img.shape[1]))

        # Add the rows of zeros before the image
        input_img = np.concatenate((row_of_zeros, input_img), axis=0)
    else:
        input_img = input_img[np.abs(nb_rows_before):,:]

    nb_rows_after = target_img.shape[0] - input_img.shape[0]
    nb_cols_after = target_img.shape[1] - input_img.shape[1]

    print(nb_rows_after, nb_cols_after)

    #Handle rows after the image
    if nb_rows_after>0:
        #Create the rows of zeros
        row_of_zeros = np.zeros((nb_rows_after, input_img.shape[1]))

        # Add the rows of zeros before the image
        input_img = np.concatenate((input_img, row_of_zeros), axis=0)
    else:
        input_img = input_img[0:nb_rows_after,:]

    #Handle cols after the image
    if nb_cols_after>0:
        #Create the columns of zeros
        column_of_zeros = np.zeros((input_img.shape[0], nb_cols_after))

        # Add the rows of zeros before the image
        input_img = np.concatenate((input_img, row_of_zeros), axis=1)
    else:
        input_img = input_img[:,0:nb_cols_after]

    return input_img

def find_nearest_white(img, target):
    nonzero = cv.findNonZero(img)
    distances = np.sqrt((nonzero[:,:,0] - target[0]) ** 2 + (nonzero[:,:,1] - target[1]) ** 2)
    nearest_index = np.argmin(distances)
    return nonzero[nearest_index][0]


def get_alignement_points_in_skeleton(itk_MRI_proj_skeleton, itk_Optics_skeleton, itk_Optical_mask, itk_mask_tumor, nb_MRI_keypoints):
    
    #Get tumor mask
    contours_tumor, hierarchy = cv.findContours(itk.GetArrayFromImage(itk_mask_tumor), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)


    #Get MRI skeleton components and keypoints as component centroids the closest to the tumor mask
    np_MRI_skeleton = itk.GetArrayFromImage(itk_MRI_proj_skeleton).astype(np.uint8)
    num_labels, labels, stats, centroids = cv.connectedComponentsWithStats(np_MRI_skeleton)
    centroids = centroids[1:,:].astype(int) #remove background



    #Calculate distance between the tumor contour and the centroid of each skeleton component
    dist_to_tumor = []
    for c in centroids:
        dist_to_tumor.append(cv.pointPolygonTest(contours_tumor[0],(float(c[0]),float(c[1])),True))
    dist_to_tumor = np.asarray(dist_to_tumor)

    #Only keep the first 3 keypoints closest to the tumor (inside or the closest to the tumor: max signed distance -> inside (positive), outside: negative))
    np_kp_to_keep = np.minimum(nb_MRI_keypoints,centroids.shape[0])
    id_max = np.argsort(dist_to_tumor)[-np_kp_to_keep:]
    centroids = centroids[id_max,:]


    kpts_MRI_tumor_phys = []
    kpts_MRI_tumor = []
    for c in centroids:
        kpts_MRI_tumor.append(c)
        kpts_MRI_tumor_phys.append(itk_mask_tumor.TransformIndexToPhysicalPoint([int(c[0]), int(c[1])]))


    # kpts_MRI_tumor_phys = []
    # kpts_MRI_tumor = []
    # for i in range(id_max.shape[0]):
    #     # coords for component i
    #     coords = np.column_stack(np.where(labels == id_max[i]))

    #     # centroid (float)
    #     centroid = coords.mean(axis=0)   # (cy, cx)

    #     # compute distances
    #     dists = np.linalg.norm(coords - centroid, axis=1)

    #     # closest pixel
    #     P = coords[np.argmin(dists)]   
    #     kpts_MRI_tumor.append(P)
    #     kpts_MRI_tumor_phys.append(itk_mask_tumor.TransformIndexToPhysicalPoint([int(P[0]), int(P[1])]))




    #Get Optical skeleton components and define the optical keypoint as component centroid the closest to the center of the img mask
    np_optics_skeleton = itk.GetArrayFromImage(itk_Optics_skeleton).astype(np.uint8)
    np_optics_mask = itk.GetArrayFromImage(itk_Optical_mask).astype(np.uint8)

    #Calculate mask centroid
    ys, xs = np.where(np_optics_mask > 0) 
    centroid_mask = (int(xs.mean()), int(ys.mean()))

    #Calculate centroids for each skeleton component
    num_labels, labels, stats, centroids = cv.connectedComponentsWithStats(np_optics_skeleton)
    centroids = centroids[1:,:].astype(int) #remove background


    #Calculate distance between component centroid and mask centroid
    dist_to_center = []
    for c in centroids:
        dist_to_center.append(cv.norm(centroid_mask - c, cv.NORM_L2))
    dist_to_center = np.asarray(dist_to_center)

    

    
    
    kp_Optics = [int(centroids[np.argmin(dist_to_center),0]), int(centroids[np.argmin(dist_to_center),1])]
    kp_Optics_phys = itk_mask_tumor.TransformIndexToPhysicalPoint(kp_Optics)


    return kp_Optics, kp_Optics_phys, kpts_MRI_tumor, kpts_MRI_tumor_phys



def resize_rect(x, y, w, h, f):
    # Center of the rectangle
    cx = x + w / 2.0
    cy = y + h / 2.0

    # New size
    new_w = w * f
    new_h = h * f

    # New top-left corner
    new_x = int(cx - new_w / 2.0)
    new_y = int(cy - new_h / 2.0)

    return new_x, new_y, int(new_w), int(new_h)



def get_regular_skeleton_points_in_rect(skel, rect, spacing_mm, min_spacing_mm):
    """
    skel : binary skeleton (0/255)
    rect : (xmin, xmax, ymin, ymax) in pixel coordinates
    spacing_mm : mm per pixel (float)
    min_spacing_mm : minimal spacing between points (in mm)
    """
    xmin, ymin, w, h = rect
    xmax = xmin+w
    ymax = ymin+h
    # clamp
    xmin = max(0, xmin)
    ymin = max(0, ymin)
    xmax = min(skel.shape[1], xmax)
    ymax = min(skel.shape[0], ymax)

    # Extract skeleton points inside the rectangle
    region = skel[ymin:ymax, xmin:xmax]
    ys, xs = np.where(region > 0)
    if len(xs) == 0:
        return np.empty((0,2), dtype=float)

    # Convert to global coordinates
    pts_px = np.column_stack([xs + xmin, ys + ymin]).astype(float)

    # Convert minimal spacing into pixels
    min_spacing_px = min_spacing_mm / spacing_mm

    # Storage for selected points
    selected = []

    for p in pts_px:
        if not selected:
            selected.append(p)
        else:
            # Compute distance to all previously selected points
            d = np.linalg.norm(np.array(selected) - p, axis=1)
            if np.all(d >= min_spacing_px):
                selected.append(p)

    return selected

def get_alignment_points(itk_optical_mask, itk_optical_skeleton, itk_MRI_skeleton, itk_tumor_mask, kpts_MRI_tumor = None, kp_Optics = None, space_between_kpt_mm = 8, enlarge_tumor_roi_factor = 1):
    
    if kp_Optics == None:
        #Get center of optical mask
        center_Optics = [ np.average(indices) for indices in np.where(itk.GetArrayFromImage(itk_optical_mask) > 0) ]
        kp_Optics = [int(center_Optics[1]), int(center_Optics[0])]

    vessel_img = itk.GetArrayFromImage(itk_optical_skeleton)
    temp = find_nearest_white(vessel_img, kp_Optics)
    kp_Optics = [int(temp[0]), int(temp[1])]


    if kpts_MRI_tumor == None:
        #Contour tumor mask
        contours_tumor, hierarchy = cv.findContours(itk.GetArrayFromImage(itk_tumor_mask), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        #Bounding box of the contour
        x,y,w,h = cv.boundingRect(contours_tumor[0]) #x,y,w,h

        #resize tumor ROI rectangle
        x, y, w, h = resize_rect(x, y, w, h, enlarge_tumor_roi_factor)
        rect = (x,y,w,h)


        #Get center of mass of tumor  
        reso_MRI_mm = np.min(itk_MRI_skeleton.GetSpacing())
        kpts_MRI_tumor = get_regular_skeleton_points_in_rect(itk.GetArrayFromImage(itk_MRI_skeleton), rect, reso_MRI_mm, space_between_kpt_mm)


    kp_Optics_phys = itk_tumor_mask.TransformIndexToPhysicalPoint(kp_Optics)

    kpts_MRI_tumor_phys = []
    for i in range(len(kpts_MRI_tumor)):
        # kpts_MRI_tumor[i] = np.asarray(kpts_MRI_tumor[i]).astype(int) 
        kpts_MRI_tumor_phys.append(itk_tumor_mask.TransformIndexToPhysicalPoint([int(kpts_MRI_tumor[i][0]), int(kpts_MRI_tumor[i][1])]))

    return kp_Optics, kp_Optics_phys, kpts_MRI_tumor, kpts_MRI_tumor_phys



def enhance_Blood_vessel(itk_image, resolution_mm, sigma_minimum_mm, sigma_maximum_mm, number_of_sigma_steps, alpha, beta, gamma, Light_structures):
    
    #Covnert in pixels
    sigma_minimum = int(sigma_minimum_mm/resolution_mm)
    sigma_maximum = int(sigma_maximum_mm/resolution_mm)


    objectness_filter = itk.HessianToObjectnessMeasureImageFilter.New()
    objectness_filter.SetBrightObject(Light_structures)
    # objectness_filter.SetScaleObjectnessMeasure(False)
    objectness_filter.SetAlpha(alpha)
    objectness_filter.SetBeta(beta)
    objectness_filter.SetGamma(gamma)

    multi_scale_filter = itk.MultiScaleHessianBasedMeasureImageFilter.New()
    multi_scale_filter.SetInput(itk_image)
    multi_scale_filter.SetHessianToMeasureFilter(objectness_filter)
    multi_scale_filter.SetSigmaStepMethodToLogarithmic()
    multi_scale_filter.SetSigmaMinimum(sigma_minimum)
    multi_scale_filter.SetSigmaMaximum(sigma_maximum)
    multi_scale_filter.SetNumberOfSigmaSteps(number_of_sigma_steps)

    # return multi_scale_filter_mri.GetOutput()
    return itk.GetArrayFromImage(multi_scale_filter.GetOutput())

    # mri_frangi = itk.GetArrayFromImage(multi_scale_filter_mri.GetOutput())








def print_nifti_info(filename):
    print(os.path.basename(filename))
    
    vol = itk.imread(filename)
    print("Spacing",vol.GetSpacing())
    print("Origin",vol.GetOrigin())
    print("Direction",vol.GetDirection())
    print("Size",itk.size(vol))




def open_itksnap_with_overlay(main_image_path, overlay_image_path, overlay_image_path2="", overlay_opacity=0.5):
    """
    Open ITK-SNAP with a main image and an additional image as a semi-transparent overlay.

    :param main_image_path: Path to the main image file.
    :param overlay_image_path: Path to the overlay image file.
    :param overlay_opacity: Opacity of the overlay image (0.0 to 1.0).
    """
    # Construct the command to open ITK-SNAP with the main image and overlay
    command = [
        'itksnap',
        '-g', main_image_path,          # Main image
        '-o', overlay_image_path#,       # Overlay image
    ]


    if overlay_image_path2 != "":
        command.append('-o')
        command.append(overlay_image_path2)


    # Run the command
    subprocess.call(command)



def open_MRIcroGL_with_overlay(mri_file, overlay_file):
    """
    Opens MRIcroGL to display an MRI volume and overlay in render mode.

    Parameters:
        mri_file (str): Path to the MRI volume file (e.g., NIfTI file).
        overlay_file (str): Path to the overlay file (e.g., NIfTI file).
    """
    # Validate input files
    if not os.path.isfile(mri_file):
        raise FileNotFoundError(f"MRI file not found: {mri_file}")
    if not os.path.isfile(overlay_file):
        raise FileNotFoundError(f"Overlay file not found: {overlay_file}")


    #Set filename in MRIcroGL display file
    replace_line_in_file(file_path="module/display_MRIcroGL.py",
                         key="gl.loadimage",
                         new_string="gl.loadimage("+"'"+mri_file+"')\n")
    replace_line_in_file(file_path="module/display_MRIcroGL.py",
                         key="gl.overlayload(",
                         new_string="gl.overlayload("+"'"+overlay_file+"')\n")

    

    # Run MRIcroGL with the generated script
    subprocess.call(['MRIcroGL','module/display_MRIcroGL.py'])


def replace_line_in_file(file_path, key, new_string):
    # Read the file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Replace lines starting with "(Centerorotation"
    modified_lines = [(new_string if line.startswith(key) else line) for line in lines]

    # Write the modified lines back to the file
    with open(file_path, 'w') as file:
        file.writelines(modified_lines)




def change_origin(filenames_MRI, filenames_optics, kpt_MRI = [0,0], kpt_Optics = [0,0]):
    
    
    if (len(filenames_MRI)==0 or len(filenames_optics)==0):
        print("[change_origin] empty lists !")
        return
    


    #rename MRI volumes (do not change origin!)
    for f in filenames_MRI:
        vol = itk.imread(f, itk.F)
        itk.imwrite(vol, f.split('.')[0] + "_origin_changed.nii.gz")

    #Change origin in optics volume only
    for f in filenames_optics:
        vol = itk.imread(f, itk.F)
        vol.SetOrigin([kpt_MRI[0] - kpt_Optics[0], kpt_MRI[1] - kpt_Optics[1]])
        itk.imwrite(vol, f.split('.')[0] + "_origin_changed.nii.gz")



def getSignedDistanceMap(binary_image):
    # Create the distance map filter
    distance_map_filter = itk.SignedMaurerDistanceMapImageFilter.New(Input=binary_image)

    # Set InsideIsPositive to False if inside should have negative values (default is True)
    distance_map_filter.SetInsideIsPositive(False)

    # Update the filter
    distance_map_filter.Update()

    # Get the signed distance map
    return distance_map_filter.GetOutput()




def optics_itk_rotation_2D(angle, itk_input, MRI_proj, kp_Optics, kp_MRI_phys ):
        
        
    #rotate np image
    np_rotated = Rotation_2D(angle, itk_input, center = kp_Optics)
    #Binarize image
    # np_rotated[np_rotated>0] = 1

    #Get new origin after rotation
    (h, w) = np_rotated.shape[:2]
    (cX, cY) = (w / 2, h / 2)
    kp_Optics_phys = MRI_proj.TransformIndexToPhysicalPoint([int(cX), int(cY)])

    #Write rotated image with correct origin
    rotated_optics = itk.GetImageFromArray(np.ascontiguousarray(np_rotated))
    rotated_optics.SetSpacing(itk_input.GetSpacing())
    rotated_optics.SetDirection(itk_input.GetDirection())
    rotated_optics.SetOrigin([kp_MRI_phys[0] - kp_Optics_phys[0], kp_MRI_phys[1] - kp_Optics_phys[1]])

    return rotated_optics


 
def Rotation_2D(angle, itk_input, center = None):

    image =  itk.GetArrayFromImage(itk_input)

    
    (h, w) = image.shape[:2]

    cX = center[0]
    cY = center[1]

    # grab the rotation matrix (applying the negative of the
    # angle to rotate clockwise), then grab the sine and cosine
    # (i.e., the rotation components of the matrix)
    M = cv.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])

    # compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))

    # adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY

    # perform the actual rotation and return the image
    rotated =  cv.warpAffine(image, M, (nW, nH))

   
    return rotated




def Rotate_Volume_Back_To_T1_volume(R, T, filename_input, ref, center_rotation, filename_out, Dimension = 3):
    
    input = itk.imread(filename_input,itk.F)

    #Create an affine transform
    AffineTransformType = itk.AffineTransform[itk.D, Dimension]
    affine_transform = AffineTransformType.New()

    # Set the matrix and translation
    affine_transform.SetMatrix(itk.matrix_from_array(R))
    affine_transform.SetTranslation(T.tolist())
    # Set Center of rotation
    affine_transform.SetCenter(center_rotation)

    #Get inverse transform
    inverse_affine_transform = affine_transform.GetInverseTransform()

    composite_transform = itk.CompositeTransform[itk.D, Dimension].New()
    composite_transform.AddTransform(inverse_affine_transform)

    #Apply the inverse transform
    inversed_vol = itk.resample_image_filter(input,
                                             transform=composite_transform,
                                             use_reference_image=True,
                                             reference_image=ref)
    
    itk.imwrite(inversed_vol,filename_out)



def get_inverse_similarity_transform(filename_params_reg):
    #Create a similarity transform
    params_transform_reg = itk.ParameterObject.New()
    params_transform_reg.AddParameterFile(filename_params_reg)
    pm0 = params_transform_reg.GetParameterMap(0)



    similarity_transform = itk.Similarity2DTransform.New()

    center = [float(p) for p in pm0['CenterOfRotationPoint']]
    fixed_parameters = itk.OptimizerParameters[itk.D](len(center))
    for i, p in enumerate(center):
        fixed_parameters[i] = p
    similarity_transform.SetFixedParameters(fixed_parameters)

    elx_parameters = [float(p) for p in pm0['TransformParameters']]
    itk_parameters = itk.OptimizerParameters[itk.D](len(elx_parameters))
    for i, p in enumerate(elx_parameters):
        itk_parameters[i] = p

    similarity_transform.SetParameters(itk_parameters)


    # Calculate inverse transform
    inverse_transform = similarity_transform.GetInverseTransform()



    # When creating the composite transform for itk, 
    # take into account that elastix uses T2(T1(x)) while itk does this the other way around.
    # So to get the correct composite transform, add the last transform in elastix first in itk.
    composite_transform = itk.CompositeTransform[itk.D, 2].New()
    composite_transform.AddTransform(inverse_transform)

    return composite_transform

def Apply_Afffine_Transform(R, T, input, center_rotation, filename_out="", Dimension = 3):

    #Create an affine transform
    AffineTransformType = itk.AffineTransform[itk.D, Dimension]
    affine_transform = AffineTransformType.New()

    # Set the matrix and translation
    affine_transform.SetMatrix(itk.matrix_from_array(R))
    affine_transform.SetTranslation(T.tolist())
    # Set Center of rotation
    affine_transform.SetCenter(center_rotation)

    #6) Use the resampling filter to apply the transform
    resample_filter = itk.ResampleImageFilter.New(Input=input)
    resample_filter.SetTransform(affine_transform)
    resample_filter.SetOutputSpacing(input.GetSpacing())

    resample_filter.SetSize(input.GetLargestPossibleRegion().GetSize())
    resample_filter.SetOutputOrigin(input.GetOrigin())



    np_dir_vnl = itk.GetVnlMatrixFromArray(np.eye(3))
    direction = input.GetDirection()
    direction.GetVnlMatrix().copy_in(np_dir_vnl.data_block())

    resample_filter.SetOutputDirection(direction)

    # resample_filter.SetOutputDirection(input.GetDirection())

    resample_filter.SetDefaultPixelValue(0)  # Assuming background is 0

    mri_rotated = resample_filter.GetOutput()
    mri_rotated.Update()

    if filename_out != "":
        itk.imwrite(mri_rotated,filename_out)

    return mri_rotated

    # print("input size",input_size)
    # print("new size", new_size)


    # resampler = itk.ResampleImageFilter.New(Input=input, Transform=affine_transform)
    # # Set the new size, spacing, and origin
    # resampler.SetSize([input_size[0]*2, input_size[1]*2, input_size[2]*2])
    # resampler.SetOutputSpacing(input.GetSpacing())
    # resampler.SetOutputOrigin(input.GetOrigin())


    # # Set the interpolator
    # interpolator = itk.LinearInterpolateImageFunction.New(input)
    # resampler.SetInterpolator(interpolator)

    # # Update the resampler
    # resampler.Update()

    # # Get the transformed image
    # mri_rotated = resampler.GetOutput()
    # itk.imwrite(mri_rotated,filename_out)



def reconstruct_Optical_img_on_MRI_volume(image_to_reconstruct, rotated_surface, rotated_tumor, filename_out):

    #Create projection
    np_surface_rotated = itk.GetArrayFromImage(rotated_surface)
    np_tumor_rotated = itk.GetArrayFromImage(rotated_tumor)
    Projected_optical_rotated = create_MRI_volume_from_Projection_np(image_to_reconstruct, np_surface_rotated, np_tumor_rotated, Projection="Transverse")

    #Create itk object
    rec_Optical_vol = itk.GetImageFromArray(np.ascontiguousarray(Projected_optical_rotated))
    rec_Optical_vol.SetSpacing(rotated_surface.GetSpacing())
    rec_Optical_vol.SetDirection(rotated_surface.GetDirection())
    rec_Optical_vol.SetOrigin(rotated_surface.GetOrigin())

    # Write result
    itk.imwrite(rec_Optical_vol, filename_out)



def create_MRI_volume_from_Projection_np(proj, brain_surface, tumor, Projection):


    data_MRI_out = np.zeros(brain_surface.shape)

    #Get center of mass of the tumor and the location along the projection axis
    #Identify if the projection has to be done on the first or second projection plane
    center_of_mass_tumor = ndimage.center_of_mass(tumor)
    if Projection== "Sagital":
        center_of_mass_tumor_axis_proj = center_of_mass_tumor[2]
        if int((center_of_mass_tumor_axis_proj-1)/2)>tumor.shape[2]/2:
            id_proj = 1
        else:
            id_proj = 0

    if Projection== "Transverse":
        center_of_mass_tumor_axis_proj = center_of_mass_tumor[0]
        if int((center_of_mass_tumor_axis_proj-1)/2)>tumor.shape[0]/2:
            id_proj = 1
        else:
            id_proj = 0

    if Projection== "Coronal":
        center_of_mass_tumor_axis_proj = center_of_mass_tumor[1]
    
        if int((center_of_mass_tumor_axis_proj-1)/2)>tumor.shape[1]/2:
            id_proj = 1
        else:
            id_proj = 0




    for i in range(proj.shape[0]):
        for j in range(proj.shape[1]):

            if Projection== "Sagital":
                data_surface = brain_surface[i,j,:]

                #Get idx of non zero elements
                non_zero_idx_surface = np.nonzero(data_surface)[0]

                if non_zero_idx_surface.size==0:
                    continue            
                
                #Separate non_zero idx into contiguous arrays
                idx_split = np.split(non_zero_idx_surface, np.where(non_zero_idx_surface[1:] != non_zero_idx_surface[:-1] + 1)[0] + 1)

                if len(idx_split) == 2 :
                    idx = idx_split[id_proj][:]              
                else:
                    idx = idx_split[0][:]

                data_MRI_out[i,j,idx] = proj[i,j]


                
            if Projection== "Transverse":
                data_surface = brain_surface[:,i,j]

                #Get idx of non zero elements
                non_zero_idx_surface = np.nonzero(data_surface)[0]

                if non_zero_idx_surface.size==0:
                    continue            
                
                #Separate non_zero idx into contiguous arrays
                idx_split = np.split(non_zero_idx_surface, np.where(non_zero_idx_surface[1:] != non_zero_idx_surface[:-1] + 1)[0] + 1)

                if len(idx_split) == 2 :
                    idx = idx_split[id_proj][:]              
                else:
                    idx = idx_split[0][:]

                data_MRI_out[idx,i,j] = proj[i,j] 




            if Projection== "Coronal":
                data_surface = brain_surface[i,:,j]

                #Get idx of non zero elements
                non_zero_idx_surface = np.nonzero(data_surface)[0]

                if non_zero_idx_surface.size==0:
                    continue            
                
                #Separate non_zero idx into contiguous arrays
                idx_split = np.split(non_zero_idx_surface, np.where(non_zero_idx_surface[1:] != non_zero_idx_surface[:-1] + 1)[0] + 1)

                if len(idx_split) == 2 :
                    idx = idx_split[id_proj][:]              
                else:
                    idx = idx_split[0][:]
                    
                data_MRI_out[i,idx,i] = proj[i,j]

    return data_MRI_out



def create_simple_MRI_projection(MRI_vol, brain_surface, Projection, id_proj):
    
    #Create projection (numpy: z,x,y) itk (x,y,z)
    if Projection== "Sagital":
        id_axis = 2
        proj = np.zeros((MRI_vol.shape[0],MRI_vol.shape[1]))

    if Projection== "Transverse":
        id_axis = 0
        proj = np.zeros((MRI_vol.shape[1],MRI_vol.shape[2]))

    if Projection== "Coronal":
        id_axis = 1
        proj = np.zeros((MRI_vol.shape[0],MRI_vol.shape[2]))

    for i in range(proj.shape[0]):
            for j in range(proj.shape[1]):

                if Projection== "Sagital":
                    data_MRI = MRI_vol[i,j,:]
                    data_surface = brain_surface[i,j,:]
                    
                if Projection== "Transverse":
                    data_MRI = MRI_vol[:,i,j]
                    data_surface = brain_surface[:,i,j]


                if Projection== "Coronal":
                    data_MRI = MRI_vol[i,:,j]
                    data_surface = brain_surface[i,:,j]

                #Get idx of non zero elements
                non_zero_idx_surface = np.nonzero(data_surface)[0]

                if non_zero_idx_surface.size==0:
                    continue

                #Separate non_zero idx into contiguous arrays
                idx_split = np.split(non_zero_idx_surface, np.where(non_zero_idx_surface[1:] != non_zero_idx_surface[:-1] + 1)[0] + 1)
                
                #Handle the case where there is more than 2 non_zero arrays (case where a portion of the skin, liquid or skull is identified)
                id = id_proj
                idx = idx_split[id]
                
                proj[i,j] = np.max(data_MRI[idx])

    return proj


def create_MRI_projection_np(MRI_vol, brain_surface, tumor, Projection="Transverse", remove_artifacts=False, project_on_tumor = False):



    #Create projection (numpy: z,x,y) itk (x,y,z)
    if Projection== "Sagital":
        id_axis = 2
        proj = np.zeros((MRI_vol.shape[0],MRI_vol.shape[1]))

    if Projection== "Transverse":
        id_axis = 0
        proj = np.zeros((MRI_vol.shape[1],MRI_vol.shape[2]))

    if Projection== "Coronal":
        id_axis = 1
        proj = np.zeros((MRI_vol.shape[0],MRI_vol.shape[2]))



    mask_MRI = np.zeros(proj.shape,dtype=np.uint8)
    mask_tumor = np.zeros(proj.shape,dtype=np.uint8)


    #Get center of mass of the tumor and the location along the projection axis
    #Identify if the projection has to be done on the first or second projection plane
    center_of_mass_tumor = ndimage.center_of_mass(tumor)
    center_of_mass_brain = ndimage.center_of_mass(brain_surface)

    if project_on_tumor:
        if int(center_of_mass_tumor[id_axis])>tumor.shape[id_axis]/2:
        # if center_of_mass_tumor[id_axis]>center_of_mass_brain[id_axis]:
            id_proj = -1
        else:
            id_proj = 0
    else:
        id_proj = 0 


    for i in range(proj.shape[0]):
        for j in range(proj.shape[1]):

            if Projection== "Sagital":
                data_MRI = MRI_vol[i,j,:]
                data_surface = brain_surface[i,j,:]
                data_tumor = tumor[i,j,:]
                
            if Projection== "Transverse":
                data_MRI = MRI_vol[:,i,j]
                data_surface = brain_surface[:,i,j]
                data_tumor = tumor[:,i,j]


            if Projection== "Coronal":
                data_MRI = MRI_vol[i,:,j]
                data_surface = brain_surface[i,:,j]
                data_tumor = tumor[i,:,j]

            #Get idx of non zero elements
            non_zero_idx_surface = np.nonzero(data_surface)[0]

            if non_zero_idx_surface.size==0:
                continue


            mask_tumor[i,j] = np.max(data_tumor)
            
            
            #Separate non_zero idx into contiguous arrays
            idx_split = np.split(non_zero_idx_surface, np.where(non_zero_idx_surface[1:] != non_zero_idx_surface[:-1] + 1)[0] + 1)


            
            #Handle the case where there is more than 2 non_zero arrays (case where a portion of the skin, liquid or skull is identified)
            id = id_proj
            if remove_artifacts:
                if len(idx_split) > 2 : 
                    if id_proj == 0:
                        id +=1
                    else:
                        id -=1
            
            
            
            idx = idx_split[id]
            
            proj[i,j] = np.max(data_MRI[idx])




    #Apply closing to remove holes in projection
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(3,3))
    proj = cv.morphologyEx(proj, op=cv.MORPH_CLOSE, kernel=kernel)


    mask_MRI[proj>0] = 1


    return proj, mask_MRI, mask_tumor




def optics_to_MRI_slices_registration_multi_metric_multi_images(fixed_skeleton,
                                                                fixed_signed_distance,
                                                                moving_skeleton,
                                                                moving_signed_distance,
                                                                fixed_mask,
                                                                output_log_dir,
                                                                parameter_file,
                                                                output_filename="registration_out.txt",
                                                                log_to_console= False,):
    

    parameter_object = itk.ParameterObject.New()
    parameter_object.AddParameterFile(parameter_file)


    try:
        # Load Elastix Image Filter Object
        elastix_object = itk.ElastixRegistrationMethod.New(fixed_skeleton, moving_skeleton)
        elastix_object.SetFixedMask(fixed_mask)

        elastix_object.AddFixedImage(fixed_signed_distance)  # For the signed distance map
        elastix_object.AddMovingImage(moving_signed_distance)           

        elastix_object.SetParameterObject(parameter_object)

        # Set additional options
        elastix_object.SetLogToConsole(log_to_console)
        elastix_object.SetOutputDirectory(output_log_dir)
        elastix_object.SetLogFileName(output_filename)
        

        # Update filter object (required)
        elastix_object.UpdateLargestPossibleRegion()

        # Results of Registration
        img_registered = elastix_object.GetOutput()
        result_transform_parameters = elastix_object.GetTransformParameterObject()

    except RuntimeError:
        img_registered = None
        result_transform_parameters = None
 
    return img_registered, result_transform_parameters



def optics_to_MRI_slices_registration(fixed_img,
                                      moving_img,
                                      fixed_mask=None,
                                      output_log_dir="",
                                      output_filename="registration_out.txt",
                                      log_to_console= False):
    
    parameter_object = itk.ParameterObject.New()
    parameter_object.AddParameterFile('../data/parameters_Similarity_slice_fixed_rotation.txt')

    #Process registration
    try:
        img_registered, result_transform_parameters = itk.elastix_registration_method(
            fixed_img, moving_img,
            fixed_mask = fixed_mask,
            parameter_object=parameter_object,
            log_to_console=log_to_console,
            output_directory=output_log_dir,
            log_to_file=True,
            log_file_name=output_filename)
    except RuntimeError:
        img_registered = None
        result_transform_parameters = None

    return img_registered, result_transform_parameters




def MRI_volume_registration(fixed_img,
                            moving_img,
                            fixed_mask = None,
                            output_log_dir = "",
                            output_filename = "log_registration.txt",
                            log_to_console = False,
                            parameter_files=['../data/parameters_Affine.txt']):
    """
    Register moving img to fixed img (the transforms depend on the registratio type (affine, bspline)
    
    """
    parameter_object = itk.ParameterObject.New()
    
    for i in parameter_files:
        parameter_object.AddParameterFile(i)
       
        
    #Process registration
    img_registered, result_transform_parameters = itk.elastix_registration_method(
        fixed_img, moving_img,
        fixed_mask = fixed_mask,
        parameter_object=parameter_object,
        log_to_console=log_to_console,
        output_directory=output_log_dir,
        log_to_file=True,
        log_file_name=output_filename
        )
    
    return img_registered, result_transform_parameters
    


def euclidean_distance(pt1, pt2, reso_mm):
    return reso_mm*np.sqrt((pt2[1]-pt1[1])**2 + (pt2[0]-pt1[0])**2)


def get_max_size_mask_mm(mask, reso_mm):

    #Get min area rectangle around surgical window
    contours, hierarchy = cv.findContours(np.copy(mask), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    rect = cv.minAreaRect(contours[0])
    box = cv.boxPoints(rect)
    box = np.intp(box)

    #Get rect dimension in px

    max_size_surgical_window_mm = np.array([euclidean_distance(box[1],box[0],reso_mm), euclidean_distance(box[2],box[1],reso_mm)]).max()

    return max_size_surgical_window_mm

def get_final_registration_metrics(file, key):
    result = np.nan
    with open(file) as input_data:
        for line in input_data:
            if key in line:
                # print(line)
                split = line.split(' ')
                # print(split)
                result = float(split[-1])
                break
    return result

def apply_transform(moving_img, transform_params):
    """
    Appy rigid transform to moving img
    """
    
    # transform_params.SetParameter('affine')
    result_image_transformix = itk.transformix_filter(
        moving_img.astype(itk.F),  # transformix only works with float pixels
        transform_params,
        # reference image?
    )
    
    return result_image_transformix


def extract_brain(filename, use_bet, f_bet):
    
    #Get filenames of new files
    filename_no_extension = filename.split('.')[0]

    filename_mask = filename_no_extension+ '_bet_mask.nii.gz'
    filename_brain = filename_no_extension+ '_bet.nii.gz'

    if use_bet:
        args ='/home/caredda/fsl/bin/bet "'+filename+'" "'+filename_brain+'" -m -S -B -R -f ' +str(f_bet)
    else: # Use HD-bet
        args ='hd-bet -i '+filename
    
    call(args, shell=True)

    return filename_mask,filename_brain
    



    
def get_Surface_mask(filename, kernel_size = 10):

    #Get path from filename
    dirname = os.path.dirname(filename)

    #Load brain mask
    brain_mask = itk.imread(filename, itk.US)


    #Define kernel for erosion
    kernel = StructuringElement(kernelType='Ball', kernelSize=kernel_size, spatialDimension=3)

    #erosion
    eroded_mask = ErodeFilter(brain_mask,kernel)


    # Apply substraction
    mask_surface = SubtractFilter(brain_mask, eroded_mask)

    # Write surface mask
    itk.imwrite(mask_surface,dirname+'/surface_mask.nii.gz')
    # Write volume mask
    itk.imwrite(brain_mask,dirname+'/volume_mask.nii.gz')


    # #Define kernel for the dilatation
    # kernel = StructuringElement(kernelType='Ball', kernelSize=2, spatialDimension=3)
    
    # #Load brain mask
    # brain_mask = itk.imread(filename, itk.US)
    
    # #Dilate brain mask
    # brain_mask_dilate = DilateFilter(brain_mask, kernel)
    
    # #Define kernel for erosion
    # kernel = StructuringElement(kernelType='Ball', kernelSize=10, spatialDimension=3)
    
    # #erosion
    # eroded_mask = ErodeFilter(brain_mask_dilate,kernel)
    
    # # Apply substraction
    # mask_surface = SubtractFilter(brain_mask_dilate, eroded_mask)
    
    # # Write surface mask
    # itk.imwrite(mask_surface,dirname+'/surface_mask.nii.gz')
    # # Write volume mask
    # itk.imwrite(brain_mask_dilate,dirname+'/volume_mask.nii.gz')
        
        
  
def apply_brain_mask(filename,
                     filename_brain_mask,
                     output_name):
    #Load volumes
    vol = itk.imread(filename, itk.F)
    brain_mask = itk.imread(filename_brain_mask, itk.F)
        
    #Multiply filter
    vol = MultiplyFilter(vol,brain_mask)
    itk.imwrite(vol, output_name)

    return output_name
   

 

# Calculate the vector between two points in 3D space
def vector(point1, point2):
    """
    Return the vector defined by point2-point1

    """
    x = point2[0] - point1[0]
    y = point2[1] - point1[1]
    z = point2[2] - point1[2]
    return (x, y, z)


# Calculate an orthogonal basis for a given vector
def orthonormal_basis_from_Z_vector(V):


    """ Compute an orthonormal basis where V is the new z-axis. """
    # Normalize the vector V to get the new axis
    z_axis = V/np.linalg.norm(V)
    
    # Find an arbitrary vector that is not parallel to V
    if np.abs(z_axis[0]) < np.abs(z_axis[1]):
        arbitrary_vector = np.array([1, 0, 0])
    else:
        arbitrary_vector = np.array([0, 1, 0])
    
    # Compute the new x-axis using the cross product
    x_axis = np.cross(arbitrary_vector, z_axis)
    x_axis /= np.linalg.norm(x_axis)
    
    # Compute the new y-axis using the cross product of z_axis and x_axis
    y_axis = np.cross(z_axis, x_axis)
    
    # Form the orthonormal basis
    basis_np = np.stack((x_axis, y_axis, z_axis), axis=-1)
    basis_itk = np.stack((z_axis, x_axis, y_axis), axis=-1)
    
    return basis_np, basis_itk



def orthonormal_basis_from_X_vector(V):


    """ Compute an orthonormal basis where V is the new x-axis. """
    # Normalize the vector V to get the new axis
    x_axis = V/np.linalg.norm(V)
    
    # Find an arbitrary vector that is not parallel to V
    if np.abs(x_axis[0]) < np.abs(x_axis[1]):
        arbitrary_vector = np.array([0, 1, 0])
    else:
        arbitrary_vector = np.array([0, 0, 1])
    
    # Compute the new y-axis using the cross product
    y_axis = np.cross(arbitrary_vector, x_axis)
    y_axis /= np.linalg.norm(y_axis)
    
    # Compute the new z-axis using the cross product of x_axis and y_axis
    z_axis = np.cross(x_axis, y_axis)
    
    # Form the orthonormal basis
    basis_np = np.stack((x_axis, y_axis, z_axis), axis=-1)
    basis_itk = np.stack((z_axis, x_axis, y_axis), axis=-1)
    
    return basis_np, basis_itk



def orthonormal_basis_from_Y_vector(V):


    """ Compute an orthonormal basis where V is the new y-axis. """
    # Normalize the vector V to get the new axis
    y_axis = V/np.linalg.norm(V)
    
    # Find an arbitrary vector that is not parallel to V
    if np.abs(y_axis[0]) < np.abs(y_axis[1]):
        arbitrary_vector = np.array([1, 0, 0])
    else:
        arbitrary_vector = np.array([0, 0, 1])
    
    # Compute the new y-axis using the cross product
    x_axis = np.cross(arbitrary_vector, y_axis)
    x_axis /= np.linalg.norm(x_axis)
    
    # Compute the new z-axis using the cross product of x_axis and y_axis
    z_axis = np.cross(x_axis, y_axis)
    
    # Form the orthonormal basis
    basis_np = np.stack((x_axis, y_axis, z_axis), axis=-1)
    basis_itk = np.stack((z_axis, x_axis, y_axis), axis=-1)
    
    return basis_np, basis_itk




# Compute histogram normalization
def NormalizeHist(img,mask):
    # get coordinates of the surgical window
    coord = np.where(mask>0)


    v = img[coord]
    v_norm = (v - v.min())/(v.max()-v.min())

    normalized_img = np.zeros(img.shape)
    for i, C in enumerate(zip(coord[0], coord[1])):
        normalized_img[C[0], C[1]] = v_norm[i]

    return normalized_img



# Compute histogram equalization within the surgical window of RGB image
def EqualizeHist(img,mask):

    # get coordinates of the surgical window
    coord = np.where(mask>0)
    
    if img.ndim == 3:
        r = np.copy(img[:,:,0])
        g = np.copy(img[:,:,1])
        b = np.copy(img[:,:,2])
        r_pixels = r[coord]
        g_pixels = g[coord]
        b_pixels = b[coord]
        r_equalized_pixels = cv.equalizeHist(r_pixels)
        g_equalized_pixels = cv.equalizeHist(g_pixels)
        b_equalized_pixels = cv.equalizeHist(b_pixels)
        for i, C in enumerate(zip(coord[0], coord[1])):
            r[C[0], C[1]] = r_equalized_pixels[i][0]
            g[C[0], C[1]] = g_equalized_pixels[i][0]
            b[C[0], C[1]] = b_equalized_pixels[i][0]

        equalized_img = np.dstack([r,g,b])
        equalized_img = cv.cvtColor(equalized_img,cv.COLOR_BGR2GRAY)
    
    else:
        v = img[coord]
        v_equalized = cv.equalizeHist(v)
        equalized_img = np.zeros(img.shape)
        for i, C in enumerate(zip(coord[0], coord[1])):
            equalized_img[C[0], C[1]] = v_equalized[i][0]

    return equalized_img
   


def process_mesh(filename,nsub):
    #Loasd data
    data= nib.load(filename)
    np_data = data.get_fdata()

     
    # Segment the ROI
    segmented_data = np_data > 0.5  # Adjust threshold as necessary

    # Generate the mesh using marching cubes
    verts, faces, normals, values = measure.marching_cubes(segmented_data, level=0)

    # Convert faces to the format required by PyVista
    faces_formatted = np.hstack([[3] + list(face) for face in faces])

    # Create the PyVista mesh
    mesh = pv.PolyData(verts, faces_formatted)

    # Subdivide the mesh to increase resolution
    if nsub<=1:
        return mesh
   
    return mesh.subdivide(nsub=nsub)  # 'nsub' is the number of subdivisions




def get_id_kp_MRI_angle(filename):
    #Load metric
    angles = np.arange(0,360)
    output_metric = np.loadtxt(filename)

    #Get best match
    if (output_metric.ndim > 1):
        temp = np.array([])
        idx_min_per_init_point = []
        for i in range(output_metric.shape[0]):
            if np.all(np.isnan(output_metric[i,:])):
                idx_min_per_init_point.append(np.nan)
                temp = np.append(temp,np.nan)
                continue
            idx_min_per_init_point.append(np.nanargmin(output_metric[i,:]))
            temp = np.append(temp,np.nanmin(output_metric[i,:]))
            
        id_kp_MRI = np.nanargmin(temp)
        angle = angles[idx_min_per_init_point[id_kp_MRI]]

    else:
        id_kp_MRI = 0
        angle = np.nanargmin(output_metric)

    return angle, id_kp_MRI




def resize_Optics_image(filename_initial_img, itk_image, resolution, interpolation_type=cv.INTER_NEAREST):
    #Load images
    np_img = itk.GetArrayFromImage(itk_image)
    initial_img = cv.imread(filename_initial_img)

    #Get resize factor
    x_factor = itk_image.GetSpacing()[0]/resolution
    y_factor = itk_image.GetSpacing()[1]/resolution

    #resize np_img
    np_img = cv.resize(np_img,(initial_img.shape[1],initial_img.shape[0]),interpolation=interpolation_type)

    
    #Create itk image
    out_image = itk.GetImageFromArray(np.ascontiguousarray(np_img))
    out_image.SetSpacing([resolution,resolution])
    # out_image.SetOrigin([itk_image.GetOrigin()[0]*x_factor, itk_image.GetOrigin()[1]*y_factor])
    out_image.SetOrigin(itk_image.GetOrigin())
    return out_image

def interpolate_MRI_image(itk_image, resolution, interpolation_type=cv.INTER_NEAREST):
    np_img = itk.GetArrayFromImage(itk_image)

    x_factor = itk_image.GetSpacing()[0]/resolution
    y_factor = itk_image.GetSpacing()[1]/resolution

    #new size
    new_width = int(x_factor*np_img.shape[1])
    new_height = int(y_factor*np_img.shape[0])

    #interpolate image
    np_img = cv.resize(np_img, (new_width,new_height), interpolation=interpolation_type)

    #Create itk image
    out_image = itk.GetImageFromArray(np.ascontiguousarray(np_img))
    out_image.SetSpacing([resolution,resolution])
    # out_image.SetOrigin([itk_image.GetOrigin()[0]*x_factor, itk_image.GetOrigin()[1]*y_factor])
    out_image.SetOrigin(itk_image.GetOrigin())
    return out_image




def calculate_upscaled_Parameter_file(params_transform_reg, x_factor, y_factor):

    # Access ParameterMap 0
    parameter_map = params_transform_reg.GetParameterMap(0)

    # # Update the center of rotation
    # center_of_rotation = tuple(map(float, parameter_map["CenterOfRotationPoint"]))  # Convert tuple elements to float
    # center_of_rotation = (
    #     int(center_of_rotation[0]* x_factor),  # Scale x-coordinate
    #     int(center_of_rotation[1]* y_factor)   # Scale y-coordinate
    # )
    # parameter_map["CenterOfRotationPoint"] = tuple(map(str, center_of_rotation))  # Convert back to strings

    # # Update the translation
    # transform_parameters = list(map(float, parameter_map["TransformParameters"]))  # Convert to float
    # translation = transform_parameters[-2:]  # Last two values are the translation
    # translation[0] += x_factor/2
    # translation[1] += y_factor/2
    # transform_parameters[-2:] = translation
    # parameter_map["TransformParameters"] = tuple(map(str, transform_parameters))


    # Update the size
    Size = tuple(map(float, parameter_map["Size"]))  # Convert tuple elements to float
    Size = (
        int(Size[0]* x_factor),  # Scale x-coordinate
        int(Size[1]* y_factor)   # Scale y-coordinate
    )
    parameter_map["Size"] = tuple(map(str, Size))  # Convert back to strings

    # Update the Spacing
    Spacing = tuple(map(float, parameter_map["Spacing"]))  # Convert tuple elements to float
    Spacing = (
        Spacing[0]/ x_factor,  # Scale x-coordinate
        Spacing[1]/ y_factor   # Scale y-coordinate
    )
    parameter_map["Spacing"] = tuple(map(str, Spacing))  # Convert back to strings

    # Update the ParameterObject with the modified ParameterMap
    params_transform_reg.SetParameterMap(0, parameter_map)
    return params_transform_reg


def Project_Optical_img_on_MRI_projection(optical_img,
                                       optical_mask,
                                       angle,
                                       optical_spacing,
                                       res_mri_in_mm,
                                       res_opt_in_mm,
                                       kp_Optics,
                                       kp_MRI_phys, 
                                       params_transform_reg,
                                       use_upscaled_images):
    
    #Apply mask
    optical_img = optical_img*optical_mask

    #Adapt the resolution to MRI
    if not use_upscaled_images:
        sigma = int(res_mri_in_mm/res_opt_in_mm)+1
        optical_img = pyramid_reduce(optical_img, downscale=sigma)

    # Create itk image
    optics_vol = itk.GetImageFromArray(np.ascontiguousarray(optical_img))

    #If use upscaled image
    if use_upscaled_images:
        #Calculate scaling factors
        x_factor = optical_spacing[0]/res_opt_in_mm
        y_factor = optical_spacing[1]/res_opt_in_mm

        #Set optics resolution
        optics_vol.SetSpacing([res_opt_in_mm,res_opt_in_mm])
        
        #update kpt optics
        new_Kp_Optics = [int(kp_Optics[0]*x_factor),
                         int(kp_Optics[1]*y_factor)]
        
    else:
        optics_vol.SetSpacing(optical_spacing)

        new_Kp_Optics = [int(kp_Optics[0]),
                         int(kp_Optics[1])]

    #Apply rotation to the image
    np_rotated = Rotation_2D(angle, optics_vol, center = new_Kp_Optics)

    #Get new origin after rotation
    (h, w) = np_rotated.shape[:2]
    (cX, cY) = (w / 2, h / 2)

    #Should work for both cases (use_upscaled_images)
    # kp_Optics_phys = MRI_proj.TransformIndexToPhysicalPoint([int(cX), int(cY)])
    kp_Optics_phys = optics_vol.TransformIndexToPhysicalPoint([int(cX), int(cY)])

    #Write rotated image with correct origin
    rotated_optics = itk.GetImageFromArray(np.ascontiguousarray(np_rotated))
    rotated_optics.SetSpacing(optics_vol.GetSpacing())
    rotated_optics.SetDirection(optics_vol.GetDirection())
    rotated_optics.SetOrigin([kp_MRI_phys[0] - kp_Optics_phys[0], kp_MRI_phys[1] - kp_Optics_phys[1]])


    #Apply projection to optics vol
    optics_vol_registered = apply_transform(rotated_optics,params_transform_reg)

    return itk.GetArrayFromImage(optics_vol_registered)



def get_centered_uint_values(in_data,min,max):
    temp = np.zeros(in_data.shape)

    #Values >0 are normalized between 127-255
    if min != max:
        temp[in_data>0] = (in_data[in_data>0] *((255-127)/max)) + 127

        #Values <0 are normalized between 0-127
        temp[in_data<=0] = (in_data[in_data<=0] - min) *((127)/(-min))
    else:
        temp = (255*(in_data-in_data.min())/(in_data.max() - in_data.min()))

    temp[temp>255] = 255
    temp[temp<0] =0
    temp = temp.astype(np.uint8)

    return temp
