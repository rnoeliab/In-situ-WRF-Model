# In-situ-WRF-Model
In this repository there are three folders. Each folder has a specific function in order to fulfill the final objective, which would be to compare the WRF model with the In-situ data from some CETESB stations within our study area. 

## 1. Extract_WRF_CETESB

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
To run the scripts:
  ```
 python qualar_py.py 
 python WRF_extract.py
 ```
For a better understanding of the qualar_py.py and WRF_extract.py scripts,  go to https://github.com/quishqa/WRF-Chem_SP
 
## 2. Read_save_data

* In this folder, we are going to focus on reading the extracted data from the WRF model and from the CETESB. For this, the script (https://github.com/rnoeliab/In-situ-WRF-Model/blob/main/Read_save_data/save_data_station_wrf_cetesb.py) will help us read the data "all_met", "all_photo" and " wrfout. dat " separating it by each station.

### How to use?

The script is divided into three parts:
`The first` part is to place" the libraries "that we are going to use,
`the second` part is the body of the script, we start first by placing two functions:
The first function is to eliminate the accents of the Portuguese names, so the script does not generate errors for the Portuguese language; 
```python
def strip_accents(text):
    try:
        text = unicode(text, 'utf-8')
    except NameError: # unicode is a default on python 3 
        pass
    text = unicodedata.normalize('NFD', text)\
           .encode('ascii', 'ignore')\
           .decode("utf-8")
    return str(text)
```
the second function is to create a folder if it is not already created. 
```python
def path(ouput):
    if not os.path.exists(ouput):
        os.makedirs(ouput)
    return ouput
```
Then add the path where the coordinates of the CETESB stations to be analyzed (https://github.com/rnoeliab/In-situ-WRF-Model/blob/main/extract_WRF_CETESB/cetesb_station_2017_codes_qualr_original.csv), the path of the data extracted "INPUT", and the path to save the generated excel ".csv" files. 

The next point is to read all the extracted data and put it in a list: 
```python
listdir = os.listdir(INPUT)
```
Specify the variables that we are going to analyze "meteorological" and "pollutants". 

Ending with the body of the script, use a For loop to read the variables for each station. 
```python
for index,i in enumerate(cetesb_stations.code):
    print(strip_accents(cetesb_stations["name"][index]), i)   
    name_station = strip_accents(cetesb_stations["name"][index]).replace('.','_').replace('-','_').replace(' ','_')
 ####### reading the wrf model files #########
    station_wrf = str(i)+"_wrfout4.dat"
    if str(station_wrf) in listdir:
        by_wrf = pd.read_csv(INPUT+str(station_wrf))
        .
        .
        .
 else:
        pass
######### reading pollutants data from cetesb  #############
    station_pol_cetesb = "all_photo_"+str(i)+".csv"
    if str(station_pol_cetesb) in listdir:
        by_cetestb_pol = pd.read_csv(INPUT+str(station_pol_cetesb))
        .
        .
        .
    else:
        pass               
######### reading meteorological  data from cetesb  #############
    station_cetesb = "all_met_"+str(i)+".csv"
    if str(station_cetesb) in listdir:
        cetestb = pd.read_csv(INPUT+str(station_cetesb))
        .
        .
        .
    else:
        pass
```  
`The third` part would be to save the generated excel files.
        
```python
print("saving the data")
serie_time.to_csv(OUTPUT+str(name_station)+".csv",index = False)    
```

* The script (https://github.com/rnoeliab/In-situ-WRF-Model/blob/main/Read_save_data/plot_station_meteorologicos.py) and (https://github.com/rnoeliab/In-situ-WRF-Model/blob/main/Read_save_data/plot_station_poluentes.py) are made to read the data saved by the previous script and generate time series plots for some stations. 

Example, I am showing a comparative between the WRF model and CETESB data in a time serie plot for various CETESB stations.

![Alt text](https://github.com/rnoeliab/In-situ-WRF-Model/blob/main/Read_save_data/figures/stations_temperatura.png)


## 3. comparate_data

* Finally, in this folder we are going to find two scripts to calculate the statistics between the two types of data. For this, a bibliographic reference has been used. [Emery et al. 2017](https://www.tandfonline.com/doi/full/10.1080/10962247.2016.1265027)

