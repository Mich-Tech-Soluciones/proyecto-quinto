import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_database():
    try:
        conn = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            password='root',
            host='localhost',
            port='5432'
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'kazabd'")
        exists = cursor.fetchone()
        if not exists:
            cursor.execute('CREATE DATABASE kazabd')
            print("Database kazabd created successfully.")
        else:
            print("Database kazabd already exists.")
            
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error creating database: {e}")

if __name__ == '__main__':
    create_database()
