import random
from binomial_detection import calculate_binomial_probability
from markov_chain_detection import determine_cheater
from collections import defaultdict

class Player:
    def __init__(self, probability_of_heads=0.50, cheater=False):
        self.probability_of_heads = probability_of_heads
        self.num_of_heads = 0
        self.num_of_tails = 0
        self.cheater = cheater
        self.previous_flip = None  # To track the previous flip (initially None)
        # Transition tracking
        self.transitions = {
            'H→H': 0,
            'H→T': 0,
            'T→H': 0,
            'T→T': 0
        }

    def run_heads_or_tails(self, num_flips):
        for _ in range(num_flips):
            # Simulate the coin flip
            percentage_of_heads = self.probability_of_heads * 100
            random_int_randint = random.randint(1, 100)

            # Determine the outcome of the flip
            if random_int_randint <= percentage_of_heads:
                current_flip = 'H'
                self.num_of_heads += 1
            else:
                current_flip = 'T'
                self.num_of_tails += 1

            # Update transitions if there's a previous flip
            if self.previous_flip:
                transition = f"{self.previous_flip}→{current_flip}"
                if transition in self.transitions:
                    self.transitions[transition] += 1

            # Set the current flip as the previous flip for the next iteration
            self.previous_flip = current_flip

    def get_total_flips(self):
        # Return the total number of flips (heads + tails)
        return self.num_of_heads + self.num_of_tails

    def get_transitions(self):
        # Return the simplified transition dictionary
        return self.transitions

def run_experiment(number_of_times):
    # Parameters 
    num_players = 100       # Total number of players
    num_cheaters = 30       # Number of cheaters among the players
    num_flips = 1000        # Number of coin flips per player
    alpha = 0.01            # Significance level

    total_cheaters = 0
    binomial_cheaters_caught = 0
    markov_cheaters_caught = 0
    binomial_false_positives = 0
    markov_false_positives = 0

    # Run the experiment multiple times to gather averages
    for _ in range(number_of_times):
        players = []

        # Create fair players
        for _ in range(num_players - num_cheaters):
            player = Player(probability_of_heads=0.5, cheater=False)
            player.run_heads_or_tails(num_flips)
            players.append(player)

        # Create cheating players
        for _ in range(num_cheaters):
            player = Player(probability_of_heads=0.65, cheater=True)
            player.run_heads_or_tails(num_flips)
            players.append(player)

        # Shuffle the list of players for randomness
        random.shuffle(players)

        # Detection logic
        for player in players:
            is_cheater = player.cheater
            total_cheaters += is_cheater

            # Binomial detection
            probability = calculate_binomial_probability(player)
            if probability < alpha:
                if is_cheater:
                    binomial_cheaters_caught += 1
                else:
                    binomial_false_positives += 1

            # Markov chain detection
            markov_cheater_detected = determine_cheater(player, alpha)
            if markov_cheater_detected:
                if is_cheater:
                    markov_cheaters_caught += 1
                else:
                    markov_false_positives += 1

    # Calculate averages after all experiments
    average_binomial_cheaters_caught = binomial_cheaters_caught / number_of_times
    average_markov_cheaters_caught = markov_cheaters_caught / number_of_times
    average_binomial_false_positives = binomial_false_positives / number_of_times
    average_markov_false_positives = markov_false_positives / number_of_times

    # Print results
    print("Total number of players per experiment:", num_players)
    print("Average number of cheaters per experiment:", total_cheaters / number_of_times)
    print("\nBinomial Detection Method:")
    print("Average number of cheaters caught:", average_binomial_cheaters_caught)
    print("Average number of false positives:", average_binomial_false_positives)
    print("Detection rate:", f"{(average_binomial_cheaters_caught / (num_cheaters)) * 100:.2f}%")
    print("False positive rate:", f"{(average_binomial_false_positives / ((num_players - num_cheaters))) * 100:.2f}%")

    print("\nMarkov Chain Detection Method:")
    print("Average number of cheaters caught:", average_markov_cheaters_caught)
    print("Average number of false positives:", average_markov_false_positives)
    print("Detection rate:", f"{(average_markov_cheaters_caught / (num_cheaters)) * 100:.2f}%")
    print("False positive rate:", f"{(average_markov_false_positives / ((num_players - num_cheaters))) * 100:.2f}%")

# Call the function to run the experiment
run_experiment(100)
