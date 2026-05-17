import os
import requests
import json
import urllib3

from dotenv import load_dotenv

from backend.app.core.logger import logger
from backend.app.core.exceptions import ApiError

load_dotenv()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class YandexGPTClient:
    def __init__(self, base_url: str, api_key: str | None, folder_id: str | None = None):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.folder_id = folder_id

    def _headers(self) -> dict:
        if not self.api_key:
            raise ApiError("OPENAI_API_KEY is not set.")
        
        return {
            "Authorization": f"Api-Key {self.api_key}",
            "Content-Type": "application/json",
            "x-folder-id": self.folder_id,
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
                "YANDEXGPT_API_KEY is not set. "
                "Skipping YandexGPT model requests."
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
            print("YandexGPT request failed: ", exc)

            if getattr(exc, "response", None) is not None:
                print(f"Response status: {exc.response.status_code,} body: {exc.response.text}")
            return {}
        
        if not response.text:
            return {}
        
        try:
            return response.json()
        except ValueError:
            print(
                "Failed to parse YandexGPT response as JSON. "
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
            "modelUri": f"gpt://{self.folder_id}/{model}/latest",
            "completionOptions": {
                "stream": False
            },
            "messages": messages,
        }

        if temperature is not None:
            payload["completionOptions"]["temperature"] = temperature

        if max_tokens is not None:
            payload["completionOptions"]["maxTokens"] = str(max_tokens)

        return self._request("POST", "/completion", json=payload, timeout=90)
    
    def ask(
        self,
        prompt: str,
        model: str = "yandexgpt",
        system_prompt: str | None = None
    ) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "text": system_prompt})
        messages.append({"role": "user", "text": prompt})

        data = self.chat(model=model, messages=messages)
        
        try:
            return data["result"]["alternatives"][0]["message"]["text"]
        except (KeyError, IndexError, TypeError):
            print("Unexpected response format: ", data)
            return ""
        
    def ask_json(
        self,
        prompt: str,
        model: str = "yandexgpt",
        system_prompt: str | None = None
    ) -> dict:
        response_text = self.ask(model=model, prompt=prompt, system_prompt=system_prompt)

        if response_text.startswith("```"): 
            lines = response_text.splitlines()  
            lines = lines[1:] 
            
            if lines and lines[-1].strip() == "```": 
                lines = lines[:-1] 
                
            response_text = "\n".join(lines).strip()

        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            print("Failed to parse YandexGPT response as JSON. Response text: ", response_text)
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
            "modelUri": f"gpt://{self.folder_id}/{model}/latest",
            "messages": input
        }
        return self._request("POST", "/embeddings", json=payload, timeout=90)
