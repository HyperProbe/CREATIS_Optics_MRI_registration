import os
import matplotlib.pyplot as plt
import nibabel as nib
import glob
import shutil
import platform
import torch


from module.ITK import *


from brats import AdultGliomaSegmenter
from brats.utils.constants import AdultGliomaAlgorithms
from brats_toolkit.segmentor import Segmentor

from auxiliary.normalization.percentile_normalizer import PercentileNormalizer

from brainles_preprocessing.brain_extraction import HDBetExtractor
from brainles_preprocessing.modality import Modality
from brainles_preprocessing.preprocessor import Preprocessor

from module.utils import apply_brain_mask, apply_transform

os_type = platform.system()

from brainles_preprocessing.registration import NiftyRegRegistrator  # works only on linux
from brainles_preprocessing.registration import ANTsRegistrator  # for windows






def remove_temporary_files():

    # Define the pattern for the files you want to delete
    file_pattern = "brainles_preprocessing_*.log"

    # Find all files that match the pattern
    files_to_delete = glob.glob(file_pattern)

    # Delete each file that matches the pattern
    for file_path in files_to_delete:
        if os.path.isfile(file_path):  # Check if it's a file
            os.remove(file_path)

    # Deleting a folder and all its contents
    folder_path = 'temporary_directory'
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)


def visualize_data2(t1c, t1, t2, flair, height_p=0.5):  #
    """Visualize the MRI modalities. This function is different from "visualize_data" in the following ways:
        a) it expects the four file paths directly (no naming convention required)
        b) it does not take a slice index but a percentage height (e.g. 0.5 = 50% = middle slice) as imputs may have different dimensions

    Args:
        height_p (float, optional): the percentage of slicing height. 0.5 means 50% means exactly in the middle of the cuboid
        slice_index (int, optional): Slice to be visualized (first index in data of shape (155, 240, 240)). Defaults to 75.
    """
    _, axes = plt.subplots(1, 4, figsize=(12, 10))

    for i, (mod, modality_file) in enumerate(
        [("t1", t1), ("t1c", t1c), ("t2", t2), ("flair", flair)]
    ):

        data = nib.load(modality_file).get_fdata()
        # Get the middle slice along the specified axis
        slice_index = int(
            data.shape[2] * height_p
        )  # show slice that is exactly in the middle
        slice_data = data[:, ::-1, slice_index].T

        axes[i].set_title(mod)
        axes[i].imshow(slice_data, cmap="gray")
        axes[i].axis("off")


DATA_FOLDER = "data"


def visualize_data(data_folder: str = DATA_FOLDER, slice_index: int = 75):
    """Visualize the MRI modalities for a given slice index

    Args:
        data_folder (str, optional): Path to the folder containing the t1, t1c, t2 & flair file. Defaults to DATA_FOLDER.
        slice_index (int, optional): Slice to be visualized (first index in data of shape (155, 240, 240)). Defaults to 75.
    """
    _, axes = plt.subplots(1, 4, figsize=(12, 10))

    modalities = ["t1", "t1c", "t2", "flair"]
    for i, mod in enumerate(modalities):
        modality_file = os.path.join(data_folder, f"{mod}.nii.gz")
        modality_np = nib.load(modality_file).get_fdata().transpose(2, 1, 0)
        axes[i].set_title(mod)
        axes[i].imshow(modality_np[slice_index, :, :], cmap="gray")
        axes[i].axis("off")


def visualize_segmentation(modality_file: str, segmentation_file: str, slice_p=0.5):
    """Visualize the MRI modality and the segmentation

    Args:
        modality_file (str): Path to the desired modality file
        segmentation_file (str): Path to the segmentation file
    """
    modality_np = nib.load(modality_file).get_fdata().transpose(2, 1, 0)
    seg_np = nib.load(segmentation_file).get_fdata().transpose(2, 1, 0)
    _, ax = plt.subplots(1, 2, figsize=(8, 4))

    slice_index = int(modality_np.shape[0] * slice_p)  # You can choose any slice here
    ax[0].imshow(modality_np[slice_index, :, :], cmap="gray")
    ax[1].imshow(modality_np[slice_index, :, :], cmap="gray")
    ax[1].imshow(seg_np[slice_index, :, :], cmap="plasma", alpha=0.5)
    for ax in ax:
        ax.axis("off")
    plt.tight_layout()





