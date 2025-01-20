import numpy as np
from scipy.stats import chisquare  # Correct function import

def determine_cheater(player, alpha):
    # Get the transitions from the player
    transitions = player.get_transitions()

    # Extract counts for each transition, providing default values if keys are missing
    HH = transitions.get('H→H', 0)  # From 'H' to 'H'
    HT = transitions.get('H→T', 0)  # From 'H' to 'T'
    TH = transitions.get('T→H', 0)  # From 'T' to 'H'
    TT = transitions.get('T→T', 0)  # From 'T' to 'T'

    # Observed counts
    observed = np.array([HH, HT, TH, TT])

    # Total transitions
    total_transitions = observed.sum()

    # Handle the case where total_transitions is zero to avoid division by zero
    if total_transitions == 0:
        return False  

    # Expected probabilities under fair coin
    expected_probabilities = np.array([0.25, 0.25, 0.25, 0.25])

    # Expected counts
    expected_counts = total_transitions * expected_probabilities

    # Perform chi-squared goodness-of-fit test
    chi2_stat, p_value = chisquare(f_obs=observed, f_exp=expected_counts)

    # Determine if the p-value is below the significance level
    return p_value < alpha
