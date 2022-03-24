# ta-backend
# Flask-Migrate https://flask-migrate.readthedocs.io/en/latest/
# steps on db migration
# 1. flask db init --> add a migrations folder to your application
# 2. flask db migrate -m "Initial migration." --> add initial migration
# The migration script needs to be reviewed and edited, as Alembic currently does not detect every change you make to your models
# 3. flask db upgrade --> apply the migration to the database
# Each time the database models change repeat the migrate and upgrade commands. 