def preprocess_exam_in_brats_style_ITK(filename_t1, filename_flair, filename_t1_bet, filename_mask_brain, output_dir):


    #Load files
    T1_volume = itk.imread(filename_t1,itk.F)
    FLAIR_volume = itk.imread(filename_flair,itk.F)


    #Register FLAIR To T1 volume
    parameter_object = itk.ParameterObject.New()
    parameter_object.AddParameterFile('../data/parameters_Rigid.txt')



    FLAIR_registered, params_transform = itk.elastix_registration_method(
        T1_volume, FLAIR_volume,
        parameter_object=parameter_object,
        log_to_console=False,
        output_directory=output_dir,
        log_to_file=True
        )


    FLAIR_registered = thresholdBelowImageFilter(FLAIR_registered,0.5,0)


    # Resample Volume fMRI to match T1
    resample_filter = itk.ResampleImageFilter.New(Input=FLAIR_registered,
                                                    ReferenceImage=T1_volume,
                                                    UseReferenceImage=True)
        
    FLAIR_registered = resample_filter.GetOutput()

    filename_flair = output_dir+"r_FLAIR.nii"
    itk.imwrite(FLAIR_registered,filename_flair)


    #Apply brain mask to FLAIR
    filename_flair = apply_brain_mask(filename_flair,filename_mask_brain, output_dir + "r_FLAIR_bet.nii.gz")















    # Register on atlas
    atlas_volume = itk.imread("../data/atlas/t1_skullstripped_brats_space.nii",itk.F)
    FLAIR_volume = itk.imread(output_dir + "r_FLAIR_bet.nii.gz",itk.F)
    T1_volume = itk.imread(filename_t1_bet,itk.F)

    #Register T1 To atlas volume
    T1_registered, params_transform = itk.elastix_registration_method(
        atlas_volume, T1_volume,
        parameter_object=parameter_object,
        log_to_console=False,
        output_directory=output_dir,
        log_to_file=True
        )
    
    T1_registered = thresholdBelowImageFilter(T1_registered,0.5,0)
    resample_filter = itk.ResampleImageFilter.New(Input=T1_registered,
                                                    ReferenceImage=atlas_volume,
                                                    UseReferenceImage=True)
    T1_registered = resample_filter.GetOutput()

    filename_t1 = output_dir+"r_T1_bet_atlas.nii.gz"
    itk.imwrite(T1_registered,filename_t1)      
    
    #Apply transform to FLAIR
    FLAIR_registered = apply_transform(FLAIR_volume,params_transform)
    FLAIR_registered = thresholdBelowImageFilter(FLAIR_registered,0.5,0)
    resample_filter = itk.ResampleImageFilter.New(Input=FLAIR_registered,
                                                    ReferenceImage=atlas_volume,
                                                    UseReferenceImage=True)
    FLAIR_registered = resample_filter.GetOutput()

    filename_flair = output_dir+"r_FLAIR_bet_atlas.nii.gz"
    itk.imwrite(FLAIR_registered,filename_flair)



    return params_transform

 


def register_tumor_segmentation_to_T1_space(output_dir,
                                            filename_t1_bet,
                                            filename_tumor,
                                            param_transform_atlas):
    
    Tumor_vol_atlas_space = itk.imread(filename_tumor, itk.UC)
    T1_vol = itk.imread(filename_t1_bet, itk.F)


    # print(param_transform_atlas)

    # Get the first (rigid) transform parameter map
    euler_transform = itk.Euler3DTransform[itk.D].New()
    original_map = param_transform_atlas.GetParameterMap(0)



    center = [float(p) for p in original_map['CenterOfRotationPoint']]
    fixed_parameters = itk.OptimizerParameters[itk.D](len(center))
    for i, p in enumerate(center):
        fixed_parameters[i] = p
    euler_transform.SetFixedParameters(fixed_parameters)



    elx_parameters = [float(p) for p in original_map['TransformParameters']]
    itk_parameters = itk.OptimizerParameters[itk.D](len(elx_parameters))
    for i, p in enumerate(elx_parameters):
        itk_parameters[i] = p

    euler_transform.SetParameters(itk_parameters)

    # Calculate inverse transform
    inverse_transform = euler_transform.GetInverseTransform()


    composite_transform = itk.CompositeTransform[itk.D, 3].New()
    composite_transform.AddTransform(inverse_transform)

    inverse_registered = itk.resample_image_filter(Tumor_vol_atlas_space,
                                                    transform=composite_transform,
                                                    use_reference_image=True,
                                                    reference_image=T1_vol)
                                                    



    itk.imwrite(inverse_registered, output_dir+"r_tumor_mask.nii.gz")





