import psycopg2


def createPgSchema(conn, cursor, schemaName):
    """
    Создает схему в базе данных, если таковая отсутствует
    """
    cursor.execute("CREATE SCHEMA IF NOT EXISTS {schemaName};".format(schemaName=schemaName))
    print('--- Схема {schemaName} создана ---'.format(schemaName=schemaName))
    conn.commit()