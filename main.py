# -*- coding: utf-8 -*-
"""
Created on Mon Jul  7 11:22:00 2025

@author: sehag
"""

import matplotlib.pyplot as plt

from data_object import Data_object

data_path = 'data'
female_data_file = 'MA_Exer_PikesPeak_Females.txt'
male_data_file = 'MA_Exer_PikesPeak_Males.txt'

female_data = Data_object()
male_data = Data_object()

female_data.read_data(data_path, female_data_file)
male_data.read_data(data_path, male_data_file)

female_data_results = {}
female_data.generate_age_groups()
for lbl in ['Gun Tim', 'Net Tim', 'Pace']:
    female_data_results[lbl] = {}
    female_data.clean_data(lbl)
    female_data.convert_to_seconds(lbl)
    female_data_results[lbl]['data'] = female_data.get_data(lbl)
    female_data_results[lbl]['mean'] = female_data.mean_results(lbl)
    female_data_results[lbl]['median'] = female_data.median_results(lbl)
    female_data_results[lbl]['mode'] = female_data.mode_results(lbl)
age_grps = female_data.get_age_grps()
for age_grp in age_grps:
    female_data_results[age_grp] = {}
    female_data_results[age_grp]['data'] = \
        female_data.get_data_by_age_grp('Net Tim', age_grp)
    female_data_results[age_grp]['summary'] = \
        female_data.age_grp_summary(age_grp)
female_data_results['Gun minus Net'] = {}
female_data_results['Gun minus Net']['data'] = \
    female_data.get_gun_minus_net_data()
female_data_results['Gun minus Net']['mean'] = \
    female_data.mean_gun_minus_net_results()
female_data_results['Gun minus Net']['median'] = \
    female_data.median_gun_minus_net_results()
female_data_results['Gun minus Net']['pearsonr'] = \
    female_data.pearsonr_gun_minus_net_results()

male_data_results = {}
male_data.generate_age_groups()
for lbl in ['Gun Tim', 'Net Tim', 'Pace' ]:
    male_data_results[lbl] = {}
    male_data.clean_data(lbl)
    male_data.convert_to_seconds(lbl)
    male_data_results[lbl]['data'] = male_data.get_data(lbl)
    male_data_results[lbl]['mean'] = male_data.mean_results(lbl)
    male_data_results[lbl]['median'] = male_data.median_results(lbl)
    male_data_results[lbl]['mode'] = male_data.mode_results(lbl)
age_grps = male_data.get_age_grps()
for age_grp in age_grps:
    male_data_results[age_grp] = {}
    male_data_results[age_grp]['data'] = \
        male_data.get_data_by_age_grp('Net Tim', age_grp)
    male_data_results[age_grp]['summary'] = \
        male_data.age_grp_summary(age_grp)
male_data_results['Gun minus Net'] = {}
male_data_results['Gun minus Net']['data'] = \
    male_data.get_gun_minus_net_data()
male_data_results['Gun minus Net']['mean'] = \
    male_data.mean_gun_minus_net_results()
male_data_results['Gun minus Net']['median'] = \
    male_data.median_gun_minus_net_results()
male_data_results['Gun minus Net']['pearsonr'] = \
    male_data.pearsonr_gun_minus_net_results()
male_data_results['Chris Doe'] = {}
male_data_results['Chris Doe']['results'] = male_data.chris_doe(0.1)

x = [ female_data_results['Gun Tim']['data'],
      female_data_results['Net Tim']['data'],
      male_data_results['Gun Tim']['data'],
      male_data_results['Net Tim']['data'] ]
x_lbls = [ 'Gun Times (F)', 'Net Times (F)', 'Gun Times (M)',
           'Net Times (M)' ]
plt.figure()
plt.boxplot(x, labels=x_lbls)
plt.ylabel("Time (min)")

x = [ female_data_results['Pace']['data'],
      male_data_results['Pace']['data'] ]
x_lbls = [ 'Paces (F)', 'Paces (M)' ]
plt.figure()
plt.boxplot(x, labels=x_lbls)
plt.ylabel("Pace (min/mile)")

x = [ female_data_results['Gun minus Net']['data'],
      male_data_results['Gun minus Net']['data'] ]
x_lbls = [ 'Gun - Net Times (F)', 'Gun - Net Times (M)' ]
plt.figure()
plt.boxplot(x, labels=x_lbls)
plt.ylabel("Time (min)")

fig, axes = plt.subplots(2, 2, figsize=(10, 10))

x = female_data_results['Gun minus Net']['data']
y = female_data_results['Gun Tim']['data']
axes[0, 0].scatter(x,y)
axes[0, 0].set_title("Gun v. Gun - Net (F)")
axes[0, 0].set_xlabel("Gun - Net Times (min)")
axes[0, 0].set_ylabel("Gun Times (min)")

x = female_data_results['Gun minus Net']['data']
y = female_data_results['Net Tim']['data']
axes[0, 1].scatter(x,y)
axes[0, 1].set_title("Net v. Gun - Net (F)")
axes[0, 1].set_xlabel("Gun - Net Times (min)")
axes[0, 1].set_ylabel("Net Times (min)")

x = male_data_results['Gun minus Net']['data']
y = male_data_results['Gun Tim']['data']
axes[1, 0].scatter(x,y)
axes[1, 0].set_title("Gun v. Gun - Net (M)")
axes[1, 0].set_xlabel("Gun - Net Times (min)")
axes[1, 0].set_ylabel("Gun Times (min)")

x = male_data_results['Gun minus Net']['data']
y = male_data_results['Net Tim']['data']
axes[1, 1].scatter(x,y)
axes[1, 1].set_title("Net v. Gun - Net(M)")
axes[1, 1].set_xlabel("Gun - Net Times (min)")
axes[1, 1].set_ylabel("Net Times (min)")

age_grps = female_data.get_age_grps()
x = []
x_lbls = []
for i in range(len(age_grps)):
    age_grp = age_grps[i]
    x.append(female_data_results[age_grp]['data'])
    x_lbls.append(age_grp)
plt.figure()
plt.boxplot(x, labels=x_lbls)
plt.ylabel("Net Time (min)")

age_grps = female_data.get_age_grps()
x = []
x_lbls = []
for i in range(len(age_grps)):
    age_grp = age_grps[i]
    summary = female_data_results[age_grp]['summary']
    x.append(summary)
    x_lbls.append(age_grp)
plt.figure()
plt.plot(range(len(x)), x)
plt.xticks(range(len(x)), x_lbls)
plt.ylabel("Num")

age_grps = male_data.get_age_grps()
x = []
x_lbls = []
for i in range(len(age_grps)):
    age_grp = age_grps[i]
    x.append(male_data_results[age_grp]['data'])
    x_lbls.append(age_grp)
plt.figure()
plt.boxplot(x, labels=x_lbls)
plt.ylabel("Net Time (min)")

age_grps = male_data.get_age_grps()
x = []
x_lbls = []
for i in range(len(age_grps)):
    age_grp = age_grps[i]
    summary = male_data_results[age_grp]['summary']
    x.append(summary)
    x_lbls.append(age_grp)
plt.figure()
plt.plot(range(len(x)), x)
plt.xticks(range(len(x)), x_lbls)
plt.ylabel("Num")