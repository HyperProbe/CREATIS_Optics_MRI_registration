# CREATIS_Optics_MRI_registration

Registration of 2D intraoperative optical images of the exposed brain (RGB or hyperspectral) onto a 3D T1-weighted pre-operative MRI.

The registration relies on matching common cerebral structures visible in both modalities, such as [cortical vessels / sulci / gyri, adapt to your method]. It is implemented in Python with [ITK](https://itk.org/) and [itk-elastix](https://github.com/InsightSoftwareConsortium/ITKElastix).

## Citation

If you use this code, please cite:

> [XXXX: authors, title, journal, year, DOI]

```bibtex
@article{XXXX,
  title   = {},
  author  = {},
  journal = {},
  year    = {},
  doi     = {}
}
```

## Repository structure

```
CREATIS_Optics_MRI_registration/
├── create_registration_venv     # script that creates the Python virtual environment
└── Registration/
    ├── main.ipynb               # notebook with all the registration steps
    └── Graphic_interface.py     # Qt graphical interface to display results
```

## Installation

Create the Python virtual environment with the provided script: create_registration_venv

## Usage

### 1. Registration pipeline

Open the notebook, which contains all the steps of the registration process:

```bash
jupyter notebook Registration/main.ipynb
```

Inputs:

- 2D intraoperative optical image: RGB or hyperspectral
- 2D image resolution (indicated in mm in a txt file Resolution)
- 3D pre-operative T1-weighted MRI in nifti format
- 3D pre-operative FLAIR MRI
  

Outputs:

- `[registered image / transformation parameters / overlay, etc.]`

### 2. Graphical interface

For easier visualisation of the results, use the Qt interface:

```bash
python Registration/Graphic_interface.py
```

## Method overview

1. `[Pre-processing of the optical image]`
2. `[Extraction or segmentation of the MRI structures used for matching]`
3. `[Registration with itk-elastix (transform type, metric, optimiser)]`
4. `[Visualisation / evaluation of the result]`

## Data

`[Example data availability, or note that data cannot be shared for ethical reasons.]`
