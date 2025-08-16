# Transcript Summarizer (MERN)

Upload a transcript (txt/pdf/docx), add a custom prompt, generate an AI summary (editable rich text), and share via email.

## Quick Start

### 1) Server
```bash
cd server
cp .env.example .env   # fill values (Mongo URL, OpenAI key, SMTP)
npm install
npm run dev
```
The API runs at http://localhost:4000 (health: `/api/health`).

### 2) Client
```bash
cd client
cp .env.example .env   # set VITE_API_URL if needed
npm install
npm run dev
```
Open the URL Vite prints (default http://localhost:5173).

## Notes
- Uses OpenAI Chat Completions with `gpt-4o-mini`. Change model/provider in `server/src/services/ai/openaiProvider.js`.
- Email uses SMTP via Nodemailer; configure `.env`.
- Uploaded files are stored temporarily in `server/uploads` and text is extracted and saved in MongoDB.
- Summaries are stored in MongoDB with both HTML and plain text.
- Rich text editing via React-Quill.

## Folder Structure
```
server/  # Express API
client/  # React + Vite UI
```

## Security
- This is a demo. Add authentication, rate limiting, file-type allowlists, and size limits before going to production.
```

