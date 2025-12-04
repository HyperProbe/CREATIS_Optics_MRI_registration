from module.utils import *
from module.utils_BRATS import *

from skimage.transform import resize

import json


class Registration_Params:
    def __init__(self, angle =-1, MRI_kpt=-1,  MRI_kpt_phys=-1,
                 Optics_kpt=-1,  Optics_kpt_phys=-1, registration_metric = 0):
        self.angle = angle
        self.MRI_kpt = MRI_kpt
        self.MRI_kpt_phys = MRI_kpt_phys
        self.Optics_kpt = Optics_kpt
        self.Optics_kpt_phys = Optics_kpt_phys
        self.registration_metric = registration_metric
        
    
    def save(self, filepath):
        """Save parameters to a JSON file"""
        with open(filepath, 'w') as f:
            json.dump(self.__dict__, f, indent=4)

    @classmethod
    def load(cls, filepath):
        """Load parameters from a JSON file and return a Params object"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        return cls(**data)

class Params:
    def __init__(self, thresh_MRI=5, sigma_minimum_mm_MRI=0,
                 sigma_maximum_mm_MRI=1,
                 thresh_optics=100, sigma_minimum_mm_optics=3, sigma_maximum_mm_optics=3,
                 ksize_mm_kernal_specular_reflection_optics = 2, kernel_mm_optical_mask_erosion = 0.5,
                 number_of_sigma_steps=5,
                 k_dilatation_brain=5, projection_type="Transverse",
                 touch_vessel=False, use_bet=False, f_bet=0.65,
                 MRI_keypoints_nb = 5,
                 kpts_MRI_tumor = None, kpt_optics = None, registration_type = "Skeleton",
                 use_upscaled_images = False, register_fMRI_to_T1 = True, optics_skeleton_apriori = None,
                 MRI_skeleton_apriori=None, use_top_slice_for_projection= True, projection_base_axis = "Y axis",
                 axis_projection = "Origin MRI", mask_MRI_hemisphere=True, MRI_erode_edge_mm = 40,
                 use_custom_registration_metric = True, alpha_custom_metric = 100,
                 space_between_kpt_mm = 8, tumor_ROI_enlarge_factor = 2, Optical_downsampling_factor = 1):

        #bet params
        self.use_bet = use_bet
        self.f_bet = f_bet

        #projection
        self.projection_type = projection_type
        self.use_top_slice_for_projection = use_top_slice_for_projection
        self.projection_base_axis = projection_base_axis
        self.axis_projection = axis_projection
        self.mask_MRI_hemisphere = mask_MRI_hemisphere


        #Registration
        self.register_fMRI_to_T1 = register_fMRI_to_T1
        self.use_custom_registration_metric = use_custom_registration_metric
        self.MRI_keypoints_nb = MRI_keypoints_nb
        self.alpha_custom_metric = alpha_custom_metric

        #Cortex max param
        self.k_dilatation_brain = k_dilatation_brain #Nb of voxel for getting surface blood vessels

        #MRI params for vessel extraction
        self.thresh_MRI = thresh_MRI
        self.sigma_minimum_mm_MRI = sigma_minimum_mm_MRI
        self.sigma_maximum_mm_MRI = sigma_maximum_mm_MRI
        self.MRI_erode_edge_mm = MRI_erode_edge_mm

        #Optics params for vessel extraction
        self.thresh_optics =  thresh_optics
        self.sigma_minimum_mm_optics = sigma_minimum_mm_optics
        self.sigma_maximum_mm_optics = sigma_maximum_mm_optics
        self.ksize_mm_kernal_specular_reflection_optics = ksize_mm_kernal_specular_reflection_optics
        self.kernel_mm_optical_mask_erosion = kernel_mm_optical_mask_erosion
        self.Optical_downsampling_factor = Optical_downsampling_factor

        #Frangi params
        self.number_of_sigma_steps = number_of_sigma_steps #nb of scales for frangi
        
    
        #Skeleton matching
        self.optics_skeleton_apriori = optics_skeleton_apriori
        self.MRI_skeleton_apriori = MRI_skeleton_apriori
        self.touch_vessel = touch_vessel

        #Keypoints init
        self.kpts_MRI_tumor = kpts_MRI_tumor
        self.kpt_optics = kpt_optics
        self.space_between_kpt_mm = space_between_kpt_mm
        self.tumor_ROI_enlarge_factor = tumor_ROI_enlarge_factor

        #registation
        self.registration_type = registration_type #Calculate mutli metric/image registration

        self.use_upscaled_images = use_upscaled_images




    def save(self, filepath):
        #force skeleton aprori to be None
        self.optics_skeleton_apriori = None
        self.MRI_skeleton_apriori = None

        """Save parameters to a JSON file"""
        with open(filepath, 'w') as f:
            json.dump(self.__dict__, f, indent=4)

    @classmethod
    def load(cls, filepath):
        """Load parameters from a JSON file and return a Params object"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        return cls(**data)



class Paths:
    def __init__(self, main_path="", RGB_optics=True):

        self.main_path = ""
        self.main_path_optics =""

        self.output_dir = ""
        self.output_registration_dir = ""
        self.output_MRI_projection_dir = ""
        self.output_BV_segmentation_dir = ""
        self.output_tumor_segmentation_dir = ""

        
        self.set_main_path(main_path)

        self.set_Optics_path(RGB_optics)
               


    def set_main_path(self,main_path=""):

        self.main_path = main_path

        if main_path=="":
            return
        
        # Saving directory
        self.output_dir = main_path +  "/results/"
        if not os.path.exists(self.output_dir):
            os.mkdir(self.output_dir)

        #Registration
        self.output_registration_dir = self.output_dir+"Registration/"
        if not os.path.exists(self.output_registration_dir):
            os.mkdir(self.output_registration_dir)

        #MRI projection
        self.output_MRI_projection_dir = self.output_dir+"MRI_projection/"
        if not os.path.exists(self.output_MRI_projection_dir):
            os.mkdir(self.output_MRI_projection_dir)

        #Blood vessel segmentation
        self.output_BV_segmentation_dir = self.output_dir+"Blood_vessel_segmentation/"
        if not os.path.exists(self.output_BV_segmentation_dir):
            os.mkdir(self.output_BV_segmentation_dir)


        #Blood vessel segmentation
        self.output_tumor_segmentation_dir = self.output_dir+"Tumor_segmentation/"
        if not os.path.exists(self.output_tumor_segmentation_dir):
            os.mkdir(self.output_tumor_segmentation_dir)

    def set_Optics_path(self,RGB_optics=True):
        if self.main_path =="":
            return
    
        if RGB_optics:
            self.main_path_optics = self.main_path + "/optics/" # RGB
        else:
            self.main_path_optics = self.main_path + "/optics_HSI/" # HSI





def main_extract_brain(Mypath = Paths(), params=Params()):


    main_path_MRI = Mypath.main_path + "/MRI/"
    output_dir = Mypath.output_dir

    #P66 (problem with Bet and HD bet)
    #P54
    # use_bet = True

    filename_t1 = main_path_MRI+"T1.nii"

    if not os.path.exists(filename_t1):
        return "T1 file is missing"

    ## 2) Extract brain using HD-bet
    filename_mask_brain, f = extract_brain(filename_t1, params.use_bet, params.f_bet)
    shutil.copy(filename_mask_brain, output_dir + os.path.basename(filename_mask_brain).split('.')[0]+"_no_dilatation.nii.gz")


    # #Dilate surface mask to get surface vessels
    # if params.k_dilatation_brain >0:
    #     kernel = StructuringElement(kernelType='Ball', kernelSize=params.k_dilatation_brain, spatialDimension=3)
    #     brain_mask = itk.imread(filename_mask_brain,itk.US)
    #     brain_mask = DilateFilter(brain_mask, kernel)
    #     itk.imwrite(brain_mask,filename_mask_brain)

    # #Appy mask on T1
    # filename_t1 = apply_brain_mask(filename_t1,filename_mask_brain, output_dir + "r_T1_bet.nii.gz")

    # ## 3) Compute the mask of brain surface
    # get_Surface_mask(filename_mask_brain)


    # # move file into results folder
    # os.rename(main_path_MRI+"surface_mask.nii.gz", output_dir+"surface_mask.nii.gz")
    # os.rename(main_path_MRI+"volume_mask.nii.gz", output_dir+"volume_mask.nii.gz")

    return "Success"



def main_get_surface_mask(Mypath = Paths(),params=Params()):
    
    main_path = Mypath.main_path
    output_dir = Mypath.output_dir

    main_path_MRI = main_path + "/MRI/"

    filename_t1 = main_path_MRI+"T1.nii"
    filename_mask_brain = filename_t1.split('.')[0]+ '_bet_mask.nii.gz'

    if not os.path.exists(filename_t1):
        return "T1 file is missing"
    
    if not os.path.exists(filename_mask_brain):
        return "Brain mask is missing"
    
    #Dilate surface mask to get surface vessels
    if params.k_dilatation_brain >0:
        kernel = StructuringElement(kernelType='Ball', kernelSize=params.k_dilatation_brain, spatialDimension=3)
        brain_mask = itk.imread(filename_mask_brain,itk.US)
        brain_mask = DilateFilter(brain_mask, kernel)
        itk.imwrite(brain_mask,filename_mask_brain)

    #Appy mask on T1
    filename_t1 = apply_brain_mask(filename_t1,filename_mask_brain, output_dir + "r_T1_bet.nii.gz")

    ## 3) Compute the mask of brain surface
    get_Surface_mask(filename_mask_brain)


    # move file into results folder
    os.rename(main_path_MRI+"surface_mask.nii.gz", output_dir+"surface_mask.nii.gz")
    os.rename(main_path_MRI+"volume_mask.nii.gz", output_dir+"volume_mask.nii.gz")


    

    return "Success"





def main_plot_extracted_brain(Mypath = Paths()):
    output_dir = Mypath.output_dir
    #################
    # Load mri volume
    #################

    filename_t1 = output_dir + "r_T1_bet.nii.gz"
    filename_surface_mask = output_dir+'surface_mask.nii.gz'

    if not os.path.exists(filename_t1):
        return "T1 file is missing",None

    if not os.path.exists(filename_surface_mask):
        return "Surface mask file is missing",None


    # Load MRI data
    T1 = itk.imread(filename_t1, itk.F)
    surface = itk.imread(filename_surface_mask, itk.F)

    # Get numpy arrays
    np_T1 = itk.GetArrayFromImage(T1)
    np_surface = itk.GetArrayFromImage(surface)

    
    proj1 = create_simple_MRI_projection(np_T1,np_surface,"Sagital",0)
    proj2 = create_simple_MRI_projection(np_T1,np_surface,"Sagital",-1)

    proj1 = cv.flip(proj1,0)
    proj2 = cv.flip(proj2,0)
    proj2 = cv.flip(proj2,1)

    

    display = np.zeros((proj1.shape[0],proj1.shape[1]+proj2.shape[1]))

    display[:,0:proj1.shape[1]] = proj1
    display[:,proj1.shape[1]:] = proj2

    return "Success",display


def main_get_tumor_segmentation(Mypath = Paths()):

    main_path = Mypath.main_path
    output_dir = Mypath.output_dir
    tumor_segmentation_dir = Mypath.output_tumor_segmentation_dir

    main_path_MRI = main_path + "/MRI/"

    filename_t1 = main_path_MRI+"T1.nii"
    filename_t1_bet = output_dir+"r_T1_bet.nii.gz"
    filename_flair = main_path_MRI+"FLAIR.nii"

    filename_mask_brain = output_dir+"volume_mask.nii.gz"

    if not os.path.exists(filename_t1):
        return "[main_get_tumor_segmentation] T1 file is missing"

    if not os.path.exists(filename_flair):
        return "[main_get_tumor_segmentation] Flair file is missing"
    
    if not os.path.exists(filename_mask_brain):
        return "[main_get_tumor_segmentation] Brain mask is missing"
    


    #Preprocess data in BRATS space
    param_transform_atlas = preprocess_exam_in_brats_style_ITK(filename_t1, filename_flair, filename_t1_bet, filename_mask_brain, tumor_segmentation_dir)

    #Free GPU cache
    torch.cuda.empty_cache()


    #Process tumor segmentation
    segmenter = AdultGliomaSegmenter()
    segmenter.infer_single(
        t1c = tumor_segmentation_dir+"r_T1_bet_atlas.nii.gz",
        t1n = tumor_segmentation_dir+"r_T1_bet_atlas.nii.gz",
        t2f = tumor_segmentation_dir+"r_FLAIR_bet_atlas.nii.gz",
        t2w = tumor_segmentation_dir+"r_FLAIR_bet_atlas.nii.gz",
        output_file=tumor_segmentation_dir+"segmentation_atlas_space.nii.gz",
        log_file = tumor_segmentation_dir+"log.txt"
    )


    # Registration back to T1 space"
    filename_tumor = tumor_segmentation_dir+ "segmentation_atlas_space.nii.gz"

    register_tumor_segmentation_to_T1_space(tumor_segmentation_dir, filename_t1_bet, filename_tumor, param_transform_atlas)
        

    return "Success"


def main_get_tumor_segmentation_old(Mypath = Paths()):

    main_path = Mypath.main_path
    output_dir = Mypath.output_dir

    main_path_MRI = main_path + "/MRI/"

    filename_t1 = main_path_MRI+"T1.nii"
    filename_t1_bet = output_dir+"r_T1_bet.nii.gz"
    filename_flair = main_path_MRI+"FLAIR.nii"

    if not os.path.exists(filename_t1):
        return "T1 file is missing"

    if not os.path.exists(filename_flair):
        return "Flair file is missing"
    
    # if not os.path.exists("../data/parameters_Affine.txt"):
    #     return "Affine registration parameter file is missing"

    # Process tumor segmentation using BRATS
    filename_tumor_segmentation_T1_space = process_Tumor_segmentation(filename_t1, filename_t1_bet, filename_flair)

    # move file into results folder
    # os.rename(main_path_MRI+"data_BRATS/segmentation_T1_space.nii.gz",
    #         output_dir+"r_tumor_mask.nii.gz")

    os.rename(filename_tumor_segmentation_T1_space,
              output_dir+"r_tumor_mask.nii.gz")
    
    return "Success"







def main_register_fMRI_to_T1(Mypath = Paths(), params=Params()):
    

    main_path = Mypath.main_path
    output_dir = Mypath.output_dir

    main_path_MRI = main_path + "/MRI/"
    main_path_fMRI = main_path+ "/MRI/fMRI/"

    
    filename_t1 = main_path_MRI+"T1.nii"
    filename_fMRI = main_path_fMRI+"fMRI.nii"
    filename_fMRI_stats = glob.glob(main_path_fMRI + "inferences/*")


    if not os.path.exists(filename_t1):
        return "T1 file is missing"

    if not os.path.exists(filename_fMRI):
        return "fMRI file is missing"

    if len(filename_fMRI_stats)==0:
        return "fMRI stats file is missing"


    #Create output fMRI folder
    output_fMRI = output_dir+"fMRI/"
    if not os.path.exists(output_fMRI):
        os.mkdir(output_fMRI)
    if not os.path.exists(output_fMRI+"inferences/"):
        os.mkdir(output_fMRI+"inferences/")


    #Load files
    T1_volume = itk.imread(filename_t1,itk.F)
    fMRI_volume = itk.imread(filename_fMRI,itk.F)



    if params.register_fMRI_to_T1:
        #Register fMRI To T1 volume
        # parameter_object = itk.ParameterObject.New()
        # parameter_map_rigid = parameter_object.GetDefaultParameterMap('rigid')
        # parameter_object.AddParameterMap(parameter_map_rigid)

        # fMRI_registered, params_transform = itk.elastix_registration_method(
        #     T1_volume, fMRI_volume,
        #     parameter_object=parameter_object,
        #     log_to_console=False,
        #     output_directory=output_fMRI,
        #     log_to_file=True
        #     )

        # # Save volume
        # fMRI_registered = itk.imread(output_fMRI+"result.0.nii",itk.F)


        #Register fMRI To T1 volume
        parameter_object = itk.ParameterObject.New()
        parameter_object.AddParameterFile('../data/parameters_Rigid.txt')



        fMRI_registered, params_transform = itk.elastix_registration_method(
            T1_volume, fMRI_volume,
            parameter_object=parameter_object,
            log_to_console=False,
            output_directory=output_fMRI,
            log_to_file=True
            )


        fMRI_registered = thresholdBelowImageFilter(fMRI_registered,0.5,0)


        # Resample Volume fMRI to match T1
        resample_filter = itk.ResampleImageFilter.New(Input=fMRI_registered,
                                                      ReferenceImage=T1_volume,
                                                      UseReferenceImage=True)
    
        fMRI_registered = resample_filter.GetOutput()



        filename_fMRI = output_fMRI+"r_fMRI.nii"
        itk.imwrite(fMRI_registered,filename_fMRI)



        # Apply transform to fMRI inferences
        for file in filename_fMRI_stats:

            fMRI_stats = itk.imread(file,itk.F)

            fMRI_stats_volume_registered = apply_transform(fMRI_stats,params_transform)

            #Threshold the binary mask after registration
            fMRI_stats_volume_registered = thresholdBelowImageFilter(fMRI_stats_volume_registered,0.5,0)



            # Resample Volume fMRI to match T1
            resample_filter = itk.ResampleImageFilter.New(Input=fMRI_stats_volume_registered,
                                                          ReferenceImage=T1_volume, 
                                                          UseReferenceImage=True)
            fMRI_stats_volume_registered = resample_filter.GetOutput()


            # Save registered volume
            out_filename = output_fMRI+"inferences/r_"+ os.path.basename(file)
            itk.imwrite(fMRI_stats_volume_registered, out_filename)

    else:
        # shutil.copy(filename_fMRI, output_fMRI+"r_fMRI.nii")
        # for file in filename_fMRI_stats:
        #     shutil.copy(file, output_fMRI+"inferences/r_"+os.path.basename(file))


        # Resample Volume fMRI to match T1
        resample_filter = itk.ResampleImageFilter.New(Input=fMRI_volume,
                                                      ReferenceImage=T1_volume,
                                                      UseReferenceImage=True)
    
        fMRI_volume = resample_filter.GetOutput()

        filename_fMRI = output_fMRI+"r_fMRI.nii"
        itk.imwrite(fMRI_volume,filename_fMRI)



        # Apply transform to fMRI inferences
        for file in filename_fMRI_stats:

            fMRI_stats = itk.imread(file,itk.F)

            #Threshold the binary mask after registration
            fMRI_stats = thresholdBelowImageFilter(fMRI_stats,0.5,0)



            # Resample Volume fMRI to match T1
            resample_filter = itk.ResampleImageFilter.New(Input=fMRI_stats,
                                                          ReferenceImage=T1_volume, 
                                                          UseReferenceImage=True)
            fMRI_stats = resample_filter.GetOutput()


            # Save registered volume
            out_filename = output_fMRI+"inferences/r_"+ os.path.basename(file)
            itk.imwrite(fMRI_stats, out_filename)


    return "Success"


