"""
train_model.py – Utility to trigger RASA model training programmatically.

Called by the admin panel when "Train" button is pressed.
Runs `rasa train` in the RASA project directory, and outputs model to `/rasa_core/models`.
"""

import subprocess
import os
from datetime import datetime

RASA_PROJECT_PATH = os.path.abspath("rasa_core")
MODEL_OUTPUT_PATH = os.path.join(RASA_PROJECT_PATH, "models")

def train_rasa_model():
    """
    Triggers RASA CLI to train a new model.
    :return: Tuple (success: bool, model_file or error_message)
    """
    try:
        print("[TRAIN] Starting RASA training...")
        result = subprocess.run(
            ["rasa", "train"],
            cwd=RASA_PROJECT_PATH,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode != 0:
            print(f"[TRAIN ERROR] {result.stderr}")
            return False, result.stderr.strip()

        # Find latest model file
        model_files = sorted(
            [f for f in os.listdir(MODEL_OUTPUT_PATH) if f.endswith(".tar.gz")],
            key=lambda x: os.path.getmtime(os.path.join(MODEL_OUTPUT_PATH, x)),
            reverse=True
        )

        if not model_files:
            return False, "Training succeeded but no model found."

        latest_model = model_files[0]
        print(f"[TRAIN SUCCESS] Model: {latest_model}")
        return True, latest_model

    except Exception as e:
        print(f"[TRAIN EXCEPTION] {str(e)}")
        return False, str(e)