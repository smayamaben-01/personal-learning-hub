import mysql.connector
import config

def get_db_connection():
    conn_args = {
        "host": config.DB_HOST,
        "user": config.DB_USER,
        "password": config.DB_PASSWORD,
        "database": config.DB_NAME,
    }

    if config.DB_PORT:
        conn_args["port"] = int(config.DB_PORT)

    if config.DB_SSL_CA:
        conn_args["ssl_ca"] = config.DB_SSL_CA
        conn_args["ssl_verify_cert"] = True

    return mysql.connector.connect(**conn_args)