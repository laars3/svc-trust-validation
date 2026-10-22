import numpy as np
import config, algorithms

def population_reliability(work_num, validator_num, env, rng): # reliability score randomly selected between bounds
    low, high = config.ENVIRONMENTS[env]
    worker_pool_rel = rng.uniform(low, high, size=work_num)
    validator_pool_rel = rng.uniform(low, high, size=validator_num)
    return worker_pool_rel, validator_pool_rel

def create_tasks(worker_pool_rel, rng): # tasks arriving at VCC
    mean= config.ARR_RATE_PM * 60 * config.SIM_HOURS
    task_num =rng.poisson(mean) # used to pick values around mean to model small change

    worker_i = rng.integers(0, len(worker_pool_rel), size=task_num) # controller sending task to rand worker
    task_worker_rel = worker_pool_rel[worker_i]
    random_num = rng.random(task_num)

    correct_worker = random_num < task_worker_rel

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

def validator_vote(correct_worker, task_validator_rel,rng): # sect 3, each validator makes correct call with prob R
    random_num = rng.random(task_validator_rel.shape)
    correct_call = random_num < task_validator_rel

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

def make_row(seed, work_num, validator_num, env, algorithm, k, correct_worker, accept): # result row for csv
    counts = outcome_counts(correct_worker, accept)

    row = {"seed": seed, "work_num": work_num, "validator_num": validator_num, "env":env, "algorithm": algorithm, "k":k}
    row.update(counts)

    row["Pd"]= probability_of_detection(counts)
    row["FAR"] = false_acceptance_rate(counts)
    row["FRR"] = false_rejection_rate(counts)

    return row

def simulate_run(work_num, validator_num, env, seed): # full simulation for one scenario
    rng = np.random.default_rng(seed) # random num with seed

    worker_pool_rel, validator_pool_rel = population_reliability(work_num, validator_num,env, rng)
    correct_worker= create_tasks(worker_pool_rel, rng)
    task_num = len(correct_worker)

    max_k = max(config.K_VALUES)
    validator_i = pick_validators(task_num,validator_num, max_k, rng)
    task_validator_rel = validator_pool_rel[validator_i]

    vote_valid = validator_vote(correct_worker, task_validator_rel, rng)

    rows =[]

    # algo 1 for k=1
    accept= algorithms.single_validator(vote_valid)
    rows.append(make_row(seed, work_num, validator_num, env, "single", 1, correct_worker, accept))

    # algo 2 and 3 for k>1 where k prime
    for k in config.K_VALUES:
        if k ==1:
            continue

        votes_k = vote_valid[:, :k]
        task_validator_rel_k = task_validator_rel[:, :k]

        accept= algorithms.majority_vote(votes_k)
        rows.append(make_row(seed, work_num, validator_num, env, "majority", k, correct_worker, accept))

        accept = algorithms.weighted_vote(votes_k, task_validator_rel_k)
        rows.append(make_row(seed, work_num, validator_num,env, "weighted", k, correct_worker, accept))

    return rows