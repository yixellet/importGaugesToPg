def createIndexes(conn, cursor, schemaName, gauges):
    """
    Создает индексы в таблицах и материализованных представлениях
    """
    for gauge in gauges:
        cursor.execute(
            """
            CREATE INDEX "{1}_idx" ON {0}."{1}" USING btree(date);
            """.format(schemaName, gauge[2])
        )
    conn.commit()