def main_plot_fMRI_T1_registration(Mypath = Paths()):
    
    output_dir = Mypath.output_dir


    filename_t1 = Mypath.main_path + "/MRI/T1.nii"
    filename_fMRI = output_dir+"fMRI/r_fMRI.nii"


    if not os.path.exists(filename_t1):
        return "[main_plot_fMRI_T1_registration] T1 file is missing",None,None

    if not os.path.exists(filename_fMRI):
        return "fMRI file is missing",None,None
    

    # Load MRI volumes
    volume_T1 = itk.imread(filename_t1)  # Reference (Fixed Image)
    volume_fMRI = itk.imread(filename_fMRI)  # Registered (Moving Image)

    if(itk.size(volume_T1) != itk.size(volume_fMRI)):
    
        # Resample Volume B to match Volume A
        resample_filter = itk.ResampleImageFilter.New(
            Input=volume_fMRI,
            ReferenceImage=volume_T1,  # Match shape, spacing, origin
            UseReferenceImage=True
        )
        volume_fMRI = resample_filter.GetOutput()


    # Convert to NumPy arrays
    array_T1 = itk.array_from_image(volume_T1)
    array_fMRI = itk.array_from_image(volume_fMRI)


    # Transverse slice (middle slice)
    slice_index = array_T1.shape[0] // 2
    slice_T1_transverse = array_T1[slice_index, :, :]
    slice_fMRI_transverse = array_fMRI[slice_index, :, :]  # Resampled to same shape

    #Sagital slice
    slice_index = array_T1.shape[1] // 2
    slice_T1_sagital = array_T1[:, slice_index, :]
    slice_fMRI_sagital = array_fMRI[:, slice_index, :]  # Resampled to same shape


    #Coronal slice
    slice_index = array_T1.shape[2] // 2
    slice_T1_coronal = array_T1[:, :, slice_index]
    slice_fMRI_coronal = array_fMRI[:, :, slice_index]  # Resampled to same shape


    max_rows = np.max(np.array([slice_T1_transverse.shape[0],
                               slice_T1_sagital.shape[0],
                               slice_T1_coronal.shape[0]]))
    max_cols = np.max(np.array([slice_T1_transverse.shape[1],
                               slice_T1_sagital.shape[1],
                               slice_T1_coronal.shape[1]]))
    
    print(max_rows,max_cols)
    #Resise and combine final images
    slice_T1 = np.zeros((max_rows,3*max_cols))
    slice_fMRI = np.zeros((max_rows,3*max_cols))


    slice_T1[:,0:max_cols] = cv.resize(slice_T1_transverse, (max_cols,max_rows))
    slice_T1[:,max_cols:2*max_cols] = cv.resize(slice_T1_sagital, (max_cols,max_rows))
    slice_T1[:,2*max_cols:] = cv.resize(slice_T1_coronal, (max_cols,max_rows))
    
    slice_fMRI[:,0:max_cols] = cv.resize(slice_fMRI_transverse, (max_cols,max_rows))
    slice_fMRI[:,max_cols:2*max_cols] = cv.resize(slice_fMRI_sagital, (max_cols,max_rows))
    slice_fMRI[:,2*max_cols:] = cv.resize(slice_fMRI_coronal, (max_cols,max_rows))
    

    #Vertical flip
    slice_T1 = cv.flip(slice_T1,0)
    slice_fMRI = cv.flip(slice_fMRI,0)


    return "Success",slice_T1,slice_fMRI


def main_load_MRI_projection(Mypath = Paths()):
    output_dir = Mypath.output_MRI_projection_dir

    if not os.path.exists(output_dir+"Proj_MRI.nii.gz"):
        return "[main_load_MRI_projection] projection file is missing", None

    itk_img = itk.imread(output_dir+"Proj_MRI.nii.gz")
    np_img = itk.GetArrayFromImage(itk_img)

    return "Success", np_img





def get_MRI_mask_around_tumor(Mypath = Paths(), params = Params()):
    main_path_otpics = Mypath.main_path_optics
    Projection_MRI_dir = Mypath.output_MRI_projection_dir

    file_resolution_optics = main_path_otpics+"resolution.txt"
    filename_optics_mask = main_path_otpics+"mask.png"
    filename_tumor_masks = Projection_MRI_dir+"Mask_Proj_Tumor.nii.gz"



    filename_MRI_mask_hemisphere = Projection_MRI_dir+"Hemisphere_Mask_Proj_MRI.nii.gz"
    filename_MRI_mask = Projection_MRI_dir+"Mask_Proj_MRI.nii.gz"



    if not os.path.exists(filename_optics_mask):
        return "[get_MRI_mask_around_tumor] Optical mask is missing"

    if not os.path.exists(file_resolution_optics):
        return "[get_MRI_mask_around_tumor] Optical resolution file is missing"

    if not os.path.exists(filename_MRI_mask):
        return "[get_MRI_mask_around_tumor] MRI projection mask is missing"
    
    if not os.path.exists(filename_MRI_mask_hemisphere):
        return "[get_MRI_mask_around_tumor] MRI hemisphere projection mask is missing"

    if not os.path.exists(filename_tumor_masks):
        return "[get_MRI_mask_around_tumor] Tumor mask projection file is missing"



    if params.axis_projection != "No rotation":

        #load mask
        mask = cv.imread(filename_optics_mask,cv.IMREAD_ANYCOLOR)

        mri_mask = itk.imread(filename_MRI_mask, itk.F)
        res_MRI_mm = np.max(np.array([mri_mask.GetSpacing()[0], mri_mask.GetSpacing()[1]]))
        np_mri_mask = itk.GetArrayFromImage(mri_mask)
        np_mri_mask[np_mri_mask>1] = 1
        np_mri_mask = np_mri_mask.astype(np.uint8)

        mri_mask_hemisphere = itk.imread(filename_MRI_mask_hemisphere, itk.F)
        np_mri_mask_hemisphere = itk.GetArrayFromImage(mri_mask_hemisphere)
        np_mri_mask_hemisphere[np_mri_mask_hemisphere>1] = 1
        np_mri_mask_hemisphere = np_mri_mask_hemisphere.astype(np.uint8)


        # erode edge of half hemisphere to remove central sulci
        ksize_mm = 20
        ksize_px = int(ksize_mm/res_MRI_mm)
        if ksize_px>0:
            kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(ksize_px,ksize_px))
            np_mri_mask_hemisphere = cv.morphologyEx(np_mri_mask_hemisphere, op=cv.MORPH_ERODE, kernel=kernel)

        #Remove the hemisphere that is not usefull
        np_mri_mask = np.bitwise_and(np_mri_mask,np_mri_mask_hemisphere)

        # erode edge on the full projectio of MRI mask
        ksize_mm = params.MRI_erode_edge_mm
        ksize_px = int(ksize_mm/res_MRI_mm)
        if ksize_px>0:
            kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(ksize_px,ksize_px))
            np_mri_mask = cv.morphologyEx(np_mri_mask, op=cv.MORPH_ERODE, kernel=kernel)

        if ksize_px<0:
            ksize_px = np.abs(ksize_px)
            kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(ksize_px,ksize_px))
            np_mri_mask = cv.morphologyEx(np_mri_mask, op=cv.MORPH_DILATE, kernel=kernel)

        
        
        



        tumor_mask = itk.imread(filename_tumor_masks, itk.F)
        np_tumor_mask = itk.GetArrayFromImage(tumor_mask)
        np_tumor_mask[np_tumor_mask>1] = 1
        np_tumor_mask = np_tumor_mask.astype(np.uint8)

        #Load image resolution
        res_opt_in_mm = float(np.loadtxt(file_resolution_optics))
        

        #Get min area rectangle around surgical window
        max_size_surgical_window_optics_mm = get_max_size_mask_mm(mask, res_opt_in_mm)
        max_size_tumor_MRI_mm = get_max_size_mask_mm(np_tumor_mask, res_MRI_mm)


        #process dilatation to enlarge tumor mask
        n_repet = int(np.ceil((max_size_surgical_window_optics_mm - max_size_tumor_MRI_mm/2)/res_MRI_mm))
        kernel = np.ones((3, 3), np.uint8)
        # kernel = cv.getStructuringElement(cv.MORPH_CROSS, (3, 3))
        if n_repet>0:
            np_mri_mask_tumor_enlarged = cv.dilate(np_tumor_mask, kernel, iterations=n_repet)
        else:
            np_mri_mask_tumor_enlarged = np.copy(np_tumor_mask)
        
        #apply tumor mask to MRI mask
        np_mri_mask_tumor_enlarged = np.bitwise_and(np_mri_mask,np_mri_mask_tumor_enlarged)



        #Write image
        mri_mask_tumor_enlarged = itk.GetImageFromArray(np.ascontiguousarray(np_mri_mask_tumor_enlarged))
        mri_mask_tumor_enlarged = mri_mask_tumor_enlarged.astype(itk.SS)
        mri_mask_tumor_enlarged.SetSpacing(mri_mask.GetSpacing())
        mri_mask_tumor_enlarged.SetDirection(mri_mask.GetDirection())
        mri_mask_tumor_enlarged.SetOrigin(mri_mask.GetOrigin())
        itk.imwrite(mri_mask_tumor_enlarged, Projection_MRI_dir+"Mask_Proj_MRI_around_tumor.nii.gz")

    else:

        mri_mask = itk.imread(filename_MRI_mask, itk.F)
        np_mri_mask = itk.GetArrayFromImage(mri_mask)
        np_mri_mask[np_mri_mask>1] = 1
        np_mri_mask = np_mri_mask.astype(np.uint8)

        # erode edge on the full projectio of MRI mask
        res_MRI_mm = np.max(np.array([mri_mask.GetSpacing()[0], mri_mask.GetSpacing()[1]]))
        ksize_mm = params.MRI_erode_edge_mm
        ksize_px = int(ksize_mm/res_MRI_mm)
        if ksize_px>0:
            kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(ksize_px,ksize_px))
            np_mri_mask = cv.morphologyEx(np_mri_mask, op=cv.MORPH_ERODE, kernel=kernel)

        if ksize_px<0:
            ksize_px = np.abs(ksize_px)
            kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(ksize_px,ksize_px))
            np_mri_mask = cv.morphologyEx(np_mri_mask, op=cv.MORPH_DILATE, kernel=kernel)

        mri_mask_tumor_enlarged = itk.GetImageFromArray(np.ascontiguousarray(np_mri_mask))
        mri_mask_tumor_enlarged = mri_mask_tumor_enlarged.astype(itk.SS)
        mri_mask_tumor_enlarged.SetSpacing(mri_mask.GetSpacing())
        mri_mask_tumor_enlarged.SetDirection(mri_mask.GetDirection())
        mri_mask_tumor_enlarged.SetOrigin(mri_mask.GetOrigin())
        itk.imwrite(mri_mask_tumor_enlarged, Projection_MRI_dir+"Mask_Proj_MRI_around_tumor.nii.gz")
    return "Success"


def main_select_tumor_brain_hemisphere(Mypath = Paths()):


    output_dir = Mypath.output_dir
    filename_surface_mask = output_dir+'surface_mask.nii.gz'
    filename_tumor_mask = Mypath.output_tumor_segmentation_dir+'r_tumor_mask.nii.gz'

    if not os.path.exists(filename_surface_mask):
        return "[main_select_tumor_brain_hemisphere] Surface mask is missing"
    
    if not os.path.exists(filename_tumor_mask):
        return "[main_select_tumor_brain_hemisphere] Surface mask is missing"
    






    # Read the binary mask
    mask_itk = itk.imread(filename_surface_mask)
    mask_np = itk.GetArrayFromImage(mask_itk)  # ITK → NumPy (z, y, x)

    #Load tumor mask
    tumor_mask = itk.imread(filename_tumor_mask)
    tumor_mask_np = itk.GetArrayFromImage(tumor_mask)  # ITK → NumPy (z, y, x)

    

    # Determine which axis corresponds to left–right (usually x-axis)
    # Compute mid-sagittal plane index (in voxel space)
    mid_idx = mask_np.shape[2] // 2




    #Count nb of voxel in each hemisphere
    hemisphere_mask = np.zeros(mask_np.shape, dtype=np.uint8)
    if np.count_nonzero(tumor_mask[:, :, :mid_idx]) >= np.count_nonzero(tumor_mask[:, :, mid_idx:]):
        hemisphere_mask[:, :, :mid_idx] = mask_np[:, :, :mid_idx]
    else:
        hemisphere_mask[:, :, mid_idx:] = mask_np[:, :, mid_idx:]


    # Convert back to ITK and keep metadata
    itk_hemisphere_mask = itk.GetImageFromArray(hemisphere_mask)
    itk_hemisphere_mask.SetSpacing(mask_itk.GetSpacing())
    itk_hemisphere_mask.SetOrigin(mask_itk.GetOrigin())
    itk_hemisphere_mask.SetDirection(mask_itk.GetDirection())

    # Save results
    itk.imwrite(itk_hemisphere_mask, Mypath.output_MRI_projection_dir+'hemisphere_mask.nii.gz')






    # #Load surface mask
    # nii_surface_mask = nib.load(filename_surface_mask)
    # surface_mask = np.asarray(nii_surface_mask.dataobj)
    # affine_surface_mask = nii_surface_mask.affine

    # #Load tumor mask
    # nii_tumor_mask = nib.load(filename_tumor_mask)
    # tumor_mask = np.asarray(nii_tumor_mask.dataobj)


    # # Compute voxel coordinates in world space
    # nx, ny, nz = surface_mask.shape
    # coords = np.arange(nx)
    # x_world = nib.affines.apply_affine(affine_surface_mask, np.column_stack((coords, np.zeros(nx), np.zeros(nx))))[:, 0]

    # # Find midline (x=0 in world coordinates)
    # mid_idx = np.argmin(np.abs(x_world))


    # #Count nb of voxel in each hemisphere
    # hemisphere_mask = np.zeros_like(surface_mask)
    # if np.count_nonzero(tumor_mask[:mid_idx, :, :]) >= np.count_nonzero(tumor_mask[mid_idx:, :, :]):
    #     hemisphere_mask = surface_mask[:mid_idx, :, :]
    # else:
    #     hemisphere_mask = surface_mask[mid_idx:, :, :]

    # # Save if needed
    # nib.save(nib.Nifti1Image(hemisphere_mask.astype(np.uint8), affine_surface_mask), output_dir+'hemisphere_mask.nii.gz')

    return "Success"

def main_get_MRI_projection(Mypath = Paths(), params=Params()):

    error = main_select_tumor_brain_hemisphere(Mypath)
    if error != "Success":
        return error

    output_dir = Mypath.output_dir
    result_dir = Mypath.output_MRI_projection_dir
    #################
    # Load mri volume
    #################


    filename_t1 = output_dir + "r_T1_bet.nii.gz"
    filename_surface_mask = output_dir+'surface_mask.nii.gz'
    filename_tumor = Mypath.output_tumor_segmentation_dir+'r_tumor_mask.nii.gz'
    filename_hemisphere_tumor = result_dir+'hemisphere_mask.nii.gz'
    filename_fMRI_stats = glob.glob(output_dir + "fMRI/inferences/*")


    if not os.path.exists(filename_t1):
        return "T1 file is missing"

    if not os.path.exists(filename_surface_mask):
        return "Surface mask file is missing"

    if not os.path.exists(filename_tumor):
        return "Tumor file is missing"
    
    if not os.path.exists(filename_hemisphere_tumor):
        return "Mask hemisphere file is missing"
    
    

    #remove previous files
    if len(filename_fMRI_stats)!= 0:
        out_fMRI_dir = output_dir+"fMRI/inferences/rotated/"
        if os.path.exists(out_fMRI_dir):
            shutil.rmtree(out_fMRI_dir)

        #create output directory
        os.mkdir(out_fMRI_dir)
    else:
        out_fMRI_dir = None

    # Load MRI volumes
    T1 = itk.imread(filename_t1, itk.F)
    surface = itk.imread(filename_surface_mask, itk.F)
    tumor = itk.imread(filename_tumor, itk.F)
    hemisphere_mask = itk.imread(filename_hemisphere_tumor, itk.F)


    ##################################
    # Calculate the rotation transform
    ##################################

    # Get center of mass of the tumor
    center_of_mass_tumor_itk = getGravityCenter(tumor)
    center_of_mass_MRI = getGravityCenter(surface)



    # Calculate a new orthonormal basis. Consider that the vector between the center of mass of the tumor and the origin of MRI is the z axis
    # Vector between the center of mass of the tumor and the point at the surface

    if params.axis_projection == "Origin MRI" or params.axis_projection == "Axis passing through MRI origin":
        vector_Tumor_surface = vector(center_of_mass_tumor_itk,surface.GetOrigin())
    else:
        vector_Tumor_surface = vector(center_of_mass_tumor_itk, center_of_mass_MRI)



    # Get the orthogonal matrix 
    if params.projection_base_axis == "Y axis":
        new_directionMatrix, new_directionMatrix_itk  = orthonormal_basis_from_Y_vector(vector_Tumor_surface)
    if params.projection_base_axis == "X axis":
        new_directionMatrix, new_directionMatrix_itk  = orthonormal_basis_from_X_vector(vector_Tumor_surface)
    if params.projection_base_axis == "Z axis":
        new_directionMatrix, new_directionMatrix_itk  = orthonormal_basis_from_Z_vector(vector_Tumor_surface)

    # Calculate rotation matrix between origin direction and new new_directionMatrix
    mri_base = itk.array_from_matrix(T1.GetDirection())
    R = np.dot(new_directionMatrix, np.linalg.inv(mri_base))

    #Calculate translation vector
    T = np.zeros((3,))

    if params.axis_projection == "No rotation":
        R = np.identity(3,dtype=R.dtype)

    #Save rotation matrix and translation for projection
    np.savetxt(result_dir+"Rotation_matrix_projection.txt",R)
    np.savetxt(result_dir+"Translation_vector_projection.txt",T)



    #######################
    # Apply Rotation
    #######################
    filename_MRI_surface = result_dir+'surface_mask_rotated.nii.gz'
    Apply_Afffine_Transform(R, T, surface, center_of_mass_MRI, filename_MRI_surface)

    filename_MRI_hemisphere_surface = result_dir+'hemisphere_mask_rotated.nii.gz'
    Apply_Afffine_Transform(R, T, hemisphere_mask, center_of_mass_MRI, filename_MRI_hemisphere_surface)

    filename_T1 = result_dir+'T1_rotated.nii.gz'
    Apply_Afffine_Transform(R, T, T1, center_of_mass_MRI, filename_T1)

    filename_tumor = result_dir+'Tumor_rotated.nii.gz'
    Apply_Afffine_Transform(R, T, tumor, center_of_mass_MRI, filename_tumor)


    #fMRI stats
    if out_fMRI_dir is not None:
        for file in filename_fMRI_stats:
            fMRI_stats = itk.imread(file,itk.F)
            outfilename = out_fMRI_dir + os.path.basename(file)
            Apply_Afffine_Transform(R, T, fMRI_stats, center_of_mass_MRI, outfilename)

        filename_fMRI_stats = glob.glob(out_fMRI_dir+ "*")



    #######################
    # Calculate projection T1
    #######################
    if params.axis_projection == "No rotation":
        project_on_tumor = True
    else:
        project_on_tumor = False


    # Load MRI data
    T1 = itk.imread(filename_T1, itk.F)
    surface = itk.imread(filename_MRI_surface, itk.F)
    tumor = itk.imread(filename_tumor, itk.F)
    hemisphere_mask = itk.imread(filename_MRI_hemisphere_surface, itk.F)

    #Apply hemisphere mask to rotated T1
    hemisphere_T1 = MultiplyFilter(T1,hemisphere_mask)


    # Get numpy arrays
    np_T1 = itk.GetArrayFromImage(T1)
    np_hemisphere_T1 = itk.GetArrayFromImage(hemisphere_T1)
    np_surface = itk.GetArrayFromImage(surface)
    np_tumor = itk.GetArrayFromImage(tumor)


    # Calculate projection
    np_MRI_projection, np_mask, np_tumor_mask = create_MRI_projection_np(np_T1,
                                                                        np_surface,
                                                                        np_tumor,
                                                                        Projection=params.projection_type,
                                                                        project_on_tumor=project_on_tumor)
    
    np_MRI_hemisphere_projection, np_mask_hemisphere, np_tumor_mask = create_MRI_projection_np(np_hemisphere_T1,
                                                                        np_surface,
                                                                        np_tumor,
                                                                        Projection=params.projection_type,
                                                                        project_on_tumor=project_on_tumor)

    # Get spacing
    mri_spacing = T1.GetSpacing()
    if params.projection_type == "Sagital":
        spacing_projection = [mri_spacing[2] , mri_spacing[0]]

    if params.projection_type == "Transverse":
        spacing_projection = [mri_spacing[0] , mri_spacing[1]]

    if params.projection_type == "Coronal":
        spacing_projection = [mri_spacing[2] , mri_spacing[1]]



    print("Spacing projection", spacing_projection)


    #Write itk image
    proj = itk.GetImageFromArray(np.ascontiguousarray(np_MRI_projection))
    proj.SetSpacing([spacing_projection[0], spacing_projection[1]])
    itk.imwrite(proj,result_dir+"Proj_MRI.nii.gz")

    proj = itk.GetImageFromArray(np.ascontiguousarray(np_mask))
    proj.SetSpacing([spacing_projection[0], spacing_projection[1]])
    itk.imwrite(proj,result_dir+"Mask_Proj_MRI.nii.gz")

    proj = itk.GetImageFromArray(np.ascontiguousarray(np_MRI_hemisphere_projection))
    proj.SetSpacing([spacing_projection[0], spacing_projection[1]])
    itk.imwrite(proj,result_dir+"Hemisphere_Proj_MRI.nii.gz")

    proj = itk.GetImageFromArray(np.ascontiguousarray(np_mask_hemisphere))
    proj.SetSpacing([spacing_projection[0], spacing_projection[1]])
    itk.imwrite(proj,result_dir+"Hemisphere_Mask_Proj_MRI.nii.gz")
     

    proj = itk.GetImageFromArray(np.ascontiguousarray(np_tumor_mask))
    proj.SetSpacing([spacing_projection[0], spacing_projection[1]])
    itk.imwrite(proj,result_dir+"Mask_Proj_Tumor.nii.gz")



    # Only keep grey matter around tumor by dilating tumor mask to correspond to surgical window size
    error = get_MRI_mask_around_tumor(Mypath, params)
    if error != "Success":
        return error


    #################################
    # Calculate projection fMRI stats
    #################################

    # Calculate projection for fMRI
    for file in filename_fMRI_stats:
        fMRI_stats = itk.imread(file,itk.F)
        np_fMRI_stats = itk.GetArrayFromImage(fMRI_stats)

        # Calculate projection
        np_fMRI_projection, _, _ = create_MRI_projection_np(np_fMRI_stats,
                                                            np_surface,
                                                            np_tumor,
                                                            Projection=params.projection_type,
                                                            project_on_tumor=project_on_tumor)


        output_filename = file.split('.')[0]+"_Mask_proj.nii.gz"

        proj = itk.GetImageFromArray(np.ascontiguousarray(np_fMRI_projection))
        proj.SetSpacing([spacing_projection[0], spacing_projection[1]])
        itk.imwrite(proj,output_filename)

    return "Success"


