import os

DYNO = os.environ.get("DYNO", "local.1")
PROCESS_TYPE = DYNO.split(".", 1)[0]

RELEASE = os.getenv("HEROKU_RELEASE_VERSION", "")
COMMIT = os.getenv("HEROKU_SLUG_COMMIT", "")
APP_NAME = os.getenv("HEROKU_APP_NAME", "")
