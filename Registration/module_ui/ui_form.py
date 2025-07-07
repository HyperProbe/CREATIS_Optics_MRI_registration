# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
    QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSlider, QTabWidget,
    QVBoxLayout, QWidget)

from module_ui.plot_functions import MatplotlibWidget

class Ui_main(object):
    def setupUi(self, main):
        if not main.objectName():
            main.setObjectName(u"main")
        main.resize(1019, 586)
        self.verticalLayout = QVBoxLayout(main)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget = QWidget(main)
        self.widget.setObjectName(u"widget")
        self.gridLayout_5 = QGridLayout(self.widget)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self._getDataPath = QPushButton(self.widget)
        self._getDataPath.setObjectName(u"_getDataPath")

        self.gridLayout_5.addWidget(self._getDataPath, 0, 0, 1, 1)

        self._HSI_imaging = QCheckBox(self.widget)
        self._HSI_imaging.setObjectName(u"_HSI_imaging")

        self.gridLayout_5.addWidget(self._HSI_imaging, 0, 1, 1, 1)


        self.verticalLayout.addWidget(self.widget)

        self.tabWidget = QTabWidget(main)
        self.tabWidget.setObjectName(u"tabWidget")
        self._tab_brain_extraction = QWidget()
        self._tab_brain_extraction.setObjectName(u"_tab_brain_extraction")
        self.horizontalLayout_2 = QHBoxLayout(self._tab_brain_extraction)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self._extract_brain_surface = QPushButton(self._tab_brain_extraction)
        self._extract_brain_surface.setObjectName(u"_extract_brain_surface")

        self.horizontalLayout_2.addWidget(self._extract_brain_surface)

        self._use_bet = QCheckBox(self._tab_brain_extraction)
        self._use_bet.setObjectName(u"_use_bet")

        self.horizontalLayout_2.addWidget(self._use_bet)

        self._f_bet = QLineEdit(self._tab_brain_extraction)
        self._f_bet.setObjectName(u"_f_bet")

        self.horizontalLayout_2.addWidget(self._f_bet)

        self.label = QLabel(self._tab_brain_extraction)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label)

        self._kdilatation_brain_mask = QLineEdit(self._tab_brain_extraction)
        self._kdilatation_brain_mask.setObjectName(u"_kdilatation_brain_mask")

        self.horizontalLayout_2.addWidget(self._kdilatation_brain_mask)

        self.label_2 = QLabel(self._tab_brain_extraction)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.tabWidget.addTab(self._tab_brain_extraction, "")
        self.tab_fMRI_registration = QWidget()
        self.tab_fMRI_registration.setObjectName(u"tab_fMRI_registration")
        self.horizontalLayout_3 = QHBoxLayout(self.tab_fMRI_registration)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self._process_fMRI_to_T1_registration = QPushButton(self.tab_fMRI_registration)
        self._process_fMRI_to_T1_registration.setObjectName(u"_process_fMRI_to_T1_registration")

        self.horizontalLayout_3.addWidget(self._process_fMRI_to_T1_registration)

        self._copy_fMRI_files = QCheckBox(self.tab_fMRI_registration)
        self._copy_fMRI_files.setObjectName(u"_copy_fMRI_files")

        self.horizontalLayout_3.addWidget(self._copy_fMRI_files)

        self.tabWidget.addTab(self.tab_fMRI_registration, "")
        self.tab_MRI_projection = QWidget()
        self.tab_MRI_projection.setObjectName(u"tab_MRI_projection")
        self.horizontalLayout_4 = QHBoxLayout(self.tab_MRI_projection)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self._process_all_MRI_projection = QPushButton(self.tab_MRI_projection)
        self._process_all_MRI_projection.setObjectName(u"_process_all_MRI_projection")

        self.horizontalLayout_4.addWidget(self._process_all_MRI_projection)

        self._process_tumor_segmentation = QPushButton(self.tab_MRI_projection)
        self._process_tumor_segmentation.setObjectName(u"_process_tumor_segmentation")

        self.horizontalLayout_4.addWidget(self._process_tumor_segmentation)

        self._process_MRI_projection = QPushButton(self.tab_MRI_projection)
        self._process_MRI_projection.setObjectName(u"_process_MRI_projection")

        self.horizontalLayout_4.addWidget(self._process_MRI_projection)

        self._projection_basis_choice = QComboBox(self.tab_MRI_projection)
        self._projection_basis_choice.setObjectName(u"_projection_basis_choice")

        self.horizontalLayout_4.addWidget(self._projection_basis_choice)

        self.tabWidget.addTab(self.tab_MRI_projection, "")
        self.tab_blood_vessel_enhancement = QWidget()
        self.tab_blood_vessel_enhancement.setObjectName(u"tab_blood_vessel_enhancement")
        self.gridLayout = QGridLayout(self.tab_blood_vessel_enhancement)
        self.gridLayout.setObjectName(u"gridLayout")
        self.groupBox = QGroupBox(self.tab_blood_vessel_enhancement)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.gridLayout_7 = QGridLayout(self.groupBox)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self._MRI_thresh = QLineEdit(self.groupBox)
        self._MRI_thresh.setObjectName(u"_MRI_thresh")

        self.gridLayout_7.addWidget(self._MRI_thresh, 1, 0, 1, 1)

        self.label_6 = QLabel(self.groupBox)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_7.addWidget(self.label_6, 0, 2, 1, 1)

        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_7.addWidget(self.label_4, 0, 1, 1, 1)

        self._min_vessel_MRI = QLineEdit(self.groupBox)
        self._min_vessel_MRI.setObjectName(u"_min_vessel_MRI")

        self.gridLayout_7.addWidget(self._min_vessel_MRI, 1, 1, 1, 1)

        self.label_8 = QLabel(self.groupBox)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_7.addWidget(self.label_8, 0, 0, 1, 1)

        self._max_vessel_MRI = QLineEdit(self.groupBox)
        self._max_vessel_MRI.setObjectName(u"_max_vessel_MRI")

        self.gridLayout_7.addWidget(self._max_vessel_MRI, 1, 2, 1, 1)

        self._manual_MRI_vessel_selection = QPushButton(self.groupBox)
        self._manual_MRI_vessel_selection.setObjectName(u"_manual_MRI_vessel_selection")

        self.gridLayout_7.addWidget(self._manual_MRI_vessel_selection, 1, 3, 1, 1)


        self.gridLayout.addWidget(self.groupBox, 5, 0, 1, 7)

        self._process_blood_vessel_enhancement = QPushButton(self.tab_blood_vessel_enhancement)
        self._process_blood_vessel_enhancement.setObjectName(u"_process_blood_vessel_enhancement")

        self.gridLayout.addWidget(self._process_blood_vessel_enhancement, 0, 0, 1, 4)

        self._clear_skeletons = QPushButton(self.tab_blood_vessel_enhancement)
        self._clear_skeletons.setObjectName(u"_clear_skeletons")

        self.gridLayout.addWidget(self._clear_skeletons, 0, 4, 1, 3)

        self.groupBox_2 = QGroupBox(self.tab_blood_vessel_enhancement)
        self.groupBox_2.setObjectName(u"groupBox_2")
        font = QFont()
        font.setBold(False)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.gridLayout_8 = QGridLayout(self.groupBox_2)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self._optics_thresh = QLineEdit(self.groupBox_2)
        self._optics_thresh.setObjectName(u"_optics_thresh")

        self.gridLayout_8.addWidget(self._optics_thresh, 1, 0, 1, 1)

        self.label_3 = QLabel(self.groupBox_2)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_8.addWidget(self.label_3, 0, 1, 1, 1)

        self._max_vessel_Optics = QLineEdit(self.groupBox_2)
        self._max_vessel_Optics.setObjectName(u"_max_vessel_Optics")

        self.gridLayout_8.addWidget(self._max_vessel_Optics, 1, 2, 1, 1)

        self._min_vessel_Optics = QLineEdit(self.groupBox_2)
        self._min_vessel_Optics.setObjectName(u"_min_vessel_Optics")

        self.gridLayout_8.addWidget(self._min_vessel_Optics, 1, 1, 1, 1)

        self.label_7 = QLabel(self.groupBox_2)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_8.addWidget(self.label_7, 0, 0, 1, 1)

        self.label_5 = QLabel(self.groupBox_2)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_8.addWidget(self.label_5, 0, 2, 1, 1)

        self._manual_optics_vessel_selection = QPushButton(self.groupBox_2)
        self._manual_optics_vessel_selection.setObjectName(u"_manual_optics_vessel_selection")

        self.gridLayout_8.addWidget(self._manual_optics_vessel_selection, 1, 3, 1, 1)


        self.gridLayout.addWidget(self.groupBox_2, 4, 0, 1, 7)

        self.tabWidget.addTab(self.tab_blood_vessel_enhancement, "")
        self._tabMRI_optics_MRI_registration = QWidget()
        self._tabMRI_optics_MRI_registration.setObjectName(u"_tabMRI_optics_MRI_registration")
        self.gridLayout_6 = QGridLayout(self._tabMRI_optics_MRI_registration)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self._check_init_points = QPushButton(self._tabMRI_optics_MRI_registration)
        self._check_init_points.setObjectName(u"_check_init_points")

        self.gridLayout_6.addWidget(self._check_init_points, 1, 0, 1, 1)

        self._choose_init_points = QPushButton(self._tabMRI_optics_MRI_registration)
        self._choose_init_points.setObjectName(u"_choose_init_points")

        self.gridLayout_6.addWidget(self._choose_init_points, 1, 1, 1, 1)

        self._test_manual_alignement = QPushButton(self._tabMRI_optics_MRI_registration)
        self._test_manual_alignement.setObjectName(u"_test_manual_alignement")

        self.gridLayout_6.addWidget(self._test_manual_alignement, 1, 2, 1, 1)

        self._process_optics_to_MRI_registration = QPushButton(self._tabMRI_optics_MRI_registration)
        self._process_optics_to_MRI_registration.setObjectName(u"_process_optics_to_MRI_registration")

        self.gridLayout_6.addWidget(self._process_optics_to_MRI_registration, 0, 0, 1, 3)

        self.tabWidget.addTab(self._tabMRI_optics_MRI_registration, "")
        self.tab_display_results = QWidget()
        self.tab_display_results.setObjectName(u"tab_display_results")
        self.gridLayout_2 = QGridLayout(self.tab_display_results)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self._files_fOptics = QLabel(self.tab_display_results)
        self._files_fOptics.setObjectName(u"_files_fOptics")

        self.gridLayout_2.addWidget(self._files_fOptics, 2, 0, 1, 1)

        self._select_fMRI_files = QPushButton(self.tab_display_results)
        self._select_fMRI_files.setObjectName(u"_select_fMRI_files")

        self.gridLayout_2.addWidget(self._select_fMRI_files, 1, 1, 1, 1)

        self._files_fMRI = QLabel(self.tab_display_results)
        self._files_fMRI.setObjectName(u"_files_fMRI")

        self.gridLayout_2.addWidget(self._files_fMRI, 2, 1, 1, 1)

        self._select_fOptics_files = QPushButton(self.tab_display_results)
        self._select_fOptics_files.setObjectName(u"_select_fOptics_files")

        self.gridLayout_2.addWidget(self._select_fOptics_files, 1, 0, 1, 1)

        self._process_result_files = QPushButton(self.tab_display_results)
        self._process_result_files.setObjectName(u"_process_result_files")

        self.gridLayout_2.addWidget(self._process_result_files, 0, 0, 1, 2)

        self.tabWidget.addTab(self.tab_display_results, "")
        self._tab_registration_validation = QWidget()
        self._tab_registration_validation.setObjectName(u"_tab_registration_validation")
        self.gridLayout_4 = QGridLayout(self._tab_registration_validation)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self._choose_validation_landmarks = QPushButton(self._tab_registration_validation)
        self._choose_validation_landmarks.setObjectName(u"_choose_validation_landmarks")

        self.gridLayout_4.addWidget(self._choose_validation_landmarks, 0, 0, 1, 1)

        self._calculate_registration_error = QPushButton(self._tab_registration_validation)
        self._calculate_registration_error.setObjectName(u"_calculate_registration_error")

        self.gridLayout_4.addWidget(self._calculate_registration_error, 0, 1, 1, 1)

        self._results_registration = QLabel(self._tab_registration_validation)
        self._results_registration.setObjectName(u"_results_registration")
        self._results_registration.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self._results_registration, 1, 0, 1, 2)

        self.tabWidget.addTab(self._tab_registration_validation, "")

        self.verticalLayout.addWidget(self.tabWidget)

        self.widget_2 = QWidget(main)
        self.widget_2.setObjectName(u"widget_2")
        self.gridLayout_3 = QGridLayout(self.widget_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self._display = MatplotlibWidget(self.widget_2)
        self._display.setObjectName(u"_display")

        self.gridLayout_3.addWidget(self._display, 1, 0, 2, 1)

        self._slider_legend = QLabel(self.widget_2)
        self._slider_legend.setObjectName(u"_slider_legend")
        self._slider_legend.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self._slider_legend, 2, 1, 1, 1)

        self._param_display = QSlider(self.widget_2)
        self._param_display.setObjectName(u"_param_display")
        self._param_display.setOrientation(Qt.Orientation.Vertical)

        self.gridLayout_3.addWidget(self._param_display, 1, 1, 1, 1)

        self._display_title = QLabel(self.widget_2)
        self._display_title.setObjectName(u"_display_title")
        self._display_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self._display_title, 0, 0, 1, 1)

        self.gridLayout_3.setRowStretch(1, 10)
        self.gridLayout_3.setColumnStretch(0, 1)

        self.verticalLayout.addWidget(self.widget_2)

        self._infoData = QLabel(main)
        self._infoData.setObjectName(u"_infoData")

        self.verticalLayout.addWidget(self._infoData)

        self.verticalLayout.setStretch(2, 10)

        self.retranslateUi(main)

        self.tabWidget.setCurrentIndex(3)


        QMetaObject.connectSlotsByName(main)
    # setupUi

    def retranslateUi(self, main):
        main.setWindowTitle(QCoreApplication.translate("main", u"main", None))
        self._getDataPath.setText(QCoreApplication.translate("main", u"...", None))
        self._HSI_imaging.setText(QCoreApplication.translate("main", u"HSI imaging", None))
        self._extract_brain_surface.setText(QCoreApplication.translate("main", u"Extract brain surface", None))
        self._use_bet.setText(QCoreApplication.translate("main", u"use bet", None))
        self.label.setText(QCoreApplication.translate("main", u"f_bet", None))
        self.label_2.setText(QCoreApplication.translate("main", u"Dilation brain mask (px)", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self._tab_brain_extraction), QCoreApplication.translate("main", u"Extract brain surface", None))
        self._process_fMRI_to_T1_registration.setText(QCoreApplication.translate("main", u"Register fMRI on T1", None))
        self._copy_fMRI_files.setText(QCoreApplication.translate("main", u"Only copy fMRI files (PARAM TO REMOVE)", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_fMRI_registration), QCoreApplication.translate("main", u"Register fMRI on T1", None))
        self._process_all_MRI_projection.setText(QCoreApplication.translate("main", u"Run all", None))
        self._process_tumor_segmentation.setText(QCoreApplication.translate("main", u"Brain tumor segmentation", None))
        self._process_MRI_projection.setText(QCoreApplication.translate("main", u"2D MRI projection", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_MRI_projection), QCoreApplication.translate("main", u"Create 2D MRI projection", None))
        self.groupBox.setTitle(QCoreApplication.translate("main", u"MRI skeleton", None))
        self.label_6.setText(QCoreApplication.translate("main", u"Max vessel size (mm)", None))
        self.label_4.setText(QCoreApplication.translate("main", u"Min vessel size (mm)", None))
        self.label_8.setText(QCoreApplication.translate("main", u"Threshold", None))
        self._manual_MRI_vessel_selection.setText(QCoreApplication.translate("main", u"Manual vessel selection", None))
        self._process_blood_vessel_enhancement.setText(QCoreApplication.translate("main", u"Process blood vessels enhancement", None))
        self._clear_skeletons.setText(QCoreApplication.translate("main", u"Clear optics skeleton", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("main", u"Optics skeleton", None))
        self.label_3.setText(QCoreApplication.translate("main", u"Min vessel size (mm)", None))
        self.label_7.setText(QCoreApplication.translate("main", u"Threshold", None))
        self.label_5.setText(QCoreApplication.translate("main", u"Max vessel size (mm)", None))
        self._manual_optics_vessel_selection.setText(QCoreApplication.translate("main", u"Manual vessel selection", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_blood_vessel_enhancement), QCoreApplication.translate("main", u"Blood vessels enhancement", None))
        self._check_init_points.setText(QCoreApplication.translate("main", u"Check initialization points", None))
        self._choose_init_points.setText(QCoreApplication.translate("main", u"Choose new initialization points", None))
        self._test_manual_alignement.setText(QCoreApplication.translate("main", u"Test manual aligment", None))
        self._process_optics_to_MRI_registration.setText(QCoreApplication.translate("main", u"Process optics to MRI registration", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self._tabMRI_optics_MRI_registration), QCoreApplication.translate("main", u"Optics to MRI registration", None))
        self._files_fOptics.setText(QCoreApplication.translate("main", u"No files selected", None))
        self._select_fMRI_files.setText(QCoreApplication.translate("main", u"Select fMRI files", None))
        self._files_fMRI.setText(QCoreApplication.translate("main", u"No files selected", None))
        self._select_fOptics_files.setText(QCoreApplication.translate("main", u"Select fOptics files", None))
        self._process_result_files.setText(QCoreApplication.translate("main", u"Process results files", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_display_results), QCoreApplication.translate("main", u"Display results", None))
        self._choose_validation_landmarks.setText(QCoreApplication.translate("main", u"Choose validation landmarks", None))
        self._calculate_registration_error.setText(QCoreApplication.translate("main", u"Calculate registration error (mm)", None))
        self._results_registration.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self._tab_registration_validation), QCoreApplication.translate("main", u"Registration validation", None))
        self._slider_legend.setText(QCoreApplication.translate("main", u"Alpha (%)", None))
        self._display_title.setText("")
        self._infoData.setText("")
    # retranslateUi

