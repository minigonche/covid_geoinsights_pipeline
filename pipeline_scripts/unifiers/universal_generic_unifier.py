# Script that cleans the data from the raw data


# Imports all the necesary functions
import fb_functions as fb
import general_functions as gf
import attr_agglomeration_functions as attr_agg


# Other imports
import os, sys
from datetime import datetime, timedelta
from pathlib import Path
import constants as con
import pandas as pd

#Directories
from global_config import config
data_dir = config.get_property('data_dir')
analysis_dir = config.get_property('analysis_dir')
key_string = config.get_property('key_string') 

ident = '         '

# Unifies Facebook data
location_name  = sys.argv[1] # Location name
location_folder_name = sys.argv[2] # location folder name

# If a third parameter is given is the max_date
max_date = None
if len(sys.argv) > 3:
	max_date = pd.to_datetime( sys.argv[3])

	# Adjusts max date (so that it can include the given date)
	max_date = max_date + timedelta(days = 1) - timedelta(seconds = 1)
	print(ident + f'   Max Date established: {max_date}')



# Checks if its encrypted
encrypted = gf.is_encrypted(location_folder_name)

# Loads the unifier class
unifier = con.get_unifier_class(location_folder_name)



unified_dir = unifier.unified_folder


print(ident + 'Unifies for {}'.format(location_name))
print()


# Updates Geo
print(ident + 'Updates Geo')
unifier.update_geo()
print(ident + 'Done!')
print()


print(ident + 'Builds Datasets:')

# ----------------
# -- Agg_scheme --
# ----------------
print(ident + '   Agglomeration scheme')
aggl_scheme = unifier.attr_agglomeration_scheme()


# Writes aggl_scheme
df_aggl_scheme = pd.DataFrame.from_dict(aggl_scheme, orient="index", columns=["aggl_function", "secondary_attr", "aggl_parameters"]).reset_index()
df_aggl_scheme.rename(columns={"index":"attr_name"}, inplace=True)
df_aggl_scheme.to_csv(os.path.join(unified_dir, 'aggl_scheme.csv'), index = False)


# ----------------
# ---- Cases -----
# ----------------
print(ident + '   Cases')
df_cases = unifier.build_cases_geo()

# Checks if max date is given
if max_date is not None:
	df_cases = df_cases[df_cases.date_time < max_date]

# Extracts date
cases_date = df_cases.date_time.max()

# Saves
if not encrypted:
	df_cases.to_csv(os.path.join(unified_dir, 'cases.csv'), index = False, date_format = con.date_format)
else:
	gf.encrypt_df(df_cases, os.path.join(unified_dir, 'cases.csv'), key_string)


# -------------------
# ---- Movement -----
# -------------------
print(ident + '   Movement')

final_file_location = os.path.join(unified_dir, 'movement.csv')
movement_date = fb.export_movement_batch(final_file_location, location_folder_name, max_date = max_date, ident = ident + "      ")



# -------------------
# ---- Population -----
# -------------------
print(ident + '   Population')
df_population = fb.build_population(location_folder_name)


# Checks if max date is given
if max_date is not None:
	df_population.date_time = pd.to_datetime(df_population.date_time)
	df_population = df_population[df_population.date_time < max_date]

# Extracts date
population_date = df_population.date_time.max()


# Saves
df_population.to_csv(os.path.join(unified_dir, 'population.csv'), index = False)


# -------------------
# ---- Polygons -----
# -------------------
print(ident + '   Polygons')
df_poly = unifier.build_polygons()

# Extracts date
poly_date = cases_date

# Saves
df_poly.to_csv(os.path.join(unified_dir, 'polygons.csv'), index = False)



# -------------------
# - Movement Range --
# -------------------
print(ident + '   Movement Range')
# Checks if location has movement range
if os.path.exists( os.path.join(unifier.raw_folder, 'movement_range')):
	
	print(ident + '   Movement Range')
	df_movement_range = fb.build_movement_range(location_folder_name)

	# Checks if max date is given
	if max_date is not None:
		df_movement_range.ds = pd.to_datetime(df_movement_range.ds)
		df_movement_range = df_movement_range[df_movement_range.ds < max_date]

	df_movement_range.to_csv(os.path.join(unified_dir, 'movement_range.csv'), index = False)
else:
	print(ident + '      No Movement Range Found Skipping...')


print(ident + 'Saving Dates')

#Saves the dates
with open(os.path.join(unified_dir, 'README.txt'), 'w') as file:

	file.write('Current max dates for databases:' + '\n')
	file.write('   Cases: {}'.format(cases_date) + '\n')
	file.write('   Movement: {}'.format(movement_date) + '\n')
	file.write('   Population: {}'.format(population_date) + '\n')
	file.write('   Polygons: {}'.format(poly_date) + '\n')

print(ident + 'Done! Data copied to: {}/unified'.format(location_folder_name))
print(ident + '')