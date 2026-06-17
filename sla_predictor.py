import csv
import anthropic
from datetime import datetime
from collections import defaultdict

# ── Config ──────────────────────────────────────────────────────────────────
CSV_FILE = "mock_tickets.csv"
RISK_THRESHOLD = 0.75
CLIENT = anthropic.Anthropic(api_key="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")

# ── Risk Scoring ─────────────────────────────────────────────────────────────
def score_ticket(ticket):
    sla_hours = float(ticket["sla_hours"])
    age_hours = float(ticket["age_hours"])
    assignee_load = int(ticket["assignee_open_tickets"])
    last_update = float(ticket["last_update_hours"])

    sla_pct = age_hours / sla_hours
    load_penalty = min(assignee_load / 10, 0.2)
    stale_pct = last_update / age_hours if age_hours > 0 else 0
    stale_penalty = min(stale_pct * 0.1, 0.1)

    score = sla_pct + load_penalty + stale_penalty
    return round(min(score, 1.0), 3), round(sla_pct * 100, 1)

# ── Claude: Single Ticket Explanation ────────────────────────────────────────
def get_ai_explanation(ticket, score, sla_used_pct):
    prompt = f"""You are an IT operations analyst reviewing a support ticket for SLA breach risk.

Ticket details:
- ID: {ticket['ticket_id']}
- Category: {ticket['category']}
- Priority: {ticket['priority']}
- Assignee: {ticket['assignee']} ({ticket['assignee_open_tickets']} open tickets)
- SLA window: {ticket['sla_hours']} hours
- Current age: {ticket['age_hours']} hours ({sla_used_pct}% of SLA used)
- Hours since last update: {ticket['last_update_hours']}
- Status: {ticket['status']}
- Risk score: {score}/1.0

In 2-3 sentences, explain why this ticket is at risk of breaching SLA and what action should be taken. Be specific and direct."""

    message = CLIENT.messages.create(
        model="claude-haiku-4-5",
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text.strip()

# ── Claude: Overall Summary ───────────────────────────────────────────────────
def get_overall_summary(tickets, at_risk, safe):
    assignee_risk = defaultdict(list)
    category_risk = defaultdict(list)
    for t in at_risk:
        assignee_risk[t["assignee"]].append(t["_score"])
        category_risk[t["category"]].append(t["_score"])

    assignee_summary = ", ".join(
        f"{a} ({len(s)} tickets, avg score {round(sum(s)/len(s),2)})"
        for a, s in sorted(assignee_risk.items(), key=lambda x: -len(x[1]))
    )
    category_summary = ", ".join(
        f"{c} ({len(s)} at risk)"
        for c, s in sorted(category_risk.items(), key=lambda x: -len(x[1]))
    )

    prompt = f"""You are an IT operations manager reviewing a daily SLA risk report.

Summary data:
- Total tickets: {len(tickets)}
- At-risk tickets: {len(at_risk)} ({round(len(at_risk)/len(tickets)*100)}% of total)
- On-track tickets: {len(safe)}
- Assignees with at-risk tickets: {assignee_summary}
- Categories driving risk: {category_summary}
- Average SLA consumption across all tickets: {round(sum(float(t['age_hours'])/float(t['sla_hours'])*100 for t in tickets)/len(tickets), 1)}%

Write a 3-4 sentence executive summary of the current SLA health. Identify the biggest risk areas, call out any overloaded assignees, and recommend one or two immediate actions. Be direct and operational."""

    message = CLIENT.messages.create(
        model="claude-haiku-4-5",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text.strip()

# ── Stats ─────────────────────────────────────────────────────────────────────
def print_stats(tickets, at_risk):
    avg_sla = round(sum(float(t["age_hours"])/float(t["sla_hours"])*100 for t in tickets) / len(tickets), 1)

    assignee_counts = defaultdict(int)
    category_counts = defaultdict(int)
    for t in at_risk:
        assignee_counts[t["assignee"]] += 1
        category_counts[t["category"]] += 1

    worst_assignee = max(assignee_counts, key=assignee_counts.get) if assignee_counts else "N/A"
    worst_category = max(category_counts, key=category_counts.get) if category_counts else "N/A"

    print(f"\n  STATS")
    print(f"  {'─' * 40}")
    print(f"  Avg SLA consumption (all tickets) : {avg_sla}%")
    print(f"  Most at-risk assignee             : {worst_assignee} ({assignee_counts[worst_assignee]} tickets)")
    print(f"  Most at-risk category             : {worst_category} ({category_counts[worst_category]} tickets)")

    print(f"\n  AT-RISK BREAKDOWN BY ASSIGNEE")
    for assignee, count in sorted(assignee_counts.items(), key=lambda x: -x[1]):
        bar = "█" * count
        print(f"  {assignee:<15} {bar} {count}")

    print(f"\n  AT-RISK BREAKDOWN BY CATEGORY")
    for category, count in sorted(category_counts.items(), key=lambda x: -x[1]):
        bar = "█" * count
        print(f"  {category:<20} {bar} {count}")

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    tickets = []
    with open(CSV_FILE, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            tickets.append(row)

    at_risk = []
    safe = []

    for ticket in tickets:
        score, sla_used_pct = score_ticket(ticket)
        ticket["_score"] = score
        ticket["_sla_used_pct"] = sla_used_pct
        if score >= RISK_THRESHOLD:
            at_risk.append(ticket)
        else:
            safe.append(ticket)

    at_risk.sort(key=lambda t: t["_score"], reverse=True)

    print("=" * 65)
    print("       SLA BREACH PREDICTOR — RISK REPORT")
    print(f"       Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 65)
    print(f"\n  Total tickets scanned : {len(tickets)}")
    print(f"  At-risk tickets       : {len(at_risk)}")
    print(f"  On track              : {len(safe)}")
    print(f"  Risk threshold        : {int(RISK_THRESHOLD * 100)}% SLA consumed")

    print_stats(tickets, at_risk)

    print("\n" + "─" * 65)
    print("  AT-RISK TICKETS (AI Analysis)")
    print("─" * 65)

    for t in at_risk:
        print(f"\n  🚨 {t['ticket_id']} | {t['priority']} | {t['category']}")
        print(f"     Assignee   : {t['assignee']} ({t['assignee_open_tickets']} open tickets)")
        print(f"     SLA Used   : {t['_sla_used_pct']}%  ({t['age_hours']}h of {t['sla_hours']}h)")
        print(f"     Last Update: {t['last_update_hours']}h ago")
        print(f"     Risk Score : {t['_score']}")
        print(f"\n     AI Analysis:")
        explanation = get_ai_explanation(t, t["_score"], t["_sla_used_pct"])
        for line in explanation.split(". "):
            if line.strip():
                print(f"     → {line.strip()}.")
        print()

    print("─" * 65)
    print("  ON-TRACK TICKETS")
    print("─" * 65)
    for t in safe:
        sla_remaining = round(100 - t["_sla_used_pct"], 1)
        print(f"  ✅ {t['ticket_id']} | {t['priority']:<8} | {t['category']:<20} | SLA used: {t['_sla_used_pct']}% | Remaining: {sla_remaining}%")

    print("\n" + "─" * 65)
    print("  EXECUTIVE SUMMARY (AI Generated)")
    print("─" * 65)
    summary = get_overall_summary(tickets, at_risk, safe)
    for line in summary.split(". "):
        if line.strip():
            print(f"\n  {line.strip()}.")

    print("\n" + "=" * 65)

if __name__ == "__main__":
    main()
