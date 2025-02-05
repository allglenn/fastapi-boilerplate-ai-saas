import time
import psycopg2
from config import settings

def wait_for_db():
    while True:
        try:
            conn = psycopg2.connect(
                dbname=settings.POSTGRES_DB,
                user=settings.POSTGRES_USER,
                password=settings.POSTGRES_PASSWORD,
                host=settings.POSTGRES_HOST,
                port=settings.POSTGRES_PORT
            )
            conn.close()
            break
        except psycopg2.OperationalError:
            print("Database not ready. Waiting...")
            time.sleep(1)

if __name__ == "__main__":
    wait_for_db()
    print("Database is ready!") 