# This Python file uses the following encoding: utf-8
import sys

# import PySide6
from PySide6.QtWidgets import QApplication, QWidget, QFileDialog, QLabel, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import QObject, QThread, Signal, Qt, QPoint, QThreadPool
from PySide6.QtGui import QCloseEvent

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py


from module_ui.ui_form import Ui_main
from module.worker import WorkerThread, Process_idx
from module.main_functions import *

from module_ui.plot_functions import ThrobberWindow, LoadingOverlay
import os



class main(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_main()
        self.ui.setupUi(self)

        #Init ui
        self.ui.tabWidget.setEnabled(False)
        self.ui.tabWidget.setCurrentIndex(0)
        self.ui._param_display.hide()
        self.ui._slider_legend.hide()
        self.ui._param_display.setMaximum(100)
        self.ui._param_display.setMinimum(0)
        self.ui._param_display.setValue(50)

        #Projection type
        self.ui._projection_type.addItem("Transverse")
        self.ui._projection_type.addItem("Sagital")
        self.ui._projection_type.addItem("Coronal")
        self.ui._projection_type.setCurrentIndex(0)

        # #Projection slice order
        # self.ui._projection_slice_order.addItem("Auto")
        # self.ui._projection_slice_order.addItem("Top slice")
        # self.ui._projection_slice_order.addItem("Bottom slice")

        #Projection basis choice
        self.ui._projection_basis_choice.addItem("X axis")
        self.ui._projection_basis_choice.addItem("Y axis")
        self.ui._projection_basis_choice.addItem("Z axis")
        self.ui._projection_basis_choice.setCurrentIndex(1)

        #Projection axis passing through
        self.ui._projection_axis_passing_through.addItem("Axis passing through MRI origin")
        self.ui._projection_axis_passing_through.addItem("Axis passing through MRI center of mass")
        self.ui._projection_axis_passing_through.addItem("No rotation")
        self.ui._projection_axis_passing_through.setCurrentIndex(0)



        #Process idx
        self.process_idx = Process_idx()

        #fOptics fMRI files
        self.fMRI_files = []
        self.fOptics_files = []

        #Parameters and path
        self.Mypath = Paths()
        self.params = Params()
        self.params_file = None


        # Create overlay on top of the main window
        # self.ui._loading_display.hide()





        #Connect path
        self.ui._getDataPath.clicked.connect(self.get_Data_Path)
        self.ui._HSI_imaging.stateChanged.connect(self.use_HS_imaging)

        #Slider
        self.ui._param_display.sliderReleased.connect(self.on_displaySliderChanged)

        #Connect brain extraction
        self.ui._f_bet.textChanged.connect(self.on_f_bet_changed)
        self.ui._use_bet.stateChanged.connect(self.on_use_bet)
        self.ui._kdilatation_brain_mask.textChanged.connect(self.on_kdilatation_brain_mask_changed)
        self.ui._extract_brain_surface.clicked.connect(self.brain_extraction_process)

        #Connect fMRI registration
        self.ui._copy_fMRI_files.stateChanged.connect(self.on_copy_fMRI_files)
        self.ui._process_fMRI_to_T1_registration.clicked.connect(self.fMRI_to_T1_registration_process)

        #Connect MRI projection
        self.ui._projection_type.currentTextChanged.connect(self.on_Projection_choice_changed)
        self.ui._process_tumor_segmentation.clicked.connect(self.brain_tumor_segmentation_process)
        self.ui._process_MRI_projection.clicked.connect(self.MRI_projection_process)
        self.ui._process_all_MRI_projection.clicked.connect(self.process_all_MRI_projection)
        # self.ui._projection_slice_order.currentTextChanged.connect(self.on_Projection_slice_order_changed)
        self.ui._projection_basis_choice.currentTextChanged.connect(self.on_projection_basis_choice_changed)
        self.ui._projection_axis_passing_through.currentTextChanged.connect(self.on_projection_axis_passing_through_changed)
        self.ui._MRI_erode_edge_mm.textChanged.connect(self.on_projection_MRI_erode_edge_mm_changed)


        #Connect blood vessel enhancement
        self.ui._process_blood_vessel_enhancement.clicked.connect(self.blood_vessel_enhancement_process)
        self.ui._MRI_thresh.textChanged.connect(self.on_MRI_thresh_changed)
        self.ui._optics_thresh.textChanged.connect(self.on_Optics_thresh_changed)
        self.ui._min_vessel_MRI.textChanged.connect(self.on_min_MRI_vessel_changed)
        self.ui._min_vessel_Optics.textChanged.connect(self.on_min_Optics_vessel_changed)
        self.ui._max_vessel_MRI.textChanged.connect(self.on_max_MRI_vessel_changed)
        self.ui._max_vessel_Optics.textChanged.connect(self.on_max_Optics_vessel_changed)
        self.ui._manual_optics_vessel_selection.clicked.connect(self.manual_optics_vessel_selection)
        self.ui._manual_MRI_vessel_selection.clicked.connect(self.manual_MRI_vessel_selection)
        self.ui._clear_skeletons.clicked.connect(self.clear_skeletons)
        self.ui._kernel_specular_reflection.textChanged.connect(self.on_kernel_specular_reflection_changed)
        self.ui._kernel_exterior_mask_mm.textChanged.connect(self.on_kernel_exterior_mask_mm)

        #Connect Optics/MRI registration
        self.ui._process_optics_to_MRI_registration.clicked.connect(self.Optics_MRI_registration_process)
        self.ui._check_init_points.clicked.connect(self.Optics_MRI_registration_process_check_Init_Points)
        self.ui._choose_init_points.clicked.connect(self.Optics_MRI_registration_process_define_new_Init_Points)
        self.ui._test_manual_alignement.clicked.connect(self.Optics_MRI_registration_test_manual_alignement)

        self.ui._space_between_kpt_mm.textChanged.connect(self.Optics_MRI_registration_on_New_space_between_kpt_mm)
        self.ui._tumor_ROI_enlarge_factor.textChanged.connect(self.Optics_MRI_registration_on_New_tumor_ROI_enlarge_factor)

        self.ui._use_custom_registration_metric.stateChanged.connect(self.Optics_MRI_registration_on_use_custom_registration_metric)

        #Connect display results
        self.ui._process_result_files.clicked.connect(self.Process_result_files)
        self.ui._select_fMRI_files.clicked.connect(self.Select_fMRI_files)
        self.ui._select_fOptics_files.clicked.connect(self.Select_fOptics_files)



        #Connect registration validation
        self.ui._choose_validation_landmarks.clicked.connect(self.onChooseValidationLandmarks)
        self.ui._calculate_registration_error.clicked.connect(self.onCalculate_Registration_error)


        #Advanced settings
        self.ui._advanced_settings.stateChanged.connect(self.on_advanced_setting)
        self.ui._advanced_settings.setChecked(False)
        self.on_advanced_setting(False)


        #init display
        self.init_Params()
        self.ui.tabWidget.currentChanged.connect(self.Display_restults)



        #Thread pool
        self.threadPool = QThreadPool()

        # #Create worker
        # self.worker = WorkerThread()

        # #connect slots
        # self.worker.signals.status_signal.connect(self.on_display_status)
        # self.worker.signals.display_signal.connect(self.on_display_images)


        # print("Pyside version")
        # print(PySide6.__version__)



    def closeEvent(self, event: QCloseEvent):
        if self.params_file is not None and self.params_file != "/Params.json":
            self.params.save(self.params_file)




    ########################
    # Global ui interraction
    ########################


    #Advanced settings
    def on_advanced_setting(self, state):
        print("on_advanced_setting",state)


    #Get main path
    def get_Data_Path(self):

        #Set main path
        directory = QFileDialog.getExistingDirectory(self, "Select a Directory")
        self.Mypath.set_main_path(directory)

        #By default use RGB imaging (HSI box is unheck)
        self.Mypath.set_Optics_path(RGB_optics=not self.ui._HSI_imaging.isChecked())

        #Check if path has been set
        self.ui.tabWidget.setEnabled(directory != "")

        #Display result for brain extraction
        self.Display_restults(self.process_idx.Brain_extraction)

        #Load params
        self.params_file = self.Mypath.main_path+"/Params.json"
        if os.path.exists(self.params_file):
            print("Param file exists")
            self.params = Params.load(self.params_file)
            self.init_Params()
        else:
            print("Param file does not exist")

    #Use RGB or HSI
    def use_HS_imaging(self,state):
        self.Mypath.set_Optics_path(RGB_optics=not state)



    def start_animation(self):
        self.ui._infoData.setText("Processing.........")

        # # create throbber
        # # self.throbber = LoadingOverlay(self)
        # self.throbber = ThrobberWindow()
        # self.throbber.move(self.geometry().center().x() - 80,
        #                    self.geometry().center().y() - 80)  # Center Throbber
        # self.throbber.show()  # Ensure visibility


    def stop_animation(self):
        pass
        # self.throbber.close()

    ########################
    # init parameters from ui
    ########################

    def init_Params(self):
        #Init brain extraction params
        self.ui._use_bet.setChecked(self.params.use_bet)
        self.ui._f_bet.setText(str(self.params.f_bet))
        self.ui._kdilatation_brain_mask.setText(str(self.params.k_dilatation_brain))

        #fMRI to T1 registratio (params to remove)
        self.ui._copy_fMRI_files.setChecked(not self.params.register_fMRI_to_T1)

        #blood vessel enhancement
        self.ui._MRI_thresh.setText(str(self.params.thresh_MRI))
        self.ui._optics_thresh.setText(str(self.params.thresh_optics))
        self.ui._min_vessel_MRI.setText(str(self.params.sigma_minimum_mm_MRI))
        self.ui._min_vessel_Optics.setText(str(self.params.sigma_minimum_mm_optics))
        self.ui._max_vessel_MRI.setText(str(self.params.sigma_maximum_mm_MRI))
        self.ui._max_vessel_Optics.setText(str(self.params.sigma_maximum_mm_optics))
        self.ui._kernel_specular_reflection.setText(str(self.params.ksize_mm_kernal_specular_reflection_optics))
        self.ui._kernel_exterior_mask_mm.setText(str(self.params.kernel_mm_optical_mask_erosion))


        #MRI projection
        self.ui._projection_type.setCurrentText(self.params.projection_type)
        # self.ui._projection_slice_order.setCurrentText(self.params.projection_slice_order)
        self.ui._projection_basis_choice.setCurrentText(self.params.projection_base_axis)
        self.ui._projection_axis_passing_through.setCurrentText(self.params.axis_projection)
        self.ui._MRI_erode_edge_mm.setText(str(self.params.MRI_erode_edge_mm))

        #Keypoints
        self.ui._space_between_kpt_mm.setText(str(self.params.space_between_kpt_mm))
        self.ui._tumor_ROI_enlarge_factor.setText(str(self.params.tumor_ROI_enlarge_factor))

        self.ui._use_custom_registration_metric.setChecked(self.params.use_custom_registration_metric)

    def setEnabled_App(self,status):
        self.ui.tabWidget.setEnabled(status)
        self.ui.widget.setEnabled(status)
        self.ui.widget_2.setEnabled(status)




    def updateDisplayTitle(self, index):

        match index:
            case -1:
                self.ui._display_title.setText("")

            #Brain extraction
            case self.process_idx.Brain_extraction:
                self.ui._display_title.setText("Brain extraction in T1 volume")

            #fMRI to T1 registration
            case self.process_idx.fMRI_to_T1_registration:
                self.ui._display_title.setText("fMRI to T1 registration (T1: blue; fMRI: red)")

            #Plot MRI projection
            case self.process_idx.MRI_projection_all:
                self.ui._display_title.setText("Brain tumor segementation using BRATS - 2D orthogonal projection of the brain cortex in the T1 volume (Tumor: red contour)")

            case self.process_idx.Tumor_segmentation:
                self.ui._display_title.setText("Brain tumor segementation using BRATS")

            case self.process_idx.MRI_projection:
                self.ui._display_title.setText("2D orthogonal projection of the brain cortex in the T1 volume")

            #Blood vessel enhancement
            case self.process_idx.Blood_vessel_enhancement:
                self.ui._display_title.setText("Blood vessel enhancement in MRI and optics images (Tumor: red contour, Blood vessels: green contours)")

            #Optics to MRI registration
            case self.process_idx.Optics_to_MRI_registration:
                self.ui._display_title.setText("Optics to MRI registration (MRI: red; Optics: blue; Common vessel: magenta)")

            #Check init points
            case self.process_idx.Optics_to_MRI_registration_check_Init_Points:
                self.ui._display_title.setText("MRI and optics skeletons and init points in blue")

            #Check init points
            case self.process_idx.Optics_to_MRI_registration_define_Init_Points:
                self.ui._display_title.setText("Select initialization points in MRI and optics skeletons. Then click on: Process optics to MRI registration")

            #Display registrtion results
            case self.process_idx.Display_registration_results:
                self.ui._display_title.setText("Display registration results (fMRI: Cyan; fOptics: Blue)")

            #Display registrtion results
            case self.process_idx.Registration_validation:
                self.ui._display_title.setText("Validation landmarks (MRI: Red; Optics: Blue)")
            case _:
                pass



    ########################
    # Display results
    ########################
    def on_display_images(self, proj1, proj2):
        # Stop the loading animation
        self.stop_animation()


        #Display result images
        self.ui._display.set_Images(proj1,proj2)
        self.setEnabled_App(True)

    def on_display_status(self,status):
        self.ui._infoData.setText(status)

    def Display_restults(self, index, run_in_separate_thread=True):

        if index == self.process_idx.Registration_validation:
            self.onCalculate_Registration_error()
            return

        #Clear figure
        self.ui._display.clear_figure()

        #Update title
        self.updateDisplayTitle(index)

        self.setEnabled_App(False)


        # Start the loading animation
        self.start_animation()

        #Hide or display params
        self.ui._param_display.hide()
        self.ui._slider_legend.hide()
        if index == self.process_idx.fMRI_to_T1_registration:
            self.ui._param_display.show()
            self.ui._slider_legend.show()



        #Create worker
        self.worker = WorkerThread(idx=index,
                                   process=False,
                                   fMRI_files=self.fMRI_files,
                                   fOptics_files = self.fOptics_files,
                                   Mypath = self.Mypath,
                                   params = self.params)

        #connect slots
        self.worker.signals.status_signal.connect(self.on_display_status)
        self.worker.signals.display_signal.connect(self.on_display_images)
        #start thread
        self.threadPool.start(self.worker)



    def on_displaySliderChanged(self):
        value = self.ui._param_display.value()
        self.ui._display.set_alpha(value/100)



    def launch_process(self,index,run_in_separate_thread=True):

        #Clear figure
        self.ui._display.clear_figure()

        #Update title
        self.updateDisplayTitle(index)

        self.setEnabled_App(False)

        # Start the loading animation
        self.start_animation()

        #Create worker
        self.worker = WorkerThread(idx=index,
                                   process=True,
                                   fMRI_files=self.fMRI_files,
                                   fOptics_files = self.fOptics_files,
                                   Mypath = self.Mypath,
                                   params = self.params)

        #connect slots
        self.worker.signals.status_signal.connect(self.on_display_status)
        self.worker.signals.display_signal.connect(self.on_display_images)

        #start thread
        self.threadPool.start(self.worker)




    ########################
    # Brain extraction
    ########################
    def on_f_bet_changed(self, text):
        self.params.f_bet = float(text)

    def on_kdilatation_brain_mask_changed(self, text):
        self.params.k_dilatation_brain = int(text)

    def on_use_bet(self,state):
        if state==0:
            self.params.use_bet = False
        else:
            self.params.use_bet = True

    def brain_extraction_process(self):
        self.launch_process(self.process_idx.Brain_extraction)




    ########################
    # fMRI registration to T1
    ########################

    def on_copy_fMRI_files(self,state):
        if state==0:
            self.params.register_fMRI_to_T1 = True
        else:
            self.params.register_fMRI_to_T1 = False

    def fMRI_to_T1_registration_process(self):
        self.launch_process(self.process_idx.fMRI_to_T1_registration)

    ########################
    # MRI projection
    ########################
    def process_all_MRI_projection(self):
        self.launch_process(self.process_idx.MRI_projection_all)

    def brain_tumor_segmentation_process(self):
        self.launch_process(self.process_idx.Tumor_segmentation)

    def MRI_projection_process(self):
        self.launch_process(self.process_idx.MRI_projection)

    def on_Projection_choice_changed(self, projection_type):
        self.params.projection_type = projection_type

    # def on_Projection_slice_order_changed(self, projection_slice_order):
    #     self.params.projection_slice_order = projection_slice_order

    def on_projection_basis_choice_changed(self, projection_basis):
        self.params.projection_base_axis = projection_basis

    def on_projection_axis_passing_through_changed(self, axis_projection):
        self.params.axis_projection = axis_projection

    def on_projection_MRI_erode_edge_mm_changed(self, value):
        self.params.MRI_erode_edge_mm = float(value)

    ########################
    # Blood vessel enhancement
    ########################

    def blood_vessel_enhancement_process(self):

        #Set manual skeletons if it has been defined
        if self.ui._display.optics_mask_skeleton is not None:
            self.params.optics_skeleton_apriori = self.ui._display.optics_mask_skeleton

        if self.ui._display.MRI_mask_skeleton is not None:
            self.params.MRI_skeleton_apriori = self.ui._display.MRI_mask_skeleton


        self.launch_process(self.process_idx.Blood_vessel_enhancement)

    # Manual selection of optical blood vessel for helping the registration procedure
    def manual_optics_vessel_selection(self):

        # if self.ui._display.mask_skeleton is not None:
        #     print("Plot mask test")
        #     plot_test(self.ui._display.mask_skeleton)
        # else:
        #     print("mask empty")

        error, Optics_img = main_get_optics_image(self.Mypath)
        if Optics_img is not None:
            self.ui._display.draw_optics_skeleton(Optics_img)


    def manual_MRI_vessel_selection(self):

        error, MRI_img = main_load_MRI_projection(self.Mypath)
        if MRI_img is not None:
            self.ui._display.draw_MRI_skeleton(MRI_img)


    def clear_skeletons(self):
        self.ui._display.optics_mask_skeleton = None
        self.ui._display.MRI_mask_skeleton = None
        self.params.optics_skeleton_apriori = None
        self.params.MRI_skeleton_apriori = None

        self.blood_vessel_enhancement_process()


    def on_MRI_thresh_changed(self,text):
        self.params.thresh_MRI = int(text)

    def on_Optics_thresh_changed(self,text):
        self.params.thresh_optics = int(text)

    def on_min_MRI_vessel_changed(self,text):
        self.params.sigma_minimum_mm_MRI = float(text)

    def on_min_Optics_vessel_changed(self,text):
        self.params.sigma_minimum_mm_optics = float(text)

    def on_max_MRI_vessel_changed(self,text):
        self.params.sigma_maximum_mm_MRI = float (text)

    def on_max_Optics_vessel_changed(self,text):
        self.params.sigma_maximum_mm_optics = float(text)

    def on_kernel_specular_reflection_changed(self,text):
        self.params.ksize_mm_kernal_specular_reflection_optics = float(text)

    def on_kernel_exterior_mask_mm(self, text):
        self.params.kernel_mm_optical_mask_erosion = float(text)



    #################################
    # Optics MRI registration process
    #################################

    def Optics_MRI_registration_process(self):

        #Get init points if an init has been done
        if self.ui._display.pt_Optics is not None and self.ui._display.pt_MRI is not None:
            kp = self.ui._display.pt_Optics
            for i in range(len(kp)):
                kp[i] /= self.params.Optical_downsampling_factor
            self.params.kpt_optics = kp
            self.params.kpts_MRI_tumor = self.ui._display.pt_MRI

        self.launch_process(self.process_idx.Optics_to_MRI_registration)


    def Optics_MRI_registration_process_check_Init_Points(self):
        self.Display_restults(self.process_idx.Optics_to_MRI_registration_check_Init_Points)

    def Optics_MRI_registration_process_define_new_Init_Points(self):
        #Update title
        self.updateDisplayTitle(self.process_idx.Optics_to_MRI_registration_define_Init_Points)

        #plot images
        error, MRI_img, Optics_img = main_get_skeleton_images(self.Mypath, self.params)


        if MRI_img is not None and Optics_img is not None:
            self.ui._display.plot_two_images(MRI_img,Optics_img)

    def Optics_MRI_registration_test_manual_alignement(self):
        main_place_optics_on_MRI(self.Mypath, self.params)


    def Optics_MRI_registration_on_New_space_between_kpt_mm(self, value):
        self.params.space_between_kpt_mm = float(value)
        # self.Optics_MRI_registration_process_check_Init_Points()

    def Optics_MRI_registration_on_New_tumor_ROI_enlarge_factor(self, value):
        self.params.tumor_ROI_enlarge_factor = float(value)
        # self.Optics_MRI_registration_process_check_Init_Points()

    def Optics_MRI_registration_on_use_custom_registration_metric(self, value):
        self.params.use_custom_registration_metric = value

    #################################
    # Display final results
    #################################

    def Process_result_files(self):
        self.launch_process(self.process_idx.Display_registration_results)


    def Select_fMRI_files(self):
        self.fMRI_files = []
        dir = self.Mypath.main_path+"/MRI/fMRI/inferences"

        out_msg = ""
        if os.path.exists(dir):
            self.fMRI_files, _ = QFileDialog.getOpenFileNames(None, "Select Files", dir, "NIfTI Files (*.nii *.nii.gz)")
            if self.fMRI_files == []:
                out_msg = "No files selected"
            else:
                out_msg = ""
                for f in self.fMRI_files:
                    out_msg +=os.path.basename(f)+"\n"

        else:
            self.fMRI_files = []
            out_msg = "No fMRI files"


        self.ui._files_fMRI.setText(out_msg)

        #Display results
        self.Display_restults(self.process_idx.Display_registration_results)



    def Select_fOptics_files(self):
        self.fOptics_files = []
        dir = self.Mypath.main_path_optics+"/foptics/"

        out_msg = ""
        if os.path.exists(dir):
            self.fOptics_files, _ = QFileDialog.getOpenFileNames(None, "Select Files", dir)
            if self.fOptics_files == []:
                out_msg = "No files selected"
            else:
                out_msg = ""
                for f in self.fOptics_files:
                    out_msg +=os.path.basename(f)+"\n"

        else:
            self.fOptics_files = []
            out_msg = "No fMRI files"

        self.ui._files_fOptics.setText(out_msg)

        #Display results
        self.Display_restults(self.process_idx.Display_registration_results)




    #################################
    # Registration validation
    #################################

    def onChooseValidationLandmarks(self):

        #Load images
        error, MRI_img, Optics_img = main_get_validation_landmarks_img(self.Mypath)

        #Display images
        if MRI_img is not None and Optics_img is not None:
            self.ui._display.plot_validation_landmarks(MRI_img,Optics_img, self.Mypath.output_dir)
            self.updateDisplayTitle(self.process_idx.Registration_validation)

    def onCalculate_Registration_error(self):


        #Load landmark points
        status, points_optics, points_mri, reso_MRI, Optics_img = main_load_validation_landmarks_img(self.Mypath)

        print("[onCalculate_Registration_error] "+status)

        if status == "Success":
            #Compute Euclidean distance in pixels
            dist_mm = np.sqrt(((points_optics[:,0] - points_mri[:,0])*reso_MRI[0])**2 + ((points_optics[:,1] - points_mri[:,1])*reso_MRI[1])**2)


            self.ui._display.set_Images(Optics_img)
            self.ui._infoData.setText(status)
            self.ui._results_registration.setText("Registration error: "+str(int(dist_mm.mean()*100)/100) +" mm +/- "+str(int(dist_mm.std()*100)/100)+" mm - MRI resolution: ("+str(reso_MRI[0])+" ; "+str(reso_MRI[1]) + " mm)")
            self.updateDisplayTitle(self.process_idx.Registration_validation)







if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = main()
    # widget.showFullScreen();
    widget.show()
    sys.exit(app.exec())
