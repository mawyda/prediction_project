from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
from mock_data import get_mock_data


def standard_error(observed_freq, bin_length):
    # todo: return once data model defined...
    se = np.sqrt((observed_freq * (1 - observed_freq)) / bin_length).round(4)
    print('Standard Error: {}'.format(se))

# todo: stretch goals
def calculate_standard_error(binned_data, binned_mean_obs, show_se = False):
    bin_lengths = list(len(v) for v in binned_data.values())
    if show_se:
        for bin_len, bin_m_obs in zip(bin_lengths, binned_mean_obs):
            calculate_standard_error(bin_m_obs, bin_len)

def bin_data(data_combined, number_bins):
    bins = np.linspace(0, 1, number_bins)

    binned_data = defaultdict(list)
    # break the predictions so they can be digitized.
    predictions_only = list(i[0] for i in data_combined)
    indices = np.digitize(predictions_only, bins)

    # Now, set to the dict()
    for bin_index, data in zip(indices, data_combined):
        # labels may be created as desired, replacing indices as keys
        binned_data[bin_index].append(data)

    binned_data_averaged = {k: list(map(average_list, map(list, zip(*v)))) for k, v in binned_data.items()}

    # Next, break things into separate lists so they can be plotted
    binned_mean_predictions, binned_mean_observations = map(list, zip(*binned_data_averaged.values()))

    # calculate_standard_error()

    return binned_mean_predictions, binned_mean_observations

def average_list(data):
    return round(sum(data) / len(data), 2)

def get_brier_score(user_prediction_data):
    return round((sum((each[0] - each[1])**2 for each in user_prediction_data))/ len(user_prediction_data), 2)

def plot_calibration(binned_predictions, binned_observations, title):
    plt.figure(figsize =(6,6))

    plt.plot([0, 1], [0, 1], linestyle="--", color="gray", label="Perfectly Calibrated")

    plt.plot(binned_predictions, binned_observations, marker="o", color="blue", label="Model")

    plt.xlabel("Mean Predicted Probability")
    plt.ylabel("Fraction of Positives")
    plt.title(f"Calibration Curve (Reliability Diagram) for {title}")
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.legend(loc="upper left")
    plt.grid(True)

    plt.show()


if __name__ == '__main__':
    # Initialize
    n_questions = 10
    n_users = 10
    n_bins = 6
    plot_true = True

    # Get Data
    users_prediction_data = get_mock_data(n_questions, n_users)

    # Bin and get Brier Score per user
    aggregate_user_predictions = []
    aggregate_brier_score = []
    for user in users_prediction_data:
        # Calculate Brier Score
        user['brier_score'] = get_brier_score(user['prediction_data'])
        aggregate_brier_score.append(user['brier_score'])

        # Return data ready for plot
        binned_mean_predictions, binned_mean_observations = bin_data(user['prediction_data'], n_bins)

        user['binned_data']['binned_predictions'] = binned_mean_predictions
        user['binned_data']['binned_observations'] = binned_mean_observations

        # Aggregate
        aggregate_user_predictions.extend(user['prediction_data'])

    # Get aggregate data
    aggregate_user_predictions.sort()
    binned_agg_predictions, binned_agg_observations = bin_data(aggregate_user_predictions, n_bins)

    # Find best and worst scores and agg
    brier_scores = list(user['brier_score'] for user in users_prediction_data)
    brier_scores.sort()
    briers_averaged = average_list(brier_scores)

    best_brier = brier_scores[0]
    worst_brier = brier_scores[-1]
    best_user = next(user for user in users_prediction_data if user['brier_score'] == best_brier)
    worst_user = next(user for user in users_prediction_data if user['brier_score'] == worst_brier)

    # Plots
    if plot_true:
        # Plot worst, best, and aggregate
        plot_calibration(worst_user['binned_data']['binned_predictions'], worst_user['binned_data']['binned_observations'], 'Worst User')
        plot_calibration(best_user['binned_data']['binned_predictions'], best_user['binned_data']['binned_observations'], 'Best User')
        plot_calibration(binned_agg_predictions, binned_agg_observations, 'Aggregate')

    # Build a summary from the print statements above.
    print('The user with the Worst Brier Score:', worst_user['username'], worst_user['brier_score'])
    print('The user with the Best Brier Score:', best_user['username'], best_user['brier_score'])
    print('The aggregate brier score was', briers_averaged)