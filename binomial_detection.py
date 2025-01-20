import math

def binomial_probability(n, k, p):
    # Calculate binomial coefficient: n choose k
    binom_coeff = math.comb(n, k)
    
    # Calculate the probability using the binomial distribution formula
    probability = binom_coeff * (p ** k) * ((1 - p) ** (n - k))
    
    return probability

# Calculate probability of player having some number of heads 
def calculate_binomial_probability(player):
    num_of_heads = player.num_of_heads
    num_of_tails = player.num_of_tails
    num_of_trials = num_of_heads + num_of_tails
    p = 0.50

    return binomial_probability(num_of_trials, num_of_heads, p)


