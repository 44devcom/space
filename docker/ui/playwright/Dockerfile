# Playwright Docker image for UI testing
FROM mcr.microsoft.com/playwright:v1.40.0-focal

WORKDIR /app

# Copy package.json and install dependencies
COPY tests/ui/package.json /app/package.json
RUN npm install

# Install Playwright browsers (already installed in base image, but ensure chromium)
RUN npx playwright install chromium

# Copy test files
COPY tests/ui /app/tests/ui
COPY tests/ui/playwright.config.ts /app/playwright.config.ts

ENV BASE_URL=${BASE_URL:-http://api:8000}
ENV CI=1

CMD ["npx", "playwright", "test", "--project=chromium"]

