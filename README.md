## bookshelf app

----
This project is a virtual bookshelf where users are able to add their books to the bookshelf, give them a rating, update the rating and search through their book lists. 

---
#### Pre-requisites
* Have Python3, pip and node installed on your local machines.

* **Start your virtual environment** 
From the backend folder run
```bash
# Mac users
python3 -m venv venv
source venv/bin/activate
# Windows users
> py -3 -m venv venv
> venv\Scripts\activate
```

* **Install dependencies**<br>
From the backend folder run 
```bash
# All required packages are included in the requirements file. 
pip3 install -r requirements.txt
# In addition, you will need to UNINSTALL the following:
pip3 uninstall flask-socketio -y
```

### Step 1 - Create and Populate the database

1. **Create the database
In your terminal, navigate to the */backend/* directory, and run the following:
```bash
# Connect to the PostgreSQL
psql postgres
#View all databases
\l
# Create the database
\i setup.sql
# Exit the PostgreSQL prompt
\q
```


3. **Create tables**<br>
Once your database is created, you can create tables (`bookshelf`) and apply contraints
```bash
# Mac users
psql -f books.psql -U student -d bookshelf
# Linux users
su - postgres bash -c "psql bookshelf < /path/to/exercise/backend/books.psql"

```
**You can even drop the database and repopulate it, if needed, using the commands above.** 


### Step 2: Start the backend
Start the (backend) Flask server by running the command below from the `/backend/` directory.
```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```



### Step 3: Start the frontend
(You can start the frontend even before the backend is up!)
From the `frontend` folder, run the following commands to start the client: 
```
npm install // only once to install dependencies
npm start 
```
By default, the frontend will run on `localhost:3000`. Close the terminal if you wish to stop the frontend server. 


---

#### Running Tests
Navigate to the `/backend` folder and run: 
```bash

python test_flaskr.py
```