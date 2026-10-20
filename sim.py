import numpy as np
import config

def population_reliability(work_num, validator_num, env, rng): # reliability score randomly selected between bounds
    low, high = config.ENVIRONMENTS[env]
    r_workers = rng.uniform(low, high, size=work_num)
    r_validators = rng.uniform(low, high, size=validator_num)
    return r_workers, r_validators

def create_tasks(r_workers, rng):
    mean= config.ARR_RATE_PM * 60 * config.SIM_HOURS
    task_num =rng.poisson(mean) # used to pick values around mean to model small change

    worker_i = rng.integers(0, len(r_workers), size=task_num)

    task_rel = r_workers[worker_i]

    random_num = rng.random(task_num)

    correct_worker = random_num < task_rel

    return correct_worker

def pick_validators(task_num, val_num, k, rng):
