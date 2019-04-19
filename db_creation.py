import psycopg2 as pg2

conn = pg2.connect(dbname="postgres", host="localhost") #Need to connect to postgres first, so it then can create your new table
conn.autocommit = True  ## This is required to remove or create databases

cur = conn.cursor()
#Below lines substitute movies for the name of your database you want
cur.execute('DROP DATABASE IF EXISTS movies;')
cur.execute('CREATE DATABASE movies;')
conn.commit()
conn.close()

##change movies here to the name of your database

conn = pg2.connect(dbname="movies", host="localhost")
cur = conn.cursor()

##here is an example of one table -- id serial will automatically create a unique ID and autoincrement it

tables = """CREATE TABLE ratings (id serial PRIMARY KEY,
                                    title VARCHAR(100),
                                    rating VARCHAR(10),
                                    release_year VARCHAR(25));
                                    """
cur.execute(tables)
conn.commit()
conn.close()