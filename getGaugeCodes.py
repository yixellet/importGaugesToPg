import os

def getGaugeCodes(directory):
    """
    Получает список кодов гидропостов на основании
    каталогов, содержащихся в директории.
    Предполагается, что имя каталога строится по шаблону 'код_Название'.
    В директории не должно быть ничего кроме каталогов с наблюдениями.
    """
    gaugeCodesArray = []

    with open(os.path.join(directory, 'gauges.csv'), 'r', encoding='utf-8') as data:
        dataArr = data.read().splitlines()
        for line in dataArr:
            lineArr = line.split(',')
            gaugeCodesArray.append(lineArr[1])
    
    print('--- Сформирован перечень кодов гидропостов ---')
    return gaugeCodesArray
