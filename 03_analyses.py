#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 02:05:51 2023

@author: yamahi0318
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# set the default figure resolution
plt.rcParams["figure.dpi"] = 300

colname = ["STATE","FIP","Year"]
use_type = {col:str for col in colname}
merged = pd.read_csv("own_fat_rate.csv", dtype=use_type)

#%%

# draw the regresion line for the entire US

# create a new single-panel figure
fig,ax1 = plt.subplots()

sns.regplot(data=merged, x="own_rate", y="fat_rate", ax=ax1)

# set the title
ax1.set_title("Gun Ownership and Firearm Fatality across the US")
ax1.set_xlabel("Household Firearm Ownership Rate (HFR)")
ax1.set_ylabel("Firearm Fatality Rate")

# finalize the spacing of labels and axes in figures
fig.tight_layout()
fig.savefig("plot_US.png")

#%%

# rank the top 5 states with each high and low HFR

# pick out the states
own_2016 = merged.query("Year == '2016'").sort_values("own_rate")
high = own_2016[-5:]
low = own_2016[:5]

# create a new two-panel figure
fig,(ax1,ax2) = plt.subplots(2,1)

# set the figure title
fig.suptitle("Top 5 States with High & Low HFR (2016)")

# create horizontal bar graphs
high.plot.barh(x="STATE", y="own_rate", ax=ax1, legend=None)
# fix the width of the axis
ax1.set_xlim([0, 1])
ax1.set_ylabel(None)

low.plot.barh(x="STATE", y="own_rate", ax=ax2, legend=None)
ax2.set_xlim([0, 1])
ax2.set_ylabel(None)
ax2.set_xlabel("Household Firearm Ownership Rate (HFR)")

fig.tight_layout()
fig.savefig("rank_HFR.png")

#%%

# draw regression lines by state

# set index for picking up the data for the states with the 5 higest and lowest HFR
merged_idx = merged.set_index(["STATE","FIP"])
high_idx = high.set_index(["STATE","FIP"])
low_idx = low.set_index(["STATE","FIP"])
idx = pd.concat([high_idx,low_idx])

# create a series to pick up the data
picked = merged_idx.index.isin(idx.index)

# create the data set
merged_lm = merged_idx[picked].reset_index()

# draw regressions
jg = sns.lmplot(data=merged_lm, x="own_rate", y="fat_rate", hue="STATE")

jg.set_axis_labels("Household Firearm Ownership Rate (HFR)", "Firearm Fatality Rate")

jg.tight_layout()
jg.savefig("plot_high_low.png")

#%%

# break down the regressions for each state

picked_high = merged_idx.index.isin(high_idx.index)
high_lm = merged_idx[picked_high].reset_index()

jg = sns.lmplot(data=high_lm, x="own_rate", y="fat_rate", col="STATE", height=3)

jg.tight_layout()
jg.savefig("plot_high.png")

picked_low = merged_idx.index.isin(low_idx.index)
low_lm = merged_idx[picked_low].reset_index()

jg = sns.lmplot(data=low_lm, x="own_rate", y="fat_rate", col="STATE", height=3)

jg.tight_layout()
jg.savefig("plot_low.png")

#%%

# separate the years into three periods

late = [2016,2015,2014,2013,2012]
middle = [2011,2010,2009,2008,2007]
early = [2006,2005,2004,2003,2002]

high_lm_per = high_lm.copy()

for y in late:
    high_lm_per["Year"] = high_lm_per["Year"].replace(f"{y}", "2012-2016")

for y in middle:
    high_lm_per["Year"] = high_lm_per["Year"].replace(f"{y}", "2007-2011")

for y in early:
    high_lm_per["Year"] = high_lm_per["Year"].replace(f"{y}", "2002-2006")

jg = sns.relplot(data=high_lm_per, x="own_rate", y="fat_rate", col="STATE", 
                hue="Year", height=2.6)

jg.savefig("plot_high_per.png")


low_lm_per = low_lm.copy()

for y in late:
    low_lm_per["Year"] = low_lm_per["Year"].replace(f"{y}", "2012-2016")

for y in middle:
    low_lm_per["Year"] = low_lm_per["Year"].replace(f"{y}", "2007-2011")

for y in early:
    low_lm_per["Year"] = low_lm_per["Year"].replace(f"{y}", "2002-2006")

jg = sns.relplot(data=low_lm_per, x="own_rate", y="fat_rate", col="STATE", 
                hue="Year", height=2.6)

jg.savefig("plot_low_per.png")

#%%

# explore the gun ownership trend over time

# calculate the average fatality rate during the last and the earliest 5 years
post = merged[:250]
post_grouped = post.groupby(["STATE", "FIP"])
post_own_mean = post_grouped["own_rate"].mean()

pre = merged[-250:]
pre_grouped = pre.groupby(["STATE", "FIP"])
pre_own_mean = pre_grouped["own_rate"].mean()

# convert the series into the Pandas dataframe
own_trend = pd.DataFrame({"own_ave_2012_2016":post_own_mean, 
                          "own_ave_2002_2006":pre_own_mean})

# conduct 45 degree line analysis to see gun ownership trend over time
fig,ax1 = plt.subplots()
plt.axline((0,0), (0.7,0.7), color="r")

sns.regplot(data=own_trend, x="own_ave_2002_2006", y="own_ave_2012_2016", ax=ax1)

# set the title
ax1.set_title("a) Gun Ownership Trend over Time across the US")
ax1.set_xlabel("Average HFR (2002-2006)")
ax1.set_ylabel("Average HFR (2012-2016)")

fig.tight_layout()
fig.savefig("own_trend.png")

#%%

# explore the gun fatality trend over time

# calculate the average fatality rate during the last and the oldest 5 years
post_fat_mean = post_grouped["fat_rate"].mean()
pre_fat_mean = pre_grouped["fat_rate"].mean()

# convert the series into the Pandas dataframe
fat_trend = pd.DataFrame({"fat_ave_2012_2016":post_fat_mean, 
                          "fat_ave_2002_2006":pre_fat_mean})

# conduct 45 degree line analysis to see gun fatality trend over time
fig,ax1 = plt.subplots()
plt.axline((0,0), (23,23), color="r")

sns.regplot(data=fat_trend, x="fat_ave_2002_2006", y="fat_ave_2012_2016", ax=ax1)

# set the title
ax1.set_title("b) Firearm Fatality Trend over Time across the US")
ax1.set_xlabel("Average Fatality Rate (2002-2006)")
ax1.set_ylabel("Average Fatality Rate (2012-2016)")

fig.tight_layout()
fig.savefig("fat_trend.png")
