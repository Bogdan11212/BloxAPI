# Security Policy

## Supported Versions

We currently provide security updates for the following versions of BloxAPI:

| Version | Supported          |
| ------- | ------------------ |
| 2.x.x   | :white_check_mark: |
| 1.5.x   | :white_check_mark: |
| 1.0.x-1.4.x | :x:           |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take the security of BloxAPI seriously. If you believe you've found a security vulnerability, please follow these steps:

1. **Do not disclose the vulnerability publicly**
2. **Email us at security@bloxapi.com** with details about the vulnerability
3. Include the following information in your report:
   - Type of vulnerability
   - Full path to source file(s) related to the issue
   - Steps to reproduce
   - Potential impact
   - Suggested fix if possible

## Response Timeline

- We will acknowledge receipt of your vulnerability report within 48 hours
- We will provide a more detailed response within 7 days
- We aim to release a fix within 30 days, depending on the severity and complexity of the issue
- We will keep you informed of our progress throughout the process

## Security Best Practices

When using BloxAPI, we recommend following these security best practices:

### API Keys and Authentication

- Never hardcode API keys or authentication credentials in your source code
- Use environment variables or secure key management systems to store sensitive credentials
- Rotate API keys regularly
- Use the minimum permissions necessary for your application

### Rate Limiting and Throttling

- Implement rate limiting in your applications to prevent abuse
- Respect Roblox API rate limits to avoid being blocked
- Use the built-in rate limiting features in BloxAPI

### Data Handling

- Validate all input data before processing
- Sanitize user input to prevent injection attacks
- Be cautious when storing or logging data that might contain sensitive information

### Network Security

- Use HTTPS for all API requests
- Verify SSL/TLS certificates
- Consider using a proxy or API gateway for additional security

### Deployment Security

- Keep all dependencies updated
- Regularly check for security advisories
- Use least privilege principles for service accounts

## Security Features

BloxAPI includes several security features:

- TLS/SSL support for secure communications
- Input validation and sanitization
- Rate limiting and throttling
- Detailed error logging for security events
- Authentication and authorization controls

## Vulnerability Disclosure Policy

We believe in responsible disclosure of security vulnerabilities. After we've addressed a security issue:

1. We will publish a security advisory through GitHub's security advisory feature
2. We will credit the reporter (unless anonymity is requested)
3. We will provide details about the vulnerability, its impact, and how to remediate it

## Security Updates

Security updates are delivered through our standard release channels. For critical vulnerabilities, we may issue out-of-cycle releases.

To ensure you're using a secure version:

- Subscribe to GitHub security advisories for this repository
- Watch our releases on GitHub
- Follow our announcements on Twitter: [@BloxAPI](https://twitter.com/bloxapi)

## Security Contact

For security-related inquiries or to report vulnerabilities:

- Email: security@bloxapi.com
- PGP Key: [Download PGP Key](https://bloxapi.com/security/pgp-key.asc)

Fingerprint: `5F3D F123 B8FC A987 D367 7B21 A76D 9C36 F418 EA45`