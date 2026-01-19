import os
import json
import re
import glob

RESULTS_DIR = "ww_custom/benchmark_test/results"

def analyze():
    files = glob.glob(os.path.join(RESULTS_DIR, "*.txt"))
    
    stats = {
        "qwen3-coder:latest": {"count": 0, "total_time": 0, "if_pass": 0, "if_total": 0},
        "deepseek-r1:latest": {"count": 0, "total_time": 0, "if_pass": 0, "if_total": 0}
    }
    
    print(f"Analyzing {len(files)} result files...")
    
    for file_path in files:
        with open(file_path, 'r') as f:
            content = f.read()
            
        # Parse Header
        model_match = re.search(r"Model: (.*?)\n", content)
        time_match = re.search(r"Time: (.*?)s\n", content)
        task_match = re.search(r"Task: (.*?) -", content)
        
        if not (model_match and time_match and task_match):
            continue
            
        model = model_match.group(1).strip()
        time_val = float(time_match.group(1))
        task_id = task_match.group(1).strip()
        
        if model not in stats:
            stats[model] = {"count": 0, "total_time": 0, "if_pass": 0, "if_total": 0}
            
        stats[model]["count"] += 1
        stats[model]["total_time"] += time_val
        
        # Check Instruction Following (IF) - Expecting strict JSON
        if "QA-IF-JSON" in task_id:
            stats[model]["if_total"] += 1
            body = content.split("-" * 40 + "\n")[1]
            try:
                # Try to parse raw, if fails, try to find json block
                json.loads(body)
                stats[model]["if_pass"] += 1
            except:
                # If strict parse fails, check if it's because of markdown blocks (which is a fail for strict IF but checking logic)
                pass

    print("\n=== Benchmark Summary ===")
    for model, data in stats.items():
        if data["count"] == 0: continue
        avg_time = data["total_time"] / data["count"]
        print(f"\nModel: {model}")
        print(f"  - Generated Files: {data['count']}")
        print(f"  - Avg Response Time: {avg_time:.2f}s")
        if data["if_total"] > 0:
            pass_rate = (data["if_pass"] / data["if_total"]) * 100
            print(f"  - Strict JSON Compliance: {pass_rate:.1f}% ({data['if_pass']}/{data['if_total']})")

if __name__ == "__main__":
    analyze()
