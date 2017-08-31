# Import python modules
import pandas


# read in a daily streamflow data set
def read_daily_streamflow(file_name, drainage_area_m2, file_colnames=None, delimiter='\t', header='infer'):
    
    # if file_colnames are supplied, use header=None
    if file_colnames is not None:
        header=None
    
    # read in the data
    daily_data=pandas.read_table(file_name, delimiter=delimiter, header=header) 
    
    # set columns, if header=None
    if file_colnames is not None:
        daily_data.columns=file_colnames
    else:
        file_colnames=list(daily_data.columns)
        
    # calculate cfs to cms conversion, or vice versa
    if 'flow_cfs' in daily_data.columns:
        flow_cfs=daily_data['flow_cfs']
        flow_cms=flow_cfs/(3.28084**3)
        flow_mmday=flow_cms*1000*3600*24/drainage_area_m2
        
    elif 'flow_cms' in daily_data.columns:
        flow_cms=daily_data['flow_cms']
        flow_cfs=flow_cms*(3.28084**3)
        flow_mmday=flow_cms*1000*3600*24/drainage_area_m2
            
    # determine the datetime
    date_index=[file_colnames.index(each) for each in ['year','month','day']]
    row_dates=pandas.to_datetime(daily_data[date_index])
    
    # generate the daily_flow and set the datetime as row indices
    daily_flow=pandas.concat([flow_cfs, flow_cms, flow_mmday],axis=1)
    daily_flow.set_index(row_dates, inplace=True)
    daily_flow.columns=['flow_cfs', 'flow_cms', 'flow_mmday']
    return(daily_flow)

# read in a daily precipitation data set
def read_daily_precip(file_name, file_colnames=None, header='infer', delimiter='\s+'):
    
    # if file_colnames are supplied, use header=None
    if file_colnames is not None:
        header=None
    
    # read in the data
    daily_data=pandas.read_table(file_name, delimiter=delimiter, header=header) 
    
    # set columns, if header=None
    if file_colnames is not None:
        daily_data.columns=file_colnames
    else:
        file_colnames=list(daily_data.columns)
    
    # calculate cfs to cms conversion, or vice versa
    if 'precip_m' in daily_data.columns:
        precip_m=daily_data['precip_m']
        precip_mm=precip_m*1000
    
    # determine the datetime
    date_index=[file_colnames.index(each) for each in ['year','month','day']]
    row_dates=pandas.to_datetime(daily_data[date_index])
    
    # generate the daily_flow and set the datetime as row indices
    daily_precip=pandas.concat([precip_m, precip_mm],axis=1)
    daily_precip.set_index(row_dates, inplace=True)
    daily_precip.columns=['precip_m', 'precip_mm']
    return(daily_precip)

# read in a daily SNOTEL observation data set
def read_daily_snotel(file_name, file_colnames=None, usecols=None, delimiter=',', header='infer'):
    
    # if file_colnames are supplied, use header=None
    if file_colnames is not None:
        header=None
    
    # read in the data
    daily_data=pandas.read_table(file_name, usecols=usecols, header=header, delimiter=delimiter)
    
    # reset the colnames
    daily_data.columns=['Date', 'Tmax_C', 'Tmin_C', 'Tavg_C', 'Precip_mm']
    
    # transform the data
    daily_data['Tmax_C']=(daily_data['Tmax_C'] -32)/1.8
    daily_data['Tmin_C']=(daily_data['Tmin_C'] -32)/1.8
    daily_data['Tavg_C']=(daily_data['Tavg_C'] -32)/1.8
    daily_data['Precip_mm']=daily_data['Precip_mm'] *25.4
    
    # determine the datetime
    row_dates=pandas.to_datetime(daily_data.Date)
    
    # generate the daily_flow and set the datetime as row indices
    daily_snotel=daily_data[['Tmax_C', 'Tmin_C', 'Tavg_C', 'Precip_mm']]
    daily_snotel.set_index(row_dates, inplace=True)
    return(daily_snotel)


# ### Data Processing functions

# In[ ]:

