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
In a real environment this data would be pulled directly from a ticketing system like Zendesk or ServiceNow. For this project, I used Claude to generate a realistic mock dataset that mirrors what a live support queue looks like, with fields for SLA window, ticket age, assignee workload, and last update time.

<img width="1033" height="592" alt="Screenshot 2026-06-17 at 6 19 36 PM" src="https://github.com/user-attachments/assets/524943b2-78d4-4300-b6b4-31d67825479c" />

-------------------------------------------------------------------------------------------------
Two files power the whole thing. The CSV holds the ticket data and the Python script does the scoring, calls the Claude API, and builds the report. Nothing else needed.

<img width="1149" height="505" alt="Screenshot 2026-06-17 at 6 10 56 PM" src="https://github.com/user-attachments/assets/a456705a-f616-425b-9c0f-4c61fe0c2b46" />

-------------------------------------------------------------------------------------------------
The scoring logic weighs three signals per ticket: how much of the SLA window is used up, how many open tickets the assignee is carrying, and how long since the last update. Anything scoring above 0.75 gets flagged. From there the Claude API takes over and generates a plain-English explanation for each flagged ticket and an executive summary at the end.

<img width="1710" height="1072" alt="Screenshot 2026-06-17 at 6 11 33 PM" src="https://github.com/user-attachments/assets/f4945e40-dafa-4de6-b5bc-606cac05eb48" />

<img width="1707" height="952" alt="Screenshot 2026-06-17 at 6 25 00 PM" src="https://github.com/user-attachments/assets/f538c701-12e5-4bd2-b70f-0af0961ffaa8" />

 
-------------------------------------------------------------------------------------------------
Demo - [![SLA Breach Predictor Demo](https://img.youtube.com/vi/PAlvik8sW00/0.jpg)](https://www.youtube.com/watch?v=PAlvik8sW00)


