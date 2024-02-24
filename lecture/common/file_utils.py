import os

from lecture.common.pdf_utils import convert_to_pinyin, check_chinese


def get_exec_file_name():
    script_name = __file__
    absolute_path = os.path.abspath(script_name)
    return absolute_path


def get_directory_name(path):
    dir_name = os.path.basename(path)
    return dir_name


def get_system_data_directory():
    current_dir = os.getcwd()
    current_dir = current_dir[0:current_dir.rfind("\\Lecture") + len("Lecture") + 1]
    data_dir = os.path.join(current_dir, "lecture_data")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    return data_dir


def get_resource_folder(folder_type: str):
    current_dir = os.getcwd()
    current_dir = current_dir[0:current_dir.rfind("\\Lecture") + len("Lecture") + 1]
    resource_dir = os.path.join(current_dir, "resource")
    if not os.path.exists(resource_dir):
        os.makedirs(resource_dir)
    resource_folder_dir = os.path.join(resource_dir, folder_type)
    if not os.path.exists(resource_folder_dir):
        os.makedirs(resource_folder_dir)
    return resource_folder_dir


def get_lectures_directory():
    data_dir = get_system_data_directory()
    lectures_dir = os.path.join(data_dir, "lecture")
    if not os.path.exists(lectures_dir):
        os.makedirs(lectures_dir)
    return lectures_dir


def get_create_lecture_directory(lecture_name: str, lecture_id: str):
    lecture_name_pinyin = lecture_name
    if check_chinese(lecture_name):
        lecture_name_pinyin = convert_to_pinyin(lecture_name)
    lectures_dir = get_lectures_directory()
    lecture_name_dir = os.path.join(lectures_dir, lecture_name_pinyin)
    if not os.path.exists(lecture_name_dir):
        os.makedirs(lecture_name_dir)
    lecture_id_dir = os.path.join(lecture_name_dir, lecture_id)
    if not os.path.exists(lecture_id_dir):
        os.makedirs(lecture_id_dir)
    return lecture_id_dir


def check_lecture_path(lecture_name: str, lecture_id: str, file: str) -> str:
    lecture_directory = get_lectures_directory()
    if file.find(lecture_directory) == 0:
        return file
    else:
        return os.path.join(lecture_directory, lecture_name, lecture_id, file)


def add_filename_tail(file_path: str, tail: str) -> str:
    index_dot = file_path.rfind('.')
    return file_path[0:index_dot] + tail + file_path[index_dot:len(file_path)]
