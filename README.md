# FMRI to GEO

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