import os

def getGaugeCodes(directory):
    """
    Получает список кодов гидропостов на основании
    каталогов, содержащихся в директории.
    Предполагается, что имя каталога строится по шаблону 'код_Название'.
    В директории не должно быть ничего кроме каталогов с наблюдениями.
    """
    gaugeCodesArray = []
    print('--- Будут импортированы следующие гидропосты:')

    for folderName in os.listdir(directory):
        gaugeName = folderName.split('_')
        print('{code} - {name}'.
            format(code=gaugeName[0], 
                name=gaugeName[1]+' '+gaugeName[2] if len(gaugeName) == 3 else gaugeName[1]
            )
        )
        gaugeCodesArray.append(gaugeName[0])
    
    print('--- Сформирован перечень кодов гидропостов ---')
    return gaugeCodesArray
