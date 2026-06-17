# AI-Powered SLA Breach Predictor
## Objective
Built a tool that predicts SLA breaches before they happen. It pulls open ticket data, scores each ticket for risk, and uses AI to explain what is going wrong and what to do about it so teams can get ahead of problems instead of cleaning them up after the fact.
 
Built using Python and the Claude API, the scoring weighs SLA consumption, assignee workload, and how long since the last update. The AI layer turns that data into plain-English analysis at the ticket level and a full operational summary at the end.
## What It Does
1.	Reads open ticket data and scores every ticket for breach risk
2.	Flags anything above the risk threshold before it actually breaches
3.	Calls the Claude API to explain why each flagged ticket is at risk and what action to take
4.	Produces an executive summary at the end covering overloaded assignees, high-risk categories, and next steps
5.	Outputs a full risk report directly in the terminal
### Skills Learned
-	AI Integration: Connecting to the Claude API and prompting it to return useful, specific output from structured ticket data.
-	Risk Scoring: Building a weighted algorithm that combines multiple signals into a single score.
-	Python Development: Scripting CSV ingestion, data processing, API calls, and formatted terminal output end to end.
- Operational Problem Solving: Taking a real workflow problem and turning it into a working technical tool.
- Prompt Engineering: Writing prompts that produce consistent, actionable AI output at both the ticket and summary level.
### Tools Used
- Python: Core scripting and data processing.
- Claude API (Haiku): Ticket-level explanations and end-of-run executive summary.
- Zendesk-style ticket data: Simulated dataset built to represent a real support queue.
### Outcome
- Catches at-risk tickets before they breach, giving teams time to actually do something about it.
- Replaces manual ticket reviews with an automated risk report that runs in seconds.
- Gives every flagged ticket a plain-English explanation with no interpreting charts or dashboards required.
- Produces an executive summary that tells a manager exactly where to focus and what to do next.
## All automations built independently. Ticket data is simulated and based on real workflows from my current role but contains no proprietary employer data.
## Steps
Risk Scoring - Three signals go into each ticket's score: how much of the SLA window is used up, how many open tickets the assignee is carrying, and how long it has been since the last update. Those combine into a score from 0 to 1. Anything above 0.75 gets flagged.
 
-------------------------------------------------------------------------------------------------
AI Ticket Analysis - Every flagged ticket gets sent to the Claude API with its full details and risk score. Claude comes back with a 2-3 sentence explanation of what is driving the risk and what action to take. A rule-based system can flag a ticket. It cannot tell you why it is actually going to breach.
 
<img width="1033" height="592" alt="Screenshot 2026-06-17 at 6 19 36 PM" src="https://github.com/user-attachments/assets/524943b2-78d4-4300-b6b4-31d67825479c" />

-------------------------------------------------------------------------------------------------
Executive Summary - After all flagged tickets are analyzed, the tool sends an aggregated picture to Claude: total tickets, at-risk count, assignee breakdown, category breakdown. Claude returns a 3-4 sentence summary with the biggest risk areas and what to do about them right now.
 
<img width="857" height="591" alt="Sample executive summary output" src="https://github.com/user-attachments/assets/77bee370-e8d3-47e9-9b46-6fb1bc44dcbf" />
-------------------------------------------------------------------------------------------------
Full Report Output - The terminal report shows every at-risk ticket with its score, assignee load, SLA consumption, and AI analysis, followed by on-track tickets and the executive summary at the bottom.
 
-------------------------------------------------------------------------------------------------
Demo - https://github.com/user-attachments/assets/bc7aba9c-7754-4dbd-aff5-f3a5b0e306cf


