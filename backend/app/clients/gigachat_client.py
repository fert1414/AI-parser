import os
import requests
import json
import urllib3

from dotenv import load_dotenv

from app.core.exceptions import ApiError

load_dotenv()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class GigaChatClient:
    def __init__(self, base_url: str, api_key: str | None):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

    def _get_access_token(self) -> str:
        url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

        payload={
            "scope": "GIGACHAT_API_PERS"
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "RqUID": "3d1892c8-c2c4-4cf3-af16-88c3e7a0f2a0",
            "Authorization": f"Basic {os.getenv('GIGACHAT_API_KEY')}"
        }

        response = requests.request("POST", url, headers=headers, data=payload, verify=False)

        return response.json().get("access_token", "")

    def _headers(self) -> dict:
        if not self.api_key:
            raise ApiError("GIGACHAT_API_KEY is not set.")
        
        return {
            "Authorization": f"Bearer {self._get_access_token()}",
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
                "GIGACHAT_API_KEY is not set. "
                "Skipping GigaChat model requests."
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
            print("GigaChat request failed: ", exc)

            if getattr(exc, "response", None) is not None:
                print(f"Response status: {exc.response.status_code,} body: {exc.response.text}")
            return {}
        
        if not response.text:
            return {}
        
        try:
            return response.json()
        except ValueError:
            print(
                "Failed to parse GigaChat response as JSON. "
                "Response text: ", response.text
            )
            return {"raw_response": response.text}

# ------------------------------------MODELS INFO------------------------------------
    def get_models(self) -> dict:
        return self._request("GET", "/models")

    def print_available_models(self) -> None:
        models = self.get_models()
        print("GigaChat models:")
        print(json.dumps(models, indent=4))

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
        model: str = "Gigachat-Max",
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
            print("Unexpected GigaChat response format: ", data)
            return ""
        
    def ask_json(
        self,
        prompt: str,
        model: str,
        system_prompt: str | None = None
    ) -> dict:
        response_text = self.ask(model=model, prompt=prompt, system_prompt=system_prompt)

        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            print("Failed to parse GigaChat response as JSON. Response text: ", response_text)
            return {"raw_response": response_text}
        
# -------------------------------------EMBEDDINGS-------------------------------------
    def create_embeddings(
        self,
        input: str | list[str],
        model: str = "GigaEmbeddings-3B-2025-09",
    ) -> dict:
        payload = {
            "model": model,
            "input": input
        }
        return self._request("POST", "/embeddings", json=payload, timeout=90)
    
    def get_balance(self) -> dict:
        return self._request("GET", "/balance", timeout=30)
    
# ----------------------------------FUNCTION CALLING----------------------------------

    def validate_fuction(self, function_schems: dict) -> dict:
        return self._request("POST", "/functions/validate", json=function_schems, timeout=30)
    
    def chat_with_functions(
        self,
        model: str,
        messages: list[dict],
        functions: list[dict],
        function_call: str | dict = "auto",
    ) -> dict:
        payload = {
            "model": model,
            "messages": messages,
            "functions": functions,
            "function_call": function_call
        }

        return self._request("POST", "/chat/completions", json=payload, timeout=90)