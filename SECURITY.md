# Security Policy

## Supported Versions

BloxAPI is currently in active development. We provide security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take the security of BloxAPI seriously. If you believe you've found a security vulnerability, please follow these steps:

1. **Do not disclose the vulnerability publicly** until it has been addressed by our team.
2. Email your findings to [security@example.com](mailto:security@example.com). You should receive a response within 48 hours.
3. Provide detailed information about the vulnerability, including:
   - Steps to reproduce
   - Potential impact
   - Any suggested fixes (if available)

## Security Measures

BloxAPI implements the following security measures:

- Regular dependency updates through Dependabot
- Automated security scanning through GitHub Actions
- Code review for all changes to the codebase
- Input validation for all API endpoints
- Rate limiting to prevent abuse
- Proper error handling to prevent information disclosure

## Security Best Practices for Users

When deploying BloxAPI, we recommend the following security best practices:

1. Always use HTTPS in production
2. Set a strong, unique `SESSION_SECRET` environment variable
3. Regularly update to the latest version
4. Enable rate limiting in your proxy server
5. Monitor for unusual activity
6. Follow the principle of least privilege when setting up service accounts

## Responsible Disclosure

We encourage responsible disclosure of vulnerabilities following industry best practices. We promise not to pursue legal action against security researchers who:

- Make a good faith effort to avoid privacy violations, destruction of data, and disruption of services
- Only interact with accounts they own or have explicit permission to test
- Report vulnerabilities directly to us through the appropriate channels
- Keep vulnerability details private until we have addressed them

We appreciate your help in keeping BloxAPI and its users secure.