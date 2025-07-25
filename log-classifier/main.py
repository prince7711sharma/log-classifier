import streamlit as st
import pandas as pd
from classify import classify


st.set_page_config(page_title="Log Classifier", layout="wide")
st.title("🔍 Log Classification App")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    if "source" not in df.columns or "log_message" not in df.columns:
        st.error("CSV must have 'source' and 'log_message' columns.")
    else:
        st.success("File uploaded successfully. Starting classification...")
        logs = list(zip(df["source"], df["log_message"]))
        df["target_label"] = classify(logs)

        st.subheader("📊 Classification Results")
        st.dataframe(df)

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Results as CSV", data=csv, file_name="classified_logs.csv", mime="text/csv")

from processor_regex import classify_with_regex
from processor_bert import classify_with_bert
from processor_llm import classify_with_llm

def classify(logs):
    labels = []
    for source, log_msg in logs:
        if source == "LegacyCRM":
            label = classify_with_llm(log_msg)
        else:
            label = classify_with_regex(log_msg)
            if not label:
                label = classify_with_bert(log_msg)
        labels.append(label)
    return labels
