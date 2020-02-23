# Traveler news site
Build by using Django3 and Python3

- Sign in / Sign up with email verification (Sendgrid and Celery)
- Create post and add attachment (image) using Markdown
- Add comment to the post with sending an email notification to post author (Sendgrid and Celery)

# Deploy project on your local machine

1 - To deploy project on your local machine create new virtual environment and execute this command:

`pip install -r requirements.txt`

2 - Insert your own db configuration settings (see example secret.env):
and change file name to .env:

`DB_PASSWORD`,
`DB_NAME`,
`DB_USER`

3 - Migrate db models to PostgreSQL:

`python3 manage.py migrate`

4 - Run app:

`python3 manage.py runserver`

5 - Run celery by next command:

`celery -A subscription_service worker -l info`

Project was deployed to Heroku, but w/o Sendgrid add-on (some issue from Heroku side), so, unfortunately, it's work w/o emails confirmation and notifications:

`heroku run python manage.py createsuperuser -a traveler-news`

https://traveler-news.herokuapp.com/