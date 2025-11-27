# Run UI Tests Command

## Purpose
Execute UI tests in the Dockerized test environment.

## Usage
```
/run ui-tests
```

## What It Does
- Starts required Docker services (if not running)
- Executes UI test suite using the configured tool
- Generates test reports
- Stores videos and screenshots in `reports/ui/`
- Displays test results summary
- Exits with proper status code (0 for success, non-zero for failure)

## Execution Flow
1. Check if Docker services are running
2. If not, start services using `docker-compose up -d`
3. Execute `tests/ui/run-ui-tests.sh` inside the UI test container
4. Collect test results
5. Generate HTML report
6. Store artifacts (videos, screenshots)
7. Display summary

## Output
- Test execution logs
- HTML test report in `reports/ui/`
- Videos in `reports/ui/videos/`
- Screenshots in `reports/ui/screenshots/`
- Error logs in `reports/ui/errors.log` (if failures occur)

## Integration
This command can be:
- Run manually during development
- Integrated into CI/CD pipelines
- Added to plan execution via `run-plan-agent`
