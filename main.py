#
#   Masters of Engineering Practice
#   Electrical and Electronics
#   10/11/2022
#
#


#################################################################################
#################################################################################
#       STEP 1 - Read all the data 
#       STEP 2 - Plot the DATA  
#                   - function to parse pv values/date/time        
#       STEP 3 - Statistics functions on pv values .describe() etc
#       STEP 4 - how volitile is the data (rate of change?)
#       STEP 5 -                                
#################################################################################
#################################################################################
#   import requried libraries
import numpy as np
import pandas as pd
import os
from os.path import isfile, join
from typing import List
import matplotlib.pyplot as plt


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

#################################################################################
#################################################################################
#       STEP 1 - Read all the data                                 
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
        sitesList.append(SiteData(siteName, siteFilesList))
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
            _frame = data_frames[i]
        else:
            try:
               _frame = _frame.merge(data_frames[i], how='outer')
            except:
                print("An exception occurred")
    #print(_frame)
    if _frame is not None:     
        for column in _frame.columns:
            try:
                _frame = _frame[column].str.strip()
            except:
                print("Stripping no good bro")
                print(filePath)
            print(_frame)
    return _frame

#################################################################################
#################################################################################
#       STEP 2 - Plot the DATA                                 
#################################################################################
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
#      
 def plot_csv_site(site: SiteData, plottingTags: PlottingTags):
    if site.csv is not None:
        #print(site.csv.columns)
        #print(plottingTags.exampleTag)
        #plt.plot(site.csv[site.csv.columns[1]], site.csv[site.csv.columns[-1]])
        plt.plot(site.siteName, plottingTags.time_range)
       # plt.show()       
        
        fig, ax1 = plt.subplots()
        
        ax1.set_ylabel("Level (m)", color="blue")
        ax1.set_xlabel("time")
        ax1.plot(   , distance, "blue")
        ax1.set_yticks(np.linspace(*ax1.get_ybound(), 10))
        ax1.tick_params(axis="y", labelcolor="blue")
        ax1.xaxis.grid()
        ax1.yaxis.grid()
        
        ax2 = ax1.twinx() # create another y-axis sharing a common x-axis
        
        
        ax2.set_ylabel("Flow (L/s)", color="green")
        ax2.set_xlabel("Flow")
        
        ax2.tick_params(axis="y", labelcolor="green")
        ax2.plot(time, velocity, "green")
        ax2.set_yticks(np.linspace(*ax2.get_ybound(), 10))
        
        fig.set_size_inches(7,5)
        fig.set_dpi(100)
        fig.legend(["Level", "Flow"])
        plt.show()
        
# this should have our plot of res vs flow per site


#################################################################################
#################################################################################


#   our main function 
def main():
    sites:List[SiteData] = get_all_sites()
    siteDict = {}
    for site in sites:
        siteCsv = read_csv_for_site(site.csvFiles)
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
                        print(time_bound)
                    except:
                        print("A time series exception occurred")
            except:
                print("Could not get time entires for site = " + site.siteName)
            #time_bound = (time_entries[0], time_entries[-1])
    #print(site_to_test.csv[site_to_test.csv.columns[1]])
    plot_csv_site(site, plottingTags)
#   main executable for program
main()

