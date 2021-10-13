def buildLegendUidString(legend, symbolsString, gauge, year, date, log):
    """
    Создает строковое представление списка uid'ов 
    на основе строки с условными знаками
    """

    legSymbols = []
    for sym in legend:
        legSymbols.append(sym[2])

    if len(symbolsString) != 0:
        symbolUidStr = '{'
        for symbol in symbolsString:
            try:
                if symbol == 'H':
                    symbolIdx = legSymbols.index('Н')
                elif symbol == 'Ч' or symbol == 'X' or symbol == 'x' or symbol == 'х':
                    symbolIdx = legSymbols.index('Х')
                elif symbol == 'C' or symbol == 'с' or symbol == 'c':
                    symbolIdx = legSymbols.index('С')
                elif symbol == 'K' or symbol == 'k' or symbol == 'к':
                    symbolIdx = legSymbols.index('К')
                else:
                    symbolIdx = legSymbols.index(symbol)
            except ValueError:
                log.write(symbolsString + '          ' + gauge + '   ' + year + '   ' + date + '      ' + '\n')
            else:
                symbolUidStr = symbolUidStr + legend[symbolIdx][1] + ','
        symbolUidStr = symbolUidStr[:-1] + '}'
        return symbolUidStr
    else:
        return "{}"