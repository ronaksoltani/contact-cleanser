# Contact Cleanser API

A small FastAPI service that normalizes email addresses and phone numbers and flags a short, editable list of disposable email domains. It returns a structured result instead of silently rewriting a user's input.

## Quick start

```bash
python -m venv .venv
python -m pip install -e .
uvicorn contact_cleanser.api:app --reload
```

Open `/docs` for the interactive API schema. `POST /v1/contacts/validate` accepts `{ "email": "person@example.com", "phone": "(415) 555-0100", "region": "US" }`. The phone region is an ISO 3166-1 alpha-2 code used when the phone input is not international.

## Response and privacy

The service has no database and intentionally does not log request bodies. Email syntax checks and the bundled disposable-domain sample list are best-effort; they cannot prove that a mailbox exists. Add a consent and retention policy before using real contact data in production.

## Learning notes

This project practices request/response models, dependency management, pure normalization functions, and HTTP status handling. Phone parsing uses Google's `phonenumbers` data rather than an ad hoc regex.

## Development

```bash
python -m pip install -e ".[dev]"
pytest
```

## License

MIT. See [LICENSE](LICENSE).
