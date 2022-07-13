import requests
from bs4 import BeautifulSoup
import json
from prettytable import PrettyTable

def get_bs(filter):
    session_id = '...'
    component_id = '...'
    cookie = '...'
    url = 'https://pk.mipt.ru/bachelor/competition-list/?ajax=Y&action=_getNameListHtml&filter%5BphdLevelId%5D=' + str(filter[0]) + \
        '&filter%5Bseason%5D=' + str(filter[1]) + \
        '&filter%5Blevel%5D=' + str(filter[2]) + \
        '&filter%5Bcondition%5D=' + str(filter[3]) + \
        '&filter%5Bspeciality%5D=' + str(filter[4][0]) + \
        '&filter%5Bcompetitive%5D=' + str(filter[5][0]) + \
        '&filter%5Bform%5D=' + str(filter[6][0]) + \
        '&filter%5Boriginal%5D=' + str(filter[7]) + \
        '&filter%5Bagreement%5D=' + str(filter[8]) + \
        '&filter%5Bapp_date_from%5D=' + str(filter[9]) + \
        '&filter%5Bapp_date_to%5D=' + str(filter[10]) + \
        '&filter%5Benrolled%5D=' + str(filter[11]) + \
        '&filter%5Ball_priorities%5D=' + str(filter[12]) + \
        '&filter%5Bsupervisor%5D=' + str(filter[13]) + \
        '&filter%5Bprogram%5D=' + str(filter[14]) + \
        '&sessid=' + session_id + \
        '&component_id=' + component_id

    HEADERS = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Cookie': cookie,
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Origin': 'https://pk.mipt.ru',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Content-Length': '0'
    }

    r = requests.post(url, headers = HEADERS)
    j = json.loads(r.text)
    if 'html' in j:
        print('OK')
        return BeautifulSoup(j['html'], features="html.parser")
    else:
        print('ERROR')
        return False

def get_list(bs):
    return bs.find_all('tr', {'class': 'entrant entrant-success'})

def collect_db(db, el_list, filter):
    num = int(el_list.find('td', {'title': '№'}).get_text())
    priority = int(el_list.find('td', {'title': 'Приоритет заявления'}).get_text())
    stud_id = el_list.find('td', {'class': 'text-center'}).get_text().strip()

    bvi = el_list.find('td', {'class': 'bvi'})
    if bvi is None:
        score = 0
        s1 = el_list.find('td', {'class': 'sum'}).get_text().strip()
        s2 = el_list.find('td', {'class': 'achievements'}).get_text().strip()
        if s1.isdigit():
            score += int(s1)
        if s2.isdigit():
            score += int(s2)
    else:
        score = 310

    if stud_id not in db:
        db[stud_id] = [[filter[5][1], priority, score, num]]
    else:
        db[stud_id].append([filter[5][1], priority, score, num])

    return db

def equal_mas(m1, m2):
    for i in range(len(m1)):
        if type(m1[i]) == "<class 'list'>":
            if not equal_mas(m1[i], m2[i]):
                return False
        elif m1[i] != m2[i]:
            return False
    return True

filter_all = [
    3,
    11,
    1,
    [[1, 'ОК'], [2, 'БВИ']],
    [[1, 'ПМИ', [423, 424]], [2, 'ПМФ', [428, 430, 434, 435, 437, 440, 443, 445, 686]], [3, 'ИВТ', [446, 448, 610, 687]], [4, 'ТехнФиз', [450]], [5, 'БТ', [453, 689]], [6, 'САУ', [456, 688]], [7, 'КБ', [457]], [29, 'ЭлИНаноэл', [618]]],
    [[423, 'ПМИ'], [424, 'ERP'], [428, 'РТ'], [430, 'ЛФИ'], [434, 'ФАКТ АвиаТехн'], [435, 'ФАКТ ГНиТ'], [437, 'ФЭФМ ФизПерспТехн'], [440, 'ФПМИ ПМФ'], [443, 'ФБМФ'], [445, 'ИНБИКСТ'], [686, 'ФБВТ ПМФ'], [446, 'ФАКТ КомпМодел'], [448, 'ФПМИ СисПрог'], [610, 'ФПМИ ПМиКТ'], [687, 'ВШПИ'], [618, 'ФЭФМ'], [450, 'ФАКТ ТехнФиз'], [453, 'ФБМФ'], [689, 'ФБВТ БТ'], [456, 'ФАКТ САУ'], [688, 'ФБВТ САУ'], [457, 'ФРКТ КБ']],
    [[1, 'Контракт'], [2, 'Бюджет']],
    '',
    'false',
    '',
    '',
    '',
    'true',
    '',
    ''
]

filter_my = [
    filter_all[0], filter_all[1], filter_all[2], filter_all[3][0][0],
    filter_all[4][0], filter_all[5][0], filter_all[6][1],
    filter_all[7],filter_all[8],filter_all[9],filter_all[10],
    filter_all[11],filter_all[12],filter_all[13],filter_all[14]
]

db = dict()
db_my = dict()
for k1 in filter_all[4]:
    for k2 in filter_all[5]:
        if k2[0] in k1[2]:
            if k2[0] == 687:
                form = filter_all[6][0]
            else:
                form = filter_all[6][1]

            f = [filter_all[0], filter_all[1], filter_all[2], filter_all[3][0][0],
                 k1, k2, form,
                 filter_all[7],filter_all[8],filter_all[9],filter_all[10],
                 filter_all[11],filter_all[12],filter_all[13],filter_all[14]]

            list_of_k = get_list(get_bs(f))
            if len(list_of_k) > 0:
                for el in list_of_k:
                    db = collect_db(db, el, f)

            if equal_mas(f, filter_my):
                if len(list_of_k) > 0:
                    for el in list_of_k:
                        db_my = collect_db(db_my, el, f)


head_table = ['Код', 'Программа', 'Приоритет', 'Балл', 'Место в списке']
table = PrettyTable(head_table)
for el in db_my:
    el_now = db[el]
    flag_first = True
    for each_el_now in el_now:
        if flag_first:
            row = [el] + each_el_now
            flag_first = False
        else:
            row = [''] + each_el_now
        table.add_row(row)

print(table)
