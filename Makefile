redis:
	heroku redis:cli -a covidapp -c covidapp

parse:
	heroku run python manage.py parse_data
