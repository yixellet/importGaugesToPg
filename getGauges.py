def getGauges(cursor, schemaName):
    """
    Получает из БД перечень гидропостов
    """

    cursor.execute("""SELECT * FROM {schemaName}.gauges WHERE type = 'gauge'"""
        .format(schemaName=schemaName))
    return cursor.fetchall()