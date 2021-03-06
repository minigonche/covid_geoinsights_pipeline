# Unify all script

# Usual imports
import pandas as pd
import os
from datetime import datetime


import excecution_functions as ef


# Resets Progress
ef.reset_progress()

# Stages variables
stages = ['EXTRACT','UNIFY', 'AGGLOMERATE', 'CONSTRUCT', 'ANALYSE', 'WRAPPING']
stages_names = ['Extract','Unify', 'Agglomerate', 'Construct', 'Analyse','Wrapping']


# Read the locations
df_locations = pd.read_csv('pipeline_scripts/configuration/selected_excecutions.csv')

# Exctracts PRE
df_pre = df_locations[df_locations.stage == 'PRE']
df_pre = df_pre[df_pre.excecute == 'YES'].sort_values('position')

# Extracts POS
df_pos = df_locations[df_locations.stage == 'POS']
df_pos = df_pos[df_pos.excecute == 'YES'].sort_values('position')

# Filters out
df_locations = df_locations[df_locations.excecute == 'YES']
df_locations = df_locations[df_locations.stage != 'PRE']
df_locations = df_locations[df_locations.stage != 'POS'].copy()




# -------------------
# ----- Pre Scripts

# Excecute PRE scripts
print('Excecuting for Pre Scripts for All Locations')


print('Detected: {} Pre Scripts'.format(df_pre.shape[0]))

for ind, row in df_pre.iterrows():

	# Locations od the scripts
	scripts_location = os.path.join('pipeline_scripts/',  row.folder_location)

	print('      Excecuting {} ({}) for {}'.format(row.script_name, row.script_type, row.location_name))
	
	ef.excecute_script(scripts_location, row.script_name, row.script_type, row.script_parameters)
	print('')

print('   Done')
print('')


print('Excecuting for Each Location')

# Extracts locations
locations = df_locations.location_name.unique()

# Sets the stages
df_locations.stage = df_locations.stage.apply(lambda s: s.upper())

print('Detected: {} Scripts'.format(locations.size))

# Counter
processed = 0

for loc in locations:

	processed += 1
	print('Started Pipeline for: {} ({} of {})'.format(loc, processed, locations.size))


	df_temp =  df_locations[df_locations.location_name == loc]


	for i in range(len(stages)):

		print('   Stage: {}'.format(stages_names[i]))


		# Starts Stage
		df_stage = df_temp[df_temp.stage == stages[i]].sort_values('position')
		print('   Found {} Scripts'.format(df_stage.shape[0]))

		for ind, row in df_stage.iterrows():

			# Locations od the scripts
			scripts_location = os.path.join('pipeline_scripts/',  row.folder_location)

			print('      Excecuting {} ({})'.format(row.script_name, row.script_type))
			
			ef.excecute_script(scripts_location, row.script_name, row.script_type, row.script_parameters)
			print('')

		print('   Done')
		print('')

	print('Finished Pipeline for: {} ({} of {})'.format(loc, processed, locations.size))
	print('--------------')
	print('')



# -------------------
# ----- Pos Scripts

# Excecute PRE scripts
print('Excecuting for Pos Scripts for All Locations')


print('Detected: {} Pos Scripts'.format(df_pos.shape[0]))

for ind, row in df_pos.iterrows():

	# Locations od the scripts
	scripts_location = os.path.join('pipeline_scripts/',  row.folder_location)

	print('      Excecuting {} ({}) for {}'.format(row.script_name, row.script_type, row.location_name))
	
	ef.excecute_script(scripts_location, row.script_name, row.script_type, row.script_parameters)
	print('')

print('   Done')
print('')




print('')
print('---------------')
print('All Done!')


