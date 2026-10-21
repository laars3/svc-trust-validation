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

    # redraw rows if repeat, since k is small compared to pool it's fine
    while redraw_i.size > 0:
        new_rows = rng.integers(0, validator_num, size=(redraw_i.size, k))
        validator_i[redraw_i] = new_rows

        dup = has_dup(validator_i[redraw_i])
        redraw_i = redraw_i[dup]

    return validator_i

def validator_vote(correct_worker, validator_rel,rng): # sect 3, each validator makes correct call with prob R
    random_num = rng.random(validator_rel.shape)
    correct_call = random_num < validator_rel

    worker_correct_column = correct_worker[:, None]

    vote_valid = correct_call == worker_correct_column

    return vote_valid

def outcome_counts(correct_worker, accept): # worker result outcomes

    wrong_worker = 1-correct_worker
    rejected = 1-accept

    detected = wrong_worker * rejected
    undetected = wrong_worker * accept

    correct_accept = correct_worker * accept
    correct_reject = correct_worker * rejected

    # classify events
    counts = {"detected_fail": int(detected.sum()), "undetected_fail": int(undetected.sum()), "true_accept": int(correct_accept.sum()), "false_reject":int(correct_reject.sum())}

    return counts

def probability_of_detection(counts): # section 11
    incorrect_total = counts["detected_fail"] + counts["undetected_fail"]

    Pd = counts["detected_fail"] / incorrect_total
    return Pd

def false_acceptance_rate(counts): # section 13
    incorrect_total = counts["detected_fail"] + counts["undetected_fail"]

    FAR = counts["undetected_fail"] /incorrect_total

    return FAR

def false_rejection_rate(counts): #section 14
    correct_total = counts["true_accept"] + counts["false_reject"]

    FRR = counts["false_reject"]/ correct_total

    return FRR
