# In-situ-WRF-Model
In this repository there are three folders. Each folder has a specific function in order to fulfill the final objective, which would be to compare the WRF model with the In-situ data from some CETESB stations within our study area. 

# 1. Extract_WRF_CETESB

This folder contains five scripts, the objective is to extract the meteorological and gas data from the WRF model and from various CETESB stations. 

* [qualar] (https://github.com/rnoeliab/In-situ-WRF-Model/blob/main/extract_WRF_CETESB/qualar_py.py) This script must be run before running the [WRF_extract] (https://github.com/rnoeliab/In-situ-WRF-Model/blob/main/extract_WRF_CETESB/WRF_extractor.py) script. In the WRF_extract script it should only be modified: the path where the outputs of the WRF model (wrfout) are located, the excel of the coordinates of the CETESB stations of which we are going to carry out the study, the path where the data "all_met", "all_photo" and "wrfout4.dat" will be saved and finally put username and password from website CETESB. 

* If we only want to download the cetesb data for a large period and for several stations, the following script can be used: (https://github.com/rnoeliab/In-situ-WRF-Model/blob/main/extract_WRF_CETESB/qualar_extractor.py).

* To work with meteorological data between the WRF model and the CETESB stations, it is recommended to use the following scripts: (https://github.com/rnoeliab/In-situ-WRF-Model/blob/main/extract_WRF_CETESB/qualar_meteo_py.py) and (https://github.com/rnoeliab/In-situ-WRF-Model/blob/main/extract_WRF_CETESB/WRF_meteo_extractor.py).

 To run these scripts it is necessary to take into account that we use the programming language "python". For this, it is recommended to install [anaconda] (https://docs.anaconda.com/anaconda/install/). Then create an environment (or project) to install the necessary libraries. 
 
 First, download or clone this respository:
 ```
 git clone https://github.com/rnoeliab/In-situ-WRF-Model.git
 ```
Second, create an enviroment to run this scripts:
 ```
 conda create --name wrf_insitu python=3.7 matplotlib
 conda activate wrf_insitu
 ```
Finally, install the libraries
 ```
 conda install netCDF4
 conda install pandas
 conda install wrf-python
 conda install requests 
 conda install beautifulsoup4 
 conda install lxml
 ```
For a better understanding of the qualar_py.py and WRF_extract.py scripts,  https://github.com/quishqa/WRF-Chem_SP
 
# 2. Read_save_data





# 3. comparate_data

