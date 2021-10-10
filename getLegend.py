def getLegend(cursor, schemaName, tableName):
    """
    Получает условные обозначения из БД
    """
    cursor.execute("SELECT * FROM {0}.{1}".format(schemaName, tableName))
    
    return cursor.fetchall()