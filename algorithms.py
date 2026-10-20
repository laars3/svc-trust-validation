def single_validator(vote_valid): # algorithm 1
    accept = vote_valid[:, 0] # one validator per result
    return accept

def majority_vote(vote_valid): # algorithm 2
    k = vote_valid.shape[1] # num of validators per result

    n_valid = vote_valid.sum(axis=1) # each row checked for VALID
    n_invalid = k- n_valid
    accept = n_valid > n_invalid # odd k so no tie

    return accept

def weighted_vote(vote_valid, ): # algorithm 3