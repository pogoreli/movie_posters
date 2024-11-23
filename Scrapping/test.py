from sql import SQL
sql_instance = SQL()
sql_instance.initialize()
sql_instance.insert_genre("Comedy")
sql_instance.insert_genre("Horror")