from climate import repo

def initialise_db():
    repo.RepoContext().configure()
    repo.init()
