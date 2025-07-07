"""
All needed ITK python functions used for the project
"""

import itk   
from math import atan2, sqrt
import numpy as np
#%% Arithmetic operators

def AdditionFilter(spatialObject1, spatialObject2):
    """
    Parameters
    ----------
    spatialObject1 : ITK image
    spatialObject2 : ITK image

    Returns
    -------
    
    Pixel-wise sum of spatialObject1 and spatialObject2

    """
    ImageType = type(spatialObject1)
    print(ImageType)
    additionFilter = itk.AddImageFilter[ImageType, ImageType, ImageType].New()
    additionFilter.SetInput1(spatialObject1)
    additionFilter.SetInput2(spatialObject2)
    additionFilter.Update()
    return additionFilter.GetOutput()

def SubtractFilter(spatialObject1, spatialObject2):
    """
    Parameters
    ----------
    spatialObject1 : ITK image
    spatialObject2 : ITK image

    Returns
    -------
    
    Pixel-wise difference between spatialObject1 and spatialObject2

    """
    ImageType = type(spatialObject1)
    subtractFilter = itk.SubtractImageFilter[ImageType, ImageType, ImageType].New()
    subtractFilter.SetInput1(spatialObject1)
    subtractFilter.SetInput2(spatialObject2)
    subtractFilter.Update()
    return subtractFilter.GetOutput()

def MultiplyFilter(spatialObject1, spatialObject2):
    """
    Parameters
    ----------
    spatialObject1 : ITK image
    spatialObject2 : ITK image

    Returns
    -------
    
    Pixel-wise multiplication between spatialObject1 and spatialObject2

    """
    ImageType = type(spatialObject1)
    multiplyFilter = itk.MultiplyImageFilter[ImageType, ImageType, ImageType].New()
    multiplyFilter.SetInput1(spatialObject1)
    multiplyFilter.SetInput2(spatialObject2)
    multiplyFilter.Update()
    return multiplyFilter.GetOutput()

def DivideFilter(spatialObject1, spatialObject2):
    """
    Parameters
    ----------
    spatialObject1 : ITK image
    spatialObject2 : ITK image

    Returns
    -------
    
    Pixel-wise division of spatialObject1 and spatialObject2
    
    """
    ImageType = type(spatialObject1)
    divideFilter = itk.DivideImageFilter[ImageType, ImageType, ImageType].New()
    divideFilter.SetInput1(spatialObject1)
    divideFilter.SetInput2(spatialObject2)
    divideFilter.Update()
    return divideFilter.GetOutput()


#%% Morphological operators

def StructuringElement(kernelType,kernelSize,spatialDimension):
    """
    
    Define of morphological structuring element

    Parameters
    ----------
    kernelType : 'Ball', 'Cross', 'Box'
    kernelSize : the number of pixels that the neighborhood extends outward from the center pixel. 
    For example, a 2D BinaryBallStructuringElement object with a radius of 2x2 has sides of length 5x5
    spatialDimension : dimension of the space

    Returns
    -------
    structuringElement

    """
    StructuringElementType = itk.FlatStructuringElement[spatialDimension]
    if kernelType == 'Ball':
        structuringElement = StructuringElementType.Ball(kernelSize)
    if kernelType =='Cross':
        structuringElement = StructuringElementType.Cross(kernelSize)
    if kernelType == 'Box':
        structuringElement = StructuringElementType.Box(kernelSize)   
    return structuringElement

def ErodeFilter(spatialObject,kernel, foregroundValue=1, backgroundValue=0):
    ImageType = type(spatialObject)
    erodeFilter = itk.BinaryErodeImageFilter[ImageType, ImageType, kernel].New()
    erodeFilter.SetInput(spatialObject)
    erodeFilter.SetKernel(kernel)
    erodeFilter.SetForegroundValue(foregroundValue)
    erodeFilter.SetBackgroundValue(backgroundValue)
    erodeFilter.Update()
    return erodeFilter.GetOutput()

def DilateFilter(spatialObject, kernel, foregroundValue=1, backgroundValue=0):
    ImageType = type(spatialObject)
    dilateFilter = itk.BinaryDilateImageFilter[ImageType, ImageType, kernel].New()
    dilateFilter.SetInput(spatialObject)
    dilateFilter.SetKernel(kernel)
    dilateFilter.SetForegroundValue(foregroundValue)
    dilateFilter.SetBackgroundValue(backgroundValue)
    dilateFilter.Update()
    return dilateFilter.GetOutput()