def main_resize_np_projection(itk_img):

    spacing = itk_img.GetSpacing()

    np_img = itk.GetArrayFromImage(itk_img) 

    ratio = spacing[0]/spacing[1]

    if spacing[0] == spacing[1]:
        return np_img
    else:

        # Resize the image to make it square
        if spacing[0] > spacing[1]: 
            width = np_img.shape[1]
            height = np_img.shape[0]*ratio*spacing[1]
        else:
            width = np_img.shape[1]*spacing[0]/ratio
            height = np_img.shape[0]
  
        new_shape = (int(width), int(height))
        resized_img = cv.resize(np_img, new_shape, interpolation=cv.INTER_CUBIC)

        return resized_img



def main_draw_tumor_contour_on_projection(Mypath = Paths(), MRI_projection=None):
    
    if MRI_projection is None:
        return "[main_draw_tumor_contour_on_projection] MRI projection is missing",None
    
    if MRI_projection.ndim != 3:
        return "[main_draw_tumor_contour_on_projection] MRI projection is not RGB",None
    
    #Get tumor contour
    filename_tumor_masks = Mypath.output_MRI_projection_dir+"Mask_Proj_Tumor.nii.gz"

    if not os.path.exists(filename_tumor_masks):
        return "[main_draw_tumor_contour_on_projection] Tumor mask projection file is missing",None
    
    tumor_mask = itk.imread(filename_tumor_masks, itk.F)
    np_tumor_mask = itk.GetArrayFromImage(tumor_mask).astype(np.uint8)
    contours, hierarchy = cv.findContours(np_tumor_mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    
    #Draw contours on MRI projection
    cv.drawContours(MRI_projection, contours, -1, (0,0,255), 1)

    return "Success",MRI_projection


def main_plot_MRI_Projection(Mypath = Paths()):


    output_dir = Mypath.output_MRI_projection_dir
    #######################
    # Display projection
    #######################

    filename_proj = output_dir+"Proj_MRI.nii.gz"
    filename_mask_proj_hemisphere_tumor = output_dir+"Mask_Proj_MRI_around_tumor.nii.gz"

    if not os.path.exists(filename_proj):
        return "[main_plot_MRI_Projection] T1 projection file is missing",None
    
    if not os.path.exists(filename_mask_proj_hemisphere_tumor):
        return "[main_plot_MRI_Projection] Mask projection (hemisphere + tumor) is missing",None

    proj = itk.imread(filename_proj, itk.F)
    np_MRI_projection = itk.GetArrayFromImage(proj)

    mask_MRI = itk.imread(filename_mask_proj_hemisphere_tumor, itk.F)
    np_mask_MRI = itk.GetArrayFromImage(mask_MRI).astype(np.uint8)

    #Display only - Plot MRI and tumor projection
    np_MRI_projection = 255*(np_MRI_projection-np_MRI_projection.min())/(np_MRI_projection.max() - np_MRI_projection.min())
    np_MRI_projection = np_MRI_projection.astype(np.uint8)

    #Convert in RGB
    np_MRI_projection = cv.cvtColor(np_MRI_projection,cv.COLOR_GRAY2BGR)

    #Draw tumor contour
    status, np_MRI_projection = main_draw_tumor_contour_on_projection(Mypath, np_MRI_projection)
    if status != "Success":
        return status,None
    

    cv.imwrite(output_dir+"MRI_projection2.png",np_MRI_projection)
    
    #Draw mask MRI
    contours, hierarchy = cv.findContours(np_mask_MRI, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cv.drawContours(np_MRI_projection, contours, -1, (255,0,0), 1)
    

    #Apply median filter for display only
    cv.imwrite(output_dir+"MRI_projection.png",np_MRI_projection)

    #Convert in BGR
    np_MRI_projection = cv.cvtColor(np_MRI_projection,cv.COLOR_BGR2RGB)

    if status != "Success":
        return status, None

    return "Success",np_MRI_projection




def main_get_vessels_in_MRI(Mypath = Paths(), params=Params()):
    
    result_dir = Mypath.output_BV_segmentation_dir
    filename_MRI = Mypath.output_MRI_projection_dir+"Proj_MRI.nii.gz"

    # if params.mask_MRI_hemisphere:
    #     prefix = "Hemisphere_"
    # else:
    #     prefix = ""
    # filename_MRI_mask = Mypath.output_MRI_projection_dir+prefix+"Mask_Proj_MRI.nii.gz"
    filename_MRI_mask = Mypath.output_MRI_projection_dir+"Mask_Proj_MRI_around_tumor.nii.gz"


    if not os.path.exists(filename_MRI):
        return "[main_get_vessels_in_MRI] MRI projection is missing"

    if not os.path.exists(filename_MRI_mask):
        return "[main_get_vessels_in_MRI] MRI projection is missing"


    #################################
    ######## T1 volume ##############
    #################################

    #Normalize MRI data data to uint16
    mri = itk.imread(filename_MRI, itk.F)
    np_mri = itk.GetArrayFromImage(mri)
    np_mri = (1600)*(np_mri - np_mri.min())/(np_mri.max() - np_mri.min())
    np_mri = np_mri.astype(np.uint16)


    _mri = itk.GetImageFromArray(np.ascontiguousarray(np_mri))
    _mri = _mri.astype(itk.SS)
    _mri.SetSpacing(mri.GetSpacing())
    _mri.SetDirection(mri.GetDirection())
    _mri.SetOrigin(mri.GetOrigin())


    #Load data
    mask_mri_itk = itk.imread(filename_MRI_mask, itk.SS)

    #Get np volumes
    np_mri = itk.GetArrayFromImage(_mri)
    mask_mri = itk.GetArrayFromImage(mask_mri_itk)


    res_mri = np.min(mri.GetSpacing())

    if params.sigma_minimum_mm_MRI < res_mri:
        params.sigma_minimum_mm_MRI = res_mri

    #Enhance blood vessel
    mri_enhanced = enhance_Blood_vessel(itk_image = _mri,
                                        resolution_mm=res_mri,
                                        sigma_minimum_mm = params.sigma_minimum_mm_MRI,
                                        sigma_maximum_mm = params.sigma_maximum_mm_MRI,
                                        number_of_sigma_steps = params.number_of_sigma_steps,
                                        alpha = 0.15,
                                        beta = 1.0,
                                        gamma = 10,
                                        # alpha = 0.5,
                                        # beta = 0.5,
                                        # gamma = 0.5,
                                        Light_structures = True)

    #BLood vessel segmentation
    mri_enhanced = ((mri_enhanced - mri_enhanced.min())/(mri_enhanced.max() - mri_enhanced.min())*255).astype(np.uint8)
    cv.imwrite(result_dir+"MRI_proj_enhanced.png",mri_enhanced)






    #Use optics skeleton apriori if available
    if params.MRI_skeleton_apriori is not None and params.MRI_skeleton_apriori.sum() > 0:
        print("[main_get_vessels_in_MRI] Using MRI skeleton apriori")

        mri_vessels = np.copy(params.MRI_skeleton_apriori)

    else:
        #Binarization
        th,mri_vessels = cv.threshold(np.copy(mri_enhanced), params.thresh_MRI, 255, cv.THRESH_BINARY)

        mri_vessels = mri_vessels*mask_mri

        #Remove small contours
        min_area_mm = 3
        min_ara_pixels = (min_area_mm/res_mri)**2
        contours, hierarchy = cv.findContours(np.copy(mri_vessels.astype(np.uint8)), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        # mri_vessels = np.zeros(mri_vessels.shape)
        for i in range(len(contours)):
            if cv.contourArea(contours[i]) < min_ara_pixels:
                cv.drawContours(mri_vessels,contours,i,0,cv.FILLED)



    #Create skeleton
    skeleton_MRI = cv.ximgproc.thinning(mri_vessels.astype(np.uint8))
    cv.imwrite(result_dir+"MRI_proj_skeleton.png",skeleton_MRI)


    #Create binary image
    skeleton_MRI = skeleton_MRI/skeleton_MRI.max()




    #Write images
    itk_mri = itk.GetImageFromArray(np.ascontiguousarray(mri_vessels))
    itk_mri.SetSpacing(mri.GetSpacing())
    itk.imwrite(itk_mri, result_dir+"T1_proj_mask_large_vessels.nii.gz")


    itk_mri = itk.GetImageFromArray(np.ascontiguousarray(mri_enhanced))
    itk_mri.SetSpacing(mri.GetSpacing())
    itk.imwrite(itk_mri, result_dir+"T1_proj_enhanced.nii.gz")

    mri_enhanced = mri_enhanced*mask_mri
    itk_mri = itk.GetImageFromArray(np.ascontiguousarray(mri_enhanced))
    itk_mri.SetSpacing(mri.GetSpacing())
    itk.imwrite(itk_mri, result_dir+"T1_proj_enhanced_masked.nii.gz")

    itk_mri = itk.GetImageFromArray(np.ascontiguousarray(skeleton_MRI))
    itk_mri.SetSpacing(mri.GetSpacing())
    itk.imwrite(itk_mri, result_dir+"T1_proj_skeleton.nii.gz")

    itk_mri = itk.GetImageFromArray(np.ascontiguousarray(mask_mri))
    itk_mri.SetSpacing(mri.GetSpacing())
    itk.imwrite(itk_mri, filename_MRI_mask.split('.')[0] + "_erode.nii.gz")


    #Convert binary masks into signed distance image
    skeleton = itk.imread(result_dir+"T1_proj_skeleton.nii.gz", itk.F)
    MRI_signed_distance_skeleton = getSignedDistanceMap(skeleton)
    MRI_signed_distance_skeleton = MultiplyFilter(MRI_signed_distance_skeleton, itk.imread(filename_MRI_mask, itk.F))
    # np_MRI_signed_distance_skeleton = itk.GetArrayFromImage(MRI_signed_distance_skeleton)
    itk.imwrite(MRI_signed_distance_skeleton, result_dir +"MRI_signed_distance.nii.gz")

    return "Success"

def main_get_vessels_in_optics(Mypath = Paths(), params=Params()):

    main_path_otpics = Mypath.main_path_optics

    #Set output directory
    result_dir = Mypath.output_BV_segmentation_dir
    

    #create results directory for optical threshold
    result_dir = result_dir+ "Optics_thresh_"+str(params.thresh_optics)+"/"
    if not os.path.exists(result_dir):
        os.mkdir(result_dir)

    
    #################################
    ######## Optical imaging ########
    #################################

    filename_MRI = Mypath.output_MRI_projection_dir+"Proj_MRI.nii.gz"
    filename_optics = main_path_otpics+"initial_img.png"
    filename_optics_mask = main_path_otpics+"mask.png"
    file_resolution_optics = main_path_otpics+"resolution.txt"

    if not os.path.exists(filename_optics):
        return "[main_get_vessels_in_optics] Optical image is missing"

    if not os.path.exists(filename_optics_mask):
        return "[main_get_vessels_in_optics] Optical mask is missing"

    if not os.path.exists(file_resolution_optics):
        return "[main_get_vessels_in_optics] Optical resolution file is missing"
    
    if not os.path.exists(filename_MRI):
        return "[main_get_vessels_in_optics] MRI projection is missing"
    

    #Get resolution of MRI
    mri = itk.imread(filename_MRI, itk.F)
    res_mri = np.min(mri.GetSpacing())

    #Check if image is RGB or HSI
    _,suffix_out_optics = is_RGB_optical_image(filename_optics)


    # Load image
    img = cv.imread(filename_optics,cv.IMREAD_ANYCOLOR)
    mask = cv.imread(filename_optics_mask,cv.IMREAD_ANYCOLOR)/255

        
    #Load image resolution
    res_opt_in_mm = float(np.loadtxt(file_resolution_optics))

    #Check if initial image is RGB
    if img.ndim>2:
        img = img[:,:,2]
        # cv.imwrite(result_dir+"Optical_red_channel.png", img)

    # img = img*mask




    # Apply opening to remove specular reflection
    ksize_mm = params.ksize_mm_kernal_specular_reflection_optics
    ksize_px = int(ksize_mm/res_opt_in_mm)
    if ksize_px >0:
        kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(ksize_px,ksize_px))
        img = cv.morphologyEx(img, op=cv.MORPH_OPEN, kernel=kernel)

    cv.imwrite(result_dir+"Optics_enhanced"+suffix_out_optics+".png",img)
    itk_optics = itk.imread(result_dir+"Optics_enhanced"+suffix_out_optics+".png", itk.SS)

    #Enhance blood vessel
    if params.sigma_minimum_mm_optics == 0 and params.sigma_maximum_mm_optics ==0:
        optics_enhanced = np.copy(img)
    
    else:
        optics_enhanced = enhance_Blood_vessel(itk_image = itk_optics,
                                            resolution_mm = res_opt_in_mm,
                                            sigma_minimum_mm = params.sigma_minimum_mm_optics,
                                            sigma_maximum_mm = params.sigma_maximum_mm_optics,                                                                            
                                            number_of_sigma_steps = params.number_of_sigma_steps,                                    
                                            alpha = 0.5,                                    
                                            beta = 0.5,                                    
                                            gamma = 5,                                    
                                            Light_structures = False)


    #erode mask to remove edge effects
    ksize_mm = params.kernel_mm_optical_mask_erosion
    ksize_px = int(ksize_mm/res_opt_in_mm)
    if ksize_px>0:
        kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(ksize_px,ksize_px))

        #Erode mask to remove edge effects
        mask = cv.morphologyEx(mask, op=cv.MORPH_ERODE, kernel=kernel).astype(np.uint8)

    #Apply mask of saturated pixel
    # optics_enhanced = optics_enhanced*mask_saturated_pixels
    optics_enhanced = optics_enhanced * mask







    #Write images
    optics_enhanced_display = 255*(optics_enhanced - optics_enhanced.min())/(optics_enhanced.max()-optics_enhanced.min())
    cv.imwrite(result_dir+"Optical_enhanced_full_res"+suffix_out_optics+".png",optics_enhanced_display.astype(np.uint8))




    #Adapt the resolution to MRI
    min_area_mm = 3

    params.Optical_downsampling_factor = int(res_mri/res_opt_in_mm)+1
    optics_enhanced = pyramid_reduce(optics_enhanced, downscale=params.Optical_downsampling_factor)
    mask = (cv.resize(mask,(optics_enhanced.shape[1],optics_enhanced.shape[0]))).astype(np.uint8)
    mask[mask>0] = 1


    optics_spacing = mri.GetSpacing()
    min_ara_pixels = (min_area_mm/res_mri)**2


    #Normalize data
    optics_enhanced = ((optics_enhanced - optics_enhanced.min())/(optics_enhanced.max() - optics_enhanced.min())*255).astype(np.uint8)
    cv.imwrite(result_dir+"Optical_enhanced"+suffix_out_optics+".png",optics_enhanced)




    #Use optics skeleton apriori if available
    if params.optics_skeleton_apriori is not None and params.optics_skeleton_apriori.sum() > 0:
        print("[main_get_vessels_in_optics] Using optics skeleton apriori")
        
        #Apply closing to connect points
        ksize_px = 5
        kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(ksize_px,ksize_px))
        # temp = cv.morphologyEx(params.optics_skeleton_apriori, op=cv.MORPH_CLOSE, kernel=kernel)
        temp = cv.morphologyEx(params.optics_skeleton_apriori, op=cv.MORPH_DILATE, kernel=kernel)
        
        #Resize skeleton
        optics_vessels = cv.resize(temp, (optics_enhanced.shape[1],optics_enhanced.shape[0]),interpolation=cv.INTER_NEAREST)    


        # plt.figure()
        # plt.subplot(131)
        # plt.imshow(params.optics_skeleton_apriori)
        # plt.subplot(132)
        # plt.imshow(temp)
        # plt.subplot(133)
        # plt.imshow(optics_vessels)
        # plt.show(block=True)
    else:
        print("[main_get_vessels_in_optics] Thresholding process")
        
        
        #Apply closing to fill blood vessel in Frangi
        ksize_px = 5
        kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(ksize_px,ksize_px))
        optics_enhanced = cv.morphologyEx(optics_enhanced, op=cv.MORPH_CLOSE, kernel=kernel)
    
        
        
        
        #Binarisation
        th,optics_vessels = cv.threshold(np.copy(optics_enhanced), params.thresh_optics, 255, cv.THRESH_BINARY)

        # #Remove small blobs
        # contours, hierarchy = cv.findContours(np.copy(optics_vessels.astype(np.uint8)), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        # for i in range(len(contours)):
        #     if cv.contourArea(contours[i]) < min_ara_pixels:
        #         cv.drawContours(optics_vessels,contours,i,0,cv.FILLED)




    #Create skeleton
    skeleton_optics_tmp = cv.ximgproc.thinning(optics_vessels.astype(np.uint8))

    



    #Get skeleton components and remove small ones 
    skeleton_optics = np.zeros(skeleton_optics_tmp.shape,dtype=skeleton_optics_tmp.dtype)
    num_labels, labels = cv.connectedComponents(skeleton_optics_tmp)

    for i in range(1, num_labels): #skip background
        #get component coordinates
        coords = np.column_stack(np.where(labels == i))

        #Remove components having less than 10 pixels
        if len(coords)>10:
            skeleton_optics[coords[:, 0], coords[:, 1]] = 255


    cv.imwrite(result_dir+"Total_Optical_skeleton"+suffix_out_optics+".png",skeleton_optics)

    #resize skeleton
    skeleton_optics = cv.resize(skeleton_optics, (optics_enhanced.shape[1],optics_enhanced.shape[0]),interpolation=cv.INTER_NEAREST)


    #Create binary image
    skeleton_optics = skeleton_optics/skeleton_optics.max()


    #Write images
    optics_vol = itk.GetImageFromArray(np.ascontiguousarray(mask))
    optics_vol.SetSpacing(optics_spacing)
    itk.imwrite(optics_vol, result_dir+"optics_mask"+suffix_out_optics+".nii.gz")

    optics_vol = itk.GetImageFromArray(np.ascontiguousarray(optics_vessels))
    optics_vol.SetSpacing(optics_spacing)
    itk.imwrite(optics_vol, result_dir+"optics_mask_large_vessels"+suffix_out_optics+".nii.gz")

    optics_vol = itk.GetImageFromArray(np.ascontiguousarray(optics_enhanced))
    optics_vol.SetSpacing(optics_spacing)
    itk.imwrite(optics_vol, result_dir+"optics_enhanced"+suffix_out_optics+".nii.gz")

    optics_vol = itk.GetImageFromArray(np.ascontiguousarray(skeleton_optics))
    optics_vol.SetSpacing(optics_spacing)
    itk.imwrite(optics_vol, result_dir+"optics_skeleton"+suffix_out_optics+".nii.gz")


    #Convert binary masks into signed distance image
    skeleton = itk.imread(result_dir+"optics_skeleton"+suffix_out_optics+".nii.gz", itk.F)
    optics_signed_distance_skeleton = getSignedDistanceMap(skeleton)
    optics_signed_distance_skeleton = MultiplyFilter(optics_signed_distance_skeleton, itk.imread(result_dir+"optics_mask"+suffix_out_optics+".nii.gz", itk.F))
    itk.imwrite(optics_signed_distance_skeleton, result_dir +"optics_signed_distance"+suffix_out_optics+".nii.gz")
    # np_optics_signed_distance_skeleton = itk.GetArrayFromImage(optics_signed_distance_skeleton)

    print("end")
    return "Success"

