import csv, os

def to_csv(approvals, out_path="output.csv"):
    rows = []

    for item in approvals:
        row = {
            "id": item.get("id", {}),
            "title": item.get("displayName", {}),
            "approvalType": item.get("approvalType", {}),
            "createdDateTime": item.get("createdDateTime", {}),
            "allowCancel": item.get("allowCancel", {}),
            "allowEmailNotifications": item.get("allowEmailNotifications", {}),
            "description": item.get("description", {}),
            "completedDateTime": item.get("completedDateTime", {}),
            "responsePrompts": item.get("responsePrompts", {}),
            "state": item.get("state", {}),
            "result": item.get("result", {}),
            "approvers" : ";".join(
                [a.get("user", {}).get("id", {}) for a in item.get("approvers", [])]
            ),
            "viewPoint": item.get("viewPoint", {}).get("roles", {}),
            "owner" : item.get("owner", {}).get("user", {}).get("id", {}),
        }
        rows.append(row)

    with open(out_path, "w", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    return out_path
