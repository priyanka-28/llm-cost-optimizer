"""
LLM Observatory - Analyze Your LLM Costs
Upload your Anthropic/OpenAI usage CSV and get detailed insights
"""

from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import json
from datetime import datetime
import io
import os
from collections import defaultdict

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Pricing data (per 1M tokens)
PRICING = {
    # Anthropic
    "claude-opus-4-20250514": {"input": 15.00, "output": 75.00, "quality": 10},
    "claude-3-opus-20240229": {"input": 15.00, "output": 75.00, "quality": 10},
    "claude-3-5-sonnet-20241022": {"input": 3.00, "output": 15.00, "quality": 9},
    "claude-sonnet-4-5-20250929": {"input": 3.00, "output": 15.00, "quality": 9},
    "claude-3-sonnet-20240229": {"input": 3.00, "output": 15.00, "quality": 8.5},
    "claude-3-5-haiku-20241022": {"input": 0.80, "output": 4.00, "quality": 7.5},
    "claude-3-haiku-20240307": {"input": 0.25, "output": 1.25, "quality": 7.5},
    
    # OpenAI
    "gpt-4": {"input": 30.00, "output": 60.00, "quality": 10},
    "gpt-4-turbo": {"input": 10.00, "output": 30.00, "quality": 9.5},
    "gpt-4o": {"input": 2.50, "output": 10.00, "quality": 9.5},
    "gpt-3.5-turbo": {"input": 0.50, "output": 1.50, "quality": 7},
}

def estimate_complexity_from_tokens(input_tokens):
    """Estimate task complexity based on input token count"""
    if input_tokens < 200:
        return "simple"
    elif input_tokens < 1000:
        return "medium"
    else:
        return "complex"

def find_optimal_model(current_model, complexity):
    """Find the cheapest model that meets quality requirements"""
    min_quality = {
        "simple": 7,
        "medium": 8.5,
        "complex": 9.5
    }[complexity]
    
    current_pricing = PRICING.get(current_model, {"input": 30, "output": 60, "quality": 10})
    
    # Find all suitable models
    suitable_models = []
    for model, pricing in PRICING.items():
        if pricing["quality"] >= min_quality:
            suitable_models.append((model, pricing))
    
    # Sort by total cost (input + output average)
    suitable_models.sort(key=lambda x: x[1]["input"] + x[1]["output"])
    
    if suitable_models:
        recommended_model = suitable_models[0][0]
        recommended_pricing = suitable_models[0][1]
        
        # Calculate potential savings
        current_cost = current_pricing["input"] + current_pricing["output"]
        recommended_cost = recommended_pricing["input"] + recommended_pricing["output"]
        
        if recommended_cost < current_cost:
            return {
                "model": recommended_model,
                "savings_potential": True,
                "pricing": recommended_pricing
            }
    
    return {
        "model": current_model,
        "savings_potential": False,
        "pricing": current_pricing
    }

def parse_bedrock_cloudwatch_csv(file):
    """Parse AWS Bedrock CloudWatch metrics CSV"""
    df = pd.read_csv(file, skiprows=5)  # Skip header rows
    
    # The CSV has aggregated metrics per time period
    calls = []
    
    for _, row in df.iterrows():
        timestamp = row.iloc[0]  # First column is timestamp
        
        # Skip empty rows
        if pd.isna(timestamp):
            continue
            
        try:
            # Extract metrics (columns are: InputTokenCount, InvocationLatency, Invocations, OutputTokenCount)
            input_tokens = float(row.iloc[1]) if not pd.isna(row.iloc[1]) else 0
            latency = float(row.iloc[2]) if not pd.isna(row.iloc[2]) else 0
            invocations = float(row.iloc[3]) if not pd.isna(row.iloc[3]) else 0
            output_tokens = float(row.iloc[4]) if not pd.isna(row.iloc[4]) else 0
            
            # Skip if no invocations
            if invocations == 0:
                continue
            
            # These are AVERAGES per invocation in this time period
            # We'll treat each time period as representing the average call during that period
            # Bedrock uses Claude models through AWS
            model = "claude-sonnet-4-5-20250929"  # Default - user can adjust
            
            # Calculate cost per call (averages)
            pricing = PRICING.get(model, {"input": 3.00, "output": 15.00})
            cost_per_call = (
                (input_tokens / 1_000_000 * pricing["input"]) +
                (output_tokens / 1_000_000 * pricing["output"])
            )
            
            # Create one entry per invocation in this period
            # Since these are aggregates, we'll represent the period as a single "average" call
            for i in range(int(invocations)):
                call = {
                    "timestamp": timestamp,
                    "model": model,
                    "input_tokens": int(input_tokens),
                    "output_tokens": int(output_tokens),
                    "thinking_tokens": 0,  # Bedrock doesn't expose this
                    "cost": cost_per_call,
                    "latency_ms": latency  # Additional info
                }
                calls.append(call)
                
        except (ValueError, IndexError):
            continue
    
    return calls

