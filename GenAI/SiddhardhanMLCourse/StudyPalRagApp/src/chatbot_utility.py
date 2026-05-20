import os

working_dir = os.path.dirname(os.path.abspath(__file__)) # "/Users/shashank/project/app"
parent_dir = os.path.dirname(working_dir) # "/Users/shashank/project"


def get_chapter_list(selected_subject):

    if selected_subject == "Science":
        subject_name = selected_subject.lower()
        chapters_dir = f"{parent_dir}/data/Class_8/{subject_name}"
        chapters_list = os.listdir(chapters_dir)
        chapters_list = [x[:-4] for x in chapters_list]
        chapters_list.sort(key=lambda x : int(x.split(".")[0]))
        return chapters_list

# chapters_list = get_chapter_list("Science")
# print(chapters_list)