def getTable(cursor, schemaName, tableName):
    """
    Получает из БД перечень гидропостов
    """

    cursor.execute("""SELECT * FROM {0}.{1}"""
        .format(schemaName, tableName))
    return cursor.fetchall()