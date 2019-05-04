import os, subprocess
import core.settings

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


# TODO: celery task
def pull_or_clone(profile, user_folder, git_repository_name):
	git_link = "https://github.com/{}/{}.git".format(profile.git_username, git_repository_name)
	with cd(user_folder):
		pull_or_clone = "git -C {} pull || git clone {} {}".format(git_repository_name, git_link, git_repository_name)
		os.system(pull_or_clone)

def stop_containers():
	os.system("sudo docker-compose down")

def start_containers():
	os.system("sudo docker-compose up --abort-on-container-exit")

def grade(course_participants, submissions):

	for cp in course_participants:
		profile = cp.student
		git_username = profile.git_username
		git_repository_name = cp.git_repository_name
		user_folder = "{}/../../../repositories/{}".format(os.path.dirname(os.path.realpath(__file__)), git_username)
		os.system("mkdir -p {}".format(user_folder))
		pull_or_clone(profile, user_folder, git_repository_name)

	for submission in submissions:
		submission_id = submission.id
		task = submission.task
		task_name = task.folder_name
		testfile = task.testfile
		testfile_path = core.settings.MEDIA_ROOT + testfile.name
		assignment = task.assignment
		assignment_name = assignment.folder_name

		course_participant = submission.course_participant
		git_repository_name = course_participant.git_repository_name
		profile = course_participant.student
		git_username = profile.git_username

		user_folder = "{}/../../../repositories/{}".format(os.path.dirname(os.path.realpath(__file__)), git_username)
		# os.system("mkdir -p {}".format(new_folder))
		# pull_or_clone(profile, new_folder, git_repository_name)

		tests_file = "{}/../../../repositories/{}/{}/{}/{}/tests.yml".format(os.path.dirname(os.path.realpath(__file__)), \
																git_username, git_repository_name, assignment_name, task_name)
		os.system("cp {} {}".format(testfile_path, tests_file))

		task_folder = "{}/{}/src/{}/{}".format(user_folder, git_repository_name, assignment_name, task_name)

		with cd(task_folder):
			os.system("cp {} .".format(DOCKERCOMPOSE_PATH))
			os.system("cp {} .".format(DOCKERFILE_PATH))
			os.system("touch env.yml")
			with open("env.yml", "a") as f:
				f.write("submission_id: {}\n".format(submission_id))
				f.write("X_API_KEY: {}".format(core.settings.X_API_KEY))
			start_containers()
			# stop_containers()


if __name__ == "__main__":
	pass
	# assignment_folder = "assignment_1"
	# task_folder = "task_1"
	#
	# git_username = "kenenalmat"
	# git_repository = "sim.git"
	# git_link = "https://github.com/{}/{}".format(git_username, git_repository)
	# new_folder = "{}/../../../repositories/{}".format(os.path.dirname(os.path.realpath(__file__)), git_username)
	# os.system("mkdir -p {}".format(new_folder))
	#
	# docker_compose_path = ""
	# dockerfile_path = ""
	#
