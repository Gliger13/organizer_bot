import json
import os


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


def load_information():
    path = "case_information.json"
    current_data = {}
    with open(path, 'r') as file:
        if os.path.getsize(path) != 0:
            current_data.update(json.load(file))
        return current_data


def load_user_information(user_id):
    return load_information()[user_id]


def update_information(user_id, task_list):
    some_dict = {user_id: task_list}
    path = "case_information.json"
    data = load_information()
    data.update(some_dict)
    with open(path, 'w') as file:
        json.dump(data, file)
