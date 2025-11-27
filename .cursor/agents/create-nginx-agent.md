# Create Nginx Agent

## Purpose
Generate Nginx reverse proxy configuration with SSL/HTTPS support.

## Inputs
- Domain name (optional)
- SSL/HTTPS requirements
- Backend service configuration (Laravel, FastAPI, Node.js)
- Static file serving requirements

## Outputs
- Nginx configuration files
- SSL configuration (if domain/email provided)
- ACME challenge routing
- Docker Compose service block

## Workflow
1. Detect if SSL is required (domain, email, https keywords present)
2. Generate Nginx configuration:
   - If domain present: use HTTPS configuration template with Let's Encrypt
   - Else: generate HTTP-only template
3. Generate SSL redirect rules (HTTP → HTTPS)
4. Generate ACME challenge handling (`/.well-known/acme-challenge/`)
5. Generate SSL/TLS configuration with modern ciphers
6. Generate Docker Compose service block
7. Generate SSL scripts (if SSL enabled):
   - generate-dhparam.sh
   - letsencrypt-init.sh
   - renew-ssl.sh
   - enable-ssl.sh

## SSL Configuration Rules
- Must include HTTP → HTTPS redirect
- Must route ACME challenges to `/var/www/letsencrypt`
- Must use TLSv1.2 and TLSv1.3 only
- Must include Diffie-Hellman parameters
- Must enable OCSP stapling
- Must set proper security headers

## Integration
- Integrates with create-docker-agent for SSL generation
- Works with certbot service in Docker Compose
- Supports Laravel, FastAPI, and Node.js backends

