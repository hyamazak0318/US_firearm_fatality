#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 23:39:18 2023

@author: yamahi0318
"""

# construct a panel data consisting of 15 years of firearm-related fatalities 
# and gun ownership

import pandas as pd
import geopandas as gpd

# build a data set of household firearm ownership rate

# convert the input excel file into the Pandas dataframe
exc = pd.read_excel("TL-354-State-Level Estimates of Household Firearm Ownership.xlsx", 
                    sheet_name=None)
own = exc["State-Level Data & Factor Score"]

# convert the numbers into strings
own[["FIP", "Year"]] = own[["FIP", "Year"]].astype(str)

# make the FIPS code usable
num = [1,2,3,4,5,6,7,8,9]
for n in num:
    own["FIP"] = own["FIP"].replace(f"{n}", f"0{n}")

# trim down the data
own = own[["FIP", "Year", "STATE", "HFR"]]

#%%

# merge the firearm ownership data on the fatality data
use_type = {"FIP":str, "Year":str}
fat = pd.read_csv("fatality.csv", dtype=use_type)

merged = fat.merge(own, on=["STATE","FIP","Year"], validate="m:1", indicator=True)
print(merged["_merge"].value_counts(), "\n")

# organize the columns
merged = merged.drop(columns=["_merge"])
merged = merged.rename(columns={"HFR":"own_rate"})

#%%

# separate the columns of the panel data by year
by_year = merged.drop_duplicates(subset=["STATE", "FIP"])
by_year = by_year[["STATE","FIP"]]
y_list = [2016,2015,2014,2013,2012,2011,2010,2009,2008,2007,2006,2005,2004,2003,2002]
for y in y_list:
    year = merged[merged["Year"] == f"{y}"].reset_index()
    by_year[f"fat_rate_{y}"] = year["fat_rate"]
    by_year[f"own_rate_{y}"] = year["own_rate"]

#%%%

# create a GeoPandas dataframe from the US state shapefile
geodata = gpd.read_file("tl_2020_us_state.zip")

# merge the gun ownership information onto the geographical data
geodata = geodata.merge(by_year, left_on="GEOID", right_on="FIP", how="right", 
                        validate="1:1", indicator=True)

# print the merge indicator and drop the column
print(geodata["_merge"].value_counts())
geodata = geodata.drop(columns="_merge")

# write out the geodata to a geopackage file
geodata.to_file("map.gpkg", layer="own_fat_rate")

#%%

# write out the panel data to a csv file
merged = merged.set_index(["STATE","FIP","Year"])
merged.to_csv("own_fat_rate.csv")