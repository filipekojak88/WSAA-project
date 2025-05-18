# Name: Actor DAO
# Description: This is a data access object (DAO) for the Actor table in a MySQL database.
# It provides methods to perform CRUD (Create, Read, Update, Delete) operations on the Actor table.
# Author: Filipe Carvalho

import mysql.connector
import dbconfig as cfg
class ActorDAO:
    connection=""
    cursor =''
    host=       ''
    user=       ''
    password=   ''
    database=   ''
    
    def __init__(self):
        self.host=       cfg.mysql['host']
        self.user=       cfg.mysql['user']
        self.password=   cfg.mysql['password']
        self.database=   cfg.mysql['database']

    def getcursor(self): 
        self.connection = mysql.connector.connect(
            host=       self.host,
            user=       self.user,
            password=   self.password,
            database=   self.database,
        )
        self.cursor = self.connection.cursor()
        return self.cursor

    def closeAll(self):
        self.connection.close()
        self.cursor.close()
         
    def getAll(self):
        cursor = self.getcursor()
        sql="""SELECT actor.id, actor.name, actor.gender, actor.dob, country.name 
             FROM actor 
             JOIN country ON actor.country_id = country.id"""
        cursor.execute(sql)
        results = cursor.fetchall()
        returnArray = []        
        for result in results:            
            returnArray.append(self.convertToDictionary(result))        
        self.closeAll()
        return returnArray

    def findByID(self, id):
        cursor = self.getcursor()
        sql="""SELECT actor.id, actor.name, actor.gender, actor.dob, country.name 
             FROM actor 
             JOIN country ON actor.country_id = country.id
             WHERE actor.id = %s"""
        values = (id,)

        cursor.execute(sql, values)
        result = cursor.fetchone()
        returnvalue = self.convertToDictionary(result)
        self.closeAll()
        return returnvalue

    def create(self, actor):
        cursor = self.getcursor()
               
        sql="INSERT INTO actor (name, gender, dob, country_id) VALUES (%s, %s, %s, %s)"
        values = (actor.get("name"), actor.get("gender"), actor.get("dob"), actor.get("country_id"))
        print("Actor to insert:", actor)
        print("SQL Values:", values)
        cursor.execute(sql, values)

        self.connection.commit()
        new_actor_id = cursor.lastrowid
        actor["id"] = new_actor_id
        self.closeAll()
        return actor


    def update(self, id, actor):
        cursor = self.getcursor()
        sql = "UPDATE actor SET name=%s, gender=%s, dob=%s, country_id=%s WHERE id=%s"
        print(f"Update actor {actor}")
        values = (actor.get("name"), actor.get("gender"), actor.get("dob"), actor.get("country_id"), id)
        cursor.execute(sql, values)
        self.connection.commit()
        self.closeAll()
        
    def delete(self, id):
        cursor = self.getcursor()
        sql="DELETE FROM actor WHERE id = %s"
        values = (id,)

        cursor.execute(sql, values)

        self.connection.commit()
        self.closeAll()
        
        print("Deleted actor successfully!")

    def convertToDictionary(self, result_line):
        attkeys = ['id', 'name', 'gender', 'dob', 'country']
        actor = {}
        for i, attrib in enumerate(result_line):
            actor[attkeys[i]] = attrib
        return actor
    
    def getAllCountries(self):
        cursor = self.getcursor()
        sql = "SELECT id, name FROM country ORDER BY name"
        cursor.execute(sql)
        results = cursor.fetchall()
        country_list = [{"id": row[0], "name": row[1]} for row in results]
        self.closeAll()
        return country_list

        
actorDAO = ActorDAO()