from datetime import timedelta, date
import re
import random

id_code_list = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
check_code_list = [1, 0, 'X', 9, 8, 7, 6, 5, 4, 3, 2]


def gen_id_card(area_code, age, gender):
    # if str(area_code) not in area_dict.keys():
    #     return None
    datestring = str(date(date.today().year - int(age), 1, 1) + timedelta(days=random.randint(0, 364))).replace("-", "")
    rd = random.randint(0, 999)
    if gender == 0:
        gender_num = rd if rd % 2 == 0 else rd + 1
    else:
        gender_num = rd if rd % 2 == 1 else rd - 1
    result = str(area_code) + datestring + str(gender_num).zfill(3)
    return result + str(check_code_list[sum([a * b for a, b in zip(id_code_list, [int(a) for a in result])]) % 11])