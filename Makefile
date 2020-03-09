redis:
	heroku redis:cli -a covidapp -c covidapp CACHE

parse:
	heroku run python manage.py parse_data -a covidapp

capture-backup:
	heroku pg:backups:capture --app covidapp

clear-db:
	echo 'DROP SCHEMA public CASCADE; CREATE SCHEMA public;' | python manage.py dbshell

pull-db:
	curl -o latest.dump `heroku pg:backups:public-url --app covidapp`

restore-db:
	-pg_restore --clean --no-acl --no-owner -d covidapp latest.dump

reload-db: capture-backup pull-db clear-db restore-db
