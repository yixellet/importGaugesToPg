def buildLegendUidString(legend, symbolsString, gauge, year, date):
    """
    Создает строковое представление списка uid'ов 
    на основе строки с условными знаками
    """

    log = open('log.txt', 'a')

    legSymbols = []
    for sym in legend:
        legSymbols.append(sym[2])

    if len(symbolsString) != 0:
        symbolUidStr = '{'
        for symbol in symbolsString:
            try:
                if symbol == 'H':
                    symbolIdx = legSymbols.index('Н')
                elif symbol == 'Ч' or symbol == 'X' or symbol == 'х' or symbol == 'x':
                    symbolIdx = legSymbols.index('Х')
                elif symbol == 'K':
                    symbolIdx = legSymbols.index('К')
                elif symbol == 'C':
                    symbolIdx = legSymbols.index('С')
                else:
                    symbolIdx = legSymbols.index(symbol)
            except ValueError:
                log.write(symbolsString + '          ' + gauge + '   ' + year + '   ' + date + '      ' + '\n')
            else:
                symbolUidStr = symbolUidStr + legend[symbolIdx][1] + ','
        symbolUidStr = symbolUidStr[:-1] + '}'
        log.close()
        return symbolUidStr
    else:
        return "{}"