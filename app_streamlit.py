import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import requests
import json
from pathlib import Path

# Set page configuration
st.set_page_config(
    page_title="Cricket Performance Predictor",
    page_icon="🏏",
    layout="wide"
)

# Define paths
MODEL_PATH = Path("models") / "cricket_model.pkl"
API_URL = "http://localhost:5050"  # Flask API URL

# Function to load model directly
@st.cache_resource
def load_model():
    if MODEL_PATH.exists():
        return joblib.load(MODEL_PATH)
    else:
        st.error(f"Model file not found at {MODEL_PATH}")
        return None

# Function to make API prediction
def predict_via_api(data):
    try:
        response = requests.post(
            f"{API_URL}/predict", 
            json=data,
            headers={"Content-Type": "application/json"}
        )
        return response.json()
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to API. Is the Flask server running?")
        return None

# Function to make direct prediction
def predict_direct(model, data):
    if model is None:
        return None
    
    # Convert input to DataFrame
    input_df = pd.DataFrame([data])
    
    # Make prediction
    prediction = model.predict(input_df)[0]
    
    return {
        "predicted_runs": round(float(prediction), 2),
        "input_data": data,
        "status": "success"
    }

# Main app
def main():
    # Header
    st.title("🏏 Cricket Performance Predictor")
    st.markdown("### Predict a player's total runs based on performance metrics")
    
    # Model loading (for direct prediction option)
    model = load_model()
    
    # Sidebar for prediction mode
    prediction_mode = st.sidebar.radio(
        "Prediction Mode",
        ["Use API", "Direct Prediction"],
        index=0
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### About")
    st.sidebar.info(
        "This app predicts a cricket player's total runs based on "
        "various performance metrics using a machine learning model. "
        "The model was trained on ODI cricket data."
    )
    
    # Input form
    with st.form("prediction_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            strike_rate = st.number_input("Strike Rate", min_value=50.0, max_value=150.0, value=90.0, step=0.1)
            total_balls_faced = st.number_input("Total Balls Faced", min_value=1000, max_value=20000, value=10000, step=100)
            total_matches_played = st.number_input("Total Matches Played", min_value=10, max_value=500, value=200, step=1)
        
        with col2:
            matches_won = st.number_input("Matches Won", min_value=0, max_value=300, value=120, step=1)
            matches_lost = st.number_input("Matches Lost", min_value=0, max_value=300, value=70, step=1)
        
        submit = st.form_submit_button("Predict Total Runs")
    
    # Make prediction when form is submitted
    if submit:
        # Prepare input data
        input_data = {
            "strike_rate": strike_rate,
            "total_balls_faced": total_balls_faced,
            "total_matches_played": total_matches_played,
            "matches_won": matches_won,
            "matches_lost": matches_lost
        }
        
        with st.spinner("Making prediction..."):
            if prediction_mode == "Use API":
                prediction = predict_via_api(input_data)
            else:
                prediction = predict_direct(model, input_data)
            
            if prediction:
                # Display prediction results
                st.success(f"### Predicted Total Runs: {prediction['predicted_runs']:,.0f}")
                
                # Display input data used
                st.subheader("Input Parameters")
                
                # Create a DataFrame from the input for better display
                input_df = pd.DataFrame([input_data])
                st.dataframe(input_df)
                
                # Key performance metrics visualization
                st.subheader("Performance Visualization")
                
                # Create a bar chart of input metrics
                chart_data = pd.DataFrame({
                    'Metric': ['Strike Rate', 'Matches Won', 'Matches Lost'],
                    'Value': [strike_rate, matches_won, matches_lost]
                })
                st.bar_chart(chart_data.set_index('Metric'))
                
                # Win-loss ratio calculation and display
                win_loss_ratio = matches_won / matches_lost if matches_lost > 0 else "N/A"
                
                # Display KPIs
                col1, col2, col3 = st.columns(3)
                col1.metric("Strike Rate", f"{strike_rate:.1f}")
                col2.metric("Total Matches", total_matches_played)
                col3.metric("Win-Loss Ratio", f"{win_loss_ratio:.2f}" if isinstance(win_loss_ratio, float) else win_loss_ratio)
                
    # Health check for API connection
    if prediction_mode == "Use API":
        try:
            response = requests.get(f"{API_URL}/health")
            if response.status_code == 200:
                st.sidebar.success("✅ API connection is healthy")
            else:
                st.sidebar.error("❌ API is not responding correctly")
        except requests.exceptions.ConnectionError:
            st.sidebar.error("❌ Cannot connect to API")

if __name__ == "__main__":
    main() 