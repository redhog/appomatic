# Installation instructions

Run the following commands in a terminal (replace $NAME with any name
you see fit):

```
   virtualenv $NAME
   cd $NAME
   . bin/activate
   pip install appomatic
   appomatic syncdb
   appomatic runserver
```
In a web-browser, go to localhost:8000/admin and log in with the
username/password you entered in the syncdb step above. Click on
"Applications" then "Download new applications" to install some
usefull applications for your new site.

# How to make an auto discoverable django app
Start by creating a directory called apps in the root of your virtualenv.
Inside this directory create another one for your django app. For this app directory to be auto discovered and loaded by appomatic as a django app, it has to

* be named appomatic_SOMENAME
* contain a file _ _ init _ _.py, can be empty
* contain a file _ _ app _ _.py, can be empty

In addition, it can contain all the "normal" django app files, such as models.py, as well as the following optional files

* _ _ settings _ _.py any lines here will be virtually appended to settings.py in the django project
* _ _ urls _ _.py this will be included by the projects urls.py, with no url prefix

So, with this, you can create a single-directory app that gets loaded automatically, and can add stuff to settings.py and urls.py. But distributing this would still be rather clunky by itself. Appomatic supports pip packages, so all you need to do is to make a pip package, named appomatic_SOMENAME that installs a single python module, name appomatic_SOMENAME, that contains the files from above (_ _ app _ _.py etc). An installed such pip package will be auto discovered just like modules under the apps directory.

# What you can do with _ _ apps _ _.py
```
    INSTALLED_APPS = ["some_django_app_name", "some_other_name"]
```
Appends to INSTALLED_APPS in settings.py. Note however that this list is pre-populated with the name of the appomatic app itself (appomatic_SOMENAME), so if you set its value rather than appending to it, you are actually replacing this app with some other app in the list of installed apps. This is usefull to create appomatic "wrapper apps" for django apps that already come as a pip package - wrap up its config in _ _ urls _ _.py, _ _ settings _ _.py (and maybe _ _ app _ _.py), and make it replace the appomatic app in INSTALLED_APPS.
```
    HAS_PARTS = True
```
Treats this directory as a directory of apps instead of as an app, recursively loading any appomatic_SOMENAME/appomatic_SOMEOTHERNAME.
```
    PRE = ["appomatic_OTHERAPP1", "appomatic_OTHERAPP2"]
    POST = ["appomatic_OTHERAPP3", "appomatic_OTHERAPP4"]
```
Causes appomatic_OTHERAPP1 and appomatic_OTHERAPP2, if installed, to be sorted before this app in INSTALLED_APPS (and in urls.py and settings.py), and appomatic_OTHERAPP3 and appomatic_OTHERAPP4 to be sorted after this app.

# Special stuff to do with _ _ settings _ _.py
```
    SOME_NAME = get_app_config_list('SOME_NAME')
```
This will extract the variable SOME_NAME from _ _ app _ _.py in all installed apps (sorted according to their PRE and POST directives). The values all has to be tuples/lists, and they will be concatenated and returned by this function. This is how INSTALLED_APPS is handled:
```
    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.comments',
    ) + get_app_config_list('INSTALLED_APPS')
```