def main_plot_vessel_skeletons(Mypath = Paths(), params = Params()):
   
    #Get skeleton images
    status, mri_skeleton_display, optics_skeleton_display = main_get_skeleton_images(Mypath,params)
    

    if status != "Success":
        return status, None
    
    print(status)
    print(mri_skeleton_display.shape)
    print(optics_skeleton_display.shape)


    # Get the maximum shape for both images
    max_shape = (np.maximum(mri_skeleton_display.shape[0],optics_skeleton_display.shape[0]), np.maximum(mri_skeleton_display.shape[1],optics_skeleton_display.shape[1]))
    display = np.zeros((max_shape[0],2*max_shape[1],3))

    display[:,0:max_shape[1]] = cv.resize(mri_skeleton_display,(max_shape[1],max_shape[0]))
    display[:,max_shape[1]:] = cv.resize(optics_skeleton_display,(max_shape[1],max_shape[0]))
    
                                        

    # plt.figure(figsize=(20,20))
    # plt.subplot(121)
    # plt.imshow(mri_skeleton_display,cmap='gray')
    # plt.subplot(122)
    # plt.imshow(optics_skeleton_display,cmap='gray')
    # plt.show()

    return "Success", display.astype(np.uint8)




def main_plot_Frangi_images(Mypath = Paths(), params = Params()):
   
    #Get skeleton images
    status, mri_Frangi, optics_Frangi = main_get_Frangi_images(Mypath,params)
    

    if status != "Success":
        return status, None
    
    print(status)
    print(mri_Frangi.shape)
    print(optics_Frangi.shape)


    # Get the maximum shape for both images
    max_shape = (np.maximum(mri_Frangi.shape[0],optics_Frangi.shape[0]), np.maximum(mri_Frangi.shape[1],optics_Frangi.shape[1]))
    display = np.zeros((max_shape[0],2*max_shape[1],3))

    display[:,0:max_shape[1]] = cv.resize(mri_Frangi,(max_shape[1],max_shape[0]))
    display[:,max_shape[1]:] = cv.resize(optics_Frangi,(max_shape[1],max_shape[0]))
    
                                        

    # plt.figure(figsize=(20,20))
    # plt.subplot(121)
    # plt.imshow(mri_Frangi,cmap='gray')
    # plt.subplot(122)
    # plt.imshow(optics_Frangi,cmap='gray')
    # plt.show()

    return "Success", display.astype(np.uint8)


def main_get_skeleton_images(Mypath = Paths(), params = Params()):
    
    main_path_otpics = Mypath.main_path_optics
    MRI_proj_dir = Mypath.output_MRI_projection_dir
    BV_segmentation_dir = Mypath.output_BV_segmentation_dir


    filename_optics = main_path_otpics+"initial_img.png"


    if not os.path.exists(filename_optics):
        return "[main_get_skeleton_images] Optical initial image is missing",None, None

    _,suffix_out_optics = is_RGB_optical_image(filename_optics)

    filename_MRI_skeleton = BV_segmentation_dir+"T1_proj_skeleton.nii.gz"
    filename_MRI_proj = MRI_proj_dir+"Proj_MRI.nii.gz"
    filename_optics_skeleton = BV_segmentation_dir+"Optics_thresh_"+str(params.thresh_optics)+"/optics_skeleton"+suffix_out_optics+".nii.gz"

    filename_full_res_optics_enhanced = BV_segmentation_dir+"Optics_thresh_"+str(params.thresh_optics)+"/Optical_enhanced_full_res.png"



    if not os.path.exists(filename_MRI_skeleton):
        return "[main_get_skeleton_images] MRI skeleton file is missing",None,None
    if not os.path.exists(filename_MRI_proj):
        return "[main_get_skeleton_images] MRI proj file is missing",None,None
    if not os.path.exists(filename_optics_skeleton):
        return "[main_get_skeleton_images] Optics skeleton file is missing",None,None
    if not os.path.exists(filename_full_res_optics_enhanced):
        return "[main_get_skeleton_images] Full res Optics enhanced file is missing",None,None




    in_optics = cv.imread(filename_optics)

    itk_optics = itk.imread(filename_optics_skeleton, itk.F)
    skeleton_optics = itk.GetArrayFromImage(itk_optics)
    skeleton_optics = (skeleton_optics*255).astype(np.uint8)

    optics_enhanced_full_res = cv.imread(filename_full_res_optics_enhanced,cv.IMREAD_GRAYSCALE)


    itk_mri = itk.imread(filename_MRI_skeleton, itk.F)
    skeleton_MRI = itk.GetArrayFromImage(itk_mri)

    itk_mri_proj = itk.imread(filename_MRI_proj, itk.F)
    mri_proj = itk.GetArrayFromImage(itk_mri_proj)
    mri_proj = 255*(mri_proj-mri_proj.min())/(mri_proj.max() - mri_proj.min())
    mri_proj = mri_proj.astype(np.uint8)
    mri_proj = cv.cvtColor(mri_proj,cv.COLOR_GRAY2BGR)


    ############# Get full res optics skeleton ###################
    
    #Binarisation
    th,optics_vessels = cv.threshold(np.copy(optics_enhanced_full_res), params.thresh_optics, 255, cv.THRESH_BINARY)

    #Create skeleton
    optics_vessels = cv.ximgproc.thinning(optics_vessels.astype(np.uint8))
    ksize=3
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(ksize,ksize))
    optics_vessels = cv.morphologyEx(optics_vessels, op=cv.MORPH_DILATE, kernel=kernel)



    ################# Display ###########################

    alpha = 0

    #MRI display
    mri_skeleton_display = np.zeros(mri_proj.shape)
    mri_skeleton_display[:,:,1] = 255*skeleton_MRI
    mri_skeleton_display = mri_skeleton_display.astype(np.uint8)

    mri_display = merge_two_colored_img(mri_proj, mri_skeleton_display, skeleton_MRI, alpha)

    #Optics display
    # skeleton_optics = cv.resize((skeleton_optics*255).astype(np.uint8),(in_optics.shape[1],in_optics.shape[0]),cv.INTER_NEAREST)
    
    # in_optics = cv.resize(in_optics,(skeleton_optics.shape[1],skeleton_optics.shape[0]),cv.INTER_CUBIC)
    # optics_skeleton_display = np.zeros(in_optics.shape)
    # optics_skeleton_display[:,:,1] = skeleton_optics
    # optics_skeleton_display = optics_skeleton_display.astype(np.uint8)
    # optics_skeleton_display = merge_two_colored_img(in_optics, optics_skeleton_display, skeleton_optics, alpha)


    optics_skeleton_display = np.zeros(in_optics.shape)
    optics_skeleton_display[:,:,1] = optics_vessels
    optics_skeleton_display = optics_skeleton_display.astype(np.uint8)

    optics_skeleton_display = merge_two_colored_img(in_optics, optics_skeleton_display, optics_vessels, alpha)


    #Draw tumor contour
    status, mri_display = main_draw_tumor_contour_on_projection(Mypath, mri_display)

    if status != "Success":
        return status, None, None
    
    #Convert in BGR
    mri_display = cv.cvtColor(mri_display.astype(np.uint8),cv.COLOR_BGR2RGB)
    optics_skeleton_display = cv.cvtColor(optics_skeleton_display.astype(np.uint8),cv.COLOR_BGR2RGB)


    return "Success", mri_display, optics_skeleton_display




def main_get_Frangi_images(Mypath = Paths(), params = Params()):
    
    main_path_otpics = Mypath.main_path_optics
    BV_segmentation_dir = Mypath.output_BV_segmentation_dir


    filename_in_optics = main_path_otpics+"initial_img.png"

    if not os.path.exists(filename_in_optics):
        return "[main_get_Frangi_images] Optical initial image is missing",None, None

    _,suffix_out_optics = is_RGB_optical_image(filename_in_optics)

    filename_MRI = BV_segmentation_dir+"T1_proj_enhanced_masked.nii.gz"
    filename_optics = BV_segmentation_dir+"Optics_thresh_"+str(params.thresh_optics)+"/optics_enhanced"+suffix_out_optics+".nii.gz"

    if not os.path.exists(filename_MRI):
        return "[main_get_Frangi_images] MRI Frangi image is missing",None,None
    if not os.path.exists(filename_optics):
        return "[main_get_Frangi_images] Optics Frangi image is missing",None,None



    itk_optics = itk.imread(filename_optics, itk.F)
    np_optics = itk.GetArrayFromImage(itk_optics)
    np_optics = 255*(np_optics-np_optics.min())/(np_optics.max() - np_optics.min())
    np_optics = np_optics.astype(np.uint8)
    np_optics = cv.cvtColor(np_optics,cv.COLOR_GRAY2BGR)

    itk_mri = itk.imread(filename_MRI, itk.F)
    np_mri = itk.GetArrayFromImage(itk_mri)
    np_mri = 255*(np_mri-np_mri.min())/(np_mri.max() - np_mri.min())
    np_mri = np_mri.astype(np.uint8)
    np_mri = cv.cvtColor(np_mri,cv.COLOR_GRAY2BGR)
    
    
    


    ################# Display ###########################



    #Draw tumor contour
    status, np_mri = main_draw_tumor_contour_on_projection(Mypath, np_mri)

    if status != "Success":
        return status, None, None
    
    #Convert in BGR
    np_mri = cv.cvtColor(np_mri.astype(np.uint8),cv.COLOR_BGR2RGB)


    return "Success", np_mri, np_optics

def main_plot_Optics_MRI_alignement_points(Mypath = Paths(), params=Params()):

    main_path_optics = Mypath.main_path_optics

    BV_segmentation_dir = Mypath.output_BV_segmentation_dir
    Optics_BV_segmentation_dir = BV_segmentation_dir+"Optics_thresh_"+str(params.thresh_optics)+"/"
    MRI_projection_dir = Mypath.output_MRI_projection_dir


    if not os.path.exists(main_path_optics+"initial_img.png"):
        return "Optical initial image is missing", None


    #Load initial optical image
    filename_initial_img_optics = main_path_optics+"initial_img.png"
    if not os.path.exists(filename_initial_img_optics):
        return "Optical initial image is missing", None

    #Check if optical imaging is RGB or HSI
    _,suffix_out_optics = is_RGB_optical_image(filename_initial_img_optics)



    #Load volumes
    filename_MRI = BV_segmentation_dir+"T1_proj_skeleton.nii.gz"
    filename_optics = Optics_BV_segmentation_dir+"optics_skeleton"+suffix_out_optics+".nii.gz"
    filename_mask_otpics = Optics_BV_segmentation_dir+"optics_mask"+suffix_out_optics+".nii.gz"
    filename_tumor = MRI_projection_dir+"Mask_Proj_Tumor.nii.gz"
    file_resolution_optics = main_path_optics+"resolution.txt"

    if not os.path.exists(file_resolution_optics):
        return "[main_get_vessels_in_optics] Optical resolution file is missing"

    if not os.path.exists(filename_MRI):
        return os.path.basename(filename_MRI)+ " is missing", None

    if not os.path.exists(filename_optics):
        return os.path.basename(filename_optics)+ " is missing", None

    if not os.path.exists(filename_tumor):
        return (os.path.basename(filename_tumor)+ " is missing"), None

    if not os.path.exists(filename_mask_otpics):
        return (os.path.basename(filename_mask_otpics)+ " is missing"), None





    # Load itk volumes
    MRI_proj = itk.imread(filename_MRI,itk.UC)
    Optics_img = itk.imread(filename_optics,itk.UC)
    Optical_mask=  itk.imread(filename_mask_otpics,itk.UC)
    mask_tumor = itk.imread(filename_tumor,itk.UC)

    #Load image resolution
    res_opt_in_mm = float(np.loadtxt(file_resolution_optics))
    res_mri = np.min(MRI_proj.GetSpacing())

    downscale_factor = int(res_mri/res_opt_in_mm)+1


    #Get MRI and optics alignement keypoints
    kp_Optics, kp_Optics_phys, _kpts_MRI_tumor, _kpts_MRI_tumor_phys = get_alignment_points(Optical_mask, Optics_img,
                                                                                            MRI_proj, mask_tumor, 
                                                                                            params.kpts_MRI_tumor, params.kpt_optics,
                                                                                            space_between_kpt_mm= params.space_between_kpt_mm,
                                                                                            enlarge_tumor_roi_factor=params.tumor_ROI_enlarge_factor)

    # kp_Optics, kp_Optics_phys, _kpts_MRI_tumor, _kpts_MRI_tumor_phys = get_alignement_points_in_skeleton(MRI_proj, Optics_img, Optical_mask, mask_tumor, params.MRI_keypoints_nb)


    kpts_MRI_tumor = _kpts_MRI_tumor
    kpts_MRI_tumor_phys = _kpts_MRI_tumor_phys

    #Get colored skeletons
    status, np_MRI_projection, np_Optics_img = main_get_skeleton_images(Mypath,params)
    if status != "Success":
        return status, None
    
    
    

    
    #Plot init points in MR image
    color_points = (0,0,255)
    radius = 2
    for i in range(len(kpts_MRI_tumor)):
        cv.circle(np_MRI_projection,(int(kpts_MRI_tumor[i][0]),int(kpts_MRI_tumor[i][1])),radius,color_points,-1)

    cv.imwrite(Mypath.output_registration_dir+"Alignement_point_MRI.png",cv.cvtColor(np_MRI_projection,cv.COLOR_BGR2RGB))

    #Plot init point in optics image
    radius = 10
    cv.circle(np_Optics_img, (int(kp_Optics[0]*downscale_factor), int(kp_Optics[1]*downscale_factor)), radius, color_points, -1)
    cv.imwrite(Mypath.output_registration_dir+"Alignement_point_Optics.png",cv.cvtColor(np_Optics_img,cv.COLOR_BGR2RGB))

    #Create output image
    max_shape = (np.maximum(np_Optics_img.shape[0],np_MRI_projection.shape[0]), np.maximum(np_MRI_projection.shape[1],np_Optics_img.shape[1]))
    display = np.zeros((max_shape[0],2*max_shape[1],3))

    display[:,0:max_shape[1]] = cv.resize(np_MRI_projection,(max_shape[1],max_shape[0]))
    display[:,max_shape[1]:] = cv.resize(np_Optics_img,(max_shape[1],max_shape[0]))


    
    return "Success", display.astype(np.uint8)
    

def get_registration_result_dir(Mypath = Paths(), params=Params(), create_dir = False, id_kp = -1):
    
    
    #Create registration result directory
    result_dir = Mypath.output_registration_dir
    
    if params.registration_type == "Multi metric":
        result_dir += "Mutli_metric_image/"
    
    if params.registration_type == "Skeleton":
        result_dir += "Skeleton/"
    
    if params.registration_type == "Frangi":
        result_dir += "Frangi_images/"

    if create_dir:
        if not os.path.exists(result_dir):
            os.mkdir(result_dir)
        
    
    result_dir += "Optics_thresh_"+str(params.thresh_optics)+"/"
    
    if create_dir:
        if not os.path.exists(result_dir):
            os.mkdir(result_dir)

    if id_kp != -1:
        result_dir += str(id_kp)+"/"
        if create_dir:
            if not os.path.exists(result_dir):
                os.mkdir(result_dir)
       
    return result_dir




