# Security Policy

## Supported versions

This repository contains AI skill files (markdown + YAML). There is no versioned software package or runtime artifact — the current `main` branch is the only supported version.

## Reporting a vulnerability

If you discover a security issue in this repository — exposed credentials, a prompt injection risk in a skill, or a vulnerability in the Python scripts — please report it privately:

https://github.com/jeckyl2010/skills/security/advisories/new

Do not open a public issue for security concerns.

## Scope

- Credentials or secrets accidentally committed
- Prompt injection patterns in skill content that could cause harm if loaded by an AI agent
- Vulnerabilities in `scripts/validate.py` or `scripts/index_builder.py`

Out of scope: opinions on skill content, style, or coverage.
