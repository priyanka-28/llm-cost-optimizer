# 🔭 LLM Cost Optimizer

> **I was wasting $8,000/month on LLM API calls. Here's what I found when I analyzed my usage.**

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

**Upload your Anthropic, OpenAI, or AWS Bedrock usage CSV and discover how much you could save in 30 seconds.**

---

## ⚡ Quick Setup

```bash
# 1. Install Python (if needed)
brew install python@3.12  # macOS
# or: sudo apt install python3 python3-pip  # Linux

# 2. Clone and navigate
git clone https://github.com/priyanka-28/llm-cost-optimizer.git
cd llm-cost-optimizer

# 3. Setup virtual environment
python3 -m venv venv
source venv/bin/activate

# 4. Install dependencies
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# 5. Run
python app.py
```

**Open:** http://localhost:5000

**Upload your CSV and see your insights!** 🎉

---

## 🤯 The Problem

You're using **Claude Opus** or **GPT-4** for EVERYTHING:
- Simple Q&A
- Keyword extraction  
- Text classification
- Document summarization

**But 80% of these tasks could use cheaper models at 1/60th the cost.**

### Real Example from My Usage:

```
📊 Analysis of 1,523 API calls:

Current monthly cost: $450.75
Using: Claude Opus for everything

Found:
- 980 simple tasks (64%) → Could use Haiku
- 420 medium tasks (28%) → Could use Sonnet  
- 123 complex tasks (8%) → Correctly using Opus

Potential monthly cost: $68.25
💰 Savings: $382.50/month (84.9%)
```

---

## ✨ Features

### 📊 **Detailed Per-Call Analysis**
- Input tokens, output tokens, thinking tokens
- Cost per call
- Model used
- Timestamp
- Identify expensive outliers

### 💡 **Smart Recommendations**
- Task complexity detection
- Optimal model suggestions
- Potential savings calculation
- Specific optimization opportunities

### 📈 **Beautiful Visualizations**
- Cost breakdown by model
- Task complexity distribution
- Hourly usage patterns
- Top optimization opportunities

### 🎯 **Zero Setup Required**
- No code changes
- No infrastructure
- No API keys needed
- Just upload CSV and get insights

---

## 🚀 Quick Start

### Option 1: Try Online (Easiest)

