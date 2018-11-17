# sdc

This is the central repo for the SDC (software-defined control) project.

Python 2.7 is required. The code is NOT compatible with Python 3.

# Packages
globalview: prototype of global view based on the controller starting from scratch.

onos: prototype of decision maker based on the ONOS controller, draft of the global view is also provided.

# Clone and install
For using Global view, you are supposed to install mongoDB in your computer and using $./mongod to run database first. 

$ git clone git@github.com:JpKuo24/sdc.git

$ cd sdc/globalview

$ python test.py   # create data in the database

$ python Manager.py
