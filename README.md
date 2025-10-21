# KrakenMeter
Git Repo: https://github.com/AakashAxe/KrakenMeter
## My Appraoch:
Before Developing I read the requirements and on a piece of paper designed the flow. 
Brainstormed how the database will look and support extendablility, did the same for when designing what the code would look like.

## Assumptions:
- First and last line for file dont matter, i assume they are some sort of customer information. I tried making sense of it but didnt see the answer in the linked page.

## Design
- There is the core App Kraken Flow and the sub app whch is the flow processor. Two seperate apps is for seperations of concerns, we want to avoid overloading the main app with all the functionality, in the future same project could be used to implement a different set of requirements.
- When i was designing this i took into consideration that in the future we could ingest more codes than we do right now.
    This is why in models i have gone with the have heirarchy approach, and the code is extendable just need to modify one file and add a new processing method per new code added.
- Inside the project. 
    I have used services to perform the complex logic
    Repository class to handle reading and writing to Db
    Other Default classes to create api and models.


## Time Limitations:
- I would have liked to add more exception handling and test those with additional test cases

## Instructions to run the code:
We will need python 3 installed
```
python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

python3 manage.py migrate flow_processor
```

This will install all dependencies, and complete the migration as well.

## Run the code - Command Line
Example:
```
python3 manage.py import_command sample_data/DTC5259515123502080915D0010.uff
```

## Run the Django Server
Run from KrakenMeter project directory
```
python3 manage.py runserver
```
The url to test:
http://127.0.0.1:8000/flow/read/sample_data

The files are successfully saved into the db you can view it by 
http://127.0.0.1:8000/admin

Login details:
admin
admin

incase you have to create a super user, the commands are 
```
python3 manage.py createsuperuser
```

you can then add your username and password.


## Run Tests:

```
python3 manage.py test
```



    


