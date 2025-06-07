# Peptidesource

Simple FastAPI server that forwards chat prompts to the OpenAI API.

```
source venv/bin/activate
pip install -r requirements.txt
uvicorn server:app --reload
```

Set `OPENAI_API_KEY` in your environment before starting the server.

Example chat request:

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Hello"}'
```