def OpeningFilter(spatialObject,kernel):
    ImageType = type(spatialObject)
    openingFilter = itk.BinaryMorphologicalOpeningImageFilter[ImageType, ImageType, kernel].New()
    openingFilter.SetInput(spatialObject)
    openingFilter.SetKernel(kernel)
    openingFilter.Update()
    return openingFilter.GetOutput()

def ClosingFilter(spatialObject,kernel):
    ImageType = type(spatialObject)
    closingFilter = itk.BinaryMorphologicalClosingImageFilter[ImageType, ImageType, kernel].New()
    closingFilter.SetInput(spatialObject)
    closingFilter.SetKernel(kernel)
    closingFilter.Update()
    return closingFilter.GetOutput()

def TopHatFilter(spatialObject,kernel):
    ImageType = type(spatialObject)
    tophatFilter = itk.WhiteTopHatImageFilter[ImageType, ImageType, kernel].New()
    tophatFilter.SetInput(spatialObject)
    tophatFilter.SetKernel(kernel)
    tophatFilter.Update()
    return tophatFilter.GetOutput()

def BlackHatFilter(spatialObject,kernel):
    ImageType = type(spatialObject)
    blackhatFilter = itk.BlackTopHatImageFilter[ImageType, ImageType, kernel].New()
    blackhatFilter.SetInput(spatialObject)
    blackhatFilter.SetKernel(kernel)
    blackhatFilter.Update()
    return blackhatFilter.GetOutput()

#%% Transform

def CenteredEuler3DTransfrom(center,rotation,translation):    
    """
    Define a 3D Euler transform giving a rotation matrix, a center of rotation and a translation vector

    Parameters
    ----------
    center : coordinnates of the center of rotation
    rotation : rotation matrix
    translation : translation vector

    Returns
    -------
    centeredeuler3dtransform : ITK 3D euler transform 

    """
    centeredeuler3dtransform = itk.CenteredEuler3DTransform[itk.D].New()
    centeredeuler3dtransform.SetCenter(center)
    centeredeuler3dtransform.SetTranslation(translation)
    euler_x = atan2(rotation[2, 1], rotation[2, 2])
    euler_y = atan2(-rotation[2, 0], sqrt(rotation[2, 1] ** 2 + rotation[2, 2] ** 2))
    euler_z = atan2(rotation[1, 0], rotation[0, 0])
    centeredeuler3dtransform.SetRotation(euler_x,euler_y,euler_z)
    return centeredeuler3dtransform

def Euler3DTransfrom(center,rotation,translation):    
    euler3dtransform = itk.Euler3DTransform[itk.D].New()
    euler3dtransform.SetCenter(center)
    euler3dtransform.SetTranslation(translation)
    euler_x = atan2(rotation[2, 1], rotation[2, 2])
    euler_y = atan2(-rotation[2, 0], sqrt(rotation[2, 1] ** 2 + rotation[2, 2] ** 2))
    euler_z = atan2(rotation[1, 0], rotation[0, 0])
    euler3dtransform.SetRotation(euler_x,euler_y,euler_z)
    return euler3dtransform



#%% ImageGrid

def LinearResampler(spatialObject, shape, spacing, direction, origin, transform=None):
    """
    
    Return linearly resampled object spatialObject after applying a transform. 

    Parameters
    ----------
    spatialObject : ITK input image
    shape : output shape of the resampled image
    spacing : output spacing of the resampled image
    direction : output direction of the resampled image
    origin : output origin of the resampled image
    transform : ITK 3D transform

    Returns
    -------
    spatialObject_resampled 

    """
    ImageType = type(spatialObject)
    resampler = itk.ResampleImageFilter[ImageType, ImageType].New()  
    pixel_interpolation_type = itk.D  # itk linear interpolator is not wrapped for [[itk.F, itk, F], itk.F]
    interpolator = itk.LinearInterpolateImageFunction[ImageType, pixel_interpolation_type].New() 
    resampler.SetInterpolator(interpolator)
    resampler.SetInput(spatialObject)
    resampler.SetSize(shape)
    resampler.SetOutputSpacing(spacing)
    resampler.SetOutputDirection(itk.GetMatrixFromArray(direction))  # The direction type most be: itk matrix D33
    resampler.SetOutputOrigin(origin)
    if transform is not None:
        resampler.SetTransform(transform)
    spatialObject_resampled = resampler.GetOutput()
    spatialObject_resampled.Update()
    return spatialObject_resampled

