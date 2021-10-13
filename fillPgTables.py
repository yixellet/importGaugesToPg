import os
import psycopg2
from buildLegendUidString import buildLegendUidString

def fillPgTables(conn, cursor, schemaName, directory, legend):
    """
    Заполняет таблицы в БД данными из CSV-файлов
    """

    log = open('log.txt', 'a')

    for gaugeDirName in os.listdir(directory):
        code = gaugeDirName.split('_')[0]
        gaugeDir = os.path.join(directory, gaugeDirName)
        for file in os.listdir(gaugeDir):
            with open(os.path.join(gaugeDir, file), 'r', encoding='utf-8') as data:
                try:
                    dataArr = data.read().splitlines()
                    for line in dataArr:
                        lineArr = line.split(',')
                        try:
                            if len(lineArr[0]) != 0 and len(lineArr[1]) != 0:
                                if lineArr[0].find('1900') != -1:
                                    print(code + '  ' + file + '    1900')
                                if len(lineArr) == 3:
                                    legUidStr = buildLegendUidString(legend, lineArr[2], code, file, lineArr[0], log)
                                else:
                                    legUidStr = '{}'
                                try:
                                    cursor.execute('INSERT INTO {0}."{1}" (date, value, props) VALUES (\'{2}\', {3}, \'{4}\') ON CONFLICT DO NOTHING;' \
                                        .format(schemaName, code, lineArr[0].replace('"', ''), lineArr[1].replace('"', ''), legUidStr))
                                except:
                                    log.write('SyntaxError -> ' + code + '   ' + file + ' ' + line + '\n')
                        except IndexError:
                            log.write('IndexError -> ' + code + '   ' + file + '\n')
                except UnicodeDecodeError:
                    log.write('НЕВЕРНАЯ КОДИРОВКА -> '+ code + ' ' + file + '\n')

    log.close()
    conn.commit()
    print('--- Таблицы заполнены ---')
                    