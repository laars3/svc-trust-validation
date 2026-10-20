N_VEHICLES = 500
SCENARIOS = ((400,100), (300, 200), (200, 300)) # (worker node, validator node)
ENVIRONMENTS = {"Trusted": (0.9, 1.0), "Semi-Trusted": (0.7, 0.9),"Untrusted": (0.5, 0.7)} # trust envs low:high
K_VALUES = [1,3,5,7] # num of validators assigned to one worker result
SIM_HOURS = 24
N_SEEDS = 1000