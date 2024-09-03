import pandas as pd
# xlrd==1.2.0
import xlrd, datetime, os
<<<<<<< Updated upstream
xlrd.xlsx.ensure_elementtree_imported(False, None)
xlrd.xlsx.Element_has_iter = True

def read_observations_excel(observations_folder):
=======
import numpy as np

def read_observations_excel(observations_folder, skiprows=1):
>>>>>>> Stashed changes

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
        Observations_namesLocations = pd.read_csv(observations_folder + '/observations_locations.csv')
    except: 
        Observations_namesLocations = pd.read_excel(observations_folder + '/observations_locations.xlsx', engine='openpyxl')

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

        if discharge_location[0] + '.xlsx' in observed_folder_list:
            book = xlrd.open_workbook(observed_discharge_folder + '/' + discharge_location[0] + '.xlsx')
            sheet = book.sheet_by_index(0)
            num_rows = sheet.nrows

<<<<<<< Updated upstream
            _Dates_observed = [xlrd.xldate_as_tuple(int(sheet.cell(row, 0).value), 0) for row in range(2, num_rows)]
            Dates_observed = [datetime.datetime(d[0], d[1], d[2]) for d in _Dates_observed]

            Flows_observed = [sheet.cell(row, 1).value for row in range(2, num_rows)]
=======
            sheet = pd.read_excel(os.path.join(observed_discharge_folder, discharge_location[0] + '.xlsx'),
                                     header=None, skiprows=skiprows,
                                     names=['Date', 'Observation'])


            sheet['Date'] = pd.to_datetime(sheet['Date'], format='mixed', dayfirst=True).dt.date
            Dates_observed = sheet['Date'].tolist()
            Flows_observed = np.array(sheet['Observation'].tolist())

            # negative values transformed to NaN
            Flows_observed = np.where(Flows_observed >= 0, Flows_observed, np.nan)
>>>>>>> Stashed changes

            DATES_observed.append(Dates_observed)
            FLOWS_observed.append(Flows_observed)

        else:
            print('missing ' + discharge_location[0])
            DATES_observed.append([])
            FLOWS_observed.append([])

    return Observations_namesLocations_array, DATES_observed, FLOWS_observed

<<<<<<< Updated upstream
=======
def read_simulations_excel(simulated_stations_folder, Observations_namesLocations_array, skiprows=1):

    DATES_simulated = []
    FLOWS_simulated = []
    
    simulated_stations_folder_list = os.listdir(simulated_stations_folder)
    print('Loading simulations from Excel')

    for discharge_location in Observations_namesLocations_array:

        if discharge_location[0] + '.xlsx' in simulated_stations_folder_list:

            sheet = pd.read_excel(os.path.join(simulated_stations_folder, discharge_location[0] + '.xlsx'),
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
            print('missing ' + discharge_location[0])
            DATES_simulated.append([])
            FLOWS_simulated.append([])
            
    return DATES_simulated, FLOWS_simulated












>>>>>>> Stashed changes
