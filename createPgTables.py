def createPgTables(conn, cursor, schemaName, gaugeCodesArray):
    """
    Создает таблицы в схеме
    """
    for code in gaugeCodesArray:
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS {0}."{1}" ( \
                id bigserial NOT NULL, \
                date date NOT NULL, \
                value integer, \
                props uuid[], \
                PRIMARY KEY (id) \
            ); \
            ALTER TABLE IF EXISTS {0}."{1}" OWNER to postgres; \
            '.format(schemaName, code)
        )
    cursor.execute(
        """
        CREATE TABLE {0}."meanAnnuals"
        (
            id serial NOT NULL,
            gauge uuid NOT NULL,
            "allPeriod" double precision,
            "iceFree" double precision,
            PRIMARY KEY (id),
            FOREIGN KEY (gauge)
                REFERENCES {0}.gauges (uuid) MATCH SIMPLE
                ON UPDATE NO ACTION
                ON DELETE NO ACTION
                NOT VALID
        );
        ALTER TABLE IF EXISTS {0}."meanAnnuals" OWNER to postgres;
        """.format(schemaName)
    )
    conn.commit()
    print('--- Созданы таблицы в БД ---')