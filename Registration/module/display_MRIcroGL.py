import gl
gl.resetdefaults()
#open background image
gl.loadimage('/home/caredda/Videos/Optical_MRI_data/P_023/results/r_T1_bet.nii.gz')
#open overlay: show positive regions
gl.overlayload('/home/caredda/Videos/Optical_MRI_data/P_023/results/Projection/Rec_Optical_T1.nii.gz')
gl.colorname(1,'4hot')