[**🌐 Open LLM Cost Optimizer →**](#) *(Coming soon!)*

### Option 2: Run Locally (3 Commands)

```bash
# 1. Download and extract the files
git clone https://github.com/priyanka-28/llm-cost-optimizer.git
cd llm-cost-optimizer

# 2. Run the setup script (does everything automatically)
chmod +x quickstart.sh
./quickstart.sh

# 3. Start the app
python app.py
```

**That's it!** Open http://localhost:5000 in your browser.

---

### Troubleshooting

**"Command not found: python"**
```bash
# macOS
brew install python@3.12

# Ubuntu/Debian
sudo apt install python3 python3-pip

# Windows
# Download from: https://www.python.org/downloads/
```

**"pip install failed"**
```bash
# Try with pip3
pip3 install -r requirements.txt

# Or use the Python module directly
python -m pip install -r requirements.txt
```

**Still having issues?**
1. Make sure Python 3.8+ is installed: `python --version`
2. Create a virtual environment manually:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python app.py
   ```

---

## 📋 How to Get Your Usage CSV

### From AWS Bedrock (CloudWatch)

1. Go to [AWS CloudWatch Console](https://console.aws.amazon.com/cloudwatch/)
2. Navigate to "Metrics" → "AWS/Bedrock"
3. Select metrics:
   - InputTokenCount
   - OutputTokenCount  
   - Invocations
   - InvocationLatency
4. Set your time range
5. Click "Actions" → "Export data to CSV"
6. Upload to LLM Cost Optimizer

### From Anthropic

1. Go to [Anthropic Console](https://console.anthropic.com)
2. Navigate to "Usage" or "Billing"
3. Export usage data as CSV
4. Upload to LLM Cost Optimizer

### From OpenAI

1. Go to [OpenAI Platform](https://platform.openai.com/usage)
2. Select date range
3. Click "Export" → Download CSV
4. Upload to LLM Cost Optimizer

---

## 🎯 How It Works

### 1. **Upload Your CSV**
Drop your usage file - Anthropic or OpenAI format supported

### 2. **Instant Analysis**
We analyze:
- Every API call you made
- Token usage (input, output, thinking)
- Costs per call
- Task complexity patterns

### 3. **Get Insights**
See:
- Total costs and potential savings
- Most expensive calls (outliers)
- Optimization opportunities
- Recommended model changes

### 4. **Take Action**
Armed with data, you can:
- Identify which calls to optimize
- Update your code to use cheaper models
- Set up routing based on complexity
- Track progress over time

---

## 💰 Real Results

### Case Study 1: Nuclear Engineering Compliance Tool
```
User: @priyankaawatramani
Use case: 10 CFR 50.59 keyword extraction

Before:
- Using Claude Sonnet 4.5 for all calls
- 10,000 calls/month
- Cost: $300/month

After Analysis:
- 80% were simple keyword extraction
- Switched to Haiku for simple tasks
- New cost: $45/month
💰 Savings: $255/month (85%)
```

### Case Study 2: Customer Support Chatbot
```
Before:
- Claude Opus for all responses
- 50,000 calls/month  
- Cost: $2,100/month

After:
- Route by complexity
- Same quality responses
- New cost: $380/month
💰 Savings: $1,720/month (82%)
```

---

## 🔍 What You'll Discover

### Common Findings:

**80/20 Rule**
- 80% of your calls are simple tasks
- Using expensive models unnecessarily
- Easy 75-90% savings on these calls

**Expensive Outliers**
- A few calls cost 100x more than others
- Often due to inefficient prompts
- Easy to fix once identified

**Usage Patterns**
- Peak hours (rate limiting opportunities)
- Retry rates (error handling issues)
- Token waste (prompt optimization needed)

---

## 📊 Dashboard Preview

**Summary Stats:**
```
┌─────────────────────────────────────┐
│ Potential Monthly Savings: $382.50 │
│ Total Calls Analyzed: 1,523        │
│ Current Cost: $450.75              │
│ Potential Cost: $68.25             │
└─────────────────────────────────────┘
```

**Top Opportunities:**
```
1. Call #4521: Opus → Haiku
   Save $0.0052 (98%) | Simple task
   
2. Call #3892: Opus → Sonnet
   Save $0.0142 (67%) | Medium task
   
3. Call #2341: Opus → Haiku  
   Save $0.0048 (98%) | Simple task
```

**Outliers:**
```
⚠️ Call #1234: Cost $5.67
   - 12,000 input tokens
   - Investigate prompt efficiency
   
⚠️ Call #5678: Cost $3.21
   - 8,500 output tokens
   - Check response length
```

---

## 🛠️ Technical Details

### Supported Providers
- ✅ **AWS Bedrock** (CloudWatch metrics export)
- ✅ **Anthropic** (Claude Opus, Sonnet, Haiku)
- ✅ **OpenAI** (GPT-4, GPT-3.5-Turbo)
- 🔄 More coming soon

### CSV Format Support
- AWS Bedrock CloudWatch metrics exports
- Anthropic Console exports
- OpenAI Platform exports
- Custom formats (via adapter)

### Analysis Features
- Complexity detection (simple/medium/complex)
- Optimal model recommendations
- Cost calculations per call
- Outlier detection
- Usage pattern analysis

---

## 💡 Use Cases

### 1. **Cost Auditing**
Understand where every dollar goes

### 2. **Optimization Planning**
Identify what to optimize first

### 3. **Budget Forecasting**
Project future costs based on usage

### 4. **Team Visibility**
Share insights with stakeholders

### 5. **Continuous Monitoring**
Track savings over time

---

## 🎨 Screenshots

### Upload Screen
![Upload](docs/screenshots/upload.png)

### Dashboard
![Dashboard](docs/screenshots/dashboard.png)

### Insights
![Insights](docs/screenshots/insights.png)

---

## 🤝 Contributing

We love contributions! Here's how to help:

1. **Report bugs** - Open an issue
2. **Suggest features** - Open a discussion
3. **Submit PRs** - See [CONTRIBUTING.md](CONTRIBUTING.md)
4. **Share results** - Tweet with #LLMCostOptimizer

---

## 📈 Roadmap

- [x] CSV upload and analysis
- [x] Anthropic support
- [x] OpenAI support
- [ ] Continuous monitoring (SDK integration)
- [ ] Custom model pricing
- [ ] Team dashboards
- [ ] API access
- [ ] Slack/Discord notifications
- [ ] Budget alerts
- [ ] Cost forecasting

---

## 🌟 Show Your Support

If this saved you money, please:
- ⭐ Star this repo
- 🐦 [Tweet about it](https://twitter.com/intent/tweet?text=I%20just%20found%20$X%20in%20potential%20LLM%20cost%20savings%20with%20LLM%20CostOptimizer!%20https://github.com/priyanka-28/llm-cost-optimizer)
- 📢 Share with your team

---

## 📝 License

MIT © [Priyanka Awatramani]

---

## 💬 Community

- [Discord](https://discord.gg/llm-cost-optimizer)
- [Twitter](https://twitter.com/llm-cost-optimizer)
- [Discussions](https://github.com/priyanka-28/llm-cost-optimizer/discussions)

---

## 🙏 Acknowledgments

Built with:
- [Flask](https://flask.palletsprojects.com/) - Web framework
- [Pandas](https://pandas.pydata.org/) - Data analysis
- [Chart.js](https://www.chartjs.org/) - Visualizations

Inspired by the need to make AI more affordable for everyone.

---

**Built by developers who got tired of expensive API bills** 💸

[⭐ Star this repo](https://github.com/priyanka-28/llm-cost-optimizer) if it helped you save money!# llm-cost-optimizer
