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
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS {0}."stageProb"
        (
            id serial NOT NULL,
            gauge uuid NOT NULL,
            source character varying(20),
            "1p" double precision,
            "3p" double precision,
            "5p" double precision,
            "10p" double precision,
            "25p" double precision,
            "50p" double precision,
            PRIMARY KEY (id),
            FOREIGN KEY (gauge)
                REFERENCES {0}.gauges (uuid) MATCH SIMPLE
                ON UPDATE NO ACTION
                ON DELETE NO ACTION
                NOT VALID
        );
        ALTER TABLE IF EXISTS {0}."stageProb" OWNER to postgres;
        )
        """
    )
    conn.commit()
    print('--- Созданы таблицы в БД ---')