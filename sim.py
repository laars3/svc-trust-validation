import numpy as np
import config

def population_reliability(n_workers, n_validators, env, rng): # reliability score randomly selected between bounds
    low, high = config.ENVIRONMENTS[env]
    r_workers = rng.uniform(low, high, size=n_workers)
    r_validators = rng.uniform(low, high, size=n_validators)
    return r_workers, r_validators

