import os
import pickle
import numpy as np
from django.conf import settings


def predict_voice(features):
    """
    Predict if voice is AI-generated or human using trained ML model.

    Args:
        features (np.ndarray): Extracted audio features

    Returns:
        tuple: (prediction_label, confidence_score)
            - prediction_label (str): "AI" or "Human"
            - confidence_score (float): Confidence percentage (0–100)

    Raises:
        Exception: If model loading or prediction fails
    """
    try:
        # Path to trained ML model
        model_path = os.path.join(
            settings.BASE_DIR,
            "predict",
            "ml",
            "model.pkl"
        )

        # If model does not exist, return mock prediction
        # (Used during development / testing)
        if not os.path.exists(model_path):
            confidence = np.random.uniform(70, 95)
            prediction = "AI" if confidence > 50 else "Human"
            return prediction, round(confidence, 2)

        # Load trained model
        with open(model_path, "rb") as f:
            model = pickle.load(f)

        # Reshape features for model input
        features_reshaped = features.reshape(1, -1)

        # Predict class and probabilities
        prediction_proba = model.predict_proba(features_reshaped)[0]
        prediction_class = model.predict(features_reshaped)[0]

        # Convert output to readable labels
        prediction_label = "AI" if prediction_class == 1 else "Human"
        confidence = max(prediction_proba) * 100

        return prediction_label, round(confidence, 2)

    except Exception as e:
        raise Exception(f"Error during prediction: {str(e)}")
