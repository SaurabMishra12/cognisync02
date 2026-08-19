# Connecting Faraday to Vibe-Coding Tools 

Your Faraday brain is now running as a highly secure, local application (`faraday-server`). 

Because it is bound strictly to `127.0.0.1` (your local machine), **it is physically impossible for the open internet or malicious actors to access your private data**. 

Here is how you connect your new local super-brain to different AI tools.

## 1. Connecting to Local Tools (Cursor, Antigravity, Cline)
Modern "vibe-coding" tools run locally on your PC, which means they can talk directly to your server with zero friction and zero security risk.

All you do is give the AI in Cursor or Antigravity the following instruction in your system prompt or custom rules:
> "Whenever you need context about me, my previous work, or my architecture, send an HTTP HTTP POST request to `http://localhost:8000/search` with the JSON payload `{"query": "your question here", "limit": 5}`. Use the returned markdown to fuel your code generation."

Because `faraday-server` handles the embeddings, you don't even need to manage APIs in Cursor. It just works.

## 2. Connecting to ChatGPT / Gemini Web Apps
ChatGPT and Gemini Web Apps exist on OpenAI/Google's servers. They cannot normally see your internal `localhost`. However, you want your data to remain secure. 

You have two secure options to pipe your context in:

### Option A: The Local Proxy API Script (Safest & Highly Recommended)
Instead of typing into the ChatGPT website, you run a small Python script locally that asks for your prompt. 
1. Your script hits `localhost:8000/search` and grabs your private Faraday Context.
2. The script *bundles* the context with your prompt and sends it to the OpenAI API or Gemini 1.5 Pro API.
3. The response prints to your terminal or a local React UI.
*Why it's secure:* Your database stays 100% offline. Only the specific text chunk needed for that specific question is ever sent to OpenAI.

### Option B: Encrypted Tunneling for "Custom GPTs"
If you absolutely must use the visual ChatGPT UI (the "Custom GPT" feature):
1. You run a secure tunnel like `ngrok` bound to your FastAPI server (`ngrok http 8000`).
2. You set up a **Bearer Token** in `faraday-server/main.py`.
3. You configure the Custom GPT Action to point to the ngrok URL and provide the secret Bearer Token.
4. *Why it's secure:* Even if someone guesses the URL, the bearer token prevents any data leakage. Turn off `ngrok` when you aren't using ChatGPT, and the connection vanishes safely.
