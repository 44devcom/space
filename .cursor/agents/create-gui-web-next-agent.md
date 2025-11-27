# Next.js Web GUI Agent

## Purpose
Generate a complete web GUI using:
- Next.js 14 App Router
- ShadCN UI
- Tailwind CSS
- Mermaid.js
- Monaco editor

## Workflow
1. Load Next.js rules.
2. Scaffold folder structure.
3. Install ShadCN + Tailwind definitions.
4. Generate:
   - Dashboard
   - Plan Viewer
   - Layers/DAG viewer
   - Logs/Console
   - SSL & Certificates screen
   - MermaidRenderer
   - JSON Editor
   - Task status widgets
   - SSL components:
     - SSLStatusCard.tsx
     - SSLCertTimeline.tsx
     - SSLActionButtons.tsx
     - NginxConfigEditor.tsx (with Monaco Editor)
5. Integrate API calls via React Query:
   - Plan/agent APIs
   - SSL APIs: /api/ssl/status, /api/ssl/enable, /api/ssl/renew, /api/ssl/reload-nginx, /api/ssl/nginx-config
6. Use SSE/WebSocket for live updates.
7. Provide `package.json`, `next.config.js`.

## Output
A ready-to-start dev environment:

```bash
cd gui/web/next
npm install
npm run dev
```

