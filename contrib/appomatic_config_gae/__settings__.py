import os

if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine'):
    # Running on production App Engine, so use a Google Cloud SQL database.
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': '/cloudsql/your-project-id:your-instance-name',
            'NAME': 'db-name',
            'USER': 'username',
            'PASSWORD': 'password'
        }
    }
else:
    # Running in development, but want to access the Google Cloud SQL instance
    # in production.
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': 'cloud-sql-instance-ip-address',
            'NAME': 'db-name',
            'USER': 'username',
            'PASSWORD': 'password'
        }
    }