def process_Optics_to_MRI_registration_1Kpt(result_dir, suffix_out_optics,
                                            kp_MRI_phys, kp_Optics_phys, kp_Optics,
                                            parameter_filename, angles,
                                            Mypath = Paths(), params = Params()):


    BV_segmentation_dir = Mypath.output_BV_segmentation_dir
    Optics_BV_segmentation_dir = BV_segmentation_dir+"Optics_thresh_"+str(params.thresh_optics)+"/"
    MRI_projection_dir = Mypath.output_MRI_projection_dir

    #Image filenames
    filename_MRI_Frangi = BV_segmentation_dir+"T1_proj_enhanced.nii.gz"
    filename_MRI_Frangi_masked = BV_segmentation_dir+"T1_proj_enhanced_masked.nii.gz"
    filename_optics_Frangi =Optics_BV_segmentation_dir +"optics_enhanced"+suffix_out_optics+".nii.gz"

    filename_MRI_skeleton = BV_segmentation_dir+"T1_proj_skeleton.nii.gz"
    filename_optics_skeleton = Optics_BV_segmentation_dir+"optics_skeleton"+suffix_out_optics+".nii.gz"

    filename_optics_signed_distance = Optics_BV_segmentation_dir +"optics_signed_distance"+suffix_out_optics+".nii.gz"
    filename_MRI_signed_distance = BV_segmentation_dir +"MRI_signed_distance.nii.gz"

    #if params.mask_MRI_hemisphere:
    #    prefix = "Hemisphere_"
    #else:
    #    prefix = ""
    #filename_mask_MRI = MRI_projection_dir+prefix+"Mask_Proj_MRI.nii.gz"
    filename_mask_MRI = MRI_projection_dir+"Mask_Proj_MRI_around_tumor.nii.gz"
    filename_mask_optics = Mypath.main_path_optics+"mask.png"


    # kp_MRI_phys = kpts_MRI_tumor_phys[id_kp_MRI]
    # kp_MRI = kpts_MRI_tumor[id_kp_MRI]


    #Change origin of optics slice to match keypoint
    change_origin(filenames_MRI= [filename_MRI_skeleton, filename_mask_MRI, filename_MRI_signed_distance, filename_MRI_Frangi, filename_MRI_Frangi_masked],
                filenames_optics= [filename_optics_skeleton, filename_optics_signed_distance, filename_optics_Frangi],
                kpt_Optics= kp_Optics_phys,
                kpt_MRI= kp_MRI_phys)


    #In the parameter file, change the center of rotation (set origin of optics image)
    replace_line_in_file(file_path=parameter_filename,
                        key='(CenterOfRotationPoint',
                        new_string="(CenterOfRotationPoint "+str(kp_MRI_phys[0])+" "+str(kp_MRI_phys[1])+")"+'\n')



    #Image filenamess with origin changed
    filename_MRI_skeleton = filename_MRI_skeleton.split('.')[0]+"_origin_changed.nii.gz"
    filename_mask_MRI = filename_mask_MRI.split('.')[0]+"_origin_changed.nii.gz"
    filename_MRI_signed_distance = filename_MRI_signed_distance.split('.')[0]+"_origin_changed.nii.gz"
    filename_MRI_Frangi_masked = filename_MRI_Frangi_masked.split('.')[0]+"_origin_changed.nii.gz"

    filename_optics_skeleton = filename_optics_skeleton.split('.')[0]+"_origin_changed.nii.gz"
    filename_optics_signed_distance = filename_optics_signed_distance.split('.')[0]+"_origin_changed.nii.gz"
    filename_optics_Frangi = filename_optics_Frangi.split('.')[0]+"_origin_changed.nii.gz"

    MRI_proj_skeleton = itk.imread(filename_MRI_skeleton,itk.F)
    Optics_img_skeleton = itk.imread(filename_optics_skeleton,itk.F)

    MRI_proj_Frangi = itk.imread(filename_MRI_Frangi_masked,itk.F)
    Optics_img_Frangi = itk.imread(filename_optics_Frangi,itk.F)
    
    mask_MRI = itk.imread(filename_mask_MRI,itk.UC)
    np_mask_MRI = itk.GetArrayFromImage(mask_MRI)

    np_mask_optics = cv.imread(filename_mask_optics,cv.IMREAD_ANYCOLOR)/255

    # mask_optics = itk.imread(filename_mask_optics)
    # np_mask_optics = itk.GetArrayFromImage(mask_optics)

    Optics_signed_distance = itk.imread(filename_optics_signed_distance,itk.F)
    MRI_signed_distance = itk.imread(filename_MRI_signed_distance,itk.F)


    #Get resolution
    res_mri_in_mm = np.min(MRI_proj_skeleton.GetSpacing())
    res_opt_in_mm = float(np.loadtxt(Mypath.main_path_optics+"resolution.txt"))


    metric = []
    NCC_val = []
    overlap = []

    for angle in angles:

        #rotate image
        rotated_optics_skeleton = optics_itk_rotation_2D(angle, Optics_img_skeleton, MRI_proj_skeleton, kp_Optics, kp_MRI_phys)
        rotated_optics_signed_distance = optics_itk_rotation_2D(angle, Optics_signed_distance, MRI_proj_skeleton, kp_Optics, kp_MRI_phys)
        rotated_optics_Frangi = optics_itk_rotation_2D(angle, Optics_img_Frangi, MRI_proj_skeleton, kp_Optics, kp_MRI_phys)


        #Apply registration
        if params.registration_type == "Multi metric":
            registered_vol, params_transform = optics_to_MRI_slices_registration_multi_metric_multi_images(fixed_skeleton = MRI_proj_skeleton,
                                                                                                    fixed_signed_distance = MRI_signed_distance,
                                                                                                    moving_skeleton=rotated_optics_skeleton,
                                                                                                    moving_signed_distance=rotated_optics_signed_distance,
                                                                                                    fixed_mask=mask_MRI,
                                                                                                    output_log_dir=result_dir,
                                                                                                    parameter_file=parameter_filename,
                                                                                                    output_filename="registration_out"+suffix_out_optics+".txt",
                                                                                                    log_to_console= False)

        if params.registration_type == "Skeleton":
            registered_vol, params_transform = optics_to_MRI_slices_registration(fixed_img = MRI_proj_skeleton,
                                                                                moving_img = rotated_optics_skeleton,
                                                                                fixed_mask = mask_MRI,
                                                                                output_log_dir=result_dir,
                                                                                output_filename="registration_out"+suffix_out_optics+".txt",
                                                                                log_to_console= False)
            
        if params.registration_type == "Frangi":
            registered_vol, params_transform = optics_to_MRI_slices_registration(fixed_img = MRI_proj_Frangi,
                                                                                moving_img = rotated_optics_Frangi,
                                                                                fixed_mask = mask_MRI,
                                                                                output_log_dir=result_dir,
                                                                                output_filename="registration_out"+suffix_out_optics+".txt",
                                                                                log_to_console= False)
                            
        
        if registered_vol !=None and params_transform != None:
            
            # Calculate NCC between MRI and registered optical skeleton
            NCC_val.append(itk_metric_value_fixed_space(itk.NormalizedCorrelationImageToImageMetric, MRI_proj_skeleton,  registered_vol))

            #Apply transform to optical mask
            mask_reg = Project_Optical_img_on_MRI_projection(np_mask_optics,
                                                                    np_mask_optics,
                                                                    angle,
                                                                    MRI_proj_skeleton.GetSpacing(),
                                                                    res_mri_in_mm,
                                                                    res_opt_in_mm,
                                                                    kp_Optics,
                                                                    kp_MRI_phys,
                                                                    params_transform,
                                                                    params.use_upscaled_images).astype(np.uint8)
            
            #Dilate masg reg
            mask_reg[mask_reg>0] =255
            mask_reg = mask_reg.astype(np.uint8)
            ksize=3
            kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(ksize,ksize))
            mask_reg = cv.morphologyEx(mask_reg, op=cv.MORPH_DILATE, kernel=kernel)

            #Calculate mask overlap
            overlap_mask_mri_optics_reg = overlap_coefficient(np_mask_MRI,mask_reg)
            overlap.append(float(params.alpha_custom_metric*(1-overlap_mask_mri_optics_reg)))
            

            metric.append(get_final_registration_metrics(result_dir + "/registration_out"+suffix_out_optics+".txt", "Final metric value"))
        
        else:
            NCC_val.append(np.nan)
            overlap.append(np.nan)
            metric.append(np.nan)
    
    NCC_val = np.asarray(NCC_val)
    overlap = np.asarray(overlap)
    metric = np.asarray(metric)
                          
    return metric, NCC_val, overlap, registered_vol, params_transform

def main_Optics_to_MRI_registration(Mypath = Paths(), params=Params()):

    # #get skeleton vessel in MRI
    # error = main_get_vessels_in_MRI(Mypath, params)
    # if error != "Success":
    #     return error
    
    # error = main_get_vessels_in_optics(Mypath, params)
    # if error != "Success":
    #     return error
    
    

    #Set path
    main_path_optics = Mypath.main_path_optics
    MRI_projection_dir = Mypath.output_MRI_projection_dir
    BV_segmentation_dir = Mypath.output_BV_segmentation_dir
    Optics_BV_segmentation_dir = BV_segmentation_dir+"Optics_thresh_"+str(params.thresh_optics)+"/"


    # Load registration parameter file
    if params.registration_type == "Multi metric":
        # parameter_filename = '../data/parameters_Similarity_slice_fixed_rotation_multi_metric_image.txt'
        parameter_filename = '../data/parameters_Similarity_slice_fixed_rotation.txt'

    if params.registration_type == "Skeleton":
        parameter_filename = '../data/parameters_Similarity_slice_fixed_rotation.txt'

    if params.registration_type == "Frangi":
        parameter_filename = '../data/parameters_Similarity_slice_fixed_rotation_Mutual_Information.txt'


    #Load initial optical image
    filename_initial_img_optics = main_path_optics+"initial_img.png"
    if not os.path.exists(filename_initial_img_optics):
        return "[main_Optics_to_MRI_registration] Optical initial image is missing"

    #Check if optical imaging is RGB or HSI
    _,suffix_out_optics = is_RGB_optical_image(filename_initial_img_optics)



    #Load volumes
    filename_MRI = BV_segmentation_dir+"T1_proj_skeleton.nii.gz"
    prefix = ""
    if params.mask_MRI_hemisphere:
        prefix = "Hemisphere_"
       
    #filename_mask_MRI = MRI_projection_dir+prefix+"Mask_Proj_MRI.nii.gz"
    filename_mask_MRI = Mypath.output_MRI_projection_dir+"Mask_Proj_MRI_around_tumor.nii.gz"

    filename_MRI_signed_distance = BV_segmentation_dir +"MRI_signed_distance.nii.gz"

    filename_optics = Optics_BV_segmentation_dir+"optics_skeleton"+suffix_out_optics+".nii.gz"
    filename_mask_otpics = Optics_BV_segmentation_dir+"optics_mask"+suffix_out_optics+".nii.gz"
    filename_optics_signed_distance = Optics_BV_segmentation_dir +"optics_signed_distance"+suffix_out_optics+".nii.gz"

    filename_tumor = MRI_projection_dir+"Mask_Proj_Tumor.nii.gz"


    if not os.path.exists(filename_MRI):
        return ("[main_Optics_to_MRI_registration] MRI skeleton is missing")

    if not os.path.exists(filename_optics):
        return ("[main_Optics_to_MRI_registration] Optics skeleton is missing")

    if not os.path.exists(filename_tumor):
        return ("[main_Optics_to_MRI_registration] Mask tumor proj is missing")

    if not os.path.exists(filename_mask_MRI):
        return ("[main_Optics_to_MRI_registration] mask proj MRI is missing")

    if not os.path.exists(filename_mask_otpics):
        return ("[main_Optics_to_MRI_registration] Optics mask is missing")

    if not os.path.exists(filename_MRI_signed_distance):
        return ("[main_Optics_to_MRI_registration] MRI signed distance is missing")

    if not os.path.exists(filename_optics_signed_distance):
        return ("[main_Optics_to_MRI_registration] Optics signed distance is missing")

    if not os.path.exists(parameter_filename):
        return ("[main_Optics_to_MRI_registration] Parameter file is missing")


    

    # Load itk volumes
    MRI_proj = itk.imread(filename_MRI,itk.UC)
    mask_MRI = itk.imread(filename_mask_MRI,itk.UC)
    Optics_img = itk.imread(filename_optics,itk.UC)
    Optical_mask=  itk.imread(filename_mask_otpics,itk.UC)
    mask_tumor = itk.imread(filename_tumor,itk.UC)



    #Get MRI and optics alignement keypoints
    kp_Optics, kp_Optics_phys, _kpts_MRI_tumor, _kpts_MRI_tumor_phys = get_alignment_points(Optical_mask, Optics_img,
                                                                                            MRI_proj, mask_tumor, 
                                                                                            params.kpts_MRI_tumor, params.kpt_optics,
                                                                                            space_between_kpt_mm= params.space_between_kpt_mm,
                                                                                            enlarge_tumor_roi_factor=params.tumor_ROI_enlarge_factor)

    #Get alignement points in skeleton
    # kp_Optics, kp_Optics_phys, _kpts_MRI_tumor, _kpts_MRI_tumor_phys = get_alignement_points_in_skeleton(MRI_proj, Optics_img, Optical_mask, mask_tumor, params.MRI_keypoints_nb)

    kpts_MRI_tumor = _kpts_MRI_tumor
    kpts_MRI_tumor_phys = _kpts_MRI_tumor_phys

    #Get numpy arays
    # np_MRI_projection = itk.GetArrayFromImage(MRI_proj)
    # np_Optics_img = itk.GetArrayFromImage(Optics_img)
    # np_mask_MRI = itk.GetArrayFromImage(mask_MRI)

    # plt.figure(figsize=(20,20))
    # plt.subplot(131)
    # plt.imshow(np_MRI_projection)
    # for i in range(len(kpts_MRI_tumor)):
    #     plt.scatter(kpts_MRI_tumor[i][0],kpts_MRI_tumor[i][1],color='r')
    # plt.subplot(132)
    # plt.imshow(np_mask_MRI)
    # plt.subplot(133)
    # plt.imshow(np_Optics_img)
    # plt.scatter(kp_Optics[0],kp_Optics[1],color='r')
    # plt.show()


    angles = np.arange(0,360)



    #Loop over keypoints
    for id_kp_MRI in range(len(kpts_MRI_tumor_phys)):
  
        #Create registration result directory
        result_dir = get_registration_result_dir(Mypath, params, create_dir = True, id_kp=id_kp_MRI)

    
        #Select MRI keypoint
        kp_MRI_phys = kpts_MRI_tumor_phys[id_kp_MRI]
        kp_MRI = kpts_MRI_tumor[id_kp_MRI]

        metric, NCC_val, overlap, _, _ = process_Optics_to_MRI_registration_1Kpt(result_dir, suffix_out_optics,
                                            kp_MRI_phys, kp_Optics_phys, kp_Optics,
                                            parameter_filename, angles, Mypath, params)

        custom_metric = NCC_val + overlap
        if not np.all(np.isnan(metric)):
            #save registration metric
            np.savetxt(result_dir +"/metrics"+suffix_out_optics+".txt",metric)
            np.savetxt(result_dir +"/NCC"+suffix_out_optics+".txt",NCC_val)
            np.savetxt(result_dir +"/overlap"+suffix_out_optics+".txt",overlap)
            np.savetxt(result_dir +"/custom_metrics"+suffix_out_optics+".txt",custom_metric)

            #Get best match
            best_angle = np.nanargmin(metric)


            _, _, _, registered_vol, params_transform = process_Optics_to_MRI_registration_1Kpt(result_dir, suffix_out_optics,
                                        kp_MRI_phys, kp_Optics_phys, kp_Optics,
                                        parameter_filename, np.array([best_angle]), Mypath, params)

            #Write registered skeleton
            filename_reg = result_dir +"/registered_proj_" + str(best_angle) +suffix_out_optics+".nii.gz"
            itk.imwrite(registered_vol,filename_reg)
            itk.elxParameterObjectPython.elastixParameterObject_WriteParameterFile(params_transform,result_dir + "/Registration_params"+suffix_out_optics+".txt") 

            #Write registration params    
            reg_params = Registration_Params()
            reg_params.angle = int(best_angle)
            reg_params.registration_metric = float(metric[best_angle])

            reg_params.MRI_kpt = [int(kp_MRI[0]),int(kp_MRI[1])]
            reg_params.MRI_kpt_phys = [float(kp_MRI_phys[0]), float(kp_MRI_phys[1])]
            reg_params.Optics_kpt = [int(kp_Optics[0]),int(kp_Optics[1])]
            reg_params.Optics_kpt_phys = [float(kp_Optics_phys[0]),float(kp_Optics_phys[1])]
            
            reg_params.save(result_dir+"/Reg_params.json")


        if not np.all(np.isnan(custom_metric)):
            
            #Get best match
            best_angle = np.nanargmin(custom_metric)
            
            _, _, _, registered_vol, params_transform = process_Optics_to_MRI_registration_1Kpt(result_dir, suffix_out_optics,
                                                    kp_MRI_phys, kp_Optics_phys, kp_Optics,
                                                    parameter_filename, np.array([best_angle]), Mypath, params)


            #Write registered skeleton (custom metric)
            filename_reg = result_dir +"/registered_proj_custom_metric_" + str(best_angle) +suffix_out_optics+".nii.gz"
            itk.imwrite(registered_vol,filename_reg)
            itk.elxParameterObjectPython.elastixParameterObject_WriteParameterFile(params_transform,result_dir + "/Registration_params_custom_metric"+suffix_out_optics+".txt") 

            #Write registration params
            reg_params = Registration_Params()    
            reg_params.angle = int(best_angle)
            reg_params.registration_metric = float(custom_metric[best_angle])

            reg_params.MRI_kpt = [int(kp_MRI[0]),int(kp_MRI[1])]
            reg_params.MRI_kpt_phys = [float(kp_MRI_phys[0]), float(kp_MRI_phys[1])]
            reg_params.Optics_kpt = [int(kp_Optics[0]),int(kp_Optics[1])]
            reg_params.Optics_kpt_phys = [float(kp_Optics_phys[0]),float(kp_Optics_phys[1])]
            
            reg_params.save(result_dir+"/Reg_params_custom_metric.json")

    #Show registration for the minimal metric
    # open_itksnap_with_overlay(filename_MRI, filename_reg)

    return "Success"


def get_best_MRI_keypoint(Mypath = Paths(), params = Params()):

    #Get result directory for all keypoints
    result_dir = get_registration_result_dir(Mypath, params)
    result_dirs = glob.glob(result_dir+"*")

    labels = []

    #Multi metric
    metric = []

    if params.use_custom_registration_metric:
        param_file_name = "Reg_params_custom_metric.json"
    else:
        param_file_name = "Reg_params.json"

    file_exists = False

    for dir in result_dirs:
        if os.path.exists(dir+"/"+param_file_name):
            reg_params = Registration_Params.load(dir+"/"+param_file_name)
            metric.append(reg_params.registration_metric)
            file_exists = True
            labels.append(os.path.basename(dir))
    
    if not file_exists:
        return "[get_best_MRI_keypoint] Registration json file does not exists", -1
    
    
    metric = np.asarray(metric)
    label_idx = os.path.basename(labels[metric.argmin()])
    print("[get_best_MRI_keypoint] best MRI kpt is ", label_idx)

    return "Success", label_idx



