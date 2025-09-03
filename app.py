import streamlit as st
import openai
import pandas as pd
from io import BytesIO

# 🔑 Put your API key here
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="AI Test Case Generator", page_icon="🧪", layout="wide")
st.title("🧪 AI Test Case & Scenario Generator")
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

            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=800
                )

                output = response.choices[0].message.content.strip()

                st.subheader("Generated Test Cases")
                st.write(output)

                # Save as CSV
                df = pd.DataFrame([x.split(" | ") for x in output.split("\n") if "|" in x])
                df.columns = ["Test Case ID", "Scenario", "Steps", "Expected Result", "Type"]

                csv = BytesIO()
                df.to_csv(csv, index=False)
                st.download_button(
                    label="📥 Download Test Cases as CSV",
                    data=csv.getvalue(),
                    file_name="test_cases.csv",
                    mime="text/csv",
                )

            except Exception as e:
                st.error(f"Error: {e}")
