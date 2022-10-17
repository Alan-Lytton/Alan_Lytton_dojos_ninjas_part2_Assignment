#this whole file can be changed depending on what we need to do with the data and how we want our OOP instances to appear.

# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
# model the class after the Ninja table from our database
class Ninja:
    def __init__( self , data ):
        self.id = data['id']
        self.dojo_id = data['dojo_id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.age = data['age']
        self.id_for_dojo = data['id_of_dojo']
        self.dojo_name = data['name_of_dojo']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    # Now we use class methods to query our database

    @classmethod
    def get_some(cls, data):
        # adjust the "FROM" target to be the required table
        query = "SELECT ninjas.id, ninjas.dojo_id, ninjas.first_name, ninjas.last_name, ninjas.age, ninjas.created_at, ninjas.updated_at, dojos.id AS id_of_dojo, dojos.name AS name_of_dojo  FROM ninjas JOIN dojos ON ninjas.dojo_id = dojos.id WHERE dojo_id = %(dojo_id)s;"
        # make sure to call the connectToMySQL function with the DB schema you are targeting.
        results = connectToMySQL('dojos_and_ninjas_schema').query_db(query,data)
        # Create an empty list to append our instances of ninjas
        ninjas = []
        # Iterate over the db results and create instances of ninjas with cls.
        for ninja in results:
            ninjas.append( cls(ninja) )
        return ninjas

    @classmethod
    def get_one(cls, data):
        query = "SELECT ninjas.id, ninjas.dojo_id, ninjas.first_name, ninjas.last_name, ninjas.age, ninjas.created_at, ninjas.updated_at, dojos.id AS id_of_dojo, dojos.name AS name_of_dojo  FROM ninjas JOIN dojos ON ninjas.dojo_id = dojos.id WHERE ninjas.id = %(ninja_id)s;"
        results = connectToMySQL('dojos_and_ninjas_schema').query_db(query,data)
        ninjas = []
        for ninja in results:
            ninjas.append( cls(ninja) )
        return ninjas

    @classmethod
    def add_ninja(cls, data):
        query = "INSERT INTO ninjas (dojo_id, first_name, last_name, age, created_at, updated_at) VALUES (%(dojo_id)s, %(fname)s, %(lname)s, %(age)s,now(),now());"
        return connectToMySQL('dojos_and_ninjas_schema').query_db(query,data)

    @classmethod
    def delete_ninja(cls, data):
        query = "DELETE FROM ninjas WHERE id = %(ninja_id)s;"
        return connectToMySQL('dojos_and_ninjas_schema').query_db(query,data)

    @classmethod
    def update_ninja(cls,data):
        query = "UPDATE ninjas SET first_name = %(fname)s, last_name = %(lname)s, age = %(age)s WHERE id = %(ninja_id)s;"
        return connectToMySQL('dojos_and_ninjas_schema').query_db(query,data)