import requests
import json
import sys
import os
from datetime import datetime

# Configuration
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://ai.wisewires.com:11434")
TEST_PROMPT = "이커머스 로그인 관련 테스트케이스 만들어줘."
SYSTEM_PROMPT_PATH = "ww_custom/modes/manual-test-engineer/manual-test-engineer.json"

def get_system_prompt():
    try:
        with open(SYSTEM_PROMPT_PATH, "r") as f:
            config = json.load(f)
            # Find the manual-test-engineer mode config
            # It might be wrapped in customModes or a single object
            if "customModes" in config:
                for mode in config["customModes"]:
                    if mode["slug"] == "manual-test-engineer":
                        return f"{mode['roleDefinition']}\n\n{mode['customInstructions']}"
            else:
                 return f"{config['roleDefinition']}\n\n{config['customInstructions']}"
    except Exception as e:
        print(f"Error loading system prompt: {e}")
        return "You are a Manual Test Engineer."

def benchmark_model(model_name):
    print(f"Starting benchmark for {model_name}...")
    system_prompt = get_system_prompt()
    
    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": TEST_PROMPT}
        ],
        "stream": False,
        "options": {
            "temperature": 0.7
        }
    }
    
    try:
        start_time = datetime.now()
        response = requests.post(f"{OLLAMA_HOST}/api/chat", json=payload, timeout=120)
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        if response.status_code == 200:
            result = response.json()
            content = result.get("message", {}).get("content", "")
            print(f"Model {model_name} responded in {duration:.2f}s")
            
            # Save output
            output_file = f"benchmark_output_{model_name.replace(':', '_')}.txt"
            with open(output_file, "w") as f:
                f.write(f"Model: {model_name}\n")
                f.write(f"Time: {duration:.2f}s\n")
                f.write("-" * 40 + "\n")
                f.write(content)
            print(f"Output saved to {output_file}")
            return True
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"Benchmark failed: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 benchmark_models.py <model1> <model2> ...")
        sys.exit(1)
        
    for model in sys.argv[1:]:
        benchmark_model(model)
