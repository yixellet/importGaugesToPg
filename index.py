from config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_SCHEMA, \
    DB_USER, CSV_DIRECTORY
from connection import connectToDB
from createPgSchema import createPgSchema
from getGaugeCodes import getGaugeCodes
from createPgTables import createPgTables
from createFunctions import createFunctions
from getLegend import getLegend
from fillPgTables import fillPgTables
from getGauges import getGauges
from createMatViews import createMatViews
from createIndexes import createIndexes
from calcStatistics import calcMeanAnnuals

(connection, cursor) = connectToDB(
    DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)

createPgSchema(connection, cursor, DB_SCHEMA)

gaugeCodes = getGaugeCodes(CSV_DIRECTORY)

createPgTables(connection, cursor, DB_SCHEMA, gaugeCodes)

createFunctions(connection, cursor)

legend = getLegend(cursor, DB_SCHEMA, 'legend')

fillPgTables(connection, cursor, DB_SCHEMA, CSV_DIRECTORY, legend)

gauges = getGauges(cursor, DB_SCHEMA)

createMatViews(connection, cursor, DB_SCHEMA, gauges)

#createIndexes(connection, cursor, DB_SCHEMA, gauges)

calcMeanAnnuals(connection, cursor, DB_SCHEMA, gauges)
