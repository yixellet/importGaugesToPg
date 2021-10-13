def createViews(conn, cursor, schema, gauges):
    """
    Создает материализованные представления
    """

    for gauge in gauges:
        cursor.execute("""
            CREATE OR REPLACE VIEW {0}."{1}abs"
            AS
            SELECT date,
                   round(({0}.getrefelev(date, %(uid)s) + value::double precision/100)::numeric, 2) AS stage,
                   props
            FROM {0}."{1}";
            """.format(schema, gauge[2]),
            {'uid': gauge[0]})
    conn.commit()
    print('--- Созданы представления ---')