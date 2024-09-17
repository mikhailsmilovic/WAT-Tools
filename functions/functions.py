import pandas as pd
import os, xlrd
import numpy as np

def read_observations_excel(observations_folder, skiprows=1):


    # Returns three arrays:
    #   Observations_namesLocations_array, [Stations[i], Latitudes[i], Longitudes[i]]_i
    #   DATES_observed, [Observation dates for station i]_i
    #   FLOWS_observed, [Observation values for station i]_i

    # observations_folder holds one excel (observation_locations.xlsx) with names and locations, and
    # a folder (Observations) with an Excel file for each station. The Excel files are named after the station names.
    #
    # observations_locations.xlsx has three columns: Station name, Latitude, Longitude
    #
    # FOLDER STRUCTURE
    # observations_folder
    # ↵ observations_locations.xlsx
    # ↵ Observations
    #   ↵ StationName1.xlsx #first two rows not read
    #   ↵ StationName2.xlsx #first two rows not read
    #   ↵ ...

    # Read list of observation stations

    try: 
        observations_list_file = os.path.join(observations_folder, 'observations_locations.csv')
        Observations_namesLocations = pd.read_csv(observations_list_file)
    except: 
        observations_list_file = os.path.join(observations_folder, 'observations_locations.xlsx')
        Observations_namesLocations = pd.read_excel(observations_list_file, engine='openpyxl')

    Stations = Observations_namesLocations['Station'].tolist()
    Latitudes = Observations_namesLocations['Latitude'].tolist()
    Longitudes = Observations_namesLocations['Longitude'].tolist()

    Observations_namesLocations_array = []

    for i in range(len(Stations)):
        Observations_namesLocations_array.append([Stations[i], Latitudes[i], Longitudes[i]])

    # Read observation time series

    DATES_observed = []
    FLOWS_observed = []

    observed_discharge_folder = os.path.join(observations_folder, 'Observations')
    observed_folder_list = os.listdir(observed_discharge_folder)

    print('Loading observations')

    for discharge_location in Observations_namesLocations_array:

        if str(discharge_location[0]) + '.xlsx' in observed_folder_list:
            #book = xlrd.open_workbook(observed_discharge_folder + '/' + str(discharge_location[0]) + '.xlsx')
            #sheet = book.sheet_by_index(0)
            #num_rows = sheet.nrows


            sheet = pd.read_excel(os.path.join(observed_discharge_folder, str(discharge_location[0]) + '.xlsx'),
                                     header=None, skiprows=skiprows,
                                     names=['Date', 'Observation'])


            sheet['Date'] = pd.to_datetime(sheet['Date'], format='mixed', dayfirst=True).dt.date
            Dates_observed = sheet['Date'].tolist()
            Flows_observed = np.array(sheet['Observation'].tolist())

            # negative values transformed to NaN
            Flows_observed = np.where(Flows_observed >= 0, Flows_observed, np.nan)

            DATES_observed.append(Dates_observed)
            FLOWS_observed.append(Flows_observed)

        else:
            print('missing ' + str(discharge_location[0]))
            DATES_observed.append([])
            FLOWS_observed.append([])

    return Observations_namesLocations_array, DATES_observed, FLOWS_observed


def read_simulations_excel(simulated_stations_folder, Observations_namesLocations_array, skiprows=1):

    DATES_simulated = []
    FLOWS_simulated = []
    
    simulated_stations_folder_list = os.listdir(simulated_stations_folder)
    print('Loading simulations from Excel')

    for discharge_location in Observations_namesLocations_array:

        if str(discharge_location[0]) + '.xlsx' in simulated_stations_folder_list:

            sheet = pd.read_excel(os.path.join(simulated_stations_folder, str(discharge_location[0]) + '.xlsx'),
                                     header=None, skiprows=skiprows,
                                     names=['Date', 'Observation'])


            sheet['Date'] = pd.to_datetime(sheet['Date'], format='mixed', dayfirst=True).dt.date
            Dates_simulated = sheet['Date'].tolist()
            Flows_simulated = np.array(sheet['Observation'].tolist())

            # negative values transformed to NaN
            # Flows_simulated = np.where(Flows_simulated >= 0, Flows_simulated, np.nan)

            DATES_simulated.append(Dates_simulated)
            FLOWS_simulated.append(Flows_simulated)

        else:
            print('missing ' + str(discharge_location[0]))
            DATES_simulated.append([])
            FLOWS_simulated.append([])
            
    return DATES_simulated, FLOWS_simulated