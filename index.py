from config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_SCHEMA, \
    DB_USER, CSV_DIRECTORY, STATIC_DATA
from connection import connectToDB
from createPgSchema import createPgSchema
from getGaugeCodes import getGaugeCodes
from createPgTables import createPgTables
from fillStaticPgTables import fillStaticPgTables
from createFunctions import createFunctions
from getTable import getTable
from fillPgTables import fillPgTables
from createViews import createViews
from createIndexes import createIndexes
from calcStatistics import calcMeanAnnuals

(connection, cursor) = connectToDB(
    DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)

createPgSchema(connection, cursor, DB_SCHEMA)

gaugeCodes = getGaugeCodes(STATIC_DATA)

createPgTables(connection, cursor, DB_SCHEMA, gaugeCodes)

createFunctions(connection, cursor, DB_SCHEMA)

fillStaticPgTables(connection, cursor, DB_SCHEMA, STATIC_DATA)

legend = getTable(cursor, DB_SCHEMA, 'legend')
gauges = getTable(cursor, DB_SCHEMA, 'gauges')

fillPgTables(connection, cursor, DB_SCHEMA, CSV_DIRECTORY, legend)

createViews(connection, cursor, DB_SCHEMA, gauges)

createIndexes(connection, cursor, DB_SCHEMA, gauges)

calcMeanAnnuals(connection, cursor, DB_SCHEMA, gauges)
