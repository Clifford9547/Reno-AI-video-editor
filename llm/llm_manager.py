import requests

MODEL_CATALOG = {
    "openai": {
        "api_url": "https://api.openai.com/v1/chat/completions",
        "models": ["gpt-3.5-turbo", "gpt-4o", "gpt-4o-mini"]
    },
    "gemini": {
        "api_url": "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent",
        "models": ["gemini-pro"]
    },
    "deepseek": {
        "api_url": "https://api.deepseek.com/v1/chat/completions",
        "models": ["deepseek-chat"]
    }
}

class LLMManager:
    def __init__(self, provider, model, api_key=None):
        self.provider = provider.lower()
        self.model = model
        self.api_key = api_key
        self.api_url = MODEL_CATALOG.get(self.provider, {}).get("api_url", "")

    def generate_text(self, prompt, max_tokens=1000, temperature=0.7):
        headers = {'Content-Type': 'application/json'}

        if self.provider == 'openai':
            headers['Authorization'] = f'Bearer {self.api_key}'
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": max_tokens,
                "temperature": temperature
            }

        elif self.provider == 'gemini':
            if 'key=' not in self.api_url and self.api_key:
                connector = '&' if '?' in self.api_url else '?'
                self.api_url += f"{connector}key={self.api_key}"

            payload = {
                "contents": [
                    {"parts": [{"text": prompt}]}
                ]
            }

        elif self.provider == 'deepseek':
            headers['Authorization'] = f'Bearer {self.api_key}'
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                "stream": False
            }

        else:
            payload = {
                "prompt": prompt,
                "max_tokens": max_tokens,
                "temperature": temperature
            }
            if self.api_key:
                headers['Authorization'] = f'Bearer {self.api_key}'

        response = requests.post(
            self.api_url,
            headers=headers,
            json=payload,
            timeout=60
        )
        response.raise_for_status()

        try:
            data = response.json()
            if "choices" in data:
                return data["choices"][0]["message"]["content"]
            if "candidates" in data:
                return data["candidates"][0]["content"]["parts"][0]["text"]
            return data.get("content") or data.get("script") or response.text
        except Exception:
            return response.text
