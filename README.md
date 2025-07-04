# AI CLI Tools Testing Framework

## Overview

This framework provides automated testing and comparison of three leading AI CLI tools using **real GitHub repositories** and **o3 LLM evaluation**:

- **Claude Code** (Anthropic) - Agentic coding with MCP support
- **OpenAI Codex** - Open-source multimodal coding assistant
- **Google Gemini CLI** - Large context CLI tool (community implementation)

## What's New

### Real Repository Testing
- Tests run on actual production codebases from GitHub
- No synthetic test cases - real-world code challenges
- Repositories include Flask apps, React projects, CLI tools, and more

### o3 LLM Evaluation
- Automated code review using OpenAI's advanced reasoning model
- Detailed scoring with reasoning for each criterion
- Objective evaluation of code quality, completeness, and correctness

### MCP Integration Testing
- Dedicated test for Model Context Protocol (Claude Code)
- External service integration (filesystem search)
- Equivalent tests for other tools using their native capabilities

## Test Suite

### 1. Complex Codebase Analysis
- **Repository**: [Flasky](https://github.com/miguelgrinberg/flasky) (Flask application)
- **Tasks**: Architecture documentation, security audit, improvements
- **Evaluates**: Code understanding, analysis depth

### 2. Feature Implementation
- **Repository**: [React Real World App](https://github.com/gothinkster/react-redux-realworld-example-app)
- **Tasks**: Add dark mode with persistence and tests
- **Evaluates**: Feature development, UI/UX, testing

### 3. Bug Detection and Fixing
- **Repository**: [HTTPie](https://github.com/httpie/httpie) (CLI tool)
- **Tasks**: Find and fix real bugs, add regression tests
- **Evaluates**: Debugging skills, security awareness

### 4. Large-Scale Refactoring
- **Repository**: [Python Data Science Handbook](https://github.com/jakevdp/PythonDataScienceHandbook)
- **Tasks**: Convert notebooks to modular package
- **Evaluates**: Code organization, best practices

### 5. Test Suite Creation
- **Repository**: [Payment Microservice](https://github.com/microservices-demo/payment-service)
- **Tasks**: Full test coverage with CI/CD
- **Evaluates**: Testing strategies, automation

### 6. MCP/External Integration
- **Repository**: [Flasky](https://github.com/miguelgrinberg/flasky)
- **Tasks**: Integrate Slack/GitHub for error reporting
- **Evaluates**: API integration, tool extensibility

## Quick Start

### 🚀 One-Command Setup & Run

The easiest way to get started:

```bash
# Clone and run everything in one command
git clone <repository-url>
cd AutomaticCLI
./run_tests.sh
```

This single script will:
1. ✅ Set up Python virtual environment
2. ✅ Install all dependencies  
3. ✅ Install AI CLI tools (Claude Code, Codex, Gemini CLI)
4. ✅ Clone test repositories once (cached for reuse)
5. ✅ Run comprehensive tests
6. ✅ Generate reports and visualizations
7. ✅ Display results summary

### Command Options

```bash
# Quick tests only (3 tests, ~15 minutes)
./run_tests.sh --quick

# Test specific tools
./run_tests.sh --tools claude_code,codex

# Skip visualization generation
./run_tests.sh --no-viz

# Custom results directory
./run_tests.sh --results-dir my_results

# Show help
./run_tests.sh --help
```

### Manual Setup (Alternative)

If you prefer manual control:

#### Prerequisites
```bash
# Required
- Python 3.8+
- Node.js 18+ (for AI CLI tools)
- Git
- Internet connection

# API Keys needed
- OPENAI_API_KEY (for o3 evaluation and Codex CLI)
- Google account (for Gemini CLI free tier)  
- Claude Code works without API key
```

#### Installation Steps
```bash
# 1. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure API keys
export OPENAI_API_KEY="sk-..."
# or edit .env file

# 4. Install AI CLI tools
npm install -g @anthropic-ai/claude-code
npm install -g @openai/codex  
npm install -g @google/gemini-cli
```

#### Run Tests Manually
```bash
# Quick test (3 tests, ~15 minutes)
python cli_tools_test.py --quick

# Full suite (6 tests, ~30 minutes)
python cli_tools_test.py

# Specific tools only
python cli_tools_test.py --tools codex gemini_cli

# Skip automatic visualization generation
python cli_tools_test.py --no-viz

# Generate visualizations manually after tests
python results.py test_results/results_TIMESTAMP.json
```

## How It Works

### Execution Flow
1. **Repository Cloning**: Each test clones a specific GitHub repository
2. **Tool Execution**: Tools receive tailored prompts for the task
3. **Output Collection**: Generated files, logs, and timing are captured
4. **LLM Evaluation**: o3/GPT-4 reviews the code and provides scores
5. **Report Generation**: Comprehensive markdown report with comparisons
6. **Visualization**: Automatic charts and graphs (optional)

### Evaluation Criteria
- **Code Quality**: Readability, efficiency, best practices
- **Completeness**: Task requirements met, edge cases handled
- **Correctness**: Technical accuracy, proper implementation
- **Innovation**: Creative solutions, modern patterns
- **Integration**: How well code fits into existing codebase

## MCP Server Example

For Claude Code's MCP test, we provide a complete example server (`mcp_server.py`) that demonstrates:
- Slack webhook integration
- GitHub issue creation
- Error reporting pipeline
- Flask application integration

Other tools are tested with equivalent integration capabilities using their native features.

## Output Structure

```
test_results/
├── test_1_codebase_understanding/
│   ├── claude_code/
│   │   ├── ARCHITECTURE.md
│   │   ├── SECURITY_AUDIT.md
│   │   └── execution_log.json
│   ├── codex/
│   └── gemini_cli/
├── results_TIMESTAMP.json       # Raw execution data
├── report_TIMESTAMP.md         # Human-readable comparison
└── *.png                       # Visualization charts

test_repositories/               # Pre-cloned repositories (cached)
├── small_python/               # Flask application
├── react_app/                  # React Redux app  
├── cli_tool/                   # HTTPie CLI tool
├── data_science/               # Jupyter notebooks
└── microservice/               # Payment service
```

## Understanding Results

### Report Sections
1. **Tool Availability**: Which tools are installed
2. **Test Summary Table**: Quick score comparison
3. **Detailed Results**: Per-test analysis with LLM reasoning
4. **Recommendations**: Best tool for each use case

### Score Interpretation
- **8-10**: Excellent performance, production-ready output
- **6-7**: Good performance, minor improvements needed
- **4-5**: Acceptable, significant areas for improvement
- **0-3**: Failed or poor performance

### Visualizations
The framework automatically generates visual charts after tests complete:
- **Overall Comparison**: Bar chart of average scores per tool
- **Test Breakdown**: Detailed performance by test category
- **Execution Time**: Performance timing comparisons
- **Success Rate**: Success/failure rates across tools
- **Criteria Heatmap**: Detailed scoring across all evaluation criteria

Charts are saved as PNG files in the test_results directory.

## Customization

### Adding New Tests
```python
{
    "id": "test_7_custom",
    "name": "Your Test Name",
    "repo": "small_python",  # or add new repo
    "prompts": {
        "claude_code": "Your Claude prompt",
        "codex": "Your Codex prompt",
        "gemini_cli": "Your Gemini prompt"
    },
    "evaluation_criteria": ["your_criteria"],
    "expected_outputs": ["expected_files.py"]
}
```

### Using Different Models
```python
# In CLIToolTester.__init__
self.evaluator = ChatOpenAI(
    model="gpt-4",  # or "gpt-3.5-turbo" for faster/cheaper
    temperature=0.1
)
```

## Troubleshooting

### Common Issues

1. **Git clone failures**
   - Check internet connection
   - Verify GitHub is accessible
   - Some repos may be large; be patient

2. **LLM evaluation errors**
   - Verify OPENAI_API_KEY is set
   - Check API rate limits
   - Falls back to heuristic scoring if needed

3. **Tool timeouts**
   - Complex tasks may take several minutes
   - Increase timeout in execute_test() if needed
   - Use --quick flag for faster testing

## Cost Considerations

- **o3/GPT-4 Evaluation**: ~$0.01-0.03 per test evaluation
- **Tool API Usage**: Varies by tool and subscription
- **Estimated Total**: $1-3 for full test suite

## Contributing

We welcome contributions! Areas for improvement:
- Additional test repositories
- More sophisticated evaluation criteria
- Support for more CLI tools
- Performance optimizations

## License

MIT License - See LICENSE file for details

## Acknowledgments

- Repository owners for providing excellent test codebases
- Tool creators for advancing AI-assisted development
- OpenAI for o3/GPT-4 evaluation capabilities