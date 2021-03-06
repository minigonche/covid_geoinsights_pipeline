# Constants

import locations.germany_functions as germany
import locations.brazil_functions as brazil
import locations.new_south_wales_functions as new_south_wales
import locations.bogota_functions as bogota
import locations.colombia_functions as colombia
import locations.chile_functions as chile
import locations.peru_functions as peru
import locations.mexico_functions as mexico

agglomeration_methods = ['radial','community','geometry']

figure_folder_name = 'report_figure_folder'
table_folder_name = 'report_table_folder'

# Progress file
progress_file = 'excecution_progress.csv'


hopkins_country_names = {"equatorial_guinea":"Equatorial Guinea",
                        "cameroon":"Cameroon",
                        "gabon":"Gabon"}


# Description file constants
# -----------------------------

# id for the google trends geographical code in the description
DECRIPTION_ID_GOOGLE_TRENDS_GEO_CODE = 'google_trends_geo_code'

# id for the first case reported
DECRIPTION_ID_FIRST_CASE = 'first_case'

# id for the main language of the location
DECRIPTION_ID_MAIN_LANGUAGE = "main_language"

# -------------------
                        
# For prediction
days_back = 5
days_ahead = 8
smooth_days = 5

date_format = "%Y-%m-%d"

def get_unifier_class(location):

	if location == "germany":

		unif = germany.Unifier()
		return(unif)


	if location == "brazil":

		unif = brazil.Unifier()
		return(unif)


	if location == "new_south_wales":

		unif = new_south_wales.Unifier()
		return(unif)

	if location == "bogota":

		unif = bogota.Unifier()
		return(unif)


	if location == "colombia":

		unif = colombia.Unifier()
		return(unif)


	if location == "chile":

		unif = chile.Unifier()
		return(unif)

	if location == "peru":

		unif = peru.Unifier()
		return(unif)

	if location == "mexico":

		unif = mexico.Unifier()
		return(unif)

	raise ValueError('No unifier found for: {}. Please add it'.format(location))