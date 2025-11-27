# Create Docker Command

## Purpose
Generate **production-ready Docker service configurations** and  
automatically validate them using the full Docker Test Suite.

This command works closely with the **Create Docker Agent**, which handles
service generation and end-to-end validation.

---

## Usage
```
/create docker <service>
```

### Examples
```bash
/create docker laravel
/create docker fastapi
/create docker redis
```

---

## Supported Services
- **laravel**
- **mysql**
- **fastapi**
- **nginx**
- **redis**

---

## Output
When invoked, this command triggers the agent to produce:

- Production-ready **Dockerfile**
- `docker-compose.yml` **service block**
- Service documentation file (`*.mdc`) with:
  - Overview and purpose
  - Image information
  - Ports and access URLs
  - Environment variables (with security recommendations)
  - Volumes configuration
  - Complete docker-compose example
  - Framework-specific configuration examples (Laravel, FastAPI, etc.)
  - Healthcheck configuration
  - Logs & debugging instructions
  - Notes and limitations
  - Testing examples
- **Security-enforced** configuration defaults
- **Healthchecks** added automatically
- CI/CD-ready **validation rules**
- Automated **Docker Test Suite execution**
- PASS/FAIL validation summary

The generated `.mdc` documentation follows the same structure as `docker-mailpit.mdc` for consistency.

---

# 🧪 Automated Testing (Executed Automatically)

After generating the Docker configuration, the command **must automatically execute**
the same validation pipeline defined in the Create Docker Agent:

---

## 1. Build all images
(Executed automatically)
```bash
docker compose build --no-cache
```

## 2. Start all services
(Executed automatically)
```bash
docker compose up -d
sleep 5
```

## 3. Check container status
(Executed automatically)
```bash
docker compose ps --format json
```

Validation includes:
- All containers must be running
- No container may be restarting
- No container may be unhealthy

## 4. Test healthchecks
(Executed automatically)
```bash
docker compose exec laravel php -v
docker compose exec fastapi python --version
docker compose exec mysql mysqladmin ping -uroot -p"$MYSQL_ROOT_PASSWORD"
docker compose exec redis redis-cli -a "$REDIS_PASSWORD" ping
docker compose exec nginx nginx -t
```

If a service is not applicable (e.g., Laravel not present), the agent skips safely.

## 5. Capture logs and scan for errors
(Executed automatically)
```bash
docker compose logs --tail=500 > docker-validation.log
grep -iE "error|panic|fatal|exception" docker-validation.log
```

If matches are found → FAIL.

## 6. Test service connectivity
(Executed automatically)
```bash
curl -f http://localhost:80 || exit 1
curl -f http://localhost:8000/health || exit 1

docker compose exec mysql mysql -uroot -p"$MYSQL_ROOT_PASSWORD" -e "SHOW DATABASES;"
docker compose exec redis redis-cli -a "$REDIS_PASSWORD" ping
```

Connectivity failures trigger an immediate error.

## 7. Shutdown and cleanup
(Executed automatically)
```bash
docker compose down
```

Optional full cleanup:
```bash
docker compose down -v
```

---

## ✅ Final Output

After all tests complete, the command prints a structured summary.

### PASS Summary
```
Docker validation successful.
All images built and all services passed health and connectivity checks.
```

### FAIL Summary
```
Docker validation FAILED.
[Detailed error logs]
[Failed step]
[Recommendations]
```