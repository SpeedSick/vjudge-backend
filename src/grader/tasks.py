from __future__ import absolute_import
from celery import group, chain, shared_task
import core.settings
import os
from authentication.models import Profile
from core.celery import app
from main.models import CourseParticipant, Submission

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
    os.system("docker-compose down")


def start_containers():
    # os.system("docker network connect vjudge-backend_default vjudge-backend_django_1")
    # os.system("NETWORK=my-net docker-compose up --abort-on-container-exit")
    os.system("docker-compose up --build --abort-on-container-exit")


def get_profile_id(cp):
    return cp.student.profile.id


def get_user_folder(cp):
    user = cp.student
    git_username = user.profile.git_username
    user_folder = "{}/../repositories/{}".format(os.path.dirname(os.path.realpath(__file__)), git_username)
    return user_folder


def get_git_repository_name(cp):
    git_repository_name = cp.git_repository_name
    return git_repository_name


@app.task
def pull_or_clone(profile_id, user_folder, git_repository_name):

    profile = Profile.objects.get(id=profile_id)
    git_link = "https://github.com/{}/{}.git".format(profile.git_username, git_repository_name)

    print("Trying to create a folder: {}".format(user_folder))
    os.system("mkdir -p {}".format(user_folder))

    with cd(user_folder):
        pull_or_clone_command = "git -C {} pull || git clone {} {}".format(git_repository_name, git_link, git_repository_name)
        os.system(pull_or_clone_command)


@app.task
def check_submissions(self, submission_ids):
    print ("HERE ARE THE SUBMISSIONS")
    print (submission_ids)
    print ("DID YOU SEE???")

    submissions = []
    for id in submission_ids:
        s = Submission.objects.get(id=id)
        submissions.append(s)


    for submission in submissions:
        print ("Trying to check the submission {}".format(submission.id))
        task = submission.task
        task_name = task.folder_name
        testfile_path = core.settings.MEDIA_ROOT + "/" + task.testfile.name
        assignment_name = task.assignment.folder_name

        course_participant = submission.course_participant
        git_repository_name = course_participant.git_repository_name
        user = course_participant.student
        git_username = user.profile.git_username

        user_folder = "{}/../repositories/{}".format(os.path.dirname(os.path.realpath(__file__)), git_username)
        task_folder = "{}/{}/src/{}/{}".format(user_folder, git_repository_name, assignment_name, task_name)

        with cd(task_folder):
            dockercompose_path = os.path.dirname(os.path.realpath(__file__)) + "/" + DOCKERCOMPOSE_PATH
            dockerfile_path = os.path.dirname(os.path.realpath(__file__)) + "/" + DOCKERFILE_PATH
            req_file = "../../../requirements.txt"

            files = [f for f in os.listdir('.') if os.path.isfile(f)]
            for f in files:
                print ("FILE " + f)

            os.system("cp {} tests.yml".format(testfile_path))
            os.system("cp {} .".format(dockercompose_path))
            os.system("cp {} .".format(dockerfile_path))
            os.system("cp {} .".format(req_file))

            os.system("touch env.yml")
            with open("env.yml", "w") as f:
                f.write("submission: {}\n".format(submission.id))
                f.write("X_API_KEY: {}\n".format(core.settings.X_API_KEY))
                f.write("url: http://django:8000/api/submission_result/\n")
                f.write("TASK_URL: http://task:5000/\n")
            start_containers()


@app.task
def grade(course_participant_ids, submission_ids):

    course_participants = []
    for id in course_participant_ids:
        cp = CourseParticipant.objects.get(id=id)
        course_participants.append(cp)


    git_pull_group = group(pull_or_clone.s(get_profile_id(cp), get_user_folder(cp),\
                                         get_git_repository_name(cp)) for cp in course_participants)

    print ("TYPE OF SUBMISSION_IDS: {}".format(str(type(submission_ids))))

    job = chain(git_pull_group, check_submissions.s(submission_ids))
    job()

    # git_pull_group()
    # check_submissions.apply_async(kwargs={'submission_ids': submission_ids})