def parse_anthropic_csv(file):
    """Parse Anthropic usage CSV"""
    df = pd.read_csv(file)
    
    calls = []
    for _, row in df.iterrows():
        # Anthropic CSV format (adjust based on actual format)
        call = {
            "timestamp": row.get("timestamp", row.get("created_at", "")),
            "model": row.get("model", "unknown"),
            "input_tokens": int(row.get("input_tokens", 0)),
            "output_tokens": int(row.get("output_tokens", 0)),
            "thinking_tokens": int(row.get("cache_creation_input_tokens", 0)),  # Approximate
            "cost": float(row.get("cost", 0)),
        }
        calls.append(call)
    
    return calls

def parse_openai_csv(file):
    """Parse OpenAI usage CSV"""
    df = pd.read_csv(file)
    
    calls = []
    for _, row in df.iterrows():
        call = {
            "timestamp": row.get("timestamp", row.get("created", "")),
            "model": row.get("model", "unknown"),
            "input_tokens": int(row.get("prompt_tokens", row.get("n_context_tokens_total", 0))),
            "output_tokens": int(row.get("completion_tokens", row.get("n_generated_tokens_total", 0))),
            "thinking_tokens": 0,
            "cost": float(row.get("cost", 0)),
        }
        calls.append(call)
    
    return calls

