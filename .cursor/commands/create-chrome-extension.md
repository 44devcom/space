---
globs:
  - "extensions/chrome/**/*"
  - "schemas/extensions/chrome/*.json"
description: "Create a new Chrome extension with manifest, content scripts, background scripts, and popup."
alwaysApply: false
---

# Create Chrome Extension

Generates a new Chrome extension with complete structure including manifest.json, content scripts, background service worker, popup UI, options page, and build configuration.

This command uses:
- Chrome Extension Manifest V3 specifications
- Project `.mdc` rules
- TypeScript/JavaScript conventions

## Parameters

- `name`: Extension name (e.g., "My Extension", "Ad Blocker")
- `description`: Extension description
- `version`: Version string (default: "1.0.0")
- `manifestVersion`: Manifest version (2 or 3, default: 3)
- `permissions`: Array of Chrome permissions (e.g., ["storage", "tabs", "activeTab"])
- `hostPermissions`: Array of host permissions (e.g., ["*://*.example.com/*"])
- `contentScripts`: Array of content script configurations
- `background`: Background script configuration (service worker or page)
- `popup`: Popup HTML/JS configuration
- `options`: Options page configuration
- `icons`: Icon sizes and paths
- `action`: Browser action configuration

## Output Structure

```
extensions/chrome/<extension-name>/
├── manifest.json
├── src/
│   ├── background/
│   │   └── service-worker.ts (or .js)
│   ├── content/
│   │   └── content-script.ts (or .js)
│   ├── popup/
│   │   ├── popup.html
│   │   ├── popup.ts (or .js)
│   │   └── popup.css
│   ├── options/
│   │   ├── options.html
│   │   ├── options.ts (or .js)
│   │   └── options.css
│   └── shared/
│       └── utils.ts (or .js)
├── public/
│   ├── icons/
│   │   ├── icon16.png
│   │   ├── icon48.png
│   │   └── icon128.png
│   └── images/
├── build/
│   └── (compiled output)
├── package.json
├── tsconfig.json (if TypeScript)
├── webpack.config.js (or vite.config.js)
└── README.md
```

## Example Usage

```
/create-chrome-extension AdBlocker
```

Or with more detail:

```json
{
  "name": "AdBlocker",
  "description": "Blocks ads on websites",
  "version": "1.0.0",
  "manifestVersion": 3,
  "permissions": ["storage", "tabs", "webRequest", "webRequestBlocking"],
  "hostPermissions": ["<all_urls>"],
  "contentScripts": [
    {
      "matches": ["<all_urls>"],
      "js": ["content-script.js"],
      "runAt": "document_start"
    }
  ],
  "background": {
    "type": "serviceWorker",
    "file": "service-worker.js"
  },
  "popup": {
    "enabled": true,
    "html": "popup.html"
  }
}
```

## Generated Files

- `manifest.json` - Extension manifest (V2 or V3)
- Content scripts for page interaction
- Background service worker for extension logic
- Popup UI for quick actions
- Options page for settings
- Build configuration (webpack/vite)
- TypeScript configuration (if TypeScript enabled)
- Package.json with dependencies

## Features

- Manifest V3 support (recommended)
- TypeScript support (optional)
- Modern build tools (webpack/vite)
- Content script injection
- Background service worker
- Popup UI
- Options page
- Chrome storage API integration
- Message passing between components

