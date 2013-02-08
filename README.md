# FMRI to GEO

Converts 4D NIfTI-1 scans (.nii or .nii.gz) to SideFX .geo files.

Outputs a sequence of lattice point clouds with a 16-bit integer (0-65535) attribute called "value".

## Prerequisites

-   Python
-   Pip
-   Numpy
-   NiBabel

### Installation

#### Ubuntu

    sudo apt-get install python python-pip
    sudo pip install numpy NiBabel


## Example usage:
   
    wget http://nifti.nimh.nih.gov/nifti-1/data/filtered_func_data.nii.gz
    ./nifti1_4d_to_geo.py -v -z 4 filtered_func_data.nii.gz