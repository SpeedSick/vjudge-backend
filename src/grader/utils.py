import os, subprocess


class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


def clone(profiles):
	for p in profiles:
		pass

if __name__ == "__main__":
	assignment_folder = "assignment_1"
	task_folder = "task_1"

	git_username = "kenenalmat"
	git_repository = "sim.git"
	git_link = "https://github.com/{}/{}".format(git_username, git_repository)
	new_folder = "{}/../../repositories/{}".format(os.path.dirname(os.path.realpath(__file__)), git_username)
	os.system("mkdir -p {}".format(new_folder))

	docker_compose_path = ""
	dockerfile_path = ""

	with cd(new_folder):
		pull_or_clone = "git -C repo pull || git clone {} repo".format(git_link)
		os.system(pull_or_clone)
		os.system()

		# To put them into $assignment/$task folder
		# os.system("cp {} .".format(docker_compose_path))
		# os.system("cp {} .".format(dockerfile_path))
		
		# Where do we specify the assignment, task and tests?
		# TODO: docker build, up stuff here.
		# maybe it should be subprocess call, because we do not want to wait for it.
		# I put 
		# Possibly will create a celery function and create submission in it.
		