def analyze_calls(calls):
    """Analyze all calls and generate insights"""
    
    if not calls:
        return {"error": "No calls found in CSV"}
    
    total_calls = len(calls)
    total_cost = sum(c["cost"] for c in calls)
    total_input_tokens = sum(c["input_tokens"] for c in calls)
    total_output_tokens = sum(c["output_tokens"] for c in calls)
    total_thinking_tokens = sum(c["thinking_tokens"] for c in calls)
    
    # Model distribution
    model_usage = defaultdict(int)
    model_costs = defaultdict(float)
    for call in calls:
        model_usage[call["model"]] += 1
        model_costs[call["model"]] += call["cost"]
    
    # Find expensive outliers (top 5% most expensive calls)
    sorted_calls = sorted(calls, key=lambda x: x["cost"], reverse=True)
    outlier_threshold = int(total_calls * 0.05)
    outliers = sorted_calls[:max(5, outlier_threshold)]
    
    # Complexity analysis and optimization opportunities
    optimization_opportunities = []
    potential_savings = 0
    
    for call in calls:
        complexity = estimate_complexity_from_tokens(call["input_tokens"])
        optimal = find_optimal_model(call["model"], complexity)
        
        if optimal["savings_potential"]:
            # Calculate actual savings for this call
            current_pricing = PRICING.get(call["model"], {"input": 30, "output": 60})
            optimal_pricing = optimal["pricing"]
            
            current_call_cost = (
                call["input_tokens"] / 1_000_000 * current_pricing["input"] +
                call["output_tokens"] / 1_000_000 * current_pricing["output"]
            )
            
            optimal_call_cost = (
                call["input_tokens"] / 1_000_000 * optimal_pricing["input"] +
                call["output_tokens"] / 1_000_000 * optimal_pricing["output"]
            )
            
            savings = current_call_cost - optimal_call_cost
            potential_savings += savings
            
            optimization_opportunities.append({
                "timestamp": call["timestamp"],
                "current_model": call["model"],
                "recommended_model": optimal["model"],
                "complexity": complexity,
                "current_cost": current_call_cost,
                "optimal_cost": optimal_call_cost,
                "savings": savings,
                "input_tokens": call["input_tokens"],
                "output_tokens": call["output_tokens"]
            })
    
    # Complexity breakdown
    complexity_breakdown = defaultdict(int)
    for call in calls:
        complexity = estimate_complexity_from_tokens(call["input_tokens"])
        complexity_breakdown[complexity] += 1
    
    # Time-based analysis
    hourly_costs = defaultdict(float)
    for call in calls:
        try:
            hour = pd.to_datetime(call["timestamp"]).hour
            hourly_costs[hour] += call["cost"]
        except:
            pass
    
    return {
        "summary": {
            "total_calls": total_calls,
            "total_cost": round(total_cost, 2),
            "average_cost_per_call": round(total_cost / total_calls, 4) if total_calls > 0 else 0,
            "total_input_tokens": total_input_tokens,
            "total_output_tokens": total_output_tokens,
            "total_thinking_tokens": total_thinking_tokens,
            "potential_monthly_savings": round(potential_savings, 2),
            "savings_percentage": round((potential_savings / total_cost * 100) if total_cost > 0 else 0, 1)
        },
        "model_distribution": dict(model_usage),
        "model_costs": {k: round(v, 2) for k, v in model_costs.items()},
        "complexity_breakdown": dict(complexity_breakdown),
        "outliers": outliers[:10],  # Top 10 most expensive calls
        "optimization_opportunities": optimization_opportunities[:20],  # Top 20 opportunities
        "hourly_costs": {k: round(v, 2) for k, v in sorted(hourly_costs.items())},
        "all_calls": calls  # For detailed view
    }

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle CSV upload and analysis"""
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    if not file.filename.endswith('.csv'):
        return jsonify({"error": "File must be a CSV"}), 400
    
    try:
        # Try different CSV formats in order
        calls = None
        
        # Try Bedrock CloudWatch format first (has specific header structure)
        try:
            file.seek(0)
            # Check if it's Bedrock format by looking for header rows
            first_lines = [file.readline().decode('utf-8') for _ in range(5)]
            file.seek(0)
            
            if any('AWS/Bedrock' in line for line in first_lines):
                calls = parse_bedrock_cloudwatch_csv(file)
                print(f"Detected AWS Bedrock CloudWatch format - parsed {len(calls)} calls")
        except Exception as e:
            print(f"Not Bedrock format: {e}")
            file.seek(0)
        
        # Try Anthropic format
        if not calls:
            try:
                calls = parse_anthropic_csv(file)
                print(f"Detected Anthropic format - parsed {len(calls)} calls")
            except Exception as e:
                print(f"Not Anthropic format: {e}")
                file.seek(0)
        
        # Fall back to OpenAI format
        if not calls:
            try:
                calls = parse_openai_csv(file)
                print(f"Detected OpenAI format - parsed {len(calls)} calls")
            except Exception as e:
                print(f"Not OpenAI format: {e}")
        
        if not calls:
            return jsonify({"error": "Could not parse CSV. Supported formats: AWS Bedrock CloudWatch, Anthropic, OpenAI"}), 400
        
        # Analyze the calls
        analysis = analyze_calls(calls)
        
        return jsonify(analysis)
        
    except Exception as e:
        return jsonify({"error": f"Error parsing CSV: {str(e)}"}), 400

@app.route('/example')
def get_example_data():
    """Return example analysis data for demo"""
    example_data = {
        "summary": {
            "total_calls": 1523,
            "total_cost": 450.75,
            "average_cost_per_call": 0.296,
            "total_input_tokens": 1_234_567,
            "total_output_tokens": 567_890,
            "total_thinking_tokens": 123_456,
            "potential_monthly_savings": 382.50,
            "savings_percentage": 84.9
        },
        "model_distribution": {
            "claude-3-opus-20240229": 1200,
            "claude-3-sonnet-20240229": 250,
            "claude-3-haiku-20240307": 73
        },
        "model_costs": {
            "claude-3-opus-20240229": 425.30,
            "claude-3-sonnet-20240229": 22.15,
            "claude-3-haiku-20240307": 3.30
        },
        "complexity_breakdown": {
            "simple": 980,
            "medium": 420,
            "complex": 123
        },
        "optimization_opportunities": [
            {
                "timestamp": "2024-02-13T14:23:15",
                "current_model": "claude-3-opus-20240229",
                "recommended_model": "claude-3-haiku-20240307",
                "complexity": "simple",
                "current_cost": 0.00525,
                "optimal_cost": 0.000088,
                "savings": 0.005162,
                "input_tokens": 150,
                "output_tokens": 50
            }
        ]
    }
    return jsonify(example_data)

if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)
