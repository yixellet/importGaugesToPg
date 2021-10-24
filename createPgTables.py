def createPgTables(conn, cursor, schemaName, gaugeCodesArray):
    """
    Создает таблицы в схеме
    """

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS {0}.gauges
        (
            uuid uuid NOT NULL,
            geom geometry NOT NULL,
            code integer,
            name character varying(50),
            river character varying(50),
            PRIMARY KEY (uuid)
        );
        ALTER TABLE IF EXISTS {0}.gauges OWNER to postgres;

        CREATE TABLE IF NOT EXISTS {0}.legend
        (
            uuid uuid NOT NULL,
            symbol character varying(4),
            description character varying(100),
            PRIMARY KEY (uuid)
        );
        ALTER TABLE IF EXISTS {0}.legend OWNER to postgres;

        CREATE TABLE IF NOT EXISTS {0}."ref_elevations"
        (
            id serial NOT NULL,
            gauge uuid NOT NULL,
            elev double precision,
            "startDate" date,
            "endDate" date,
            PRIMARY KEY (id),
            FOREIGN KEY (gauge)
                REFERENCES {0}.gauges (uuid) MATCH SIMPLE
                ON UPDATE NO ACTION
                ON DELETE NO ACTION
                NOT VALID
        );
        ALTER TABLE IF EXISTS {0}."ref_elevations" OWNER to postgres;
        """.format(schemaName)
    )
    for code in gaugeCodesArray:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS {0}."v{1}"
            (
                id bigserial NOT NULL,
                date timestamp with time zone NOT NULL,
                value integer,
                props uuid[],
                PRIMARY KEY (id)
            );
            ALTER TABLE IF EXISTS {0}."v{1}" OWNER to postgres;
            """.format(schemaName, code)
        )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS {0}."meanAnnualsGms"
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
        ALTER TABLE IF EXISTS {0}."meanAnnualsGms" OWNER to postgres;
        
        CREATE TABLE IF NOT EXISTS {0}."maxStageProbGms"
        (
            id serial NOT NULL,
            gauge uuid NOT NULL,
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
        ALTER TABLE IF EXISTS {0}."maxStageProbGms" OWNER to postgres;
        """.format(schemaName)
    )
    conn.commit()
    print('--- Созданы таблицы в БД ---')