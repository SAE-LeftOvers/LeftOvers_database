from dotenv import load_dotenv
import os
import psycopg2 as psy

load_dotenv()

def InitializeDatabaseConnection():
    try:
        co = psy.connect(host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            port=os.getenv("DB_PORT"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"))
        print("Database connected.")
        return co
    except(Exception, psy.DatabaseError) as error:
        print(error)
        exit(error)
        return None

def CloseDatabaseConnection(co):
    if co is not None:
        co.close()
    print("Database connection closed.")