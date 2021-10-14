def createViews(conn, cursor, schema, gauges):
    """
    Создает материализованные представления
    """

    for gauge in gauges:
        cursor.execute("""
            CREATE OR REPLACE VIEW {0}."s{1}"
            AS
            SELECT date,
                   round(({0}."getRefElev"(date, %(uid)s) + value::double precision/100)::numeric, 2) AS stage,
                   props
            FROM {0}."v{1}";
            """.format(schema, gauge[2]),
            {'uid': gauge[0]})
    conn.commit()
    print('--- Созданы представления ---')