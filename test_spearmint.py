def load_jobs(db, experiment_name):
    jobs = db.load(experiment_name, 'jobs')
    if jobs is None:
        jobs = []
    if isinstance(jobs, dict):
        jobs = [jobs]
    return jobs


from spearmint.utils.database.mongodb import MongoDB
db         = MongoDB(database_address="localhost")
experiment_name="simple-braninhoo-example"
jobs = load_jobs(db, experiment_name)
print jobs[0]
