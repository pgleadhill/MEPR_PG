#
#   Masters of Engineering Practice
#   Electrical and Electronics
#   10/11/2022
#
#


#################################################################################
#################################################################################
#       STEP 1 - Data Reading 
#       STEP 2 - Data Cleaning  
#       STEP 3 - Data Wrangling
#       STEP 4 - Data Analysis 
#            4.1 - Plotting                      
#            4.2 - Statistics functions on pv values .describe() etc
#            4.2 - how volitile is the data (rate of change?)
#                                         
#################################################################################
#################################################################################
#   import requried libraries
import numpy as np
import pandas as pd
import os
import math
from os.path import isfile, join
from typing import List
import matplotlib.pyplot as plt # could use seaborn?
import datetime
#import scipy.integrate as integrate     
#import scipy.special as special 

#   object representing tags in files
class PlottingTags:
    def __init__(self, time_range, pv):
        self.time_range = time_range
        self.pv = pv 
        #self.colour = 

#   object representing a water treatment site
class SiteData:
    def __init__(self, siteName, csvFiles):
        self.siteName = siteName
        self.csvFiles = csvFiles

    def set_combines_site_csv(self, csv):
        self.csv = csv
    
    def set_plotting_tags(self, tags):
        self.plotting_tags = tags

    def set_time_range(self, range):
        self.timerange = range

    def set_graph_params(self, startx, stopx, stepx):
        self.startx = startx
        self.stopx = stopx
        self.stepx = stepx








#################################################################################
#################################################################################
#       STEP 1 - Data Reading                                
#################################################################################
#################################################################################

#   where CSV data is located in folder
csv_path = 'C:/Users/pglea/Documents/MEPR_Git'

#   function to only select csv files
def ensure_csv_type(f):
    return os.path.splitext(f)[-1] == ".csv"

#   function to get all csv files for each site into a list of site objects 
def get_all_sites():
    siteList = []
    files = [f for f in os.listdir(csv_path) if  ensure_csv_type(f)]
    for fileName in files:
        filteNameSplit = fileName.split(".")
        siteList.append(filteNameSplit[1].split(' ')[0]) #List of the site names
    uniqueSiteList = set(siteList)
    #print(files)
    sitesList = []
    for siteName in uniqueSiteList:
        siteFilesList = []
        for _file in files:
            if siteName.split("_")[0] in _file:
                siteFilesList.append(_file)
                #print("Site name = {} in file {}".format(siteName, _file))
        sitesList.append(SiteData(siteName.split("_")[0], siteFilesList))
    return sitesList


#   we read the csv files and add to a list  
def read_csv_for_site(siteFiles: List[str]):
    #print('Reading all of the csvs for a given site')
    data_frames = []
    _frame = None
    for fileName in siteFiles: # For every file that exists for each site (list of csvs obtained from get_all_sites() call)
        filePath = csv_path + "/" + fileName
        pandaCsv = pd.read_csv(filePath, na_filter=False)
        data_frames.append(pandaCsv) # turn every csv file into a dataframe object
    # for every csv for a given site, combine them into one single csv (merge)
    for i in range(len(data_frames)):
        if i == 0:
            _frame = data_frames[i].rename(columns=lambda x: x.strip())
        else:
            try:
               _frame = _frame.merge(data_frames[i].rename(columns=lambda x: x.strip()), how='outer')
            except:
                print("An exception occurred")
    return _frame

#################################################################################
#################################################################################
#       STEP 2 - Data Cleaning                                
#################################################################################
#################################################################################


def data_clean(site: SiteData):

    time_arr = []
    for i in range(len(site.csv["DATE"])):
        dtstr = "{} {}".format(site.csv["DATE"][i].replace(" ", ""), site.csv["TIME"][i].replace(" ", ""))
        time_arr.append(datetime.datetime.strptime(dtstr, '%d/%m/%Y %H:%M:%S.%f'))
        #print(time_arr)
        site.csv.head()
   
    clean_cols = []
    for item in site.csv[site.csv.columns[j]]:
        for rows in site.csv[site.csv.values]:
            try:
                clean_cols.append(float(item.replace(" ","")))
            except:
                 clean_cols.append(0)    

    clean_col_3 = []
    for item in site.csv[site.csv.columns[3]]:
        try:
            clean_col_3.append(float(item.replace(" ", "")))
        except:
            clean_col_3.append(0)


    clean_col_4 = []
    for item in site.csv[site.csv.columns[4]]:
        try:
            clean_col_4.append(float(item.replace(" ", "")))
        except:
            clean_col_4.append(0)


#################################################################################
#################################################################################
#       STEP 4.1 - Data Analysis - Plotting                                
#################################################################################

#   function for plotting tags with matplotlib 
#    
# 
# x min, max, y = automatic, for pv colour = random, plot type
# average flow rate time of day, month, box plot?
# 
# https://matplotlib.org/matplotblog/posts/pyplot-vs-object-oriented-interface/
#
#   figure for object oriented graphing. 
#   x axis is time/date, y1 axis level, y2 axis flow rate




def plot_csv_site(site: SiteData):
    print("nothing")
    fig, ax1 = plt.subplots()

    ax1.set_ylabel("{}".format(site.csv.columns[3]))
    ax1.set_xlabel("time")

    ax1.plot(time_arr, clean_col_3, "blue")

    ax2 = ax1.twinx() # create another y-axis sharing a common x-axis


    ax2.set_ylabel("{}".format(site.csv.columns[4]))
    ax2.set_xlabel("time")
    ax2.plot(time_arr, clean_col_4, "green")

    fig.set_size_inches(7,5)
    fig.set_dpi(100)

    plt.show()
    print("Finished charting")
  


#################################################################################
#################################################################################
#       STEP 4.2 - Data Analysis - Statistics                                
#################################################################################
#################################################################################
#           .describe()       #min/max/mean/dist
#       Integrate the Tank level with scipy     https://docs.scipy.org/doc/scipy/tutorial/integrate.html        
#        
#       divide by quaters for seasons 
#
#################################################################################
#################################################################################


#   our main function 
def main():
    sites:List[SiteData] = get_all_sites()
    siteDict = {}
    count = 0
    for site in sites:
        # Create a single CSV (dataframe) that consists of the time column and every other column from the other csv files
        siteCsv = read_csv_for_site(site.csvFiles)
        # Set the single csv for the site
        site.set_combines_site_csv(siteCsv)
        if siteCsv is not None:
        #print(siteCsv)
            siteDict[site.siteName] = siteCsv
        #print(siteCsv.columns)
            try:
                time_entries = site.csv[siteCsv.columns[1]]
                if len(time_entries) > 2:
                    try:
                        time_bound = (time_entries[0], time_entries[len(time_entries) - 1])
                     #   print(time_bound)
                    except:
                        print("A time series exception occurred")
            except:
                print("Could not get time entires for site = " + site.siteName)
            #time_bound = (time_entries[0], time_entries[-1])
    #print(site_to_tes
    # t.csv[site_to_test.csv.colums[1]]) 
    for site in sites:
     if site.siteName == "ALEXHIL":
            plot_csv_site(site)
     
#   main executable for program
main()

