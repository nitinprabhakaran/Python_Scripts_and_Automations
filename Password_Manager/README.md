
# Password Manager v2

Version 2 has been implemented using below modules

-> PosgreSQL (psycopg2) (Used this to save the troubles of installing PostgreSQL in Mac)
    (Make sure you have a glance at ```https://pypi.org/project/psycopg2/``` documentation for initial configurations like DB Name and uswername and password )

-> hashlib

I have tried to simplify the code as much as i could and make it more robust.

## REQUIREMENTS

Make sure you have a PostgreSQL Instance running with a DB and it's username and password already created

Take a good look at the ```database manager.py``` file and set the name of the DB table, Username and Pass for the DB accordingly

In the file ```secret.py``` input the master password for your DB and then run the ```password_manager.py``` file to start the program
