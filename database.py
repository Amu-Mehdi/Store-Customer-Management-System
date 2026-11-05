import pyodbc


def get_connection():
    connection = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost;"
        "DATABASE=StoreDB;"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )
    return connection