def plot_registration_results(Mypath = Paths(), params=Params()):

    #data directory
    main_path_optics = Mypath.main_path_optics
    BV_segmentation_dir = Mypath.output_BV_segmentation_dir


    #Get best registration result
    error,label_MRI_ktp = get_best_MRI_keypoint(Mypath, params)
    if error != "Success":
        return error, None

    #Get full directory
    result_dir = get_registration_result_dir(Mypath, params)
    result_dir += label_MRI_ktp+"/"



    #Load initial optical image
    filename_initial_img_optics = main_path_optics+"initial_img.png"
    if not os.path.exists(filename_initial_img_optics):
        return "Optical initial image is missing",None

    #Check if optical imaging is RGB or HSI
    _,suffix_out_optics = is_RGB_optical_image(filename_initial_img_optics)


    #Load registration params
    if params.use_custom_registration_metric:
        suffix = "_custom_metric"
    else:
        suffix = ""
        
    filename_params_json = result_dir+"Reg_params"+suffix+".json"

    if not os.path.exists(filename_params_json):
        return "[plot_registration_results] json registrayion file is missing",None
    
    reg_params = Registration_Params.load(filename_params_json)
    angle = reg_params.angle
    


    if params.registration_type == "Skeleton" or params.registration_type == "Multi metric":

        #Set MRI and optical filenames
        filename_MRI = BV_segmentation_dir+"T1_proj_skeleton_origin_changed.nii.gz"
        filename_reg = result_dir +"registered_proj" + suffix+ "_" + str(angle) +suffix_out_optics+".nii.gz"
        if not os.path.exists(filename_MRI):
            return "[plot_registration_results] 2 MRI skeleton file is missing",None
        
        if not os.path.exists(filename_reg):
            return "[plot_registration_results] 2 Registered optical image is missing",None
        

        #Load images
        mri = itk.GetArrayFromImage(itk.imread(filename_MRI))*255
        optics = itk.GetArrayFromImage(itk.imread(filename_reg))

        
        #Threshold optical image
        thresh = 0.1
        optics[optics>thresh] = 255
        optics[optics<=thresh] = 0
        optics = cv.ximgproc.thinning(optics.astype(np.uint8))


        #Dilate MRI data for display
        # ksize=3
        # kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(ksize,ksize))
        # mri = cv.morphologyEx(mri, op=cv.MORPH_DILATE, kernel=kernel)*255

        #Display
        display_img = np.zeros((optics.shape[0],optics.shape[1],3))
        display_img[:,:,0] = mri
        display_img[:,:,2] = optics
        display_img = display_img.astype(np.uint8)


    if params.registration_type == "Frangi":


        #Set MRI and optical filenames
        filename_MRI = BV_segmentation_dir+"T1_proj_enhanced_origin_changed.nii.gz"
        filename_reg = result_dir +"registered_proj"+suffix+"_" + str(angle) +suffix_out_optics+".nii.gz"

        if not os.path.exists(filename_MRI):
            return "[plot_registration_results] 2 MRI frangi image file is missing",None
        
        if not os.path.exists(filename_reg):
            return "[plot_registration_results] 2Registered optical image is missing",None
        

        #Load images
        mri = itk.GetArrayFromImage(itk.imread(filename_MRI))
        np_result_reg = itk.GetArrayFromImage(itk.imread(filename_reg))

        
        np_result_reg = 255*((np_result_reg-np_result_reg.min())/(np_result_reg.max() - np_result_reg.min()))
        np_result_reg = np_result_reg.astype(np.uint8)

        display_img = np.zeros((np_result_reg.shape[0],np_result_reg.shape[1],3),dtype=np.uint8)
        display_img[:,:,0] = mri
        display_img[:,:,2] = np_result_reg

    # plt.subplot(122)
    # plt.title("MRI (red) and registered optical skeletons (blue)")
    # plt.imshow(cv.cvtColor(display_img,cv.COLOR_BGR2RGB))
    # plt.show()

    cv.imwrite(result_dir+"overlay_res_reg.png",display_img)




    #Show registration for the minimal metric
    # open_itksnap_with_overlay(filename_MRI, filename_reg)

    return "Success",display_img





def project_optical_image_on_MRI(Mypath = Paths(), params=Params(), result_dir="", optical_img_to_project = None):

    #data directory
    main_path_optics = Mypath.main_path_optics
    MRI_projection_dir = Mypath.output_MRI_projection_dir




    #Check if optical imaging is RGB or HSI
    filename_optics = main_path_optics+"initial_img.png"
    if not os.path.exists(filename_optics):
        return "[project_optical_image_on_MRI] Optical image is missing", None

    _,suffix_out_optics = is_RGB_optical_image(filename_optics)


    #filename MRI images
    filename_MRI_proj = MRI_projection_dir+"Proj_MRI.nii.gz"

    #filename optical images
    filename_optics_mask = main_path_optics+"mask.png"

    #Filename registration params
    if params.use_custom_registration_metric:
        filename_params_reg = result_dir +"/Registration_params_custom_metric"+suffix_out_optics+".txt"
    else:
        filename_params_reg = result_dir +"/Registration_params"+suffix_out_optics+".txt"



    if not os.path.exists(filename_MRI_proj):
        return "[project_optical_image_on_MRI] MRI proj is missing", None

    if not os.path.exists(filename_optics_mask):
        return "[project_optical_image_on_MRI] Optical mask is missing", None

    if not os.path.exists(filename_params_reg):
        return "[project_optical_image_on_MRI] Registration param file is missing", None

    if not os.path.exists(main_path_optics+"resolution.txt"):
        return "[project_optical_image_on_MRI] Optical resolution file is missing", None



    #####################################################################
    # Get angle from moving optical image used to calculate the transform
    #####################################################################

    #Load registration params
    if params.use_custom_registration_metric:
        filename_Reg_param = result_dir+"/Reg_params_custom_metric.json"
    else:
        filename_Reg_param = result_dir+"/Reg_params.json"

    if not os.path.exists(filename_Reg_param):
        return "[project_optical_image_on_MRI] registration param json file is missing", None
    
    
    reg_params = Registration_Params.load(filename_Reg_param)
    angle = reg_params.angle
    kp_Optics = reg_params.Optics_kpt
    kp_Optics_phys = reg_params.Optics_kpt_phys
    kp_MRI = reg_params.MRI_kpt
    kp_MRI_phys = reg_params.MRI_kpt_phys


    ########################################
    # Load data
    #######################################


    # Load images
    mask = cv.imread(filename_optics_mask,cv.IMREAD_ANYCOLOR)/255
    MRI_proj = itk.imread(filename_MRI_proj)



    ########################################
    # Apply transform to optical image
    ########################################

    #Get resolution
    res_mri_in_mm = np.min(MRI_proj.GetSpacing())
    res_opt_in_mm = float(np.loadtxt(main_path_optics+"resolution.txt"))

    #Load param transform
    params_transform_reg = itk.ParameterObject.New()
    params_transform_reg.AddParameterFile(filename_params_reg)



    if params.use_upscaled_images:
        #Calculate scaling factors
        x_factor = MRI_proj.GetSpacing()[0]/res_opt_in_mm
        y_factor = MRI_proj.GetSpacing()[1]/res_opt_in_mm
        
        #change transform parameter
        params_transform_reg = calculate_upscaled_Parameter_file(params_transform_reg,
                                                                x_factor, y_factor)


    #Apply transform to optical mask
    np_optical_img_registered = Project_Optical_img_on_MRI_projection(optical_img_to_project,
                                                                    mask,
                                                                    angle,
                                                                    MRI_proj.GetSpacing(),
                                                                    res_mri_in_mm,
                                                                    res_opt_in_mm,
                                                                    kp_Optics,
                                                                    kp_MRI_phys,
                                                                    params_transform_reg,
                                                                    params.use_upscaled_images).astype(np.uint8)






    return "Success", np_optical_img_registered






