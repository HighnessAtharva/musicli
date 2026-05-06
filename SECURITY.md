# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 2.x     | ✅ Yes |
| 1.x     | ❌ No (EOL) |

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, email **highnessatharva@gmail.com** with the subject line:
`[musicli] Security Vulnerability Report`

Include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

You will receive a response within **72 hours**. We take all reports seriously and will investigate promptly.

## Scope

The following are **in scope**:

- Arbitrary code execution
- Credential leakage (API key exposure in logs, files, or error messages)
- Path traversal vulnerabilities in export/backup functionality
- Dependency vulnerabilities (please check [GitHub Advisory Database](https://github.com/advisories) first)

The following are **out of scope**:

- Social engineering attacks
- Denial of service on external APIs (Last.fm, OpenAI)
- Vulnerabilities in dependencies that do not affect musicli directly

## Security Best Practices for Users

1. **Protect your API keys**: Store `LASTFM_API_KEY`, `LASTFM_API_SECRET`, and `OPENAI_API_KEY` in a `.env` file with `chmod 600 .env`, not in shell history.
2. **Keep musicli updated**: Run `pip install --upgrade musicli` regularly.
3. **Review exported files**: HTML and Markdown exports contain your ratings data — be mindful of where you share them.
4. **Local AI mode**: Use `--local` with Ollama to keep your music library data on your machine instead of sending it to OpenAI.
