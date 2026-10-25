# Production hardening

The recruiter product now includes a reusable production platform layer. Set `DATABASE_URL` to managed PostgreSQL in cloud environments; local development falls back to SQLite. `SECRET_KEY` signs login tokens, `SENTRY_DSN` enables optional error tracking, and `RATE_LIMIT_PER_MINUTE` controls API throttling.

Accounts receive an admin/user role; the first account for this project becomes admin. Authenticated users can issue API keys and register model versions/experiments. Admins can view platform counts and export audit events as CSV.

The job URL importer accepts only public HTTP(S) pages, blocks private/local network targets and caps fetched content. It is deliberately provider-neutral and does not bypass authentication, paywalls, robots rules or site terms.

`VERSION` follows semantic versioning; pushing `v*` tags triggers the release workflow.
