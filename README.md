# In-situ-WRF-Model
In this repository there are three folders. Each folder has a specific function in order to fulfill the final objective, which would be to compare the WRF model with the In-situ data from some CETESB stations within our study area. 

# 1. Extract_WRF_CETESB
* [qualar] (https://github.com/rnoeliab/In-situ-WRF-Model/blob/main/extract_WRF_CETESB/qualar_py.py) This script must be run before running the [WRF_extract] (https://github.com/rnoeliab/In-situ-WRF-Model/blob/main/extract_WRF_CETESB/WRF_extractor.py) script. In the WRF_extract script it should only be modified: the path where the outputs of the WRF model (wrfout) are located, the excel of the coordinates of the CETESB stations of which we are going to carry out the study, the path where the data "all_met", "all_photo" and "wrfout4.dat" will be saved. 

* If we only want to download the cetesb data for a large period and for several stations, the following script can be used: (https://github.com/rnoeliab/In-situ-WRF-Model/blob/main/extract_WRF_CETESB/qualar_extractor.py).

* To work with meteorological data between the WRF model and the CETESB stations, it is recommended to use the following scripts: (https://github.com/rnoeliab/In-situ-WRF-Model/blob/main/extract_WRF_CETESB/qualar_meteo_py.py) and (https://github.com/rnoeliab/In-situ-WRF-Model/blob/main/extract_WRF_CETESB/WRF_meteo_extractor.py).

# 2. Read_save_data
# 3. comparate_data

