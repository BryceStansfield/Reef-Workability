# Loads trained model pickle files, standardises their internal structure with consistent
# performance metrics, and re-saves them with sequential naming (Model_1.pkl, Model_2.pkl, Model_3.pkl).

import pickle
import numpy as np
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score


def load_and_standardize_models():
    file_mappings = {
        "best_reef_prediction_model_randomforest.pkl": "Model_1.pkl",
        "best_reef_prediction_model_gradientboosting.pkl": "Model_2.pkl",
        "best_reef_model.pkl": "Model_3.pkl"
    }

    original_data = {}
    for original_file in file_mappings.keys():
        try:
            with open(original_file, 'rb') as f:
                data = pickle.load(f)
                original_data[original_file] = data
                print(f"Loaded {original_file}")
        except Exception as e:
            print(f"Error loading {original_file}: {e}")
            return

    standardized_models = {}

    for original_file, data in original_data.items():
        print(f"\nStandardizing {original_file}...")

        standardized = {
            'model': data['model'],
            'features': data['features'],
            'model_name': data['model_name'],
            'training_info': data['training_info'],
            'threshold': data['threshold'],
            'metrics': {}
        }

        metrics = {}

        if 'f1_score' in data:
            metrics['f1_score'] = data['f1_score']
        if 'precision' in data:
            metrics['precision'] = data['precision']
        if 'recall' in data:
            metrics['recall'] = data['recall']

        if original_file == "best_reef_prediction_model_randomforest.pkl":
            metrics.update({
                'precision': 0.3519,
                'recall': 0.8085,
                'f1_score': 2 * (0.3519 * 0.8085) / (0.3519 + 0.8085),
                'accuracy': 0.89,
                'macro_avg_precision': 0.70,
                'macro_avg_recall': 0.83,
                'macro_avg_f1': 0.74,
                'weighted_avg_precision': 0.93,
                'weighted_avg_recall': 0.89,
                'weighted_avg_f1': 0.90
            })

        elif original_file == "best_reef_prediction_model_gradientboosting.pkl":
            metrics.update({
                'precision': 0.6944,
                'recall': 0.5319,
                'f1_score': 2 * (0.6944 * 0.5319) / (0.6944 + 0.5319),
                'accuracy': 0.94,
                'macro_avg_precision': 0.83,
                'macro_avg_recall': 0.75,
                'macro_avg_f1': 0.78,
                'weighted_avg_precision': 0.93,
                'weighted_avg_recall': 0.94,
                'weighted_avg_f1': 0.94
            })

        elif original_file == "best_reef_model.pkl":
            metrics.update({
                'f1_score': 0.6593,
                'precision': 0.68,
                'recall': 0.64,
                'accuracy': 0.9428,
                'macro_avg_precision': 0.82,
                'macro_avg_recall': 0.81,
                'macro_avg_f1': 0.81,
                'weighted_avg_precision': 0.94,
                'weighted_avg_recall': 0.94,
                'weighted_avg_f1': 0.94
            })

        standardized['metrics'] = metrics
        standardized['model_type'] = type(data['model']).__name__
        standardized['feature_count'] = len(data['features'])

        standardized_models[original_file] = standardized

        print(f"   Added {len(metrics)} metrics")
        print(f"   Features: {standardized['feature_count']}")
        print(f"   Model type: {standardized['model_type']}")

    print(f"\nSaving standardized models...")

    for original_file, new_file in file_mappings.items():
        if original_file in standardized_models:
            try:
                with open(new_file, 'wb') as f:
                    pickle.dump(standardized_models[original_file], f)
                print(f"Saved {new_file}")

                data = standardized_models[original_file]
                print(f"   Model: {data['model_name']}")
                print(f"   Metrics: {list(data['metrics'].keys())}")
                print(f"   Threshold: {data['threshold']}")

            except Exception as e:
                print(f"Error saving {new_file}: {e}")

    return standardized_models


def verify_saved_models():
    print(f"\nVERIFICATION - Loading saved models...")

    model_files = ["Model_1.pkl", "Model_2.pkl", "Model_3.pkl"]

    for model_file in model_files:
        try:
            with open(model_file, 'rb') as f:
                data = pickle.load(f)

            print(f"\n{model_file}:")
            print(f"   Keys: {list(data.keys())}")
            print(f"   Model: {data['model_name']}")
            print(f"   Metrics: {list(data['metrics'].keys())}")
            print(f"   Features: {len(data['features'])}")
            print(f"   Threshold: {data['threshold']}")

            if 'accuracy' in data['metrics']:
                print(f"   Accuracy: {data['metrics']['accuracy']:.4f}")
            if 'f1_score' in data['metrics']:
                print(f"   F1 Score: {data['metrics']['f1_score']:.4f}")
            if 'precision' in data['metrics']:
                print(f"   Precision: {data['metrics']['precision']:.4f}")
            if 'recall' in data['metrics']:
                print(f"   Recall: {data['metrics']['recall']:.4f}")

        except Exception as e:
            print(f"Error verifying {model_file}: {e}")


print("Starting model standardization process...")
standardized_models = load_and_standardize_models()

if standardized_models:
    print(f"\nStandardization complete!")
    verify_saved_models()

    print(f"\nSUMMARY:")
    print(f"   - Model_1.pkl: RandomForest (High Recall: 0.8085)")
    print(f"   - Model_2.pkl: GradientBoosting (Balanced: Precision 0.6944)")
    print(f"   - Model_3.pkl: RandomForest Pipeline (Good F1: 0.6593)")
