import random
import uuid
from faker import Faker

'''Intended to mimic an API call or database schema'''

def generate_prediction_metrics(n_values):
    return sorted([round(random.random(), 2) for i in range(n_values)])

def generate_observations(n_values):
    return [random.randint(0,1) for i in range(n_values)]

def get_mock_data(n_questions, n_users):
    questions = []
    for i in range(n_questions):
        questions.append({'ID': uuid.uuid4(), 'outcome': random.randint(0, 1)})

    # Initialize users
    faker = Faker()
    users = []
    for i in range(n_users):
        users.append({'ID': faker.name()})

    predictions = []
    for user in users:
        for question in questions:
            predictions.append(
                {'user_ID': user['ID'],
                 'question_ID': question['ID'], 'prediction': round(random.random(), 2),
                 'outcome': question['outcome']
                 }
            )

    # get all unique users
    unique_users = list(set([user['ID'] for user in users]))

    user_predictions = []
    for unique_user in unique_users:
        # create the combined data
        user = {'username': unique_user, 'prediction_data': [], 'brier_score': 0, 'binned_data': {'binned_predictions': [], 'binned_observations': []}}
        for prediction in predictions:
            if prediction['user_ID'] == user['username']:
                user['prediction_data'].append((prediction['prediction'], prediction['outcome']))
        user['prediction_data'] = sorted(user['prediction_data'])
        user_predictions.append(user)

    return user_predictions

if __name__ == "__main__":
    q = 10
    u = 10

    mock_prediction_data = get_mock_data(q, u)

    print('user_predictions:', mock_prediction_data[0])
    print('keys', mock_prediction_data[0].keys())








