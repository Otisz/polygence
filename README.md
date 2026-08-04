# Matching take-home exercise

A slimmed-down slice of our mentor↔student matching flow.

When we propose a student to a mentor, the mentor receives an email with **Accept** and **Decline** links. Clicking a link records their decision, then we ask a short follow-up (match rating on accept, decline reasons on reject).

## The task

Ops has seen proposal records that look accepted but also contain decline reasons. That should never happen.

1. Run the project locally.
2. Reproduce the inconsistent state.
3. Explain what went wrong (briefly).
4. Fix it in a way you would be comfortable shipping.
5. Add tests that would have caught the issue.

You may change backend and/or frontend. Prefer fitting the existing structure unless a clear refactor improves correctness.

## Stack

- Backend: Django + Django REST Framework + SQLite
- Frontend: React + Vite
- Auth: none — proposal UUIDs in the URL act as capability tokens (same idea as production signed URLs)

## Setup

### Backend

Requires [uv](https://docs.astral.sh/uv/).

```bash
cd backend
uv sync
uv run python manage.py migrate
uv run python manage.py createsuperuser # optional, for /admin
uv run python manage.py seed_proposal
uv run python manage.py runserver
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:5173](http://localhost:5173).

## Useful surfaces

| Surface | URL |
|--------|-----|
| Dev inbox (email stand-in) | http://localhost:5173/ |
| Proposals (raw `response` JSON) | http://localhost:5173/proposals |
| Django admin | http://localhost:8000/admin/ |
| Accept / decline links | printed by `seed_proposal`, also in the inbox |

Re-seed anytime:

```bash
cd backend && uv run python manage.py seed_proposal
```

## Tests

```bash
cd backend
uv run python manage.py test matching
```

## Domain sketch

```
MentorRequest  (student looking for a mentor)
     │
     └── StudentProposal  (sent to one Mentor)
              └── response JSON:
                    value: "accept" | "reject"
                    reason: { ... }          # decline follow-up
                    match_rating: 0-10       # accept follow-up
                    recorded_at: ISO datetime
```

API:

- `POST /api/review-student/<uuid>/` — record accept/reject
- `PATCH /api/review-student/<uuid>/` — record reason / match rating
- `GET /api/proposal-active/<uuid>/` — whether the student is still open + current response value
- `GET /api/outbox/` — fake emails with links
- `GET /api/proposals/` — list proposals for debugging

## What we look for

- Correctness of the state transition
- Clear reasoning about root cause
- Sensible tests
- Changes that match (or thoughtfully improve) the patterns already in the repo

Timebox: aim for a few focused hours, not a rewrite of the whole app.
