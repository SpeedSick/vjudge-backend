from __future__ import absolute_import
from celery import group, chain, shared_task
import core.settings
import os
from core.celery import app

DOCKERFILE_PATH = "docker_files/Dockerfile"
DOCKERCOMPOSE_PATH = "docker_files/docker-compose.yml"


class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


def stop_containers():
    os.system("sudo docker-compose down")


def start_containers():
    os.system("sudo docker-compose up --abort-on-container-exit")


def get_profile(cp):
    return cp.profile


def get_user_folder(cp):
    profile = cp.student
    git_username = profile.git_username
    user_folder = "{}/../../../repositories/{}".format(os.path.dirname(os.path.realpath(__file__)), git_username)
    return user_folder


def get_git_repository_name(cp):
    git_repository_name = cp.git_repository_name
    return git_repository_name

@app.task
def pull_or_clone(profile, user_folder, git_repository_name):
    git_link = "https://github.com/{}/{}.git".format(profile.git_username, git_repository_name)
    with cd(user_folder):
        pull_or_clone_command = "git -C {} pull || git clone {} {}".format(git_repository_name, git_link, git_repository_name)
        os.system(pull_or_clone_command)


@app.task
def check_submissions(submissions):
    for submission in submissions:
        task = submission.task
        task_name = task.folder_name
        testfile_path = core.settings.MEDIA_ROOT + task.testfile.name
        assignment_name = task.assignment.folder_name

        course_participant = submission.course_participant
        git_repository_name = course_participant.git_repository_name
        profile = course_participant.student
        git_username = profile.git_username

        user_folder = "{}/../../../repositories/{}".format(os.path.dirname(os.path.realpath(__file__)), git_username)
        task_folder = "{}/{}/src/{}/{}".format(user_folder, git_repository_name, assignment_name, task_name)
        with cd(task_folder):
            os.system("cp {} tests.yml".format(testfile_path))
            os.system("cp {} .".format(DOCKERCOMPOSE_PATH))
            os.system("cp {} .".format(DOCKERFILE_PATH))
            os.system("touch env.yml")
            with open("env.yml", "a") as f:
                f.write("submission_id: {}\n".format(submission.id))
                f.write("X_API_KEY: {}".format(core.settings.X_API_KEY))
            start_containers()

@app.task
def grade(course_participants, submissions):
    git_pull_group = group(pull_or_clone(get_profile(cp), get_user_folder(cp),\
                                         get_git_repository_name(cp)) for cp in course_participants)

    job = chain(git_pull_group.si(), check_submissions(submissions).si())
    job.apply_sync()


