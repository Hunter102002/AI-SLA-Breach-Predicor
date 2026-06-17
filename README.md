AI-Powered SLA Breach Predictor

Objective

Built an AI-powered ticket risk scoring system that analyzes open support tickets and predicts which ones are going to breach SLA before it happens. Rather than reacting after a breach occurs, this tool gives ops and CS teams time to intervene — surfacing the right tickets, the right reasoning, and the right next steps automatically.
Built using Python and the Claude API, the system scores every ticket based on SLA consumption, assignee workload, and update staleness, then uses AI to generate plain-English explanations and an executive summary of overall operational health.

What It Does


Ingests open ticket data and scores each ticket for breach risk
Flags at-risk tickets above a configurable risk threshold
Calls the Claude API to explain why each ticket is at risk and what action to take
Generates an end-of-run executive summary identifying overloaded assignees, high-risk categories, and recommended actions
Outputs a full operational risk report in the terminal


Skills Demonstrated


AI Integration: Connecting to and prompting the Claude API to generate contextual, actionable output from structured data.
Risk Scoring Logic: Designing a weighted algorithm that combines multiple signals into a single risk score.
Python Development: End-to-end scripting including CSV ingestion, data processing, API calls, and formatted reporting.
Operational Thinking: Translating a real ops problem (SLA breaches) into a working technical solution.
Prompt Engineering: Writing prompts that produce consistent, specific, and useful AI output per ticket and for the overall summary.


Tools Used


Python: Core scripting and data processing.
Claude API (Haiku): AI-generated explanations and executive summary.
Zendesk-style ticket data: Simulated ticket dataset representing a real support queue.


Outcome


Flags at-risk tickets before breach occurs, giving teams time to act.
Generates plain-English AI reasoning for each flagged ticket — no dashboard interpretation needed.
Produces an executive summary that identifies the biggest risk areas across the full queue.
Reduces reactive firefighting by turning ticket data into a forward-looking risk report.


Note

Ticket data used in this project is simulated. This tool is designed to connect to any CRM or ticketing system (Zendesk, ServiceNow, Jira) that can export ticket data — the scoring and AI layer sits on top of whatever the data source is.

Steps

Risk Scoring — Each ticket is scored using three signals: how much of the SLA window has been consumed, how many open tickets the assignee is carrying, and how long since the last update. These combine into a single risk score between 0 and 1. Any ticket above 0.75 is flagged.


AI Ticket Analysis — For every flagged ticket, the tool calls the Claude API with the ticket details and risk score. Claude returns a 2-3 sentence explanation of why the ticket is at risk and what action to take. This is the part a rule-based system cannot do — it reasons about the combination of signals, not just a threshold.


Executive Summary — After all flagged tickets are analyzed, the tool sends an aggregated summary to Claude covering total tickets scanned, at-risk count, assignee breakdown, and category breakdown. Claude returns a 3-4 sentence operational summary with the biggest risk areas and recommended immediate actions.


Sample Output — [Video walkthrough coming soon]
