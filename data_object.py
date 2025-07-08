# -*- coding: utf-8 -*-
"""
Created on Mon Jul  7 11:24:50 2025

@author: sehag
"""

import math
import os
import pandas as pd
import statistics
import scipy

#
class Data_object(object):
    
    #
    def __init__(self):
        self.df = None
        
    #
    def _convert_sec_to_min(self,x):
        x = x / 60
        return x
        
    #
    def _convert_to_HMS(self, x):
        y = x.split(':')
        for i in range(len(y)):
            if len(y[i]) == 1:
                y[i] == '0' + y[i]
        if len(y) == 1:
            y = [ '00', '00', y[0] ]
        elif len(y) == 2:
            y = [ '00', y[0], y[1] ]
        x = ':'.join(y)
        return x
    
    #
    def _generate_age_group(self, x):
        if math.isnan(x):
            y = 'UNKNOWN'
        elif x == -1:
            y = 'UNKNOWN'
        elif x <= 14:
            y = '0-14'
        elif x <= 19:
            y = '15-19'
        elif x <= 29:
            y = '20-29'
        elif x <= 39:
            y = '30-39'
        elif x <= 49:
            y = '40-49'
        elif x <= 59:
            y = '50-59'
        elif x <= 69:
            y = '60-69'
        elif x <= 79:
            y = '70-79'
        elif x <= 89:
            y = '80-89'
        elif x <= 99:
            y = '90-99'
        else:
            print('Missing Age Group!')
            print(x)
            y = 'Missing Age Group'
        return y
    
    #
    def age_grp_summary(self, age_grp):
        age_grp_df = self.df.loc[self.df['Age Group'] == age_grp]
        x = age_grp_df['Net Tim Min']
        num_participants = len(x)
        return num_participants
    
    #
    def chris_doe(self, quantile):
        chris_doe_row = self.df.loc[self.df['Name'] == 'Chris Doe']
        age_grp = list(chris_doe_row['Age Group'])[0]
        gun_tim = list(chris_doe_row['Gun Tim Min'])[0]
        net_tim = list(chris_doe_row['Net Tim Min'])[0]
        pace = list(chris_doe_row['Pace Min'])[0]
        age_grp_df = self.df.loc[self.df['Age Group'] == age_grp]
        gun_tim_percentile = age_grp_df['Gun Tim Min'].quantile(quantile)
        net_tim_percentile = age_grp_df['Net Tim Min'].quantile(quantile)
        pace_percentile = age_grp_df['Pace Min'].quantile(quantile)
        x = gun_tim - gun_tim_percentile
        y = net_tim - net_tim_percentile
        z = pace - pace_percentile
        return gun_tim_percentile, net_tim_percentile, pace_percentile, x, y, z
        
    #
    def clean_data(self, column_name):
        self.df[column_name + ' Cleaned'] = \
            self.df[column_name].str.replace(r'[A-Z#\*\s]', '', regex=True)
            
    #
    def convert_to_seconds(self, column_name):
        self.df[column_name + ' Min'] = self.df[column_name + ' Cleaned']
        self.df[column_name + ' Min'] = \
            self.df[column_name + ' Min'].apply(self._convert_to_HMS)
        self.df[column_name + ' Min'] = \
            pd.to_timedelta(self.df[column_name + ' Min'])
        self.df[column_name + ' Min'] = \
            self.df[column_name + ' Min'].dt.total_seconds()
        self.df[column_name + ' Min'] = \
            self.df[column_name + ' Min'].apply(self._convert_sec_to_min)
            
    #
    def generate_age_groups(self):
        self.df['Age Group'] = \
            self.df['Ag'].apply(self._generate_age_group)
            
    #
    def get_age_grps(self):
        age_grps = list(set(list(self.df['Age Group'])))
        age_grps.remove('UNKNOWN')
        age_grps = sorted(age_grps)
        return age_grps
            
    #
    def get_data(self, column_name):
        x = self.df[column_name + ' Min']
        return x
    
    #
    def get_data_by_age_grp(self, column_name, age_grp):
        age_grp_df = self.df.loc[self.df['Age Group'] == age_grp]
        x = age_grp_df[column_name + ' Min']
        return x
    
    #
    def get_gun_minus_net_data(self):
        x = self.df['Gun Tim Min']
        y = self.df['Net Tim Min']
        z = x - y
        return z
        
    #
    def mean_results(self, column_name):
        x = self.df[column_name + ' Min']
        mean_x = statistics.mean(x)
        stdev_x = statistics.stdev(x)
        statistic, p_val = scipy.stats.shapiro(x)
        return mean_x, stdev_x, statistic, p_val
    
    #
    def mean_gun_minus_net_results(self):
        x = self.df['Gun Tim Min']
        y = self.df['Net Tim Min']
        z = x - y
        mean_z = statistics.mean(z)
        stdev_z = statistics.stdev(z)
        statistic, p_val = scipy.stats.shapiro(z)
        return mean_z, stdev_z, statistic, p_val
    
    #
    def median_results(self, column_name):
        x = self.df[column_name + ' Min']
        median_x = statistics.median(x)
        iqr_x = scipy.stats.iqr(x)
        return median_x, iqr_x
    
    #
    def median_gun_minus_net_results(self):
        x = self.df['Gun Tim Min']
        y = self.df['Net Tim Min']
        z = x - y
        median_z = statistics.median(z)
        iqr_z = scipy.stats.iqr(z)
        return median_z, iqr_z
    
    #
    def mode_results(self, column_name):
        x = self.df[column_name + ' Min']
        mode_x = statistics.mode(x)
        return mode_x
    
    #
    def pearsonr_gun_minus_net_results(self):
        x = self.df['Gun Tim Min']
        y = self.df['Net Tim Min']
        z = x - y
        correlation_coefficient_x, p_val_x = scipy.stats.pearsonr(x, z)
        correlation_coefficient_y, p_val_y = scipy.stats.pearsonr(y, z)
        return correlation_coefficient_x, p_val_x, correlation_coefficient_y, p_val_y
        
    #
    def read_data(self, path, filename):
        self.df = pd.read_csv(os.path.join(path, filename), sep='\t',
                              encoding='ISO-8859-1')