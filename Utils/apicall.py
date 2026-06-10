import json
import os
import requests

SETTINGS_FILE = "settings.json"

def api_call(model, messages):
    api_key = None
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
                config = json.load(f)
                api_key = config.get("openrouter_api_key", "").strip()
        except Exception:
            pass
            
    if not api_key:
        api_key = os.environ.get("OPENROUTER_API_KEY", "").strip()

    if not api_key:
        return "Error: OpenRouter API Key is missing. Check settings.json.", messages

    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://agtx.walnutlabs.in",
        "X-Title": "Agtx Developer CLI"
    }
    
    payload = {
        "model": model,
        "messages": messages
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        
        if response.status_code != 200:
            error_msg = f"API Error (Status {response.status_code}): {response.text}"
            return error_msg, messages
            
        data = response.json()
        
        if "choices" in data and len(data["choices"]) > 0:
            content = data["choices"][0]["message"]["content"]
            if content is None:
                content = "Error: The model returned an empty string."
        else:
            content = f"Error: Unexpected response format: {json.dumps(data)}"
            
    except requests.exceptions.RequestException as e:
        content = f"Network Error: Cannot reach OpenRouter. {str(e)}"
    except Exception as e:
        content = f"Error in api call: {str(e)}"

    messages.append({"role": "assistant", "content": content})
    return content, messages