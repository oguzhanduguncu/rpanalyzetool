import subprocess


subprocess.run(["cmd", "/c", "dir"])

subprocess.run("git --version", shell=True)

subprocess.run("git rev-parse --is-inside-work-tree", shell=True)

subprocess.run("git log --pretty=format:%H", shell=True)



