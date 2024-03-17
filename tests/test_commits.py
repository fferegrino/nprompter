import git

def test_commit():
    repo = git.Repo(".")
    branches = [repo.commit(repo.active_branch.name), repo.commit("main")]
    mb =  repo.git.merge_base(*branches)
    commits = list(repo.iter_commits(f'{mb}..HEAD'))
    breakpoint()
    pass