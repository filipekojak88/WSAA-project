"""
Name: Actor DAO
Description: This is a data access object (DAO) for the Actor table in a MySQL database.
It provides methods to perform CRUD (Create, Read, Update, Delete) operations on the Actor table.
Author: Filipe Carvalho
"""

# Import necessary libraries
import mysql.connector
import dbconfig as cfg

class ActorDAO:
    """Data Access Object for Actor operations"""


    def __init__(self):
        # Initialize the database connection parameters
        self.host = cfg.mysql['host']
        self.user = cfg.mysql['user']
        self.password = cfg.mysql['password']
        self.database = cfg.mysql['database']
        self.connection = None
        self.cursor = None
    
    def getcursor(self): 
        # Establish a connection to the MySQL database
        self.connection = mysql.connector.connect(
            host = self.host,
            user = self.user,
            password = self.password,
            database = self.database,
        )
        self.cursor = self.connection.cursor()
        return self.cursor
    
    def closeAll(self):
        # Close the database connection and cursor
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        
    # CRUD operations
    def getAll(self):
        # Retrieve all actors from the database
        cursor = self.getcursor()
        sql="""SELECT id, name, gender, dob, country 
               FROM actor"""
        cursor.execute(sql)
        results = [self.convertToDictionary(row) for row in cursor.fetchall()]       
        self.closeAll()
        return results

    def findByID(self, id):
        # Retrieve an actor by ID
        cursor = self.getcursor()
        sql="""SELECT id, name, gender, dob, country 
               FROM actor 
               WHERE id = %s"""
        cursor.execute(sql, (id,))
        result = self.convertToDictionary(cursor.fetchone())
        self.closeAll()
        return result

    def create(self, actor):
        # Create a new actor into the database
        cursor = self.getcursor()
        sql="""INSERT INTO actor (name, gender, dob, country) 
               VALUES (%s, %s, %s, %s)"""
        values = (
            actor.get("name"), 
            actor.get("gender"), 
            actor.get("dob"), 
            actor.get("country")
        )
        cursor.execute(sql, values)
        self.connection.commit()
        actor["id"] = cursor.lastrowid
        self.closeAll()
        return actor

    def update(self, id, actor):
        # Update an existing actor in the database
        cursor = self.getcursor()
        sql = """UPDATE actor
                SET name=%s, gender=%s, dob=%s, country=%s 
                WHERE id=%s"""
        values = (
            actor.get("name"),
            actor.get("gender"), 
            actor.get("dob"), 
            actor.get("country"), 
            id
        )
        cursor.execute(sql, values)
        self.connection.commit()
        self.closeAll()
        
    def delete(self, id):
        # Delete an actor from the database
        cursor = self.getcursor()
        sql = """DELETE FROM actor 
                WHERE id = %s"""
        cursor.execute(sql, (id,))
        self.connection.commit()
        self.closeAll()
    
    # Helper method
    def convertToDictionary(self, result_line):
        # Convert a result line from the database into a dictionary
        keys = ['id', 'name', 'gender', 'dob', 'country']
        return dict(zip(keys, result_line)) if result_line else None
    
    # Country method
    def getAllCountries(self):
        # Retrieve all countries from the database
        cursor = self.getcursor()
        sql = """SELECT id, name 
                FROM country 
                ORDER BY name"""
        cursor.execute(sql)
        results = [{"id": row[0], "name": row[1]} for row in cursor.fetchall()]
        self.closeAll()
        return results
    
# An instance of the ActorDAO class    
actorDAO = ActorDAO()