# Resample a spatialObject with a Nearest Neighbor interpolator
def NearestNeighboorResampler(spatialObject, shape, spacing, direction, origin, factor_spacing):
    ImageType = type(spatialObject)
    resampler = itk.ResampleImageFilter[ImageType, ImageType].New()  
    pixel_interpolation_type = itk.D
    interpolator = itk.NearestNeighborInterpolateImageFunction[ImageType, pixel_interpolation_type].New()  
    resampler.SetInterpolator(interpolator)
    resampler.SetInput(spatialObject)
    resampler.SetSize(shape)
    resampler.SetOutputSpacing(spacing)
    resampler.SetOutputDirection(
        itk.GetMatrixFromArray(direction))  # The direction type most be: itk matrix D33
    resampler.SetOutputOrigin(origin)
    spatialObject_resampled = resampler.GetOutput()
    spatialObject_resampled.Update()
    normalized_spatialObject_resampled = ImageScaler(spatialObject_resampled, 1 / factor_spacing)
    return normalized_spatialObject_resampled

# Return the gravity center of a spatialObject
def getGravityCenter(spatialObject):
    # Calculate the moments of the object
    moments = itk.ImageMomentsCalculator.New(spatialObject)
    moments.Compute()
    # Return the center of gravity
    return moments.GetCenterOfGravity()

# Normalize interpolation
def ImageScaler(spatialObject, factor):
    """
    Scale pixels intensity of spatialObject by factor : factor.

    Parameters
    ----------
    spatialObject : ITK image
    factor : scaling factor

    Returns
    -------
   
    scaled image

    """
    ImageType = type(spatialObject)
    mult_filter = itk.MultiplyImageFilter[ImageType, ImageType, ImageType].New()
    mult_filter.SetInput(spatialObject)
    mult_filter.SetConstant(factor)
    scaled_spatialObject = mult_filter.GetOutput()
    scaled_spatialObject.Update()
    return scaled_spatialObject.GetOutput()

def ImagePyramid(spatialObject, numberOfLevels):
    """
    
    Apply successive gaussian filtering and subsampling on the ITK image spatialObject.

    Parameters
    ----------
    spatialObject : ITK image
    numberOfLevels : number of level of the image pyramid

    Returns
    -------
    
    Return subsampled image. To get intermediate level, specify the layer. For example if numberOfLevels=10, 
    multiresolutionpyramid.GetOutput() will return the last layer, to get layer 1,...,i,....,9, write
    multiresolutionpyramid.GetOutput(i).

    """
    ImageType = type(spatialObject)
    multiresolutionpyramid = itk.MultiResolutionPyramidImageFilter[ImageType, ImageType].New()
    multiresolutionpyramid.SetInput(spatialObject)
    multiresolutionpyramid.SetNumberOfLevels(numberOfLevels)
    multiresolutionpyramid.Update()
    return multiresolutionpyramid.GetOutput()

#%% ImageStatistics

def intensityWindowingImageFilter(spatialObject,WindowMinimum,WindownMaximum,OutputMinimum,OutputMaximum):
    ImageType = type(spatialObject)
    IntensityWindowingImageFilter = itk.IntensityWindowingImageFilter[ImageType, ImageType].New()
    IntensityWindowingImageFilter.SetInput(spatialObject)
    IntensityWindowingImageFilter.SetWindowMinimum(WindowMinimum)
    IntensityWindowingImageFilter.SetWindowMaximum(WindownMaximum)
    IntensityWindowingImageFilter.SetOutputMinimum(OutputMinimum)
    IntensityWindowingImageFilter.SetOutputMaximum(OutputMaximum)
    IntensityWindowingImageFilter.Update()
    return IntensityWindowingImageFilter.GetOutput()


