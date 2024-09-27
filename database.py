import psycopg2
import os
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import DictCursor
from contextlib import contextmanager
from flask import Flask, jsonify, json

pool = None

def setup():
    global pool
    DATABASE_URL = os.environ['DATABASE_URL']
    pool = ThreadedConnectionPool(1, 100, dsn=DATABASE_URL, sslmode='require')

setup()

@contextmanager
def get_db_connection():
    try:
        connection = pool.getconn()
        yield connection
    finally:
        pool.putconn(connection)

@contextmanager
def get_db_cursor(commit=False):
    with get_db_connection() as connection:
      cursor = connection.cursor(cursor_factory=DictCursor)
      try:
          yield cursor
          if commit:
              connection.commit()
      finally:
          cursor.close()
#============================================
def createTable():
    with get_db_cursor(True) as cur:        
        query = """
        CREATE TABLE blogs (
            ID SERIAL PRIMARY KEY,
            TITLE VARCHAR(256),
            CAT TEXT,
            TAGS TEXT [],
            CONTENT TEXT,
            PUBLISHED BOOLEAN DEFAULT FALSE,
            CREATED TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            LASTEDIT TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )"""
        cur.execute(query)
        

# createTable()
def selectAllBlog():
    with get_db_cursor(True) as cur:
        query = "SELECT * FROM blogs"
        
        cur.execute(query)
        
        results = cur.fetchall()

        return results
    
# print(selectAllBlog())

def saveBlog(data):
    with get_db_cursor(True) as cur:
        query = """
            INSERT INTO blogs (TITLE, CAT, TAGS, CONTENT) 
            VALUES (%s, %s, %s, %s)
        """
        cur.execute(query, (data['title'], data['category'], data['tags'], json.dumps(data['delta'])))
        
        print('insert successfully')
        
        return 0
    
def selectBlogsByPublished():
    with get_db_cursor(True) as cur:
        query = """SELECT * FROM blogs WHERE PUBLISHED = True"""
        cur.execute(query)
        
        results = cur.fetchall()
        
        return results
    
def selectBlogsByPublishedTitle(title):
    with get_db_cursor(True) as cur:
        
        query = """SELECT * FROM blogs WHERE TITLE = %s AND PUBLISHED = %s;"""
        
        cur.execute(query, (str(title), True))
        
        results = cur.fetchall()[0]
        
        # print(results)
        
        return results
    
def selectBlogsByPublishedTag(tags):
    with get_db_cursor(True) as cur:
        
        query = """SELECT * FROM blogs WHERE PUBLISHED = True;"""
        
        cur.execute(query)
        
        results = cur.fetchall()
        
        matches = []
        
        for elem in results:
            for items in elem[3]:
                # print(items)
                if items == tags:
                    matches.append(elem)
        
        # print(matches)
        
        return matches
    
def selectBlogsByPublishedCat(category):
    with get_db_cursor(True) as cur:
        
        # print(category)
        query = """SELECT * FROM blogs WHERE PUBLISHED = True;"""
        
        cur.execute(query)
        
        results = cur.fetchall()
        # print(results)
        matches = []
        
        if(category != None):
            for i in range(len(results)):
                if category == results[i][2]:
                    matches.append(results[i])
            return matches    

        else:
            return results

        
        # print(matches)
        


def selectBlogsByID(id):
    with get_db_cursor(True) as cur:
        query = """SELECT * FROM blogs WHERE id = %s;"""
        
        cur.execute(query, (id))
        
        results = cur.fetchall()[0]
        print(results)
        
        if(results == None):
            print('error')
        else:
            return results
    
def updateBlog(data):
    with get_db_cursor(True) as cur:
        
        query = """
            UPDATE blogs 
            SET TITLE = %s, 
            CAT = %s, 
            TAGS = %s, 
            CONTENT = %s,
            LASTEDIT = CURRENT_TIMESTAMP
            WHERE ID = %s
        """
        
        cur.execute(query, (data['title'], data['category'], data['tags'], json.dumps(data['delta']), data['id']))
        
        print("update successfully")
        
        return 0
    
def publishBlog(data):
    with get_db_cursor(True) as cur:
        
        query = """
            UPDATE blogs
            SET CONTENT = %s, PUBLISHED = True
            WHERE ID = %s
        """
        
        cur.execute(query, (data['delta'], data['id']))
        
        return 0
        