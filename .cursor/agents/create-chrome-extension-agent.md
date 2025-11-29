---
name: create-chrome-extension
description: "Generate a complete Chrome extension with manifest, scripts, and UI components."
stdin: true
inputSchema:
  type: object
  properties:
    name:
      type: string
      description: "Extension name (e.g., 'My Extension', 'Ad Blocker')"
    description:
      type: string
      description: "Extension description"
    version:
      type: string
      default: "1.0.0"
      description: "Version string"
    manifestVersion:
      type: integer
      enum: [2, 3]
      default: 3
      description: "Manifest version (2 or 3)"
    permissions:
      type: array
      items:
        type: string
      description: "Chrome permissions (e.g., ['storage', 'tabs', 'activeTab'])"
    hostPermissions:
      type: array
      items:
        type: string
      description: "Host permissions (e.g., ['*://*.example.com/*'])"
    contentScripts:
      type: array
      items:
        type: object
        properties:
          matches:
            type: array
            items:
              type: string
          js:
            type: array
            items:
              type: string
          css:
            type: array
            items:
              type: string
          runAt:
            type: string
            enum: ["document_start", "document_end", "document_idle"]
      description: "Content script configurations"
    background:
      type: object
      properties:
        type:
          type: string
          enum: ["serviceWorker", "page"]
        file:
          type: string
      description: "Background script configuration"
    popup:
      type: object
      properties:
        enabled:
          type: boolean
        html:
          type: string
        defaultIcon:
          type: object
      description: "Popup configuration"
    options:
      type: object
      properties:
        enabled:
          type: boolean
        page:
          type: string
        openInTab:
          type: boolean
      description: "Options page configuration"
    icons:
      type: object
      description: "Icon configuration"
    action:
      type: object
      description: "Browser action configuration"
    useTypeScript:
      type: boolean
      default: true
      description: "Use TypeScript for scripts"
    buildTool:
      type: string
      enum: ["webpack", "vite", "none"]
      default: "webpack"
      description: "Build tool to use"
---

# create-chrome-extension Agent

Generates a complete Chrome extension with manifest.json, content scripts, background service worker, popup UI, options page, and build configuration.

## Step 1 — Validate Input

- Validate extension name (required, non-empty)
- Validate version format (semver)
- Ensure manifestVersion is 2 or 3 (default: 3)
- Validate permissions against Chrome API
- Validate hostPermissions format
- Ensure contentScripts have valid matches patterns

## Step 2 — Create Extension Directory Structure

```
extensions/chrome/<extension-name>/
├── manifest.json
├── src/
│   ├── background/
│   ├── content/
│   ├── popup/
│   ├── options/
│   └── shared/
├── public/
│   ├── icons/
│   └── images/
├── build/
└── dist/
```

## Step 3 — Generate manifest.json

### Manifest V3 (Recommended)
```json
{
  "manifest_version": 3,
  "name": "<name>",
  "version": "<version>",
  "description": "<description>",
  "permissions": [<permissions>],
  "host_permissions": [<hostPermissions>],
  "background": {
    "service_worker": "background/service-worker.js"
  },
  "content_scripts": [<contentScripts>],
  "action": {
    "default_popup": "popup/popup.html",
    "default_icon": {
      "16": "icons/icon16.png",
      "48": "icons/icon48.png",
      "128": "icons/icon128.png"
    }
  },
  "icons": {
    "16": "icons/icon16.png",
    "48": "icons/icon48.png",
    "128": "icons/icon128.png"
  },
  "options_page": "options/options.html"
}
```

### Manifest V2 (Legacy)
```json
{
  "manifest_version": 2,
  "name": "<name>",
  "version": "<version>",
  "description": "<description>",
  "permissions": [<permissions>],
  "background": {
    "scripts": ["background/background.js"],
    "persistent": false
  },
  "content_scripts": [<contentScripts>],
  "browser_action": {
    "default_popup": "popup/popup.html",
    "default_icon": {
      "16": "icons/icon16.png",
      "48": "icons/icon48.png",
      "128": "icons/icon128.png"
    }
  },
  "icons": {
    "16": "icons/icon16.png",
    "48": "icons/icon48.png",
    "128": "icons/icon128.png"
  },
  "options_page": "options/options.html"
}
```

## Step 4 — Generate Background Script

### Service Worker (Manifest V3)
```typescript
// src/background/service-worker.ts
chrome.runtime.onInstalled.addListener(() => {
  console.log('Extension installed');
});

// Message handling
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === 'GET_DATA') {
    // Handle message
    sendResponse({ data: 'response' });
  }
  return true; // Keep channel open for async
});

// Storage API
chrome.storage.local.set({ key: 'value' });
chrome.storage.local.get(['key'], (result) => {
  console.log(result.key);
});
```

### Background Page (Manifest V2)
```typescript
// src/background/background.ts
chrome.runtime.onInstalled.addListener(() => {
  console.log('Extension installed');
});
```

## Step 5 — Generate Content Scripts