def main_project_optical_image_on_MRI(Mypath = Paths(), params=Params()):

    #data directory
    main_path_optics = Mypath.main_path_optics
    MRI_projection_dir = Mypath.output_MRI_projection_dir
    BV_segmentation_dir = Mypath.output_BV_segmentation_dir
    Optics_BV_segmentation_dir = BV_segmentation_dir+"Optics_thresh_"+str(params.thresh_optics)+"/"


    output_dir = Mypath.output_dir

    # colormap_stats_optics = cv.COLORMAP_PLASMA
    colormap_stats_optics = cv.COLORMAP_JET

    #Get best registration result
    error,label_MRI_ktp = get_best_MRI_keypoint(Mypath, params)
    if error != "Success":
        return error
    
    #Get registration result directory
    result_dir = get_registration_result_dir(Mypath, params)
    result_dir += label_MRI_ktp+"/"



    #Check if optical imaging is RGB or HSI
    filename_optics = main_path_optics+"initial_img.png"
    if not os.path.exists(filename_optics):
        return ("[main_project_optical_image_on_MRI] Optical image is missing")

    _,suffix_out_optics = is_RGB_optical_image(filename_optics)


    #filename MRI images
    filename_MRI_proj = MRI_projection_dir+"Proj_MRI.nii.gz"
    filename_fMRI_stats_proj = glob.glob(output_dir+"fMRI/inferences/rotated/*_Mask_proj.nii.gz")
    filename_MRI_enhanced_proj = BV_segmentation_dir +"MRI_proj_enhanced.png"


    #filename optical images
    filename_optics_mask = main_path_optics+"mask.png"
    filename_optics_stats = glob.glob(main_path_optics + "foptics/*.txt")


    

    if not os.path.exists(filename_MRI_proj):
        return ("[main_project_optical_image_on_MRI] MRI projection is missing")

    if not os.path.exists(filename_optics_mask):
        return ("[main_project_optical_image_on_MRI] Optical mask is missing")

    if not os.path.exists(main_path_optics+"resolution.txt"):
        return ("[main_project_optical_image_on_MRI] Optical resolution file is missing")

    if not os.path.exists(result_dir+"/metrics"+suffix_out_optics+".txt"):
        return ("[main_project_optical_image_on_MRI] Registration metric is missing")

    if not os.path.exists(filename_MRI_enhanced_proj):
        return ("[main_project_optical_image_on_MRI] MRI proj enhanced is missing")

    if not os.path.exists(main_path_optics+"resolution.txt"):
        return "[main_project_optical_image_on_MRI] Optics resolution file is missing"


    ########################################
    # Create saving directory
    #######################################

    # Saving directory
    saving_dir = output_dir + "Projection/"
    if not os.path.exists(saving_dir):
        os.mkdir(saving_dir)



    ########################################
    # Load data
    #######################################


    # Load images
    img = cv.imread(filename_optics,cv.IMREAD_ANYCOLOR)
    mask = cv.imread(filename_optics_mask,cv.IMREAD_ANYCOLOR)/255
    MRI_proj = itk.imread(filename_MRI_proj)
    np_MRI_proj_enhanced = cv.imread(filename_MRI_enhanced_proj,cv.IMREAD_GRAYSCALE)

    res_opt_in_mm = float(np.loadtxt(main_path_optics+"resolution.txt"))


    ########################################
    # Apply transform to optical mask
    ########################################

    # Apply transform
    error, np_optics_mask_registered =  project_optical_image_on_MRI(Mypath, params, result_dir, mask)
    if error != "Success":
        return error
    
    #Apply closing
    np_optics_mask_registered[np_optics_mask_registered>0.01] = 1
    ksize = 5
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(ksize,ksize))
    np_optics_mask_registered = cv.morphologyEx(np_optics_mask_registered, op=cv.MORPH_CLOSE, kernel=kernel)


    #Create contour of surgical window
    np_surgical_window = np.zeros(np_optics_mask_registered.shape)
    contours, hierarchy = cv.findContours(np_optics_mask_registered.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cv.drawContours(np_surgical_window, contours, -1, (1), 1)



    ########################################
    # Apply transform to the optical image
    ########################################

    np_optics_vol_registered = []
    if img.ndim>2: #If the initial image is RGB
        for c in range(img.shape[2]):
            error, temp = project_optical_image_on_MRI(Mypath, params, result_dir, img[:,:,c])
            if error != "Success":
                return error
            np_optics_vol_registered.append(temp*np_optics_mask_registered)

    else: #else create grayscale image
        error, temp = project_optical_image_on_MRI(Mypath, params, result_dir, img)
        if error != "Success":
            return error
        np_optics_vol_registered.append(temp*np_optics_mask_registered)
        np_optics_vol_registered.append(temp*np_optics_mask_registered)
        np_optics_vol_registered.append(temp*np_optics_mask_registered)
            

    #Reshape registred volume to match the colorspace of the initial image
    res_optical_image = np.stack(np_optics_vol_registered, axis=-1)
    res_optical_image = res_optical_image.astype(np.uint8)






    ########################################
    # Apply transform to the Optical stats maps
    ########################################

    
    np_optics_stats_color = []
    np_optics_stats_mask = []
    for file_stats_optics in filename_optics_stats:
        #Load stats map
        Optical_stats = np.loadtxt(file_stats_optics)
        Optical_stats_mask = 255*(Optical_stats != 0).astype(np.uint8)

        #Project in MRI space
        error, proj = project_optical_image_on_MRI(Mypath, params, result_dir, Optical_stats)
        if error != "Success":
            return error
        
        error, stats_mask = project_optical_image_on_MRI(Mypath, params, result_dir, Optical_stats_mask)
        if error != "Success":
            return error
            
        #Get stat mask
        stats_mask[stats_mask>0.01] = 1
        stats_mask = stats_mask*np_optics_mask_registered
        # ksize = 1
        # kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(ksize,ksize))
        # stats_mask = cv.morphologyEx(stats_mask, op=cv.MORPH_OPEN, kernel=kernel)
        # ksize = 2
        # kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(ksize,ksize))
        # stats_mask = cv.morphologyEx(stats_mask, op=cv.MORPH_CLOSE, kernel=kernel)

        np_optics_stats_mask.append(stats_mask)

        #get centered uint values
        proj = (255*(proj-proj.min())/(proj.max() - proj.min()))
        proj = proj*stats_mask


        #Apply colormap to stats mask
        stats_color = cv.applyColorMap(proj.astype(np.uint8), colormap_stats_optics)
        for i in range(stats_color.shape[2]):
            stats_color[:,:,i] *= stats_mask.astype(np.uint8)

        np_optics_stats_color.append(stats_color)





    ########################################
    # MRI Projection
    ########################################

    #Normalize MRI projection
    np_MRI_proj = itk.GetArrayFromImage(MRI_proj)
    np_MRI_proj = (255*(np_MRI_proj-np_MRI_proj.min())/(np_MRI_proj.max() - np_MRI_proj.min())).astype(np.uint8)
    np_MRI_proj = cv.medianBlur(np_MRI_proj,3)

    #Change colorspace of MRI projections
    # np_MRI_proj_enhanced = cv.applyColorMap(np_MRI_proj_enhanced, cv.COLORMAP_PLASMA)
    np_MRI_proj_enhanced = cv.cvtColor(np_MRI_proj_enhanced,cv.COLOR_GRAY2BGR)
    # np_MRI_proj = cv.applyColorMap(np_MRI_proj, cv.COLORMAP_PLASMA)
    np_MRI_proj = cv.cvtColor(np_MRI_proj,cv.COLOR_GRAY2BGR)

    if params.use_upscaled_images:
        #Calculate scaling factors
        x_factor = MRI_proj.GetSpacing()[0]/res_opt_in_mm
        y_factor = MRI_proj.GetSpacing()[1]/res_opt_in_mm
        
        new_width = int(np_MRI_proj.shape[1]*x_factor)
        new_height = int(np_MRI_proj.shape[0]*y_factor)
        np_MRI_proj = cv.resize(np_MRI_proj,(new_width,new_height))
        np_MRI_proj_enhanced = cv.resize(np_MRI_proj_enhanced,(new_width,new_height))

    weight = 0.2
    display_RGB = res_optical_image.copy() 
    display = merge_two_colored_img(np_MRI_proj, display_RGB,np_optics_mask_registered,0)
    display2 = merge_two_colored_img(np_MRI_proj_enhanced, display_RGB,np_optics_mask_registered,weight)



    ########################################
    # Write projection results
    ########################################
    cv.imwrite(saving_dir+"Optical_img_projected_on_MRI"+suffix_out_optics+".png",display)
    cv.imwrite(saving_dir+"Optical_img_projected_on_MRI2"+suffix_out_optics+".png",display2)
    cv.imwrite(saving_dir+"RGB_registered_on_MRI"+suffix_out_optics+".png",res_optical_image)
    cv.imwrite(saving_dir+"optics_mask_registered_on_MRI"+suffix_out_optics+".png",np_optics_mask_registered)
    cv.imwrite(saving_dir+"MRI_proj.png",np_MRI_proj)
    cv.imwrite(saving_dir+"MRI_proj_enhanced.png",np_MRI_proj_enhanced)





    # Merge Optical image and optical stats
    if not os.path.exists(saving_dir+"foptics_"+suffix_out_optics+"/"):
        os.mkdir(saving_dir+"foptics_"+suffix_out_optics+"/")
    for i in range(len(np_optics_stats_color)):
        display_RGB = res_optical_image.copy() 
        display_RGB = merge_two_colored_img(res_optical_image, np_optics_stats_color[i],np_optics_stats_mask[i],weight)

        cv.imwrite(saving_dir+"foptics_"+suffix_out_optics+"/"+os.path.basename(filename_optics_stats[i]).split('.')[0]+"_merged.png", display_RGB)
        cv.imwrite(saving_dir+"foptics_"+suffix_out_optics+"/"+os.path.basename(filename_optics_stats[i]).split('.')[0]+"_colormap.png", np_optics_stats_color[i])
        cv.imwrite(saving_dir+"foptics_"+suffix_out_optics+"/"+os.path.basename(filename_optics_stats[i]).split('.')[0]+"_mask.png", np_optics_stats_mask[i]*255)
        
        


    #Add fMRI contours
    if not os.path.exists(saving_dir+"fMRI/"):
        os.mkdir(saving_dir+"fMRI/")
    for fMRI_file in filename_fMRI_stats_proj:
        fMRI_proj = itk.imread(fMRI_file,itk.UC)
        np_fMRI_proj = itk.GetArrayFromImage(fMRI_proj)
        np_fMRI_proj[np_fMRI_proj>0] = 255

        
        if params.use_upscaled_images:
            new_width = int(np_MRI_proj.shape[1])
            new_height = int(np_MRI_proj.shape[0])
            np_fMRI_proj = cv.resize(np_fMRI_proj,(new_width,new_height),interpolation=cv.INTER_NEAREST)
        
        cv.imwrite(saving_dir+"fMRI/"+os.path.basename(fMRI_file).split('.')[0]+".png",np_fMRI_proj)

    return "Success"


def main_plot_Optical_image_projected_on_MRI(Mypath = Paths()):
    
    main_path_optics = Mypath.main_path_optics
    output_dir = Mypath.output_dir
    
    saving_dir = output_dir + "Projection/"


    #Check if optical imaging is RGB or HSI
    filename_optics = main_path_optics+"initial_img.png"
    if not os.path.exists(filename_optics):
        return ("Optical image is missing"),None

    _,suffix_out_optics = is_RGB_optical_image(filename_optics)


    filename_res_optical_image = saving_dir+"RGB_registered_on_MRI"+suffix_out_optics+".png"
    filename_optics_mask_registered = saving_dir+"optics_mask_registered_on_MRI"+suffix_out_optics+".png"
    filename_MRI_proj = saving_dir+"MRI_proj.png"
    filename_MRI_proj_enhanced = saving_dir+"MRI_proj_enhanced.png"

    if not os.path.exists(filename_res_optical_image):
        return "Registered optical image is missing",None
    
    if not os.path.exists(filename_optics_mask_registered):
        return "Registered optical mask is missing",None
    
    if not os.path.exists(filename_MRI_proj):
        return "MRI projection is missing",None
    
    if not os.path.exists(filename_MRI_proj_enhanced):
        return "Enhanced MRI projection is missing",None

    weight = 0.2 
    res_optical_image = cv.imread(filename_res_optical_image)
    np_optics_mask_registered = cv.imread(filename_optics_mask_registered,cv.IMREAD_GRAYSCALE)
    np_MRI_proj = cv.imread(filename_MRI_proj)
    np_MRI_proj_enhanced = cv.imread(filename_MRI_proj_enhanced)



    ########################################
    # Display results - MRI projection and optics image
    ########################################
    display_RGB = res_optical_image.copy() 
    display = merge_two_colored_img(np_MRI_proj, display_RGB,np_optics_mask_registered,0)
    display2 = merge_two_colored_img(np_MRI_proj_enhanced, display_RGB,np_optics_mask_registered,weight)

    cv.imwrite(saving_dir+"Optical_img_projected_on_MRI"+suffix_out_optics+".png",display)
    cv.imwrite(saving_dir+"Optical_img_projected_on_MRI2"+suffix_out_optics+".png",display2)


    # plt.figure(figsize=(20,20))
    # plt.subplot(121)
    # plt.imshow(cv.cvtColor(display,cv.COLOR_BGR2RGB))
    # plt.subplot(122)
    # plt.imshow(cv.cvtColor(display2,cv.COLOR_BGR2RGB))
    # plt.show()


    display2 = cv.cvtColor(display2,cv.COLOR_BGR2RGB)
    return "Success",display2







def main_plot_fOptics_fMRI_stats_projected_on_MRI(Mypath = Paths(), _fMRI_filenames=[], _fOptics_filenames=[], colors_fMRI=[], colors_fOptics=[]):
    
    
    main_path_optics = Mypath.main_path_optics
    output_dir = Mypath.output_dir


    
    saving_dir = output_dir + "Projection/"

    #Check if optical imaging is RGB or HSI
    filename_optics = main_path_optics+"initial_img.png"
    if not os.path.exists(filename_optics):
        return ("Optical image is missing"), None

    _,suffix_out_optics = is_RGB_optical_image(filename_optics)

    dir_fMRI = output_dir + "Projection/fMRI/"
    dir_foptics = output_dir + "Projection/foptics_"+suffix_out_optics+"/"


    ########################################
    # Display results - MRI projection and optics image
    ########################################

    # Load images
    filename_in_img = saving_dir+"Optical_img_projected_on_MRI2"+suffix_out_optics+".png"

    if not os.path.exists(filename_in_img):
        return (os.path.basename(filename_in_img)+ " is missing"), None

    in_img = cv.imread(filename_in_img)


    fMRI_filenames = []
    for f in _fMRI_filenames:
        fMRI_filenames.append(dir_fMRI + "r_"+os.path.basename(f).split('.')[0]+"_Mask_proj.png")

    fOptics_filenames = []
    for f in _fOptics_filenames:
        fOptics_filenames.append(dir_foptics + os.path.basename(f).split('.')[0]+"_mask.png")


    #Load fMRI stats
    fMRI_stats = []
    for file in fMRI_filenames:
        if not os.path.exists(file):
            return (os.path.basename(file)+ " is missing"), None
        fMRI_stats.append(cv.imread(file,cv.IMREAD_ANYCOLOR))

    #Load foptics stats
    fOptics_stats = []
    for file in fOptics_filenames:
        if not os.path.exists(file):
            return (os.path.basename(file)+ " is missing"), None
        fOptics_stats.append(cv.imread(file,cv.IMREAD_ANYCOLOR)) 



    display = in_img.copy()
    #Draw fOptics contour
    width = 1
    for i, data in enumerate(fOptics_stats):
        c, hierarchy = cv.findContours(data.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        cv.drawContours(display,c,-1,colors_fOptics[i],width)

    for i,data in enumerate(fMRI_stats):
        c, hierarchy = cv.findContours(data.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        cv.drawContours(display,c,-1,colors_fMRI[i],width)





    cv.imwrite(saving_dir+"Overlay_fMRI_fOptics"+suffix_out_optics+".png",display)


    display = cv.cvtColor(display,cv.COLOR_BGR2RGB)

    return "Success",display





def main_reconstruct_Optics_volume(Mypath = Paths()):

    main_path_optics = Mypath.main_path_optics
    output_dir = Mypath.output_dir
    MRI_projection_dir = Mypath.output_MRI_projection_dir

    #Check if optical imaging is RGB or HSI
    filename_optics = main_path_optics+"initial_img.png"
    if not os.path.exists(filename_optics):
        return ("Optical image is missing")

    _,suffix_out_optics = is_RGB_optical_image(filename_optics)

    
    filename_optical_img_registered = output_dir + "Projection/RGB_registered_on_MRI.png"
    filename_optical_mask_registered = output_dir + "Projection/optics_mask_registered_on_MRI.png"
    fOptics_filenames = glob.glob(output_dir + "Projection/foptics_"+suffix_out_optics+"/*_mask.png")

    filename_vol_surface_rotated = MRI_projection_dir+'surface_mask_rotated.nii.gz'
    filename_vol_tumor_rotated = MRI_projection_dir+'Tumor_rotated.nii.gz'
    filename_MRI = output_dir + "r_T1_bet.nii.gz"
    filename_MRI_surface = output_dir+'surface_mask.nii.gz'

    filename_rotation_matrix = MRI_projection_dir+"Rotation_matrix_projection.txt"
    filename_translation_vector = MRI_projection_dir+"Translation_vector_projection.txt"


    if not os.path.exists(filename_rotation_matrix):
        return "[main_reconstruct_Optics_volume] Rotation matrix is missing"

    if not os.path.exists(filename_translation_vector):
       return "[main_reconstruct_Optics_volume]Translation vector is missing"
    
    if not os.path.exists(filename_optical_img_registered):
        return "[main_reconstruct_Optics_volume]Optical image registered on MRI is missing"
    
    if not os.path.exists(filename_optical_mask_registered):
        return "[main_reconstruct_Optics_volume]Surgical window mask is missing"
    
    if not os.path.exists(filename_vol_surface_rotated):
        return "[main_reconstruct_Optics_volume]Rotated surface file is missing"

    if not os.path.exists(filename_MRI):
        return "[main_reconstruct_Optics_volume] T1 bet volume is missing"

    if not os.path.exists(filename_MRI_surface):
        return "[main_reconstruct_Optics_volume] MRi surface mask is missing"



    ########################################
    # Load data
    #######################################

    #Load MRI data
    rotated_surface = itk.imread(filename_vol_surface_rotated, itk.F)
    rotated_tumor = itk.imread(filename_vol_tumor_rotated, itk.F)
    T1 = itk.imread(filename_MRI,itk.F)
    surface = itk.imread(filename_MRI_surface, itk.F)


    #Load Optical image registered on MR
    res_optical_image = cv.imread(filename_optical_img_registered,cv.IMREAD_ANYCOLOR)
    # Load surgical window mask
    np_surgical_window = cv.imread(filename_optical_mask_registered,cv.IMREAD_GRAYSCALE)*255

    #Load foptics stats
    fOptics_stats = []
    for file in fOptics_filenames:
        fOptics_stats.append(cv.imread(file,cv.IMREAD_GRAYSCALE)) 
















    #####################################################
    # Project the optical image on the rotated MRI volume
    #####################################################

    #Grayscale optics image
    np_Gray_optics = cv.cvtColor(res_optical_image,cv.COLOR_BGR2GRAY)
    reconstruct_Optical_img_on_MRI_volume(np_Gray_optics, rotated_surface, rotated_tumor, output_dir + "Projection/Rec_Optical_rotated"+suffix_out_optics+".nii.gz")
    #RGB optics image
    reconstruct_Optical_img_on_MRI_volume(res_optical_image[:,:,0], rotated_surface, rotated_tumor, output_dir + "Projection/Rec_Optical_rotated_B"+suffix_out_optics+".nii.gz")
    reconstruct_Optical_img_on_MRI_volume(res_optical_image[:,:,1], rotated_surface, rotated_tumor, output_dir + "Projection/Rec_Optical_rotated_G"+suffix_out_optics+".nii.gz")
    reconstruct_Optical_img_on_MRI_volume(res_optical_image[:,:,2], rotated_surface, rotated_tumor, output_dir + "Projection/Rec_Optical_rotated_R"+suffix_out_optics+".nii.gz")
    
    reconstruct_Optical_img_on_MRI_volume(np_surgical_window, rotated_surface, rotated_tumor, output_dir + "Projection/Rec_Surgical_window_rotated"+suffix_out_optics+".nii.gz")


    for i, stats_data in enumerate(fOptics_stats):
        reconstruct_Optical_img_on_MRI_volume(stats_data, rotated_surface, rotated_tumor, output_dir + "Projection/foptics_"+suffix_out_optics+"/"+os.path.basename(fOptics_filenames[i]).split('.')[0] + ".nii.gz")
        







    ###################################################################################
    # Apply the inverse rotation to the reconstructed volume to go back in the T1 space
    ###################################################################################



    # Load rotation matrix and translation for projection
    R = np.loadtxt(filename_rotation_matrix)
    T = np.loadtxt(filename_translation_vector)



    # Rotate optical image into original T1 space 
    Rotate_Volume_Back_To_T1_volume(R = R,
                                    T = T,
                                    filename_input= output_dir + "Projection/Rec_Optical_rotated"+suffix_out_optics+".nii.gz",
                                    ref = T1,
                                    center_rotation = getGravityCenter(surface),
                                    filename_out =  output_dir + "Projection/Rec_Optical_T1"+suffix_out_optics+".nii.gz")

    
    # Rotate surgical into original T1 space 
    Rotate_Volume_Back_To_T1_volume(R = R,
                                    T = T,
                                    filename_input= output_dir + "Projection/Rec_Surgical_window_rotated"+suffix_out_optics+".nii.gz",
                                    ref = T1,
                                    center_rotation = getGravityCenter(surface),
                                    filename_out = output_dir + "Projection/Rec_Surgical_window_T1"+suffix_out_optics+".nii.gz")





    
    for i, stats_data in enumerate(fOptics_stats):
        Rotate_Volume_Back_To_T1_volume(R = R,
                                        T = T,
                                        filename_input= output_dir + "Projection/foptics_"+suffix_out_optics+"/"+os.path.basename(fOptics_filenames[i]).split('.')[0] + ".nii.gz",
                                        ref = T1,
                                        center_rotation = getGravityCenter(surface),
                                        filename_out = output_dir + "Projection/foptics_"+suffix_out_optics+"/"+os.path.basename(fOptics_filenames[i]).split('.')[0] + "_T1.nii.gz")

    return "Success"



def main_project_MRI_in_optics_space(Mypath = Paths(), params=Params()):
    
    main_path_optics = Mypath.main_path_optics
    MRI_proj_dir = Mypath.output_MRI_projection_dir
    BV_segmentation_dir = Mypath.output_BV_segmentation_dir
    Optics_BV_segmentation_dir = BV_segmentation_dir+"Optics_thresh_"+str(params.thresh_optics)+"/"
    output_dir = Mypath.output_dir

    saving_dir = output_dir+"Projection/"


    #Get best registration result
    error,label_MRI_ktp = get_best_MRI_keypoint(Mypath, params)
    if error != "Success":
        return error
    
    #Get registration result directory
    result_dir = get_registration_result_dir(Mypath, params)
    result_dir += label_MRI_ktp+"/"



    #Check if optical imaging is RGB or HSI
    filename_optics = main_path_optics+"initial_img.png"
    if not os.path.exists(filename_optics):
        return "Optical is missing"
    _,suffix_out_optics = is_RGB_optical_image(filename_optics)

    #get filenames
    filename_proj_MRI = MRI_proj_dir+"Proj_MRI.nii.gz"
    filename_mask_proj_MRI = MRI_proj_dir+"Mask_Proj_MRI.nii.gz"
    filename_mask_proj_tumor = MRI_proj_dir+"Mask_Proj_Tumor.nii.gz"
    filename_MRI_skeleton = BV_segmentation_dir+"T1_proj_skeleton.nii.gz"
    
    
    #Filename registration params
    if params.use_custom_registration_metric:
        filename_params_reg = result_dir +"Registration_params_custom_metric"+suffix_out_optics+".txt"
        filename_params_reg_json = result_dir +"Reg_params_custom_metric.json"

    else:
        filename_params_reg = result_dir +"Registration_params"+suffix_out_optics+".txt"
        filename_params_reg_json = result_dir +"Reg_params.json"



    filename_optics_undersampled = Optics_BV_segmentation_dir+"optics_skeleton"+suffix_out_optics+".nii.gz"
    filename_mask_optics = main_path_optics+"mask.png"
    filename_mask_optics_undersampled = Optics_BV_segmentation_dir+"optics_mask"+suffix_out_optics+".nii.gz"
    filename_optics_enhanced = Optics_BV_segmentation_dir+"Optical_enhanced_full_res"+suffix_out_optics+".png"



    filename_mask_proj_fMRI = glob.glob(output_dir+"fMRI/inferences/rotated/*_Mask_proj.nii.gz")
    # filename_optics_stats = main_path_optics+"Stats/Hb_mask.png"
    # filename_optics_Zstats = main_path_optics+"Stats/stats_Hb.txt"



    if not os.path.exists(filename_params_reg_json):
        return ("[main_project_MRI_in_optics_space] Registration param json file missing")

    if not os.path.exists(filename_proj_MRI):
        return ("[main_project_MRI_in_optics_space] MRI projection is missing")

    if not os.path.exists(filename_mask_proj_MRI):
        return ("[main_project_MRI_in_optics_space] Mask MRI projection is missing")

    if not os.path.exists(filename_mask_proj_tumor):
        return ("[main_project_MRI_in_optics_space] Mask tumor projection is missing")

    if not os.path.exists(filename_MRI_skeleton):
        return ("[main_project_MRI_in_optics_space] MRI skeleton projection is missing")

    if not os.path.exists(filename_params_reg):
        return ("[main_project_MRI_in_optics_space] Registetration params are missing")

    if not os.path.exists(filename_optics_undersampled):
        return ("[main_project_MRI_in_optics_space] Optical skeleton is missing")

    if not os.path.exists(filename_mask_optics):
        return ("[main_project_MRI_in_optics_space] Optical mask is missing")

    if not os.path.exists(filename_mask_optics_undersampled):
        return ("[main_project_MRI_in_optics_space] Optical mask is missing")

    if not os.path.exists(filename_optics_enhanced):
        return ("[main_project_MRI_in_optics_space] Optical enhanced image is missing")

    #####################################################################
    # Get angle from moving optical image used to calculate the transform
    #####################################################################

    #Load registration params
    reg_params = Registration_Params.load(filename_params_reg_json)

    #Get best angle
    angle = reg_params.angle

    #Get kpt
    kp_MRI_phys = reg_params.MRI_kpt_phys
    kp_MRI = reg_params.MRI_kpt
    kp_Optics = reg_params.Optics_kpt
    kp_Optics_phys = reg_params.Optics_kpt_phys



    ############################
    # Load data
    ###########################

    MRI_proj = itk.imread(filename_proj_MRI,itk.F)


    mask_proj_MRI = itk.imread(filename_mask_proj_MRI,itk.F)

    tumor_proj = itk.imread(filename_mask_proj_tumor,itk.UC)

    MRI_skeleton = itk.imread(filename_MRI_skeleton)

    mask_optics_undersampled = itk.imread(filename_mask_optics_undersampled,itk.UC)


    np_optical_img = cv.imread(filename_optics)
    np_mask_optics = cv.imread(filename_mask_optics,cv.IMREAD_GRAYSCALE)



    optical_img_skeleton_undersampled = itk.imread(filename_optics_undersampled, itk.F)
    np_optical_img_skeleton_undersampled = itk.GetArrayFromImage(optical_img_skeleton_undersampled)



    # #Optical stats
    # if os.path.exists(filename_optics_stats) and os.path.exists(filename_optics_Zstats):
    #     Optical_Zstats_mask = cv.imread(filename_optics_stats,cv.IMREAD_ANYCOLOR)
    #     Optical_Zstats = np.loadtxt(filename_optics_Zstats)




    #############################################
    # Calculate inverse similarity transform
    ##############################################

    composite_transform = get_inverse_similarity_transform(filename_params_reg)







    #############################################
    # Apply the inverse similarity transform
    ##############################################

    #T1
    MRI_proj_on_optics = itk.resample_image_filter(MRI_proj,
                                                transform=composite_transform,
                                                use_reference_image=True,
                                                reference_image=MRI_proj)
                                                


    np_MRI_proj_on_optics = itk.GetArrayFromImage(MRI_proj_on_optics)
    np_MRI_proj_on_optics = (np_MRI_proj_on_optics - np_MRI_proj_on_optics.min())/(np_MRI_proj_on_optics.max()-np_MRI_proj_on_optics.min())*255




    #fMRI statistical inferences
    fMRI_proj_on_optics = []
    for file in filename_mask_proj_fMRI:
        mask_fMRI_proj_MRI = itk.imread(file,itk.F)

        data = itk.resample_image_filter(mask_fMRI_proj_MRI,
                                                    transform=composite_transform,
                                                    use_reference_image=True,
                                                    reference_image=MRI_proj)
                                                    
        fMRI_proj_on_optics.append(data)
        # np_data = itk.GetArrayFromImage(fMRI_proj_on_optics)
        # np_data = (np_data - np_data.min())/(np_data.max()-np_data.min())*255
        # np_fMRI_proj_on_optics.append(np_data)


    #MRI skeleton
    MRI_skeleton_on_optics = itk.resample_image_filter(MRI_skeleton,
                                                transform=composite_transform,
                                                use_reference_image=True,
                                                reference_image=MRI_proj)
                                                
    np_MRI_skeleton_on_optics = itk.GetArrayFromImage(MRI_skeleton_on_optics)
    np_MRI_skeleton_on_optics = (np_MRI_skeleton_on_optics - np_MRI_skeleton_on_optics.min())/(np_MRI_skeleton_on_optics.max()-np_MRI_skeleton_on_optics.min())*255



    ####################################################################################
    # Apply a rotation to the transformed MRI image to go back to original optical space
    ####################################################################################


    #T1
    np_rotated_MRI_proj = Rotation_2D(-angle, MRI_proj_on_optics, center = [int(kp_MRI[0]), int(kp_MRI[1])])
    np_rotated_MRI_proj = adapt_img_size_after_roation(np_rotated_MRI_proj, np_optical_img_skeleton_undersampled, kp_Optics)

    #Skeleton
    np_rotated_MRI_skeleton = Rotation_2D(-angle, MRI_skeleton_on_optics, center = [int(kp_MRI[0]), int(kp_MRI[1])])
    np_rotated_MRI_skeleton = adapt_img_size_after_roation(np_rotated_MRI_skeleton, np_optical_img_skeleton_undersampled, kp_Optics)

    #fMRI
    np_rotated_fMRI_proj = []
    for data in fMRI_proj_on_optics:
        np_data = Rotation_2D(-angle, data, center = [int(kp_MRI[0]), int(kp_MRI[1])])
        np_data = adapt_img_size_after_roation(np_data, np_optical_img_skeleton_undersampled, kp_Optics)
        np_rotated_fMRI_proj.append(np_data)







    #####################################
    # Write results
    #####################################

    #T1
    np_rotated_MRI_proj = 255*(np_rotated_MRI_proj - np_rotated_MRI_proj.min())/(np_rotated_MRI_proj.max() - np_rotated_MRI_proj.min())
    np_rotated_MRI_proj = cv.medianBlur(np_rotated_MRI_proj.astype(np.uint8),3)
    np_rotated_MRI_proj = cv.resize(np_rotated_MRI_proj, (np_optical_img.shape[1], np_optical_img.shape[0]))

    display = cv.cvtColor(np_rotated_MRI_proj, cv.COLOR_GRAY2BGR)
    cv.imwrite(saving_dir+"MRI_projeced_on_Optics"+suffix_out_optics+".png",display)



    #fMRI
    for i in range(len(filename_mask_proj_fMRI)):
        np_rotated_fMRI_proj[i] = 255*(np_rotated_fMRI_proj[i] - np_rotated_fMRI_proj[i].min())/(np_rotated_fMRI_proj[i].max() - np_rotated_fMRI_proj[i].min())
        np_rotated_fMRI_proj[i] = cv.medianBlur(np_rotated_fMRI_proj[i].astype(np.uint8),3)
        np_rotated_fMRI_proj[i] = cv.resize(np_rotated_fMRI_proj[i], (np_optical_img.shape[1], np_optical_img.shape[0]))
        np_rotated_fMRI_proj[i][np_rotated_fMRI_proj[i]>0] = 255

        cv.imwrite(filename_mask_proj_fMRI[i].split('.')[0]+"_RGB_space.png",np_rotated_fMRI_proj[i])



    #Skeleton MRI
    np_rotated_MRI_skeleton = cv.resize(np_rotated_MRI_skeleton, (np_optical_img.shape[1], np_optical_img.shape[0]))
    np_rotated_MRI_skeleton = np_rotated_MRI_skeleton*np_mask_optics
    np_rotated_MRI_skeleton[np_rotated_MRI_skeleton>0] = 255
    np_rotated_MRI_skeleton = cv.ximgproc.thinning(np_rotated_MRI_skeleton.astype(np.uint8))
    cv.imwrite(saving_dir+"MRI_skeleton_projeced_on_Optics"+suffix_out_optics+".png",np_rotated_MRI_skeleton)



    #Skeleton optics (full size resolution)
    skeleton_optics = (np_optical_img_skeleton_undersampled*255).astype(np.uint8)
    skeleton_optics = cv.resize(skeleton_optics, (np_optical_img.shape[1], np_optical_img.shape[0]))
    skeleton_optics[skeleton_optics>0.1] = 255
    skeleton_optics = cv.ximgproc.thinning(skeleton_optics.astype(np.uint8))
    cv.imwrite(saving_dir+"Optics_skeleton_"+suffix_out_optics+".png",skeleton_optics)

    return "Success"


def main_plot_MRI_projected_on_Optics_space(Mypath = Paths()):

    main_path_optics = Mypath.main_path_optics
    output_dir = Mypath.output_dir

    #Check if optical imaging is RGB or HSI
    filename_optics = main_path_optics+"initial_img.png"
    

    if not os.path.exists(filename_optics):
        return "Optical is missing",None
    _,suffix_out_optics = is_RGB_optical_image(filename_optics)


    filename_mask_optics = main_path_optics+"mask.png"
    filename_skeleton_optics = output_dir+"Projection/Optics_skeleton_"+suffix_out_optics+".png"
    filename_MRI_skeleton = output_dir+"Projection/MRI_skeleton_projeced_on_Optics"+suffix_out_optics+".png"
    filename_MRI_proj = output_dir+"Projection/MRI_projeced_on_Optics"+suffix_out_optics+".png"

    

    if not os.path.exists(filename_mask_optics): 
        return "[main_plot_MRI_projected_on_Optics_space] Optics mask is missing",None

    if not os.path.exists(filename_skeleton_optics):    
        return "[main_plot_MRI_projected_on_Optics_space] Optics skeleton is missing",None
    
    if not os.path.exists(filename_MRI_skeleton):    
        return "[main_plot_MRI_projected_on_Optics_space] MRI skeleton is missing",None
    
    if not os.path.exists(filename_MRI_proj):    
        return "[main_plot_MRI_projected_on_Optics_space] MRI proj is missing",None
    


    # Load data
    np_rotated_MRI_proj = cv.imread(filename_MRI_proj)
    np_rotated_MRI_skeleton = cv.imread(filename_MRI_skeleton,cv.IMREAD_GRAYSCALE)
    skeleton_optics = cv.imread(filename_skeleton_optics,cv.IMREAD_GRAYSCALE)
    np_optical_img = cv.imread(filename_optics)
    np_mask_optics = cv.imread(filename_mask_optics,cv.IMREAD_GRAYSCALE)


    #resize skeleton to match initial image size
    # skeleton_optics = cv.resize(skeleton_optics, (np_optical_img.shape[1], np_optical_img.shape[0]),cv.INTER_NEAREST)

    #####################################
    # Dilate skeleton
    #####################################
    ksize = 10
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(ksize,ksize))
    # skeleton_optics = cv.morphologyEx(skeleton_optics, op=cv.MORPH_DILATE, kernel=kernel)
    np_rotated_MRI_skeleton = cv.morphologyEx(np_rotated_MRI_skeleton, op=cv.MORPH_DILATE, kernel=kernel)



    #####################################
    # Plot MRI and optics skeleton on same image
    #####################################
    display = np.zeros((np_rotated_MRI_skeleton.shape[0],np_rotated_MRI_skeleton.shape[1],3))
    display[:,:,0] = np_rotated_MRI_skeleton
    display[:,:,2] = skeleton_optics
    display = display.astype(np.uint8)

    

    #print("DICE skeletons(MRI,Optics)",dice_coefficient(np_rotated_MRI_skeleton, skeleton_optics))




    #####################################
    # Plot optics an MRI proj in optics space
    #####################################

    #Get contour of the surgical window
    contours_surgical_window, hierarchy = cv.findContours(np_mask_optics.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)


    #Display 1 undersampled image with skeleton
    # colormap = cv.COLORMAP_PLASMA
    weight = 0.8
    # display_1 =  apply_colormap_with_mask(cv.applyColorMap(np_rotated_MRI_proj,colormap), skeleton_optics, skeleton_optics, "", weight)
    display_1 = np_rotated_MRI_proj.copy()

    for r in range(display_1.shape[0]):
        for c in range(display_1.shape[1]):
            if skeleton_optics[r,c] >0:
                display_1[r,c,2] = skeleton_optics[r,c]

    # BV = np.zeros(display_1.shape)
    # BV[:,:,2] = skeleton_optics
    # display_1 = merge_two_colored_img(display_1,BV,skeleton_optics,weight)
    cv.drawContours(display_1,contours_surgical_window,-1,(0,255,0),2)


    #Display 2 RGB image and MRI projection
    weight = 0.8
    display_2 =  apply_colormap_with_mask(np_optical_img, skeleton_optics, skeleton_optics, "", weight)
    cv.drawContours(display_2,contours_surgical_window,-1,(0,255,0),2)


    cv.imwrite(output_dir+"Projection/MRI_projeced_on_Optics_contours.png",display_1)


    return "Success", cv.cvtColor(display_1,cv.COLOR_BGR2RGB)
    
    
    # plt.figure(figsize=(20,20))
    # plt.subplot(131)
    # plt.imshow(cv.cvtColor(display,cv.COLOR_BGR2RGB))
    # plt.subplot(132)
    # plt.imshow(cv.cvtColor(display_1,cv.COLOR_BGR2RGB))
    # plt.subplot(133)
    # plt.imshow(cv.cvtColor(display_2,cv.COLOR_BGR2RGB))
    # plt.show()


    # cv.imwrite(output_dir+"res_Proj_MRI_on_Optics"+suffix_out_optics+".png",display_1)
    # cv.imwrite(output_dir+"RGB_skeleton"+suffix_out_optics+".png",display_2)












    # #####################################
    # # Display results fOptics - fMRI
    # #####################################


def main_plot_fOptics_fMRI_stats_projected_on_optics(Mypath = Paths(), _fMRI_filenames=[], _fOptics_filenames=[], colors_fMRI=[], colors_fOptics=[]):
    
    
    main_path_optics = Mypath.main_path_optics
    output_dir = Mypath.output_dir


    
    saving_dir = output_dir + "Projection/"

    #Check if optical imaging is RGB or HSI
    filename_optics = main_path_optics+"initial_img.png"
    filename_mask = main_path_optics+"mask.png"
    if not os.path.exists(filename_optics):

        return ("Optical image is missing"), None
    
    if not os.path.exists(filename_mask):
            return ("Optical mask is missing"), None
    
    _,suffix_out_optics = is_RGB_optical_image(filename_optics)

    dir_fMRI = output_dir + "fMRI/inferences/rotated/"

    ########################################
    # Display results - MRI projection and optics image
    ########################################

    # Load images
    in_img = cv.imread(filename_optics)
    mask_optics = cv.imread(filename_mask,cv.IMREAD_GRAYSCALE)
    mask_optics = mask_optics/mask_optics.max()

    fMRI_filenames = []
    for f in _fMRI_filenames:
        fMRI_filenames.append(dir_fMRI + "r_"+os.path.basename(f).split('.')[0]+"_Mask_proj_RGB_space.png")

    # fOptics_filenames = []
    # for f in _fOptics_filenames:
    #     fOptics_filenames.append(dir_foptics + os.path.basename(f).split('.')[0]+"_mask.png")


    #Load fMRI stats
    fMRI_stats = []
    for file in fMRI_filenames:
        if not os.path.exists(file):
            return (os.path.basename(file)+ " is missing"), None
        fMRI_stats.append((cv.imread(file,cv.IMREAD_ANYCOLOR)*mask_optics).astype(np.uint8))

    #Load foptics stats
    fOptics_stats = []
    for file in _fOptics_filenames:
        if not os.path.exists(file):
            return (os.path.basename(file)+ " is missing"), None
        
        data = np.loadtxt(file)
        fOptics_stats.append(np.where(data != 0, 255, 0).astype(np.uint8)) 



    display = in_img.copy()
    #Draw fOptics contour
    width = 1
    for i, data in enumerate(fOptics_stats):
        c, hierarchy = cv.findContours(data.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        cv.drawContours(display,c,-1,colors_fOptics[i],width)

    for i,data in enumerate(fMRI_stats):
        c, hierarchy = cv.findContours(data.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        cv.drawContours(display,c,-1,colors_fMRI[i],width)





    cv.imwrite(saving_dir+"fOptics_fMRI_projected_on_Optics"+suffix_out_optics+".png",display)

    display = cv.cvtColor(display,cv.COLOR_BGR2RGB)

    return "Success",display











    # for i in range(len(filename_mask_proj_fMRI)):

    #     cv.imwrite(filename_mask_proj_fMRI[i].split('.')[0]+"_RGB_space.png",np_rotated_fMRI_proj[i])

    #     # display = np_optical_img.copy()

    #     # #Apply mask to fMRI
    #     # np_rotated_fMRI_proj[i] *= np_mask_optics

    #     # #Get contour of fOPtics
    #     # contours_fOptics, hierarchy = cv.findContours(Optical_Zstats_mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    #     # contours_fMRI, hierarchy = cv.findContours(np_rotated_fMRI_proj[i].copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    #     # print("DICE(fMRI,fOptics) = ",dice_coefficient(Optical_Zstats_mask, np_rotated_fMRI_proj[i]))
    #     # print("Overlap(fOptics,fMRI) = ",overlap_coefficient(Optical_Zstats_mask, np_rotated_fMRI_proj[i]))


    #     # width = 3
    #     # cv.drawContours(display,contours_fMRI,-1,(0,0,255),width)
    #     # cv.drawContours(display,contours_fOptics,-1,(255,0,0),width)


    #     # plt.figure()
    #     # plt.imshow(cv.cvtColor(display, cv.COLOR_BGR2RGB))
    #     # plt.show()

    #     # cv.imwrite(output_dir+"fOptics_fMRI_projected_on_Optics"+suffix_out_optics+".png",display)


def main_place_optics_on_MRI(Mypath = Paths(), params=Params()):

    BV_segmentation_dir = Mypath.output_BV_segmentation_dir
    Optics_BV_segmentation_dir = BV_segmentation_dir+"Optics_thresh_"+str(params.thresh_optics)+"/"
    MRI_projection_dir = Mypath.output_MRI_projection_dir
    main_path_optics = Mypath.main_path_optics

    #Set filenames
    filename_MRI = BV_segmentation_dir+"T1_proj_skeleton.nii.gz"
    filename_mask_MRI = MRI_projection_dir+"Mask_Proj_MRI.nii.gz"
    filename_tumor = MRI_projection_dir+"Mask_Proj_Tumor.nii.gz"


    #Check if image is RGB or HSI
    filename_initial_img = main_path_optics+"initial_img.png"
    _,suffix_out_optics = is_RGB_optical_image(filename_initial_img)


    filename_optics = Optics_BV_segmentation_dir+"optics_skeleton"+suffix_out_optics+".nii.gz"
    filename_mask_otpics = Optics_BV_segmentation_dir+"optics_mask"+suffix_out_optics+".nii.gz"

    #Load optics image resolution
    res_opt_in_mm = float(np.loadtxt(main_path_optics+"resolution.txt"))


    #Load files
    MRI_proj = itk.imread(filename_MRI,itk.UC)
    mask_MRI = itk.imread(filename_mask_MRI,itk.UC)
    mask_tumor = itk.imread(filename_tumor,itk.UC)

    Optics_img = itk.imread(filename_optics,itk.UC)
    Optical_mask=  itk.imread(filename_mask_otpics,itk.UC)

    # print("[main_place_optics_on_MRI] max value of MRI image: ",itk.GetArrayFromImage(MRI_proj).max())    
    # print("[main_place_optics_on_MRI] max value of optics image: ",itk.GetArrayFromImage(Optics_img).max())    
    # plt.figure()
    # plt.imshow(itk.GetArrayFromImage(Optical_mask))
    # plt.show()

    #Get MRI and optics alignement keypoints
    kp_Optics, kp_Optics_phys, _kpts_MRI_tumor, _kpts_MRI_tumor_phys = get_alignment_points(Optical_mask, Optics_img,
                                                                                            MRI_proj, mask_tumor, 
                                                                                            params.kpts_MRI_tumor, params.kpt_optics,
                                                                                            space_between_kpt_mm= params.space_between_kpt_mm,
                                                                                            enlarge_tumor_roi_factor=params.tumor_ROI_enlarge_factor)

    # kp_Optics, kp_Optics_phys, _kpts_MRI_tumor, _kpts_MRI_tumor_phys = get_alignement_points_in_skeleton(MRI_proj, Optics_img, Optical_mask, mask_tumor, params.MRI_keypoints_nb)


    kpts_MRI_tumor = _kpts_MRI_tumor
    kpts_MRI_tumor_phys = _kpts_MRI_tumor_phys


    id_kp_MRI = 0
    kp_MRI_phys = kpts_MRI_tumor_phys[id_kp_MRI]
    kp_MRI = kpts_MRI_tumor[id_kp_MRI]


    #Change origin of optics slice to match keypoint
    change_origin(filenames_MRI= [filename_MRI],
                filenames_optics= [filename_optics],
                kpt_Optics= kp_Optics_phys,
                kpt_MRI= kp_MRI_phys)


    #Load volumes with origin changed
    filename_MRI = filename_MRI.split('.')[0]+"_origin_changed.nii.gz"
    filename_optics = filename_optics.split('.')[0]+"_origin_changed.nii.gz"
        

    #Show registration for the minimal metric
    open_itksnap_with_overlay(filename_MRI, filename_optics)




def main_get_optics_image(Mypath = Paths()):

    main_path_optics = Mypath.main_path_optics
    filename_optics = main_path_optics+"initial_img.png"

    if not os.path.exists(filename_optics):
        return "Optical initial image is missing", None

    img = cv.imread(filename_optics,cv.IMREAD_ANYCOLOR)

    if img.ndim == 3:
        img = cv.cvtColor(img,cv.COLOR_BGR2RGB)

    return "Success", img



def main_get_validation_landmarks_img(Mypath = Paths()):
    # Saving directory
    output_dir = Mypath.output_dir

    # file_MRI = output_dir+"Projection/MRI_proj_enhanced.png"
    file_MRI = output_dir+"Projection/MRI_proj.png"
    
    #Load images
    if os.path.exists(file_MRI):
        mri = cv.imread(file_MRI)
    else:
        return "[main_get_validation_landmarks_img] MRI projection is missing", None, None
    

    if os.path.exists(output_dir+"Projection/RGB_registered_on_MRI.png"):
        optics = cv.cvtColor(cv.imread(output_dir+"Projection/RGB_registered_on_MRI.png"),cv.COLOR_BGR2RGB)
    else:
        return "[main_get_validation_landmarks_img] Optical image registered on MRI is missing", None, None
    
    return "Success", mri, optics


def main_load_validation_landmarks_img(Mypath = Paths()):

    output_dir = Mypath.output_dir



    filename_Optics = output_dir+"Projection/RGB_registered_on_MRI.png"
    if os.path.exists(filename_Optics):
        Optics_img = cv.cvtColor(cv.imread(filename_Optics),cv.COLOR_BGR2RGB)
    else:
        return "[main_load_validation_landmarks_img] Optical image projected on MRI is missing", None, None, None, None


    
    #Load landmarks
    if os.path.exists(output_dir+"verification_landmarks/optics.txt") and os.path.exists(output_dir+"verification_landmarks/mri.txt"):
        points_optics = np.loadtxt(output_dir+"verification_landmarks/optics.txt").astype(int)
        points_mri = np.loadtxt(output_dir+"verification_landmarks/mri.txt").astype(int)
    else:
        return "[main_load_validation_landmarks_img] Landmarks files are missing", np.nan, np.nan, np.nan, np.nan

    #Get MRI resolution
    filename_MRI_proj = Mypath.output_MRI_projection_dir+"Proj_MRI.nii.gz"
    if os.path.exists(filename_MRI_proj):
        MRI_proj = itk.imread(filename_MRI_proj, itk.F)
        reso = np.array(MRI_proj.GetSpacing())
    else:
        return "[main_load_validation_landmarks_img] MRI projection is missing", np.nan, np.nan, np.nan, np.nan

    #Plot landmarks
    for pt_optics in points_optics:
        Optics_img = cv.circle(Optics_img, pt_optics, 2, (0,0,255), -1)

    for pt_mri in points_mri:
        Optics_img = cv.circle(Optics_img, pt_mri, 2, (255,0,0), -1)

    
    return "Success", points_optics, points_mri, reso, Optics_img


    # plt.figure(figsize=(20,20))
    # plt.subplot(131)
    # plt.imshow(optics)
    # for i in range(points_optics.shape[0]):
    #     plt.plot(points_optics[i,0],points_optics[i,1],'ro')
    
    # plt.subplot(132)
    # plt.imshow(mri)
    # for i in range(points_mri.shape[0]):
    #     plt.plot(points_mri[i,0],points_mri[i,1],'ro')
    
    # plt.subplot(133)
    # plt.imshow(mri)
    # for i in range(points_mri.shape[0]):
    #     plt.plot(points_mri[i,0],points_mri[i,1],'bo')

    # for i in range(points_optics.shape[0]):
    #     plt.plot(points_optics[i,0],points_optics[i,1],'ro')
    # plt.show(block=True)


