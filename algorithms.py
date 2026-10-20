def single_validator(vote_valid): # algorithm 1
    accept = vote_valid[:, 0] # one validator per result
    return accept

def majority_vote(vote_valid): # algorithm 2
    k = vote_valid.shape[1] # num of validators per result

    n_valid = vote_valid.sum(axis=1) # each row checked for VALID
    n_invalid = k- n_valid
    accept = n_valid > n_invalid # odd k so no tie

    return accept

def weighted_vote(vote_valid,validator_rel ): # algorithm 3

    vote_invalid = 1 - vote_valid
    valid_weight = validator_rel * vote_valid # R where vote valid, else 0
    invalid_weight = validator_rel * vote_invalid

    s_valid = valid_weight.sum(axis=1)
    s_invalid = invalid_weight.sum(axis=1)

    accept = s_valid > s_invalid
    return accept