import json
import random

# Domains and Scenarios
DOMAINS = [
    "E-commerce (Checkout, Search, Cart)",
    "Fintech (Payments, KYC, Transfers)",
    "Healthcare (Patient Record, HIPAA, Appointment)",
    "IoT (Device Pairing, Firmware Update, Data Sync)",
    "Social Media (Feed, Privacy, UGC)",
    "Enterprise ERP (HR, Inventory, Reporting)"
]

# 1. Instruction Following Templates (Format focus)
IF_TEMPLATES = [
    {
        "id_prefix": "QA-IF-JSON",
        "description": "Strict JSON Generation",
        "prompt_template": "You are a QA Engineer in the {domain} domain. Generate 3 Test Cases for '{feature}'. \nOutput MUST be a strictly valid JSON array. Schema: [{{'id': 'TC_xxx', 'title': '...', 'steps': [...]}}]. \nDo NOT include markdown blocks.",
        "features": ["Login", "Payment Gateway", "User Profile", "Search Filter", "Data Export"]
    },
    {
        "id_prefix": "QA-IF-CSV",
        "description": "CSV Format Conversion",
        "prompt_template": "Convert the following requirements for {domain} into a CSV format with columns: RequirementID, Description, Priority. \nRequirements: User must be able to {feature}. User must receive email notification. \nOutput raw CSV only.",
        "features": ["Reset Password", "View Transaction History", "Update Firmware", "Share Post", "Generate Report"]
    },
    {
        "id_prefix": "QA-IF-GHERKIN",
        "description": "Gherkin Syntax Generation",
        "prompt_template": "Write a Gherkin (Cucumber) feature file for {domain} - {feature}. \nInclude Scenario Outline with Examples. \nUse strictly valid Gherkin syntax.",
        "features": ["Add to Cart", "Money Transfer", "Schedule Appointment", "Smart Light Control", "Friend Request"]
    }
]

# 2. Multistep Reasoning Templates (Logic focus)
MR_TEMPLATES = [
    {
        "id_prefix": "QA-MR-AMBIGUITY",
        "description": "Ambiguity Analysis",
        "prompt_template": "Analyze this requirement for a {domain} system: 'The {feature} feature should be fast and easy to use.' \nIdentify 3 critical ambiguities. Explain WHY they are ambiguous.",
        "features": ["Search", "Payment", "Sync", "Upload", "Reporting"]
    },
    {
        "id_prefix": "QA-MR-SECURITY",
        "description": "Security Edge Cases",
        "prompt_template": "Design 3 malicious test cases for {domain} - {feature}. \nFocus on OWASP Top 10 vulnerabilities (Injection, Broken Auth, etc.). \nExplain the attack vector.",
        "features": ["Comment Section", "Login Form", "API Endpoint", "File Upload", "Admin Panel"]
    },
    {
        "id_prefix": "QA-MR-DATA",
        "description": "Test Data Generation",
        "prompt_template": "Generate a comprehensive set of test data for a {feature} field in a {domain} app. \nInclude: Valid, Invalid, Boundary, Special Characters, and SQL Injection payloads.",
        "features": ["Age Input", "Credit Card Number", "Patient ID", "Device Serial", "Username"]
    }
]

def generate_dataset():
    dataset = []
    count = 1
    
    # Generate IF (Instruction Following) items ~50
    for _ in range(50):
        template = random.choice(IF_TEMPLATES)
        domain = random.choice(DOMAINS)
        feature = random.choice(template["features"])
        
        item = {
            "id": f"{template['id_prefix']}-{count:03d}",
            "category": "Instruction Following",
            "domain": domain,
            "description": template["description"],
            "prompt": template["prompt_template"].format(domain=domain, feature=feature),
            "expected_criteria": "Strict adherence to format"
        }
        dataset.append(item)
        count += 1

    # Generate MR (Multistep Reasoning) items ~50
    for _ in range(50):
        template = random.choice(MR_TEMPLATES)
        domain = random.choice(DOMAINS)
        feature = random.choice(template["features"])
        
        item = {
            "id": f"{template['id_prefix']}-{count:03d}",
            "category": "Multistep Reasoning",
            "domain": domain,
            "description": template["description"],
            "prompt": template["prompt_template"].format(domain=domain, feature=feature),
            "expected_criteria": "Depth of reasoning, edge identification"
        }
        dataset.append(item)
        count += 1
        
    return dataset

if __name__ == "__main__":
    data = generate_dataset()
    output_path = "ww_custom/benchmark_test/qa_prompts.json"
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Generated {len(data)} benchmark prompts to {output_path}")