def adaptiveHistogramEqualizationFilter(spatialObject,alpha,beta,radius):
    ImageType = type(spatialObject)
    histogramEqualization = itk.AdaptiveHistogramEqualizationImageFilter.New(spatialObject)
    histogramEqualization.SetAlpha(alpha)
    histogramEqualization.SetBeta(beta)
    radius1 = itk.Size[3]()
    radius1.Fill(radius)
    histogramEqualization.SetRadius(radius1)
    histogramEqualization.Update()
    return histogramEqualization.GetOutput()

def maximumImageFilter(image_a, image_b):
    # The dimension can be different to Volume3D.DIM
    image_type = type(image_a)
    max_filter = itk.MaximumImageFilter[image_type, image_type, image_type].New()
    max_filter.SetInput1(image_a)
    max_filter.SetInput2(image_b)
    max_image = max_filter.GetOutput()
    max_image.Update()

    return max_image

def normalizeImageFilter(spatialObject):
    ImageType = type(spatialObject)
    normalizeFilter = itk.NormalizeImageFilter[ImageType, ImageType].New()
    normalizeFilter.SetInput(spatialObject)
    normalizeFilter.Update()
    return normalizeFilter.GetOutput()

def maximumImageCalculator(spatialObject):
    ImageType = type(spatialObject)
    maximumCalculator = itk.MinimumMaximumImageCalculator[ImageType].New()
    maximumCalculator.SetImage(spatialObject)
    maximumCalculator.ComputeMaximum()
    return maximumCalculator

def additionImageFilter(image_a, image_b):
    # The dimension can be different to Volume3D.DIM
    image_type = type(image_a)
    add_filter = itk.AddImageFilter[image_type, image_type, image_type].New()
    add_filter.SetInput1(image_a)
    add_filter.SetInput2(image_b)
    add_image = add_filter.GetOutput()
    add_image.Update()
    
    return add_image

def histogramMatchingImageFilter(spatialObject,reference):
    # HistogramMatchingImageFilter = itk.HistogramMatchingImageFilter[itk.Image[itk.D,3], itk.Image[itk.D,3]].New()
    HistogramMatchingImageFilter = itk.HistogramMatchingImageFilter.New()
    HistogramMatchingImageFilter.SetInput(spatialObject)
    HistogramMatchingImageFilter.SetReferenceImage(reference)
    HistogramMatchingImageFilter.SetNumberOfHistogramLevels(64)
    HistogramMatchingImageFilter.ThresholdAtMeanIntensityOn()
    HistogramMatchingImageFilter.Update()
    
    return HistogramMatchingImageFilter.GetOutput()

def thresholdAboveImageFilter(spatialObject,threshold):
    ImageType = type(spatialObject)
    ThresholdImageFilter = itk.ThresholdImageFilter[ImageType,ImageType].New()
    ThresholdImageFilter.SetOutsideValue(threshold)
    ThresholdImageFilter.ThresholdAbove()
    ThresholdImageFilter.Update()
    return ThresholdImageFilter.GetOutput()

    
def thresholdBelowImageFilter(spatialObject,threshold,min_val):
    ImageType = type(spatialObject)
    ThresholdImageFilter = itk.ThresholdImageFilter[ImageType].New()
    ThresholdImageFilter.SetInput(spatialObject)
    ThresholdImageFilter.SetOutsideValue(min_val)
    ThresholdImageFilter.ThresholdBelow(threshold)
    ThresholdImageFilter.Update()
    return ThresholdImageFilter.GetOutput()
    

def binaryThreshold(spatialObject,lower_threshold=50):
    # Thresholding: Keeping all intensities above a certain value
    binary_threshold = itk.BinaryThresholdImageFilter.New(spatialObject)
    binary_threshold.SetLowerThreshold(lower_threshold)  # Adjust based on intensity histogram
    binary_threshold.SetUpperThreshold(itk.NumericTraits[itk.F].max())
    binary_threshold.SetInsideValue(1)
    binary_threshold.SetOutsideValue(0)
    binary_threshold.Update()

    # Extract the binary mask
    out = binary_threshold.GetOutput()

    # Convert to unsigned char (UC) 3D image
    out = itk.cast_image_filter(out, ttype=[type(out), itk.Image[itk.UC, 3]])
    return out

