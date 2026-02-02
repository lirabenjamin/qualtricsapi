# Security Best Practices

## Protecting Your API Credentials

### Never Commit Credentials to Version Control

Your Qualtrics API token provides full access to your account. **Never** hardcode it in your scripts or commit it to version control.

### ✅ Good Practice: Use .env File

```python
import os
from dotenv import load_dotenv
from qualtrics_api import QualtricsAPI

load_dotenv()

api = QualtricsAPI(
    api_token=os.getenv('QUALTRICS_API_TOKEN'),
    data_center=os.getenv('QUALTRICS_DATA_CENTER')
)
```

### ❌ Bad Practice: Hardcoding Credentials

```python
# DON'T DO THIS!
api = QualtricsAPI(
    api_token='aKt5gjvd0dmecW9Lykba2ZTEF8YF0wG9MeFTm6Ab',
    data_center='upenn.qualtrics.com'
)
```

## File Security Checklist

- [x] `.env` is listed in `.gitignore`
- [x] `.env.example` has placeholder values only
- [x] All scripts load credentials from `.env`
- [ ] Never share your `.env` file
- [ ] Rotate your API key if accidentally exposed

## What's Protected

The following files are in `.gitignore` and won't be committed:

- `.env` - Your actual credentials
- `venv/` - Virtual environment
- `__pycache__/` - Python cache files

## If Your API Key is Exposed

1. **Immediately** generate a new API key in Qualtrics
2. Delete the old key
3. Update your `.env` file with the new key
4. If exposed in a git repo, consider the key permanently compromised

## Additional Recommendations

- Use separate API keys for development and production
- Limit API key permissions if possible
- Regularly rotate your API keys
- Never log or print API tokens
- Use environment-specific `.env` files (`.env.development`, `.env.production`)

## Getting Your API Token

1. Log in to Qualtrics
2. Go to Account Settings > Qualtrics IDs
3. Generate a new API token
4. Copy it to your `.env` file immediately
5. Never share it

## Questions?

If you believe your API key has been compromised, contact Qualtrics support immediately.
