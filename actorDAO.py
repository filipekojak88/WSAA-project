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
        sql="select * from actor"
        cursor.execute(sql)
        results = cursor.fetchall()
        returnArray = []
        #print(results)
        for result in results:
            #print(result)
            returnArray.append(self.convertToDictionary(result))
        
        self.closeAll()
        return returnArray

    def findByID(self, id):
        cursor = self.getcursor()
        sql="SELECT * FROM actor WHERE id = %s"
        values = (id,)

        cursor.execute(sql, values)
        result = cursor.fetchone()
        returnvalue = self.convertToDictionary(result)
        self.closeAll()
        return returnvalue

    def create(self, actor):
        cursor = self.getcursor()
        sql="INSERT INTO actor (name,gender,dob) VALUES (%s,%s,%s)"
        values = (actor.get("name"), actor.get("gender"), actor.get("dob"))
        cursor.execute(sql, values)

        self.connection.commit()
        new_actor_id = cursor.lastrowid
        actor["id"] = new_actor_id
        self.closeAll()
        return actor


    def update(self, id, actor):
        cursor = self.getcursor()
        sql="UPDATE actor SET name= %s, gender=%s, dob=%s  WHERE id = %s"
        print(f"Update actor {actor}")
        values = (actor.get("name"), actor.get("gender"), actor.get("dob"), id)
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
        attkeys=['id','name','gender', "dob"]
        actor = {}
        current_key = 0
        for attrib in result_line:
            actor[attkeys[current_key]] = attrib
            current_key = current_key + 1 
        return actor

        
actorDAO = ActorDAO()