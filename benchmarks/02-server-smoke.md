# 02 — llama.cpp Server Smoke Test

## Server

- Host: `http://127.0.0.1:8080`
- Backend: CUDA
- Model: Qwen2.5-7B-Instruct Q4_K_M
- API compatibility: OpenAI-style `/v1/chat/completions`

## GET /v1/models

~~~json
{
  "object": "list",
  "data": [
    {
      "id": "/home/emin98/labs/Day20-Track2-ModelServing-Lab/models/qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf",
      "object": "model",
      "owned_by": "me",
      "permissions": []
    }
  ]
}
~~~

## POST /v1/chat/completions

Request:

~~~json
{
  "model": "local-model",
  "messages": [
    {
      "role": "user",
      "content": "Reply with exactly one word: OK"
    }
  ],
  "temperature": 0,
  "max_tokens": 8
}
~~~

Response:

~~~json
{
  "message": {
    "content": "OK",
    "role": "assistant"
  },
  "usage": {
    "prompt_tokens": 36,
    "completion_tokens": 1,
    "total_tokens": 37
  }
}
~~~

## Result

The local llama.cpp server started successfully and returned a valid chat completion response.
