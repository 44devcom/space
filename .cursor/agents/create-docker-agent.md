# Create Docker Agent

## Overview
This agent creates **boilerplate Docker configurations** for modern production environments and **automatically validates** them by building, starting, health-checking, and reviewing logs for every service.

## Core Responsibilities
- Generate multi-stage Dockerfiles
- Generate docker-compose.yml service blocks
- Add security-first configuration defaults
- Add standardized healthchecks
- Generate `.mdc` documentation with complete service reference:
  - Overview and purpose
  - Image information and version
  - Ports and access URLs
  - Environment variables (with security recommendations)
  - Volumes configuration
  - Complete docker-compose example
  - Framework-specific configuration examples (Laravel, FastAPI, Node.js, etc.)
  - Healthcheck configuration
  - Logs & debugging instructions
  - Notes and limitations
  - Testing examples
- Run automated Docker validation tests
- Provide a final PASS/FAIL report

The `.mdc` documentation should follow the structure and format of `docker-mailpit.mdc` as a template.

---

## Features
- Multi-stage build support
- Compose service generation
- Security best practices included
- Non-root runtime enforcement (when possible)
- Production-optimized builds
- Automatic healthcheck injection
- Auto-documentation per service
- Automatic Docker validation test after generation

---

## Workflow
1. Parse service type  
2. Generate Dockerfile  
3. Generate docker-compose service block  
4. Write `.mdc` service documentation (following `docker-mailpit.mdc` structure):
   - Overview section
   - Image information
   - Ports configuration
   - Environment variables with security notes
   - Volumes configuration
   - Complete docker-compose example
   - Framework-specific configuration examples
   - Healthcheck section
   - Logs & debugging section
   - Notes section
   - Testing section
5. Run automated Docker Test Suite  
6. Display results  
7. If failed → Show error logs  
8. If passed → Confirm successful validation  

---

## Standards
- Images pinned to major version
- Non-root user by default (if supported)
- Optimized layer caching
- Minimal surface area
- HEALTHCHECK required for all services
- Secrets instead of plaintext environment variables (when possible)
- Documentation follows `docker-mailpit.mdc` format and structure
- All code examples properly formatted with language tags
- Framework-specific examples included (Laravel, FastAPI, Node.js, Python, etc.)

---

## SSL Generation

If `domain`, `email`, `https`, or `ssl` are mentioned in the request:

- Generate Let's Encrypt ready Nginx configuration
- Generate ACME challenge root folder structure (`letsencrypt/`)
- Generate Diffie-Hellman parameter generation script (`scripts/generate-dhparam.sh`)
- Generate Let's Encrypt initialization script (`scripts/letsencrypt-init.sh`)
- Generate SSL renewal script (`scripts/renew-ssl.sh`)
- Add certbot service to docker-compose.yml
- Add SSL volumes (letsencrypt, dhparam) to docker-compose.yml
- Generate single enable-ssl.sh script for complete SSL setup
- Update Nginx configuration to include:
  - HTTP → HTTPS redirect
  - ACME challenge routing (`/.well-known/acme-challenge/`)
  - SSL/TLS configuration with modern ciphers
  - OCSP stapling
  - Diffie-Hellman parameters

### SSL Folder Structure Generated
```
nginx/
  conf/
    ssl.conf
    default.conf (redirect http→https)
letsencrypt/
dhparam/
scripts/
  generate-dhparam.sh
  letsencrypt-init.sh
  renew-ssl.sh
  enable-ssl.sh
```

### SSL Scripts Generated

#### generate-dhparam.sh
```bash
#!/usr/bin/env bash
mkdir -p ./dhparam
openssl dhparam -out ./dhparam/dhparam.pem 2048
```

#### renew-ssl.sh
```bash
#!/usr/bin/env bash
docker compose run certbot renew --dry-run
docker compose kill -s HUP nginx
```

#### enable-ssl.sh
```bash
#!/usr/bin/env bash
DOMAIN=$1
EMAIL=$2

if [ -z "$DOMAIN" ] || [ -z "$EMAIL" ]; then
  echo "Usage: ./enable-ssl.sh <domain> <email>"
  exit 1
fi

echo "[+] Generating dhparam..."
mkdir -p ./dhparam
openssl dhparam -out ./dhparam/dhparam.pem 2048

echo "[+] Running certbot for domain: $DOMAIN"
docker compose run certbot certonly \
  --webroot --webroot-path=/var/www/letsencrypt \
  --email $EMAIL --agree-tos --no-eff-email \
  -d $DOMAIN

echo "[+] Reloading Nginx"
docker compose restart nginx
```

---

# 🧪 **Automated Docker Validation Suite**

After creating the configuration, the agent must **automatically run all tests below**.

These tests are executed by the agent itself (not only printed).

If any step fails → the agent stops and prints diagnostics.

---

## 1. Build All Docker Images
```bash
docker compose build --no-cache
```
Fail if: build error appears in output.

## 2. Start All Services
```bash
docker compose up -d
sleep 5
```
Fail if: any container enters Exited or Restarting state.

## 3. Validate Container Status
```bash
docker compose ps --format json
```

Checks:
- All services must be running
- No container may be unhealthy
- No restarts > 0

Fail if any of these conditions are not met.

## 4. Validate Healthchecks
```bash
docker compose exec laravel php -v
docker compose exec fastapi python --version
docker compose exec mysql mysqladmin ping -uroot -p"$MYSQL_ROOT_PASSWORD"
docker compose exec redis redis-cli -a "$REDIS_PASSWORD" ping
docker compose exec nginx nginx -t
```
Each must return a success code.

## 5. Validate Connectivity
```bash
curl -f http://localhost:80 || exit 1
curl -f http://localhost:8000/health || exit 1

docker compose exec mysql \
  mysql -uroot -p"$MYSQL_ROOT_PASSWORD" \
  -e "SHOW DATABASES;" || exit 1

docker compose exec redis \
  redis-cli -a "$REDIS_PASSWORD" ping || exit 1
```

## 6. Check Logs for Errors
```bash
docker compose logs --tail=500 > docker-validation.log
grep -iE "error|panic|fatal|exception" docker-validation.log && exit 1
```

## 7. Shutdown and Cleanup
```bash
docker compose down
```

Optional full cleanup:
```bash
docker compose down -v
```

---

## ✅ Final Output Requirements

After tests finish, the agent must print:

### PASS SUMMARY
```
All Docker services validated successfully.
- All images built
- All containers healthy
- All connectivity checks passed
- No errors found in logs
```

### FAIL SUMMARY
```
Docker validation FAILED.
See below for diagnostics:

[LIST OF FAILED TESTS]
[RELEVANT LOG EXTRACTS]

Fix issues and run the agent again.
```