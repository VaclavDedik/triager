# Triager

This web application written in python and flask uses machine learning to train a classifier on bug tracking system data to predict assignees. It uses Support Vector Machine model with TF-IDF weighing and stop words removal. With this settings, it is able to achieve about 50 % accuracy and about 45 % precision and recall. The performance, however, depends on your project. Some projects are able to achieve as much as 70 % accuracy and some as little as 30 %.

## How to Use the Application

It is rather simple. First, you log in as admin (by default username 'admin' and password also 'admin'). Then all you have to do is create new project and fill in the required fields, for example name of the project, training schedule and data source. Data source is a particular source of the data that it will be retrieved from. Currently, only Jira data source is supported. You can create as many projects as possible.

When the data for the project are downloaded and the initial training is finished, you can use the application to predict assignees (developers who should fix a particular bug) by filling in the summary of the issue and its description. You can also provide feedback by selecting the assignee that is correct for the ticket/issue/bug report you filled in.

## How to Setup, Configure and Run the Application

### Requirements

You need to have this software installed on your computer:

* python 2.7
* pip

As for HW requirements, it is recommended to have a computer with at least 2 GB of RAM.

I also recommend to use a Linux distribution to install and run the application. Windows is very unlikely to work as it is not tested with it. Mac OS X should work, but it has not been tested thoroughly to be sure.

### How to Setup the Application

The application uses a lot of machine learning and natural language processing libraries, so it can be quite hard to successfully setup the application. You should first try to just run the setup script. First, though, you need to have setuptools installed. You can install it like this (on ubuntu):

    $ sudo apt-get install python-setuptools

Then you can run the setup script like this (you might need root privileges):

    $ python setup.py install  

This might fail on either numpy or scipy. If so, you can try to install these libraries via your package manager, for example on ubuntu:

    $ sudo apt-get install python-numpy python-scipy

If scikit-learn fails, you can try to install these libraries (on ubuntu):

    $ sudo apt-get install build-essential python-dev \
                     python-numpy python-scipy \
                     libatlas-dev libatlas3gf-base

And than re-run the setup script.

If you managed to successfully run the setup script, you now need to download nltk stopwords data. You can do that by running this command:

    $ python -m nltk.downloader -d $NLTK_DATA stopwords

Where NLTK_DATA is an environment variable that contains path to where you want the NLTK data to be stored. If you do not specify a directory via the -d option (and your NLTK_DATA variable is not set), the data will be downloaded into your home directory into directory "nltk_data" (~/nltk_data). Be aware that if you do not want to have the data in your home directory, you **need to** have NLTK_DATA variable set and pointed to a location with write access.

### How to Configure the Application

There is a python script "settings.py" in the "triager" directory (in the source root). You should copy this file into some directory (e.g. wherever your STORAGE_FOLDER will be, see below) and set an environment variable TRIAGER_SETTINGS that points to the file, e.g. like this:

    $ export TRIAGER_SETTINGS="/home/yourname/triager_data/settings.py"

As for configuration in the file, at the very least, you should set the DEBUG value to False. You should also consider to change the values of STORAGE_FOLDER and LOG_DIR. It is a good idea to have the variables use environment variables by changing their values like this:

    STORAGE_FOLDER = os.environ['TRIAGER_DATA_DIR']

And:

    LOG_DIR = os.environ['TRIAGER_LOG_DIR']

Be sure to have those environment variables set and the directories they point to created with write access. If you use OpenShift, I recommend to point the STORAGE_FOLDER to OPENSHIFT_DATA_DIR and the LOG_DIR to OPENSHIFT_LOG_DIR.

### How to Run the Application

The application consists of two parts. First part is the web application that serves incoming HTTP requests. The second part, the scheduler, is used to train the projects for recommendation. If you do not have the scheduler running, the application will not be able to train the projects and the web application will therefore not be able to recommend any assignees for any issues you fill in. The web application tells you if the scheduler is not running by printing "Scheduler is not running!" in the top left corner.

**To run the web application** in development, you can just run this command:

    $ python manage.py runserver

You should, however, never run the web application like this in production. The underlying WSGI server used by default cannot handle more than one request at a time. Therefore, in production, you should use a different WSGI, e.g. gunicorn or mod_wsgi. To use gunicorn, install it like this:

    $ pip install gunicorn

Or with your system package manager, for example on ubuntu:

    $ sudo apt-get install gunicorn

After that, you can run this command (in the source root where manage.py is) to run the web application with gunicorn:

    $ gunicorn -w 4 manage:app

You probably want to run the gunicorn WSGI as daemon (so that it does not get shut down when you exit your session), so you should instead run the command like this:

    $ gunicorn -w 4 manage:app -D

**To run the scheduler**, all you need to do is run this command (even in production):

    $ python manage.py runscheduler

You also, however, want the application to run in background, so you can use nohup to achieve this:

    $ nohup python manage.py runscheduler &

## Development

If you want to contribute to the project, you can use vagrant to setup your development environment for this project. There is a Vagrantfile in the source root of this project, so if you have vagrant installed (if not, get it from [here](https://www.vagrantup.com)), you can just run this command to set up your development environment:

    $ vagrant up

To start the application, you need to ssh to the vagrant virtual environment like this:

    $ vagrant ssh

And then go to directory "triager" where you can run the web application and the scheduler like this:

    $ python manage.py runserver &
    $ python manage.py runscheduler &

To access the web application, you just need to access this web page in your browser:

    http://0.0.0.0:5000
