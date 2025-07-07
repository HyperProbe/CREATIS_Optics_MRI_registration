
from PySide6.QtCore import QObject, Signal, QRunnable
from module.main_functions import *


class Process_idx:
    def __init__(self):
        #Process idx
        self.Brain_extraction = 0
        self.fMRI_to_T1_registration = 1
        self.MRI_projection_all = 2
        self.Tumor_segmentation = 2.1
        self.MRI_projection = 2.2

        self.Blood_vessel_enhancement = 3

        self.Optics_to_MRI_registration = 4
        self.Optics_to_MRI_registration_check_Init_Points = 4.1
        self.Optics_to_MRI_registration_define_Init_Points = 4.2

        self.Display_registration_results = 5

        self.Registration_validation = 6



class WorkerSignals(QObject):
    status_signal = Signal(str)
    display_signal = Signal(object, object)
    finished = Signal()

# class WorkerThread(QThread):
# class WorkerThread(QObject):
class WorkerThread(QRunnable):

    # # Signals
    # status_signal = Signal(str)
    # display_signal = Signal(object,object)
    # finished = Signal()



    def __init__(self, idx=0, process = False, fMRI_files = [], fOptics_files = [], Mypath = Paths(), params = Params()):
        super().__init__()

        # Signals
        self.signals = WorkerSignals()

        self.process_idx = Process_idx()

        #Current process idx
        self.idx = idx

        #Processing or display
        self.process = process

        #fOptics fMRI files
        self.fMRI_files = fMRI_files
        self.fOptics_files = fOptics_files

        #Parameters and path
        self.Mypath = Mypath
        self.params = params

    def setWorkerIndex(self, index=0):
        self.idx = index

    def setProcessMode(self, mode=False):
        self.process = mode

    def set_Paths(self,Mypath = Paths()):
        self.Mypath = Mypath

    def set_params(self, params = Params()):
        self.params = params

    def set_fMRI_files(self, fMRI_files = []):
        self.fMRI_files = fMRI_files

    def set_fOptics_files(self, fOptics_files = []):
        self.fOptics_files = fOptics_files

    def run(self):
        self.Main_process()


    # def run(self):
    def Main_process(self):

        if self.process: #Process
            print("In WorkerThread process_id")
            self.process_id()
        else: #Display results
            print("In WorkerThread Display_restults")
            self.Display_restults()  # Notify the main thread when done



    ##############
    # Process
    #############

    #Brain extraction
    def brain_extraction_process(self):
        error = main_extract_brain(self.Mypath, self.params)
        if error != "Success":
            return "Brain extraction: "+error

        error = main_get_surface_mask(self.Mypath, self.params)
        return "Get surface mask: "+error


    #fMRI to T1
    def fMRI_to_T1_registration_process(self):
        print("fMRI_to_T1_registration_process")
        error = main_register_fMRI_to_T1(self.Mypath, self.params)
        return "fMRI to T1 registation: "+error


    #MRI projection all
    def process_all_MRI_projection(self):
        error = self.brain_tumor_segmentation_process()
        if error != "Success":
            return error
        error = self.MRI_projection_process()
        return error

    #Brain tumor segmentation
    def brain_tumor_segmentation_process(self):
        error = main_get_tumor_segmentation(self.Mypath)
        return error

    #MRI projection
    def MRI_projection_process(self):
        error = main_get_MRI_projection(self.Mypath, self.params)
        return error

    #Blood vessel enhancement
    def blood_vessel_enhancement_process(self):
        #get skeleton vessel in MRI projection
        error = main_get_vessels_in_MRI(self.Mypath, self.params)
        if error != "Success":
            return "Blood vessel enhancement in MRI: "+error

        #get skeleton vessel in Optical image
        error = main_get_vessels_in_optics(self.Mypath, self.params)
        return "Blood vessel enhancement on optics image: "+error




    #Registration process Main
    def Optics_MRI_registration_process(self):
        # Process registration
        error = main_Optics_to_MRI_registration(self.Mypath, self.params)
        return "Optics-MRI registration: "+error

    def Process_result_files(self):

        #Project optical image/stats on MRI projection
        error = main_project_optical_image_on_MRI(self.Mypath, self.params)
        if error != "Success":
            print("[Process_result_files] error main_project_optical_image_on_MRI",error)
            return "Project MRI on optics: "+error

        #Create optical volume in T1 space
        error = main_reconstruct_Optics_volume(self.Mypath)
        if error != "Success":
            print("[Process_result_files] error main_reconstruct_Optics_volume",error)
            return "Create optics volume in T1 space: "+error

        #Project MRI on optics space
        error = main_project_MRI_in_optics_space(self.Mypath, self.params)
        if error != "Success":
            print("[Process_result_files] error main_project_MRI_in_optics_space",error)


        return "Project MRI in optics space: "+error



    def process_id(self):

        match self.idx:
            #Brain extraction
            case self.process_idx.Brain_extraction:
                error = self.brain_extraction_process()

            #fMRI to T1 registration
            case self.process_idx.fMRI_to_T1_registration:
                error = self.fMRI_to_T1_registration_process()

            #Plot MRI projection
            case self.process_idx.MRI_projection_all:
                error = self.process_all_MRI_projection()

            case self.process_idx.Tumor_segmentation:
                error = self.brain_tumor_segmentation_process()

            case self.process_idx.MRI_projection:
                error = self.MRI_projection_process()

            #Blood vessel enhancement
            case self.process_idx.Blood_vessel_enhancement:
                error = self.blood_vessel_enhancement_process()

            #Optics to MRI registration
            case self.process_idx.Optics_to_MRI_registration:
                error = self.Optics_MRI_registration_process()

            #Display registrtion results
            case self.process_idx.Display_registration_results:
                error = self.Process_result_files()

            case _:
                pass

        #Send signals
        # self.status_signal.emit(error)
        self.signals.status_signal.emit(error)

        self.Display_restults()







    #######################
    # Display results
    #######################
    def Display_restults(self):

        proj1 = None
        proj2 = None

        print("Display results",self.idx)

        match self.idx:

            #Brain extraction
            case self.process_idx.Brain_extraction:
                error, proj1 = main_plot_extracted_brain(self.Mypath)

            #fMRI to T1 registration
            case self.process_idx.fMRI_to_T1_registration:
                error, proj1, proj2 = main_plot_fMRI_T1_registration(self.Mypath)

            #Plot MRI projection
            case self.process_idx.MRI_projection:
                error,proj1 = main_plot_MRI_Projection(self.Mypath)

            case self.process_idx.MRI_projection_all:
                error,proj1 = main_plot_MRI_Projection(self.Mypath)


            #Blood vessel enhancement
            case self.process_idx.Blood_vessel_enhancement:
                error,proj1 = main_plot_vessel_skeletons(self.Mypath)



            #Optics to MRI registration
            case self.process_idx.Optics_to_MRI_registration:
                error,proj1 = plot_registration_results(self.Mypath, self.params)

            #Plot alignement points in MR and optics images
            case self.process_idx.Optics_to_MRI_registration_check_Init_Points:
                error,proj1 = main_plot_Optics_MRI_alignement_points(self.Mypath, self.params)


            #Display registrtion results
            case self.process_idx.Display_registration_results:
                error,proj1 = self.display_results_Optics_MRI()

            case _:
                pass

        #Send signals
        # self.status_signal.emit(error)
        # self.display_signal.emit(proj1,proj2)
        # self.finished.emit()

        self.signals.status_signal.emit(error)
        self.signals.display_signal.emit(proj1,proj2)
        self.signals.finished.emit()


    def display_results_Optics_MRI(self):

        # Display optical image on MRI projection only
        error1, display1 = main_plot_Optical_image_projected_on_MRI(self.Mypath)

        #Display MRI skeleton on optics image
        error2, display2 = main_plot_MRI_projected_on_Optics_space(self.Mypath)

        #Display fMRI and fOptics
        if self.fMRI_files != [] or self.fOptics_files != []:
            colors_fOptics = [(255,0,0),(0,0,255)]
            colors_fMRI = [(255,255,0),(0,215,255)]

            error1, display1 = main_plot_fOptics_fMRI_stats_projected_on_MRI(self.Mypath,
                                                                           _fMRI_filenames=self.fMRI_files,
                                                                           _fOptics_filenames=self.fOptics_files,
                                                                           colors_fMRI=colors_fMRI,
                                                                           colors_fOptics=colors_fOptics)




            error2, display2 = main_plot_fOptics_fMRI_stats_projected_on_optics(self.Mypath,
                                                            _fMRI_filenames=self.fMRI_files,
                                                            _fOptics_filenames=self.fOptics_files,
                                                            colors_fMRI=colors_fMRI,
                                                            colors_fOptics=colors_fOptics)



        error = error1+" "+error2
        if error1 != "Success" or error2 != "Success":
            return error, None

        #Merge two results
        print("[Worker] display_results_Optics_MRI", display1.shape, display2.shape)
        max_shape = (np.maximum(display1.shape[0],display2.shape[0]), np.maximum(display1.shape[1],display2.shape[1]))
        display = np.zeros((max_shape[0],2*max_shape[1],3))

        display[:,0:max_shape[1]] = cv.resize(display1,(max_shape[1],max_shape[0]))
        display[:,max_shape[1]:] = cv.resize(display2,(max_shape[1],max_shape[0]))


        return error, display.astype(np.uint8)
