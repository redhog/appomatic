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
