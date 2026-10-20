import numpy as np
import config

def population_reliability(work_num, validator_num, env, rng): # reliability score randomly selected between bounds
    low, high = config.ENVIRONMENTS[env]
    r_workers = rng.uniform(low, high, size=work_num)
    r_validators = rng.uniform(low, high, size=validator_num)
    return r_workers, r_validators

def create_tasks(r_workers, rng): # 24 hr tasks and check for worker result
    mean= config.ARR_RATE_PM * 60 * config.SIM_HOURS
    task_num =rng.poisson(mean) # used to pick values around mean to model small change

    worker_i = rng.integers(0, len(r_workers), size=task_num)
    task_rel = r_workers[worker_i]
    random_num = rng.random(task_num)

    correct_worker = random_num < task_rel

    return correct_worker

def has_dup(rows): # helper func to check if duplicates in chosen k validators
    sorted_rows= np.sort(rows, axis=1)
    left = sorted_rows[:, :-1]
    right = sorted_rows[:, 1:]
    same = left == right
    dup = same.any(axis=1)
    return dup

def pick_validators(task_num, validator_num, k, rng): # k validators per task
    validator_i = rng.integers(0, validator_num, size=(task_num, k))

    dup = has_dup(validator_i)
    redraw_i = np.flatnonzero(dup)

    while redraw_i.size > 0:
        new_rows = rng.integers(0, redraw_i.size, size=(redraw_i, k))
        validator_i[redraw_i] = new_rows

        dup = has_dup(validator_i[redraw_i])
        redraw_i = redraw_i[dup]

    return validator_i
