import pathlib
import pandas as pd
import models.model_training
import pickle

def predict_success_prob_for_reef_visits(best_model_path: pathlib.Path, reef_data: pd.DataFrame):
    with open(best_model_path, 'rb') as f:
        best_model = pickle.load(f)

    X = reef_data[models.model_training.MODEL_FEATURES]
    predicted_probabilities = best_model.predict_proba(X)[:, 1]

    reef_data['predicted_success_probability'] = predicted_probabilities

    return reef_data