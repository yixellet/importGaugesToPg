def createFunctions(conn, cursor, schemaName):
    """
     Создает все необходимые функции в БД
    """

    cursor.execute(
        """
        CREATE OR REPLACE FUNCTION {0}."count_obs"(IN tbl character varying)
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
                count(*)::integer AS filled,
                (CASE
                    WHEN date_part(''year'', date)::integer % 4 = 0 THEN 366
                    ELSE 365
                    END) AS total
            FROM {0}."' || tbl ||
            '" WHERE date_part(''year'', date) = '|| i || 
            ' GROUP BY date_part(''year'', date)'; 
        END LOOP;
        END;
        $BODY$;

        CREATE OR REPLACE FUNCTION {0}."getRefElev"(IN date date,IN uuid uuid)
            RETURNS double precision 
            LANGUAGE 'sql' 
            VOLATILE 
            PARALLEL UNSAFE 
            COST 100
        AS $BODY$
        SELECT "ref_elevations".elev
        FROM {0}."ref_elevations"
        WHERE $2 = "ref_elevations".gauge AND
        ($1 BETWEEN "ref_elevations"."startDate" AND (CASE WHEN "ref_elevations"."endDate" IS NULL THEN now() ELSE "ref_elevations"."endDate" END))
        $BODY$;

        CREATE OR REPLACE FUNCTION {0}."calcMeanAnnualTotal"(_tbl integer, OUT result numeric)
            LANGUAGE plpgsql AS
        $func$
        BEGIN
            EXECUTE 'SELECT round(avg(stage)::numeric, 2) FROM {0}."'|| _tbl || 'abs"'
            INTO result;
        END
        $func$;

        CREATE OR REPLACE FUNCTION {0}."calcMeanAnnualIceFree"(_tbl integer, OUT result numeric)
            LANGUAGE plpgsql AS
        $func$
        BEGIN
            EXECUTE 'SELECT round(avg(stage)::numeric, 2) FROM {0}."'|| _tbl || 'abs" WHERE date_part(''month'', date) > 3 AND date_part(''month'', date) < 12'
            INTO result;
        END
        $func$;

        CREATE OR REPLACE FUNCTION {0}."calcMinStage"(IN tbl integer)
            RETURNS TABLE(date date, stage numeric)
            LANGUAGE 'plpgsql'
            VOLATILE
            PARALLEL UNSAFE
            COST 100    ROWS 1    
        AS $BODY$
                BEGIN
                    RETURN QUERY
                    EXECUTE
                    'SELECT date, stage FROM {0}."'||tbl||'abs" WHERE stage = (SELECT min(stage) FROM {0}."'||tbl||'abs") LIMIT 1'; 
                END;        
        $BODY$;

        CREATE OR REPLACE FUNCTION {0}."calcMaxStage"(IN tbl integer)
            RETURNS TABLE(date date, stage numeric)
            LANGUAGE 'plpgsql'
            VOLATILE
            PARALLEL UNSAFE
            COST 100    ROWS 1    
        AS $BODY$
                BEGIN
                    RETURN QUERY
                    EXECUTE
                    'SELECT date, stage FROM {0}."'||tbl||'abs" WHERE stage = (SELECT max(stage) FROM {0}."'||tbl||'abs") LIMIT 1'; 
                END;        
        $BODY$;
        """.format(schemaName)
    )
    print('--- Созданы функции ---')
    conn.commit()