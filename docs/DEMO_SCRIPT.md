# 10–15 Minute Demo Script

## 0:00–1:00 — Task understanding

Explain that the module supports two input styles: a structured form for predictable data entry and an AI assistant for natural-language workflows.

## 1:00–3:30 — Frontend walkthrough

- Show the two-column Log HCP Interaction page.
- Search for and select an HCP.
- Show interaction type, date/time, attendees, topics, summary, materials, sentiment, outcome, and next steps.
- Submit one interaction using the structured form.

## 3:30–5:00 — Architecture

- Show the repository folders.
- Explain React + Redux, FastAPI, SQLAlchemy/PostgreSQL, LangGraph, and Groq.
- Open `docs/ARCHITECTURE.md` and explain the assistant → tools → assistant loop.

## 5:00–11:30 — Six tool demonstrations

1. `search_hcp`: “Find Dr. Sarah Mitchell.”
2. `log_interaction`: create a new interaction conversationally.
3. `add_product_sample`: add a sample to the new interaction ID.
4. `schedule_follow_up`: create a follow-up for that interaction.
5. `edit_interaction`: modify its sentiment or next step.
6. `get_interaction_history`: retrieve the HCP’s timeline.

After each prompt, point out the “Tools used” chips in the assistant panel.

## 11:30–13:00 — API and database

- Open FastAPI `/docs`.
- Show the interaction list endpoint.
- Explain that both UI modes persist through the same service layer.

## 13:00–15:00 — Closing

- Summarize the implemented requirements.
- Mention future production controls: authentication, audit logs, PHI safeguards, and observability.
