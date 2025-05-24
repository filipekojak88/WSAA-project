# WSAA Project - Actor Management System

![Actor Management System Banner](Images/Actor_Management_System_Screenshoot.png)

## Overview
This project is part of the Web Services and Applications module for the Data Analytics course at Atlantic Technological University, taught by Andrew Beatty. The Actor Management System is a web application that allows users to:

- Perform CRUD operations on actor records
- Search and import actor data from TMDB (The Movie Database)
- View detailed actor information
- Manage a local database of actors with their attributes

## Live Demo
A live version of this application is hosted on PythonAnywhere:  
🔗 [Actor Management System](https://filipekojak88.pythonanywhere.com/actorviewer.html)

## Features
- **Local Actor Management**:
  - Add, view, update, and delete actor records
  - Paginated display of actors
  - Form validation for data integrity

- **TMDB Integration**:
  - Search for actors in the TMDB database
  - View detailed actor information
  - Import actors from TMDB to local database

- **User Interface**:
  - Responsive design with Bootstrap
  - Interactive forms with client-side validation
  - Modal dialogs for detailed views

## Project Structure
```
WSAA-project/
├── actorDAO.py            # Data Access Object for actor operations
├── actorviewer.html       # Frontend HTML/JS interface
├── dbconfig.py            # Database configuration (ignored in Git)
├── dbconfig_template.py   # Template for database configuration
├── requirements.txt       # Python dependencies
├── server.py              # Flask server and API endpoints
└── tmdb_service.py        # TMDB API service
```

## Functionalities

- **actorDAO.py**: The class ActorDAO within `actorDAO.py` acts as an intermediary between the Python code and the MySQL database, handling all the database operations for actor records. It follows the DAO (Data Access Object) pattern, which helps keep the database logic separate from the rest of the application [[1]](#1). The class includes standard CRUD operations—create, read (getAll, findByID), update, and delete—allowing users to manage actor data easily. To prevent security risks like SQL injection, the code uses parameterized queries [[2]](#2), ensuring that user input is safely processed. The helper method convertToDictionary transforms database results into Python dictionaries, making the data easier to work with [[3]](#3). The script also manages database connections properly by opening and closing them in getcursor and closeAll, following best practices for resource handling [[4]](#4). Finally, the database credentials are stored separately in dbconfig.py, which improves security and makes the code more maintainable [[5]](#5).

- **actorviewer.html**: 


## Installation Instructions

### Prerequisites
- Python 3.7+
- MySQL database
- PythonAnywhere account (if deploying there)
- TMDB API account

### Setup Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/WSAA-project.git
   cd WSAA-project
   ```

2. **Set up virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Database configuration**:
   - Rename `dbconfig_template.py` to `dbconfig.py`
   - For MySQL setup on PythonAnywhere:
     - Follow the guide: [PythonAnywhere MySQL Setup](https://help.pythonanywhere.com/pages/UsingMySQL/)
   - For TMDB API:
     - Register at [TMDB Developer Portal](https://developer.themoviedb.org/docs/getting-started)
     - Get your API key and bearer token
   - Fill in your credentials in `dbconfig.py`

5. **Database setup**:
   - Create a MySQL database with the following tables:
   ```sql
   CREATE TABLE actor (
       id INT AUTO_INCREMENT PRIMARY KEY,
       name VARCHAR(255),
       gender VARCHAR(255),
       dob DATE,
       country VARCHAR(250)
   );
   
   CREATE TABLE country (
       id INT AUTO_INCREMENT PRIMARY KEY,
       name VARCHAR(250) NOT NULL
   );
   ```

6. **Run the application**:
   ```bash
   python server.py
   ```
   The application will be available at `http://localhost:5000/actorviewer.html`

## Deployment to PythonAnywhere

1. Upload all files to your PythonAnywhere account
2. Create a new web app and configure it to use your WSGI file
3. Set up the MySQL database in PythonAnywhere's database tab
4. Configure the virtual environment and install requirements
5. Update the `dbconfig.py` with your PythonAnywhere MySQL credentials

## Security Notes
- The `dbconfig.py` file is included in `.gitignore` to prevent sensitive information from being pushed to GitHub
- Always keep your API keys and database credentials secure
- Use environment variables or configuration management in production environments

## Usage Guide

### Managing Local Actors
- **Add Actor**: Click "Add Actor" button and fill in the form
- **Update Actor**: Click "Update" button on an actor row
- **Delete Actor**: Click "Delete" button on an actor row
- **View All Actors**: The main table displays all actors with pagination controls

### Using TMDB Integration
1. Enter an actor name in the search box
2. Click "Search" to view results from TMDB
3. Click "Details" to view comprehensive actor information
4. Click "Import" to add the actor to your local database

## Troubleshooting
- **Database connection issues**: Verify credentials in `dbconfig.py` and ensure MySQL service is running
- **TMDB API errors**: Check your API key and bearer token, and verify your TMDB account is active
- **Missing dependencies**: Run `pip install -r requirements.txt` to ensure all packages are installed

## Contributing
Contributions are welcome! Drop me an email to filipeferc88@gmail.com and let me know a bit about your contribution and then I can provide to you the SSH of my git repository.

## Acknowledgments
- Andrew Beatty for module instruction
- TMDB for their comprehensive API
- PythonAnywhere for hosting services

## References:
 
<a id="1">[1]</a> GeeksforGeeks (2024a) Data Access Object(DAO) design pattern, GeeksforGeeks. Available at: https://www.geeksforgeeks.org/data-access-object-pattern/ 

<a id="2">[2]</a> SQL injection prevention cheat sheet¶ (no date a) SQL Injection Prevention - OWASP Cheat Sheet Series. Available at: https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html

<a id="3">[3]</a> (No date) How to convert SQL query results into a python dictionary - stack overflow. Available at: https://stackoverflow.com/questions/28755505/how-to-convert-sql-query-results-into-a-python-dictionary

<a id="4">[4]</a> (No date a) What are best practices on managing database connections in .net? - stack overflow. Available at: https://stackoverflow.com/questions/3258788/what-are-best-practices-on-managing-database-connections-in-net 

<a id="5">[5]</a> Chapter 2 guidelines for python developers (no date) MySQL. Available at: https://dev.mysql.com/doc/connector-python/en/connector-python-coding.html. 
