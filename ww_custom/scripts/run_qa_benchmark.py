import json
import sys
import os
import requests
import time

# Configuration
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://ai.wisewires.com:11434")
BENCHMARK_FILE = "ww_custom/benchmark_test/qa_prompts.json"
OUTPUT_DIR = "ww_custom/benchmark_test/results"

def load_prompts():
    with open(BENCHMARK_FILE, "r") as f:
        return json.load(f)

def run_benchmark(models):
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    prompts = load_prompts()
    
    for model in models:
        print(f"\n--- Benchmarking Model: {model} ---")
        for test in prompts:
            print(f"Running Test: {test['id']} ({test['category']})...")
            
            payload = {
                "model": model,
                "messages": [{"role": "user", "content": test["prompt"]}],
                "stream": False,
                "options": {"temperature": 0.2} # Low temp for consistency
            }
            
            try:
                start_time = time.time()
                response = requests.post(f"{OLLAMA_HOST}/api/chat", json=payload, timeout=120)
                duration = time.time() - start_time
                
                if response.status_code == 200:
                    content = response.json()["message"]["content"]
                    
                    # Save Result
                    clean_model = model.replace(":", "_")
                    filename = f"{OUTPUT_DIR}/{test['id']}_{clean_model}.txt"
                    with open(filename, "w") as f:
                        f.write(f"Model: {model}\n")
                        f.write(f"Task: {test['id']} - {test['description']}\n")
                        f.write(f"Time: {duration:.2f}s\n")
                        f.write("-" * 40 + "\n")
                        f.write(content)
                    print(f"  -> Saved to {filename} ({duration:.2f}s)")
                else:
                    print(f"  -> Error: {response.status_code}")
            except Exception as e:
                print(f"  -> Failed: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 run_qa_benchmark.py <model1> <model2> ...")
        sys.exit(1)
    
    run_benchmark(sys.argv[1:])