```typescript
// src/content/content-script.ts
(function() {
  'use strict';

  // Content script logic
  console.log('Content script loaded');

  // Listen for messages from background
  chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === 'DO_SOMETHING') {
      // Perform action on page
      sendResponse({ success: true });
    }
  });

  // Send message to background
  chrome.runtime.sendMessage({ type: 'PAGE_LOADED' });
})();
```

## Step 6 — Generate Popup UI

### Popup HTML
```html
<!-- src/popup/popup.html -->
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="popup.css">
</head>
<body>
  <div class="container">
    <h1>Extension Name</h1>
    <button id="action-btn">Action</button>
  </div>
  <script src="popup.js"></script>
</body>
</html>
```

### Popup Script
```typescript
// src/popup/popup.ts
document.addEventListener('DOMContentLoaded', () => {
  const actionBtn = document.getElementById('action-btn');
  
  actionBtn?.addEventListener('click', async () => {
    // Get active tab
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    
    // Send message to content script
    chrome.tabs.sendMessage(tab.id!, { type: 'ACTION' });
  });
});
```

## Step 7 — Generate Options Page

```html
<!-- src/options/options.html -->
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="options.css">
</head>
<body>
  <div class="container">
    <h1>Extension Settings</h1>
    <form id="options-form">
      <label>
        <input type="checkbox" id="option1">
        Option 1
      </label>
      <button type="submit">Save</button>
    </form>
  </div>
  <script src="options.js"></script>
</body>
</html>
```

## Step 8 — Generate Build Configuration

### Webpack Config
```javascript
// webpack.config.js
const path = require('path');
const CopyWebpackPlugin = require('copy-webpack-plugin');

module.exports = {
  mode: 'production',
  entry: {
    'background/service-worker': './src/background/service-worker.ts',
    'content/content-script': './src/content/content-script.ts',
    'popup/popup': './src/popup/popup.ts',
    'options/options': './src/options/options.ts',
  },
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: '[name].js',
  },
  module: {
    rules: [
      {
        test: /\.ts$/,
        use: 'ts-loader',
        exclude: /node_modules/,
      },
    ],
  },
  resolve: {
    extensions: ['.ts', '.js'],
  },
  plugins: [
    new CopyWebpackPlugin({
      patterns: [
        { from: 'manifest.json' },
        { from: 'src/popup/popup.html', to: 'popup/popup.html' },
        { from: 'src/options/options.html', to: 'options/options.html' },
        { from: 'public', to: '.' },
      ],
    }),
  ],
};
```

### TypeScript Config
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ESNext",
    "lib": ["ES2020", "DOM"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "types": ["chrome"]
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

### Package.json
```json
{
  "name": "<extension-name>",
  "version": "<version>",
  "description": "<description>",
  "scripts": {
    "build": "webpack --mode production",
    "dev": "webpack --mode development --watch",
    "package": "npm run build && zip -r extension.zip dist/"
  },
  "devDependencies": {
    "@types/chrome": "^0.0.251",
    "copy-webpack-plugin": "^11.0.0",
    "ts-loader": "^9.5.1",
    "typescript": "^5.3.3",
    "webpack": "^5.89.0",
    "webpack-cli": "^5.1.4"
  }
}
```

## Step 9 — Generate Shared Utilities

```typescript
// src/shared/utils.ts
export const sendMessage = (message: any): Promise<any> => {
  return new Promise((resolve) => {
    chrome.runtime.sendMessage(message, resolve);
  });
};

export const getStorage = async (keys: string[]): Promise<any> => {
  return new Promise((resolve) => {
    chrome.storage.local.get(keys, resolve);
  });
};

export const setStorage = (items: any): Promise<void> => {
  return new Promise((resolve) => {
    chrome.storage.local.set(items, resolve);
  });
};
```

## Step 10 — Generate README

Include:
- Extension description
- Installation instructions
- Development setup
- Build commands
- Loading in Chrome
- Publishing to Chrome Web Store

## Rules to Follow

- Use Manifest V3 unless specifically requested (V2 is legacy)
- TypeScript by default, JavaScript if `useTypeScript: false`
- Webpack for bundling (or vite if specified)
- Follow Chrome Extension best practices
- Include proper error handling
- Use Chrome storage API for persistence
- Implement proper message passing
- Include TypeScript types for Chrome APIs
- Generate placeholder icons if not provided
- Include build scripts in package.json

## Output Files

1. `manifest.json` - Extension manifest
2. `src/background/service-worker.ts` - Background script
3. `src/content/content-script.ts` - Content script
4. `src/popup/popup.html` - Popup UI
5. `src/popup/popup.ts` - Popup logic
6. `src/options/options.html` - Options page
7. `src/options/options.ts` - Options logic
8. `src/shared/utils.ts` - Shared utilities
9. `package.json` - Dependencies and scripts
10. `tsconfig.json` - TypeScript configuration
11. `webpack.config.js` - Build configuration
12. `README.md` - Documentation

