redis:
	heroku redis:cli -a covidapp -c covidapp CACHE

parse:
	heroku run python manage.py parse_data -a covidapp
