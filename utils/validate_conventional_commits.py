import git

valid_commit_suffixes = ["feat", "fix", "chore", "docs", "style", "refactor", "perf", "test"]

repo = git.Repo(".")
branches = [repo.commit(repo.active_branch.name), repo.commit("main")]
mb = repo.git.merge_base(*branches)
commits = list(repo.iter_commits(f"{mb}..HEAD"))

for commit in commits:
    message = commit.message
    if message.split(":")[0] not in valid_commit_suffixes:
        raise ValueError(f"Commit  {commit} does not adhere to the conventional commit standard")
