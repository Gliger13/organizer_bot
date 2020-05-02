import json
import os
import os.path


# user_id = 123123412311
# time = "23.02.2020 13:00"
# text = "
#        Впервые термин «вики» для описания веб-сайта был использован в 1995 году Уордом Каннингемом,
#        разработчиком первой вики-системы WikiWikiWeb, «Портлендского хранилища образцов» программного кода[2],
#        созданной 25 марта 1995 года, который заимствовал слово гавайского языка, означающее «быстрый»[3][4].
#        Каннингем объяснил выбор названия движка тем, что он вспомнил работника международного аэропорта Гонолулу
#        "
#
# dict = {user_id1: [
#                    {time1: [text1, text2]},
#                    {time2: [text1, text2]},
#                    {time3: [text4]}
#                   ],
#         user_id2: [
#                    {time1: [text1, text2]},
#                    {time2: [text1, text2]},
#                    {time3: [text4]}
#                   ]
#         }
#

def load_information():
    path = "case_information.json"
    current_data = {}
    with open(path, 'r') as file:
        if os.path.getsize(path) != 0:
            current_data.update(json.load(file))
        return current_data


def load_user_information(id_user):
    return load_information()[str(id_user)]


def update_information(user_id, task_list):
    some_dict = {user_id: task_list}
    path = "case_information.json"
    data = load_information()
    if data and user_id in data:
        data.pop(str(user_id))
    data.update(some_dict)
    with open(path, 'w') as file:
        json.dump(data, file)