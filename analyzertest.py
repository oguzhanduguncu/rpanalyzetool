import subprocess
import json
import os

def run(cmd, cwd=None):
    result = subprocess.run(
        cmd,
        shell=True,
        cwd=cwd,
        capture_output=True,
        text=True
    )
    return result.stdout.strip()


def is_git_repo(path):
    out = run("git rev-parse --is-inside-work-tree", cwd=path)
    return out == "true"

def total_commits(path):
    return int(run("git rev-list --all --count", cwd=path))

def commit_hashes(path):
    hashes = run("git log --pretty=format:%H", cwd=path)
    return hashes.splitlines()

def commits_by_date(path):
    out = run("git log --date=short --pretty=format:%ad", cwd=path)
    dates = out.splitlines()
    result = {}
    for d in dates:
        result[d] = result.get(d, 0) + 1
    return result


def top_changed_files(path):
    out = run("git log --name-only --pretty=format:", cwd=path)
    files = [f.strip() for f in out.splitlines() if f.strip()]
    stats = {}
    for f in files:
        stats[f] = stats.get(f, 0) + 1

    return dict(sorted(stats.items(), key=lambda x: x[1], reverse=True))

def extension_stats(path):
    out = run("git ls-files", cwd=path)
    files = out.splitlines()
    stats = {}
    for f in files:
        _, ext = os.path.splitext(f)
        if ext == "":
            ext = "<noext>"
        stats[ext] = stats.get(ext, 0) + 1
    return stats

def file_line_changes(path):
    out = run("git log --numstat", cwd=path)
    result = {}

    for line in out.splitlines():
        parts = line.split("\t")
        if len(parts) != 3:
            continue
        added, removed, fname = parts
        if fname not in result:
            result[fname] = {"added": 0, "removed": 0, "commits": 0}

        if added.isdigit():
            result[fname]["added"] += int(added)
        if removed.isdigit():
            result[fname]["removed"] += int(removed)

        result[fname]["commits"] += 1

    return dict(sorted(result.items(), key=lambda x: x[1]["added"] + x[1]["removed"], reverse=True))

def analyze_repo(path):
    if not is_git_repo(path):
        raise Exception("This is not a valid git repository!")

    return {
        "total_commits": total_commits(path),
        "commit_hashes": commit_hashes(path),
        "commits_by_date": commits_by_date(path),
        "top_changed_files": top_changed_files(path),
        "extension_stats": extension_stats(path),
        "file_line_changes": file_line_changes(path),
    }

repo = r"C:\Users\oguzh\PycharmProjects\gitanalyzer"  # add git repo to anaylze
print(repo)

result = analyze_repo(repo)

print(json.dumps(result, indent=2, ensure_ascii=False))
