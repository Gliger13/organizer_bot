import data_process


class Organizer:
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.task_list = data_process.load_user_information(user_id)

    def create_task(self, time: str, info: str):
        if time in self.task_list:
            self.task_list[time].append(info)
        else:
            self.task_list.append({time: info})
        data_process.update_information(self.user_id, self.task_list)

    def remove_task(self, time_index: int):
        if len(self.task_list) < time_index:
            raise TypeError("The entered time is not in the task list")
        tasks = self.task_list[time_index]
        if len(tasks) == 1:  # If on one time only one task
            self.task_list.pop(time_index)
        else:
            raise TypeError("The entered time is not in the task list")
        data_process.update_information(self.user_id, self.task_list)

    def show_tasks(self) -> str:
        result_str = "Ваши дела:\n"
        for index, element in enumerate(self.task_list):
            time, tasks = list(*element.items())
            result_str += f"{index}) {time}: \n {tasks}\n"
        return result_str


