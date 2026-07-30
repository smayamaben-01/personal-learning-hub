import mysql.connector
import config

def get_db_connection():
    return mysql.connector.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DB_NAME,
        ssl_ca=config.DB_SSL_CA,
        ssl_verify_cert=True
    )