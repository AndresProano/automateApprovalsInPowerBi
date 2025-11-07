import csv, os

def to_csv(approvals, out_path="output.csv"):
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Title", "Details", "File", "Status", "Stage", "Source", "Create at", "Sent by", "Sent to", "Custom responses"])
        for item in approvals:
            writer.writerow([
                item.get("title"),
                item.get("details"),
                item.get("file"),
                item.get("status"),
                item.get("stage"),
                item.get("source"),
                item.get("createdDateTime"),
                item.get("SentBy"), 
                item.get("CreatedBy"),
                item.get("customResponses")
            ])
    return out_path
