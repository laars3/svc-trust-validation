import pandas as pd, config, sim

all_rows=[]

for work_num, validator_num in config.SCENARIOS: # runs every scenario and every seed
    for env in config.ENVIRONMENTS:
        for i in range(config.N_SEEDS):
            seed = config.SEED + i

            rows = sim.simulate_run(work_num, validator_num, env, seed)
            all_rows.extend(rows)

df = pd.DataFrame(all_rows)
df.to_csv("results/experiments.csv", index=False)