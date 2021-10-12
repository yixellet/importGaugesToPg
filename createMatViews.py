def createMatViews(conn, cursor, schema, gauges):
    """
    Создает материализованные представления
    """

    for gauge in gauges:
        cursor.execute("""
            CREATE MATERIALIZED VIEW IF NOT EXISTS {schemaName}."{code}abs"
            AS
            SELECT date,
                   round((hydro.getrefelev(date, %(uid)s) + value::double precision/100)::numeric, 2) AS stage,
                   props
            FROM {schemaName}."{code}"
            WITH DATA;
            """.format(schemaName=schema, code=gauge[2]),
            {'uid': gauge[5]})
    conn.commit()
    print('--- Созданы материализованные представления ---')