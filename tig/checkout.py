import os
import subprocess
import sys

CMD = "git --no-pager log --oneline --decorate=full -1 --pretty='%D' --no-color"


def main():
    commit = sys.argv[1]
    checkout(commit)


def checkout(commit):
    os.system("git clean -f")
    os.system("git checkout -- .")
    branch = is_branch(commit)
    if is_branch(commit):
        os.system("git checkout " + branch)
    else:
        os.system("git checkout " + commit)


def is_branch(commit):
    output = subprocess.getoutput(CMD + " " + commit)
    res = None
    if "HEAD -> " in output:
        output = output.split("HEAD -> ")[1]
    output = output.split(",")

    for i in output:
        if "refs/heads/" in i:
            res = i.split("/")[2]
            break
    return res


if __name__ == "__main__":
    main()
