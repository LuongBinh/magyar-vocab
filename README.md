# Magyar Vocab

Hungarian vocabulary app with IPA pronunciation, English meanings, and mnemonics. Now includes an LLM-powered translator.

## Features

- **4,550 Hungarian words** with IPA, English meaning, and mnemonic.
- **Search & filter** by letter, difficulty, and bookmarks.
- **Card / list views** with bookmarking.
- **Light / dark theme**.
- **Translator tab** — translate English, Vietnamese, or Hungarian to natural conversational Hungarian/English using an LLM API, with the local wordlist as a dictionary reference.

## Tech stack

- Next.js 14 (Pages Router)
- React 18
- CSS variables for theming
- OpenAI-compatible LLM API (e.g., OpenAI, DeepSeek, etc.)

## Local development

```bash
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

## Environment variables

Create a `.env.local` file based on `.env.example`:

```env
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-3.5-turbo
```

For DeepSeek, use:

```env
OPENAI_BASE_URL=https://api.deepseek.com
OPENAI_API_KEY=your_deepseek_key_here
OPENAI_MODEL=deepseek-chat
```

## Deployment on Vercel

1. Push the repo to GitHub.
2. Import the project on [Vercel](https://vercel.com).
3. Add the environment variables (`OPENAI_BASE_URL`, `OPENAI_API_KEY`, `OPENAI_MODEL`) in the Vercel dashboard under **Project Settings > Environment Variables**.
4. Deploy.

## Translator behavior

- The translator scans the input text and finds matching entries from the local 4,550-word database.
- Those entries are sent to the LLM as a reference dictionary, ensuring translations align with the meanings used in the app.
- The LLM is free to produce natural conversational language; it is not restricted to only the listed words.
