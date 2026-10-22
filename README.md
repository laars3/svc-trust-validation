## Static Vehicular Cloud Trust Validation

Task simulation, monte carlo in python/numpy.

Files
- config.py: all the parameters
- sim.py: reliabilities, tasks, picking validators, votes, PD/FAR/FRR
- algorithms.py: single validator, majority, weighted
- run_experiments.py: runs every config and saves results/experiments.csv
- analysis.ipynb: graphs 1,2,3

running
1) python run_experiments.py
2) run analysis.ipynb

assumptions
- arrival rate is set to 300 tasks/min, poisson, so about 432k tasks per 24h. each task goes to a random worker, assigned by vccontroller
- a validator's R is the same for correct and incorrect results
- votes are drawn once at k=7 and smaller k use the first k, so all algorithms see same votes
- 1000 seeds per config

results
- PD goes up with k. check analysis for exact results.
- Nv doesn't change PD, each result only sees k random validators from the same range
- weighted is the same as majority except at k=7 untrusted. see analysis.
- FAR = 1 - PD, FRR is about the same as FAR
