import data_process


class Organizer:
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.task_list = data_process.load_user_information(user_id)

    def create_task(self, time: str, info: str):
        if time in self.task_list:
            self.task_list[time].append(info)
        else:
            self.task_list[time] = info
        data_process.update_information(self.user_id, self.task_list)

    def remove_task(self, time_index: int, task_index=None):
        time_index -= 1
        if len(self.task_list) < time_index:
            raise TypeError("The entered time is not in the task list")
        tasks = self.task_list[time_index]
        if len(tasks) == 1:  # If on one time only one task
            self.task_list.pop(time_index)
        elif task_index:  # If many tasks on one time remove user choice task
            self.task_list[time_index].pop(task_index)
        else:
            raise TypeError("The entered time is not in the task list")
        data_process.update_information(self.user_id, self.task_list)

    def show_tasks(self) -> str:
        result_str = "Ваши дела:\n"
        for index, element in enumerate(self.task_list):
            time, tasks = self.task_list.items()
            result_str += f"{index}) {time}: \n"
            for task in tasks:
                result_str += f"{task}" if len(task) < 25 else f"{task[25]}\n"
        return result_str

    def show_task(self, time_index: int) -> str:
        time, tasks = self.task_list[time_index].items()
        result_str = f"Ваши дела на {time}:\n"
        for index, task in enumerate(tasks):
            result_str += f"{index}) {task}\n"
        return result_str

