import os

def fillStaticPgTables(conn, cursor, schemaName, statDataDir):
    """
    Заполняет таблицы gauges, legend и ref_elevations
    """
    
    with open(os.path.join(statDataDir, 'gauges.csv'), 'r', encoding='utf-8') as data:
        dataArr = data.read().splitlines()
        for line in dataArr:
            fields = line.split(',')
            cursor.execute(
                """
                INSERT INTO {0}.gauges (geom, code, name, river, uuid) VALUES ('{1}','{2}','{3}','{4}',uuid_generate_v1());
                """.format(schemaName, fields[0], fields[1], fields[2], fields[3])
        )
    
    with open(os.path.join(statDataDir, 'legend.csv'), 'r', encoding='utf-8') as data:
        dataArr = data.read().splitlines()
        for line in dataArr:
            fields = line.split(',')
            cursor.execute(
                """INSERT INTO {0}.legend (uuid, symbol, description) VALUES (uuid_generate_v1(),'{1}','{2}');
                """.format(schemaName, fields[0], fields[1])
        )
    
    with open(os.path.join(statDataDir, 'refElevs.csv'), 'r', encoding='utf-8') as data:
        dataArr = data.read().splitlines()
        for line in dataArr:
            fields = line.split(',')
            cursor.execute(
                """
                INSERT INTO {0}."ref_elevations" (gauge, elev, "startDate", "endDate") VALUES 
                (
                    (SELECT uuid FROM {0}.gauges WHERE "name" = {1}),
                    {2},{3},{4}
                );
                """.format(schemaName, fields[0], fields[1], fields[2], fields[3])
        )
    
    with open(os.path.join(statDataDir, 'maxStageProbGms.csv'), 'r', encoding='utf-8') as data:
        dataArr = data.read().splitlines()
        for line in dataArr:
            fields = line.split(',')
            cursor.execute(
                """
                INSERT INTO {0}."maxStageProbGms" (gauge, "1p", "3p", "5p", "10p", "25p", "50p") VALUES 
                (
                    (SELECT uuid FROM {0}.gauges WHERE "name" = {1}),
                    {2},{3},{4},{5},{6},{7}
                );
                """.format(schemaName, fields[0], fields[1], fields[2], fields[3], fields[4], fields[5], fields[6])
        )
    
    with open(os.path.join(statDataDir, 'meanAnnualsGms.csv'), 'r', encoding='utf-8') as data:
        dataArr = data.read().splitlines()
        for line in dataArr:
            fields = line.split(',')
            cursor.execute(
                """
                INSERT INTO {0}."meanAnnualsGms" (gauge, "allPeriod", "iceFree") VALUES 
                (
                    (SELECT uuid FROM {0}.gauges WHERE "name" = {1}),
                    {2},{3}
                );
                """.format(schemaName, fields[0], fields[1], fields[2])
        )
    conn.commit()