# Determine dates (rows) and stations (columns). Number of stations 
# is the same for each dataset but number of dates may be different
def generateVarTables (listOfDates, listOfTables, n_stations):
    # NOTE: listOfTable must contain:
    # tmin_c
    # tmax_c
    # precip_mm
    # wind_m_s
    
    len_listOfDates=len(listOfDates) # number of dates
    station_list=range(0, n_stations) # list of stations number
    
    # Create arrays of for each variable of interest (Tmin, Tmax, Precip).
    # Rows are dates of analysis and columns are the station number
    temp_min_np=np.empty([len_listOfDates,n_stations])
    temp_max_np=np.empty([len_listOfDates,n_stations])
    precip_np=np.empty([len_listOfDates,n_stations])
    wind_np=np.empty([len_listOfDates,n_stations])
    
    # fill in each array with values from each station
    for i in station_list:
        temp_min_np[:,i]=listOfTables[i].tmin_c.values.astype(float)
        temp_max_np[:,i]=listOfTables[i].tmax_c.values.astype(float)
        precip_np[:,i]=listOfTables[i].precip_mm.values.astype(float)
        wind_np[:,i]=listOfTables[i].wind_m_s.values.astype(float)
        
    # generate each variable dataframe with rows as dates and columns as stations
    temp_min_df=pandas.DataFrame(temp_min_np, columns=station_list, index=listOfDates)    
    temp_max_df=pandas.DataFrame(temp_max_np, columns=station_list, index=listOfDates)    
    precip_df=pandas.DataFrame(precip_np, columns=station_list, index=listOfDates)    
    wind_df=pandas.DataFrame(wind_np, columns=station_list, index=listOfDates)
                                               
    # Create average temperature data frame as the average of Tmin and Tmax
    temp_avg_df=pandas.DataFrame((temp_min_np+temp_max_np)/2, columns=station_list, index=listOfDates)
    
    return(temp_min_df, temp_max_df, precip_df, wind_df, temp_avg_df)

# compare two date sets for the start and end of the overlapping dates
def overlappingDates(date_set1, date_set2):
    # find recent date
    if date_set1[0] > date_set2[0]:
        start_date = date_set1[0]
    else:
        start_date = date_set2[0]
    
    # find older date
    if date_set1[-1] < date_set2[-1]:
        end_date = date_set1[-1]
    else:
        end_date = date_set2[-1]
    return(start_date, end_date)

# Calculate means by 8 different methods
def multigroupMeans(VarTable, n_stations, start_date, end_date):
    Var_daily = VarTable.loc[start_date:end_date, range(0,n_stations)]
    
    # e.g., Mean monthly temperature at each station
    month_daily=Var_daily.groupby(Var_daily.index.month).mean() # average monthly minimum temperature at each station
    
    # e.g., Mean monthly temperature averaged for all stations in analysis
    meanmonth_daily=month_daily.mean(axis=1)
    
    # e.g., Mean monthly temperature for minimum and maximum elevation stations
    meanmonth_min_maxelev_daily=Var_daily.loc[:,analysis_elev_max_station].groupby(Var_daily.index.month).mean()
    meanmonth_min_minelev_daily=Var_daily.loc[:,analysis_elev_min_station].groupby(Var_daily.index.month).mean()
    
    # e.g., Mean annual temperature
    year_daily=Var_daily.groupby(Var_daily.index.year).mean()
    
    # e.g., mean annual temperature each year for all stations
    meanyear_daily=year_daily.mean(axis=1)
    
    # e.g., mean annual min temperature for all years, for all stations
    meanallyear_daily=np.nanmean(meanyear_daily)
    
    # e.g., anomoly per year compared to average
    anom_year_daily=meanyear_daily-meanallyear_daily
    
    return(month_daily, 
           meanmonth_daily, 
           meanmonth_min_maxelev_daily, 
           meanmonth_min_minelev_daily, 
           year_daily, 
           meanyear_daily, 
           meanallyear_daily,
           anom_year_daily)

def specialTavgMeans(VarTable):
    Var_daily = VarTable.loc[start_date:end_date, range(0,n_stations)]
    
    # Average temperature for each month at each station
    permonth_daily=Var_daily.groupby(pandas.TimeGrouper("M")).mean()
    
    # Average temperature each month averaged at all stations
    meanpermonth_daily=permonth_daily.mean(axis=1)
    
    # Average monthly temperature for all stations
    meanallpermonth_daily=meanpermonth_daily.mean(axis=0)
    
    # anomoly per year compared to average
    anom_month_daily=(meanpermonth_daily-meanallpermonth_daily)/1000
    
    return(permonth_daily,
          meanpermonth_daily,
          meanallpermonth_daily,
          anom_month_daily)

