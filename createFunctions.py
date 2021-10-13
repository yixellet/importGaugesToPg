def createFunctions(conn, cursor):
    """
     Создает все необходимые функции в БД
    """

    cursor.execute(
        """
        CREATE OR REPLACE FUNCTION hydro.count_obs(IN tbl character varying)
            RETURNS TABLE(year integer, filled integer, total integer)
            LANGUAGE 'plpgsql'
            VOLATILE
            PARALLEL UNSAFE
            COST 100    ROWS 1000
        AS $BODY$
        BEGIN
        FOR i IN 1960..2021 LOOP
            RETURN QUERY
            EXECUTE
            'SELECT date_part(''year'', date)::integer AS year,
                count(*)::integer AS filled_days,
                (CASE
                    WHEN date_part(''year'', date)::integer % 4 = 0 THEN 366
                    ELSE 365
                    END) AS common_days
            FROM hydro."' || tbl ||
            '" WHERE date_part(''year'', date) = '|| i || 
            ' GROUP BY date_part(''year'', date)'; 
        END LOOP;
        END;
        $BODY$;

        CREATE OR REPLACE FUNCTION hydro.dates(IN date date,IN uuid uuid)
            RETURNS double precision
            LANGUAGE 'sql'
            VOLATILE
            PARALLEL UNSAFE
            COST 100
        AS $BODY$
        SELECT "ref_elevations".elevation
        FROM hydro."ref_elevations" 
        WHERE $2 = "ref_elevations".gauge AND
        ($1 BETWEEN "ref_elevations"."startDate" AND "ref_elevations"."endDate")
        $BODY$;

        CREATE OR REPLACE FUNCTION hydro.getRefElev(IN date date,IN uuid uuid)
            RETURNS double precision LANGUAGE 'sql' VOLATILE PARALLEL UNSAFE COST 100
        AS $BODY$
        SELECT "ref_elevations".elevation
        FROM hydro."ref_elevations"
        WHERE $2 = "ref_elevations".gauge AND
        ($1 BETWEEN "ref_elevations"."startDate" AND "ref_elevations"."endDate")
        $BODY$;
        """
    )

    conn.commit()