def preprocess_exam_in_brats_style(t1, flair) -> None:
    """
    Perform BRATS (Brain Tumor Segmentation) style preprocessing on MRI exam data.

    Args:
        t1 (str): Path to T1 file
        flair (str): Path to the FLAIR file
    Raises:
        Exception: If any error occurs during the preprocessing.


    This function preprocesses MRI exam data following the BRATS style, which includes the following steps:
    1. Normalization using a percentile normalizer.
    2. Registration and correction using NiftyReg.
    3. Brain extraction using HDBet.

    The processed data is saved in a structured directory within the input directory.

    Args:
        inputDir (str): Path to the directory containing raw MRI files for an exam.

    Returns:
        None
    """
    print("*** start ***")
    dir_name = os.path.dirname(t1)

    #Create output directory
    output_dir = dir_name+"/data_BRATS/"
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    # normalizer
    percentile_normalizer = PercentileNormalizer(
        lower_percentile=0.1,
        upper_percentile=99.9,
        lower_limit=0,
        upper_limit=1,
    )

    # define modalities
    center = Modality(
        modality_name="t1",
        input_path=t1,
        raw_bet_output_path=output_dir + "t1_bet.nii.gz",
        atlas_correction=True,
        normalizer=percentile_normalizer,
    )

    moving_modalities = [
        Modality(
            modality_name="flair",
            input_path=flair,
            raw_bet_output_path=output_dir + "fla_bet.nii.gz",
            atlas_correction=True,
            normalizer=percentile_normalizer,
        ),
    ]

    if os_type == "Linux":
        registrator=NiftyRegRegistrator()
    else:
        registrator=ANTsRegistrator()


    preprocessor = Preprocessor(
        center_modality=center,
        moving_modalities=moving_modalities,
        registrator=registrator,
        brain_extractor=HDBetExtractor(),
        temp_folder="temporary_directory",
        limit_cuda_visible_devices="0",
    )
    preprocessor.run()






def process_Tumor_segmentation(T1_filename, T1_filename_bet, FLAIR_filename):


    #Free GPU cache
    torch.cuda.empty_cache()

    print("[process_Tumor_segmentation] BRATS preprocessing")
    #Apply preprocess (coregistration, brain extraction, registration on BRATS atlas)
    preprocess_exam_in_brats_style( t1 = T1_filename,
                                    flair = FLAIR_filename)
    

    #Free GPU cache
    torch.cuda.empty_cache()

    # Delete temporary folder and log
    remove_temporary_files()

    #Get brats filename
    data_path = os.path.dirname(T1_filename)+"/data_BRATS/"
    print("[process_Tumor_segmentation] BRATS segmentation")

    #Process tumor segmentation
    segmenter = AdultGliomaSegmenter()
    segmenter.infer_single(
        t1c = data_path+"t1_bet.nii.gz",
        t1n = data_path+"t1_bet.nii.gz",
        t2f = data_path+"fla_bet.nii.gz",
        t2w = data_path+"fla_bet.nii.gz",
        output_file=data_path+"segmentation.nii.gz",
        log_file = data_path+"log.txt"
    )

    print("[process_Tumor_segmentation] Registration back to T1 space")

    # Extracted brain (T1) in BRATS space
    filename_T1_BRATS = data_path+"t1_bet.nii.gz"
    # Tumor segmentation volume in BRATS space
    filename_tumor_segmentation_BRATS = data_path+"segmentation.nii.gz"


    #Load volumes
    moving_volume= itk.imread(filename_T1_BRATS,itk.F)
    fixed_volume = itk.imread(T1_filename_bet, itk.F)
    overlay= itk.imread(filename_tumor_segmentation_BRATS, itk.F)




    #Register fMRI To T1 volume
    # parameter_object = itk.ParameterObject.New()
    # reg_param_file = "../data/parameters_Affine.txt"
    # parameter_object.AddParameterFile(reg_param_file)

    #Register fMRI To T1 volume
    parameter_object = itk.ParameterObject.New()
    parameter_object.AddParameterFile('../data/parameters_Affine.txt')



    vol_registered, result_transform_parameters = itk.elastix_registration_method(
        fixed_volume, moving_volume,
        parameter_object=parameter_object,
        log_to_console=False,
        output_directory=data_path,
        log_to_file=True
        )

    

    print("[process_Tumor_segmentation] Apply transform to segmentation")

    #Apply transform
    overlay = itk.transformix_filter(
        overlay.astype(itk.F), result_transform_parameters)

    #Threshold output
    overlay = thresholdBelowImageFilter(overlay,0.5,0)

    # Save registered overlay
    file = data_path+"segmentation_T1_space.nii.gz"
    itk.imwrite(overlay, file)

    return file