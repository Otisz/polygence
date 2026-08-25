# Matching take-home exercise

A slimmed-down slice of our mentor↔student matching flow.

When we propose a student to a mentor, the mentor receives an email with **Accept** and **Decline** links. Clicking a
link records their decision, then we ask a short follow-up (match rating on accept, decline reasons on reject).

## The task

Ops has seen proposal records that look accepted but also contain decline reasons. That should never happen.

1. Run the project locally.
    - > I don't have any runtime on my machine, so I dockerized it.
2. Reproduce the inconsistent state.
    1. > Click on the accept link
    2. > Leave the page
    3. > Click on the decline link
    4. > Submit the form
3. Explain what went wrong (briefly).
    1. > On page load (frontend) the `useEffect` calls the `api.updateReviewStudent` function that will set the status
       of the proposal. \
       Calling API inside `useEffect` is a bad practice.
    2. > On submit, the form does not set the `{response: "accept" | "reject"}` value, therefor the first action state
       will be saved, and it might be stale
4. Fix it in a way you would be comfortable shipping.
    - > "Comfortable" is very subjective. The "what would I refactor" is below.

5. Add tests that would have caught the issue.
    - > For the sake of the homework, I wrote a failing test for the route which is buggy.
    - > I also created a new route for the fixed version.

You may change backend and/or frontend. Prefer fitting the existing structure unless a clear refactor improves
correctness.

> Only minimal code changes has been done to fix the bug.
>
> What would I refactor:
> 1. The frontend has way too much `useEffect`, this should be close to zero, and also too much useState. Eliminating
     these two can be achieved via TanStack Query (and optionally with Axios). Using this tool also removes the
     `useEffect`'s side effect, which is running twice in development environment. It has its own store, therefor most
     of the `useState`s can be removed too. We can get achieve the same functionality with much more options like
     refething or mutating data.
> 2. Just by opening the proposal accept or reject link, updating state should not be called. The user is not aware of
     this action which is a bad practise in the first place.
> 3. I would split the accept and reject functionality on the backend. Accepting and rejecting would have different
     URLs, and both function sets the corresponding state by itself, so a request cannot forge an invalid state. Is this
     against the DRY principle? Yes, but who cares, just a few line of codes, but it removes `if` statements and
     unnecessary cognitive load.
> 4. Adding form validation at least on the backend. Currently, a request can be forged, and it could contain something
     like `{matching_rate: 69420}`, which is technically a valid data, so the backend will save it, unless the database
     using smallint column which will cause an SQL error. \
     On the frontend I would install TanStack Form and Zod for better DX, and removing requests with invalid data by
     implementing the same validations as the backend does.
> 5. Hiding the accept/reject forms from the OP if it was already submitted, and displaying a message accordingly. \
     If the OP wants to change the decision, then a separate functionality should allow this.

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

### Docker

Requires Docker with the Compose plugin. Builds both services and starts them with hot reload; the source tree is
bind-mounted, so edits on the host apply straight away.

```bash
docker compose up --build
```

**`migrate` is required on first boot** — the containers start before any database exists, and every page returns a "no
such table" error until you run it:

```bash
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py seed_proposal
docker compose exec backend python manage.py createsuperuser # optional, for /admin
```

Same URLs as the bare-metal setup. Tests:

```bash
docker compose exec backend python manage.py test matching
```

Override the published ports with `FORWARD_FE_PORT` / `FORWARD_BE_PORT`, and the container user with `APP_UID` /
`APP_GID`.

## Useful surfaces

| Surface                         | URL                                           |
|---------------------------------|-----------------------------------------------|
| Dev inbox (email stand-in)      | http://localhost:5173/                        |
| Proposals (raw `response` JSON) | http://localhost:5173/proposals               |
| Django admin                    | http://localhost:8000/admin/                  |
| Accept / decline links          | printed by `seed_proposal`, also in the inbox |

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
