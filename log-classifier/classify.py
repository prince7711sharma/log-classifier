from processor_regex import classify_with_regex
from processor_bert import classify_with_bert
from processor_llm import classify_with_llm
import pandas as pd

def classify(logs):
    labels = []
    for source, log_msg in logs:
        label = classify_log(source, log_msg)
        labels.append(label)
    return labels

def classify_log(source, log_msg):
    # LLM-based classification for LegacyCRM logs
    if source == "LegacyCRM":
        label = classify_with_llm(log_msg)
    else:
        # Try regex first
        label = classify_with_regex(log_msg)
        # Fall back to BERT if regex fails
        if not label:
            label = classify_with_bert(log_msg)
    return label

def classify_csv(input_file):
    try:
        df = pd.read_csv(input_file)

        if "source" not in df.columns or "log_message" not in df.columns:
            raise ValueError("CSV must contain 'source' and 'log_message' columns.")

        # Perform classification
        logs = list(zip(df["source"], df["log_message"]))
        df["target_label"] = classify(logs)

        # Save result
        output_file = "output.csv"
        df.to_csv(output_file, index=False)
        print(f"✅ Classified logs saved to: {output_file}")
        return output_file

    except Exception as e:
        print(f"❌ Error processing CSV: {e}")
        return None

if __name__ == '__main__':
    # Classify from CSV
    classify_csv("test.csv")

    # Example logs (for debugging/testing)
    logs = [
        ("ModernCRM", "IP 192.168.133.114 blocked due to potential attack"),
        ("BillingSystem", "User 12345 logged in."),
        ("AnalyticsEngine", "File data_6957.csv uploaded successfully by user User265."),
        ("AnalyticsEngine", "Backup completed successfully."),
        ("ModernHR", "GET /v2/54fadb412c4e40cdbaed9335e4c35a9e/servers/detail HTTP/1.1 RCODE  200 len: 1583 time: 0.1878400"),
        ("ModernHR", "Admin access escalation detected for user 9429"),
        ("LegacyCRM", "Case escalation for ticket ID 7324 failed because the assigned support agent is no longer active."),
        ("LegacyCRM", "Invoice generation process aborted for order ID 8910 due to invalid tax calculation module."),
        ("LegacyCRM", "The 'BulkEmailSender' feature is no longer supported. Use 'EmailCampaignManager' for improved functionality."),
        ("LegacyCRM", "The 'ReportGenerator' module will be retired in version 4.0. Please migrate to the 'AdvancedAnalyticsSuite' by Dec 2025")
    ]

    print("\n🔍 Classifying test logs:")
    labels = classify(logs)
    for (source, msg), label in zip(logs, labels):
        print(f"{source}: {label}")
