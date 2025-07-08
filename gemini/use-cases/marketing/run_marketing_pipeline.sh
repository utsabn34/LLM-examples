#!/bin/bash

# Exit immediately on error
set -e

# ---- Step 1: Install dependencies ----
echo "Installing required Python packages..."
pip install --quiet --upgrade google-genai pydantic

# ---- Step 2: Authenticate with Google Cloud ----
echo "Launching Google Cloud authentication (browser-based)..."
gcloud auth application-default login

# ---- Step 3: Set environment variables ----
echo "Setting environment variables..."
export GOOGLE_CLOUD_PROJECT="your-project-id"   # <-- Replace with your actual project ID
export GOOGLE_CLOUD_REGION="us-central1"

# ---- Step 4: Run the Gemini marketing pipeline ----
echo "Running the marketing pipeline script..."
python gemini_marketing_pipeline.py

