```
This project is cloned and developed based on https://github.com/JpKuo24/GlobalView
```

## Brief
globalview: prototype of global view based on the controller starting from scratch.

## Dependency
### Infrastructure
- Python3
- MongoDB
### Python Package
- pymongo
- networkx_viewer (Use ```pip install networkx_viewer``` to install)

## Execution
### Initilalization (first-time only)
1. Start MongoDB: ```sudo mongod```
2. Initialize DB: ```python test.py```
### Reset (Delete) the DB
1. Start MongoDB: ```sudo mongod```
2. Enter MongoDB command line: ```mongo```
3. In the command line, execute the following commands:
```
use sdcdb
db.dropDatabase()
```
### Run
1. Start MongoDB: ```sudo mongod```
2. Run the digital twin: ```python Manager.py```
