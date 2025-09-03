import streamlit as st
import pandas as pd
from io import BytesIO
import requests

# Load Hugging Face API key
HF_API_KEY = st.secrets["HF_API_KEY"]

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

headers = {"Authorization": f"Bearer {HF_API_KEY}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

st.set_page_config(page_title="AI Test Case Generator (Free)", page_icon="🧪", layout="wide")
st.title("🧪 AI Test Case & Scenario Generator (Free Version)")
st.write("Paste your requirement or user story, and AI will generate test cases for you.")

requirement = st.text_area("Enter Requirement/User Story:")

if st.button("Generate Test Cases"):
    if requirement.strip() == "":
        st.warning("Please enter a requirement.")
    else:
        with st.spinner("Generating test cases..."):
            prompt = f"""
            Generate detailed software test cases for the following requirement:
            {requirement}
            
            Format output as a table with columns:
            Test Case ID | Scenario | Steps | Expected Result | Type
            """

            result = query({"inputs": prompt})

            if isinstance(result, dict) and "error" in result:
                st.error(f"Error: {result['error']}")
            else:
                output = result[0]["generated_text"]

                st.subheader("Generated Test Cases")
                st.write(output)

                # Convert to CSV if possible
                rows = [x.split(" | ") for x in output.split("\n") if "|" in x]
                if rows:
                    df = pd.DataFrame(rows, columns=["Test Case ID", "Scenario", "Steps", "Expected Result", "Type"])
                    csv = BytesIO()
                    df.to_csv(csv, index=False)
                    st.download_button(
                        label="📥 Download Test Cases as CSV",
                        data=csv.getvalue(),
                        file_name="test_cases.csv",
                        mime="text/csv",
                    )
                else:
                    st.info("AI response was not in table format. Try again.")
