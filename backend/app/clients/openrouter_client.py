import os
import requests
import json
import urllib3

from dotenv import load_dotenv

from app.core.logger import logger
from app.core.exceptions import ApiError

load_dotenv()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class OpenRouterClient:
    def __init__(self, base_url: str, api_key: str | None):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

    def _headers(self) -> dict:
        if not self.api_key:
            raise ApiError("OPENAI_API_KEY is not set.")
        
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
    
    def _request(
        self,
        method: str,
        path: str,
        *,
        json: dict | list | None = None,
        files: dict | None = None,
        params: dict | None = None,
        timeout: int = 60
    ) -> dict:
        if not self.api_key:
            print(
                "OPENROUTER_API_KEY is not set. "
                "Skipping OpenRouter model requests."
            )
            return {}
        
        url = f"{self.base_url}{path}"

        if files is not None:
            headers = {
                "Authorization": f"Bearer {self._get_access_token()}",
                "Accept": "application/json"
            }
        else:
            headers = self._headers()

        print(method, url)

        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                json=json,
                files=files,
                params=params,
                timeout=timeout,
                verify=False
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            print("OpenRouter request failed: ", exc)

            if getattr(exc, "response", None) is not None:
                print(f"Response status: {exc.response.status_code,} body: {exc.response.text}")
            return {}
        
        if not response.text:
            return {}
        
        try:
            return response.json()
        except ValueError:
            print(
                "Failed to parse OpenRouter response as JSON. "
                "Response text: ", response.text
            )
            return {"raw_response": response.text}

# ------------------------------------MODELS INFO------------------------------------

    def get_models(self, tags=None) -> dict:
        models = self._request("GET", "/models")

        if tags:
            filtered_models = [
                model for model in models.get("data", [])
                if any(tag in model.get("id", "") for tag in tags)
            ]
            return filtered_models
        
        else:
            models = [model for model in models.get("data", [])]
            return models
        
# ----------------------------------CHAT COMPLETIONS----------------------------------
    def chat(
        self,
        model: str,
        messages: list[dict],
        *,
        temperature: float | None = None,
        max_tokens: int | None = None
    ) -> dict:
        payload = {
            "model": model,
            "messages": messages,
        }

        if temperature is not None:
            payload["temperature"] = temperature

        if max_tokens is not None:
            payload["max_tokens"] = max_tokens

        return self._request("POST", "/chat/completions", json=payload, timeout=90)
    
    def ask(
        self,
        prompt: str,
        model: str = "openai/gpt-oss-120b:free",
        system_prompt: str | None = None
    ) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        data = self.chat(model=model, messages=messages)
        
        try:
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError):
            print("Unexpected response format: ", data)
            return ""
        
    def ask_json(
        self,
        prompt: str,
        model: str = "meta-llama/llama-3.3-70b-instruct:free",
        system_prompt: str | None = None
    ) -> dict:
        response_text = self.ask(model=model, prompt=prompt, system_prompt=system_prompt)

        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            print("Failed to parse OpenRouter response as JSON. Response text: ", response_text)
            return {"raw_response": response_text}

# -------------------------------------EMBEDDINGS-------------------------------------

    def create_embeddings(
        self,
        input: str | list[str],
        model: str = "nvidia/llama-nemotron-embed-vl-1b-v2:free"
    ) -> dict:
        if not input:
            logger.warning("No input provided for embedding creation.")
            return {"data": []}
        
        payload = {
            "model": model,
            "input": input
        }
        return self._request("POST", "/embeddings", json=payload, timeout=90)
