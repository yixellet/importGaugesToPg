def createMatViews(conn, cursor, schema, gauges):
    """
    Создает материализованные представления
    """

    cursor.execute("""CREATE OR REPLACE FUNCTION hydro.getRefElev(IN date date,IN uuid uuid) \
                    RETURNS double precision LANGUAGE 'sql' VOLATILE PARALLEL UNSAFE COST 100 AS \
                    $BODY$ \
                    SELECT "ref_elevations".elevation \
                    FROM hydro."ref_elevations" \
                    WHERE $2 = "ref_elevations".gauge AND \
                    ($1 BETWEEN "ref_elevations"."startDate" AND "ref_elevations"."endDate") \
                    $BODY$;""")
    conn.commit()

    for gauge in gauges:
        cursor.execute("""
            CREATE MATERIALIZED VIEW {schemaName}."{code}abs"
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