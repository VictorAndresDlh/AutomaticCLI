#!/bin/bash
# AI CLI Tools Testing Framework - One-Command Runner
# Usage: ./run_tests.sh [options]

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Print colored output
print_status() {
    case $2 in
        "success") echo -e "${GREEN}✅ $1${NC}" ;;
        "error")   echo -e "${RED}❌ $1${NC}" ;;
        "warning") echo -e "${YELLOW}⚠️  $1${NC}" ;;
        "info")    echo -e "${BLUE}ℹ️  $1${NC}" ;;
        "header")  echo -e "${PURPLE}🚀 $1${NC}" ;;
        *)         echo -e "${CYAN}📋 $1${NC}" ;;
    esac
}

# Print header
echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║          AI CLI Tools Testing Framework                       ║"
echo "║              🤖 One-Command Runner 🤖                        ║"
echo "║                                                              ║"
echo "║  This script will:                                           ║"
echo "║  1️⃣  Set up Python environment                               ║"
echo "║  2️⃣  Install all dependencies                                ║"
echo "║  3️⃣  Install AI CLI tools                                    ║"
echo "║  4️⃣  Clone test repositories                                 ║"
echo "║  5️⃣  Run comprehensive tests                                 ║"
echo "║  6️⃣  Generate reports & visualizations                       ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Parse command line arguments
QUICK_MODE=false
NO_VIZ=false
TOOLS_SELECTED=""
RESULTS_DIR="test_results"

while [[ $# -gt 0 ]]; do
    case $1 in
        --quick)
            QUICK_MODE=true
            shift
            ;;
        --no-viz)
            NO_VIZ=true
            shift
            ;;
        --tools)
            TOOLS_SELECTED="$2"
            shift 2
            ;;
        --results-dir)
            RESULTS_DIR="$2"
            shift 2
            ;;
        --help|-h)
            echo "Usage: $0 [options]"
            echo ""
            echo "Options:"
            echo "  --quick           Run quick tests only (3 tests instead of 6)"
            echo "  --no-viz         Skip visualization generation"
            echo "  --tools TOOLS    Test specific tools (claude_code,codex,gemini_cli)"
            echo "  --results-dir DIR Custom results directory"
            echo "  --help           Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0                           # Full test suite"
            echo "  $0 --quick                   # Quick tests only"
            echo "  $0 --tools codex,claude_code # Test specific tools"
            echo "  $0 --no-viz                  # Skip charts generation"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Functions
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

check_python() {
    if command_exists python3; then
        PYTHON_CMD=python3
        print_status "Python 3 found" "success"
    elif command_exists python && python --version 2>&1 | grep -q "Python 3"; then
        PYTHON_CMD=python
        print_status "Python 3 found" "success"
    else
        print_status "Python 3 is required but not found" "error"
        echo "Please install Python 3.8+ and try again"
        exit 1
    fi
}

check_node() {
    if command_exists node && command_exists npm; then
        print_status "Node.js and npm found" "success"
    else
        print_status "Node.js/npm not found - AI CLI tools installation may fail" "warning"
        echo "Consider installing Node.js 18+ for full functionality"
    fi
}

setup_environment() {
    print_status "Setting up Python environment..." "header"
    
    # Check if virtual environment exists
    if [ ! -d ".venv" ]; then
        print_status "Creating virtual environment..." "info"
        $PYTHON_CMD -m venv .venv --prompt "ai-cli-test"
    else
        print_status "Virtual environment exists" "success"
    fi
    
    # Activate virtual environment (this needs to be sourced in current shell)
    print_status "Activating virtual environment..." "info"
    if [ -f ".venv/bin/activate" ]; then
        source .venv/bin/activate
        # Verify activation worked
        if [ -n "$VIRTUAL_ENV" ]; then
            print_status "Virtual environment activated: $(basename $VIRTUAL_ENV)" "success"
        else
            print_status "Warning: Virtual environment activation may have failed" "warning"
        fi
    else
        print_status "Virtual environment activation script not found" "error"
        exit 1
    fi
    
    # Upgrade pip
    print_status "Upgrading pip..." "info"
    pip install --upgrade pip > /dev/null 2>&1
    
    print_status "Environment setup complete" "success"
}

install_dependencies() {
    print_status "Installing Python dependencies..." "header"
    
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
        print_status "Python dependencies installed" "success"
    else
        print_status "requirements.txt not found" "error"
        exit 1
    fi
}

check_api_keys() {
    print_status "Checking API keys..." "header"
    
    # Load .env if exists
    if [ -f ".env" ]; then
        export $(grep -v '^#' .env | xargs)
        print_status ".env file loaded" "success"
    else
        print_status "No .env file found" "warning"
        if [ -f ".env.example" ]; then
            echo "Creating .env from template..."
            cp .env.example .env
            print_status ".env template created - please add your API keys" "warning"
        fi
    fi
    
    # Check OpenAI API key (required)
    if [ -z "$OPENAI_API_KEY" ]; then
        print_status "OPENAI_API_KEY not set - required for evaluation" "warning"
        echo "Set it with: export OPENAI_API_KEY='your-key' or add to .env file"
        echo "Tests will run but LLM evaluation may fail"
    else
        print_status "OpenAI API key configured" "success"
    fi
    
    print_status "Claude Code and Gemini CLI work without API keys" "info"
}

install_ai_tools() {
    print_status "Checking AI CLI tools..." "header"
    
    if command_exists npm; then
        # Check and install Claude Code
        if ! command_exists claude; then
            print_status "Installing Claude Code..." "info"
            npm install -g @anthropic-ai/claude-code 2>/dev/null || print_status "Claude Code installation failed (optional)" "warning"
        else
            print_status "Claude Code found" "success"
        fi
        
        # Check and install Codex
        if ! command_exists codex; then
            print_status "Installing OpenAI Codex..." "info"
            npm install -g @openai/codex 2>/dev/null || print_status "Codex installation failed (optional)" "warning"
        else
            print_status "OpenAI Codex found" "success"
        fi
        
        # Check and install Gemini CLI
        if ! command_exists gemini; then
            print_status "Installing Gemini CLI..." "info"
            npm install -g @google/gemini-cli 2>/dev/null || print_status "Gemini CLI installation failed (optional)" "warning"
        else
            print_status "Gemini CLI found" "success"
        fi
    else
        print_status "npm not available - skipping AI tools installation" "warning"
    fi
}

clone_test_repositories() {
    print_status "Cloning test repositories..." "header"
    
    # Create repos directory
    REPOS_DIR="test_repositories"
    if [ ! -d "$REPOS_DIR" ]; then
        mkdir -p "$REPOS_DIR"
        print_status "Created repositories directory: $REPOS_DIR" "info"
    fi
    
    # Define repositories (compatible with older bash versions)
    REPO_NAMES="small_python react_app cli_tool data_science microservice"
    REPO_small_python="https://github.com/miguelgrinberg/flasky.git"
    REPO_react_app="https://github.com/gothinkster/react-redux-realworld-example-app.git"
    REPO_cli_tool="https://github.com/httpie/httpie.git"
    REPO_data_science="https://github.com/jakevdp/PythonDataScienceHandbook.git"
    REPO_microservice="https://github.com/microsoft/vscode.git"
    
    # Clone repositories if they don't exist
    for repo_name in $REPO_NAMES; do
        repo_path="$REPOS_DIR/$repo_name"
        
        # Get URL using variable indirection
        repo_var="REPO_$repo_name"
        repo_url="${!repo_var}"
        
        if [ ! -d "$repo_path" ]; then
            print_status "Cloning $repo_name..." "info"
            if git clone --depth 1 "$repo_url" "$repo_path" >/dev/null 2>&1; then
                print_status "✓ Cloned $repo_name" "success"
            else
                print_status "✗ Failed to clone $repo_name" "warning"
                echo "  Repository: $repo_url"
                echo "  This may affect tests that use this repository"
            fi
        else
            print_status "✓ Repository $repo_name already exists" "success"
        fi
    done
    
    print_status "Repository setup complete" "success"
}

run_tests() {
    print_status "Running AI CLI Tools Tests..." "header"
    
    # Build command
    CMD="$PYTHON_CMD cli_tools_test.py --repos-dir test_repositories"
    
    if [ "$QUICK_MODE" = true ]; then
        CMD="$CMD --quick"
        print_status "Running in quick mode (3 tests)" "info"
    else
        print_status "Running full test suite (6 tests)" "info"
    fi
    
    if [ "$NO_VIZ" = true ]; then
        CMD="$CMD --no-viz"
        print_status "Visualization generation disabled" "info"
    fi
    
    if [ -n "$TOOLS_SELECTED" ]; then
        # Convert comma-separated to space-separated
        TOOLS_ARGS=$(echo "$TOOLS_SELECTED" | tr ',' ' ')
        CMD="$CMD --tools $TOOLS_ARGS"
        print_status "Testing specific tools: $TOOLS_SELECTED" "info"
    fi
    
    if [ "$RESULTS_DIR" != "test_results" ]; then
        CMD="$CMD --results-dir $RESULTS_DIR"
        print_status "Using custom results directory: $RESULTS_DIR" "info"
    fi
    
    echo ""
    print_status "Executing: $CMD" "info"
    echo ""
    
    # Run the tests
    eval $CMD
}

show_results() {
    print_status "Displaying Results..." "header"
    
    # Find latest results
    LATEST_REPORT=$(ls -t ${RESULTS_DIR}/report_*.md 2>/dev/null | head -1)
    LATEST_JSON=$(ls -t ${RESULTS_DIR}/results_*.json 2>/dev/null | head -1)
    
    echo ""
    echo "═══════════════════════════════════════════════════════════════"
    echo "🎉 TESTING COMPLETE!"
    echo "═══════════════════════════════════════════════════════════════"
    echo ""
    
    if [ -n "$LATEST_REPORT" ]; then
        print_status "📊 Latest Report: $LATEST_REPORT" "success"
        echo ""
        echo "📋 Quick Summary:"
        echo "─────────────────"
        # Show first few lines of the report
        head -20 "$LATEST_REPORT" | tail -15
        echo ""
        print_status "📖 View full report: cat $LATEST_REPORT" "info"
    fi
    
    if [ -n "$LATEST_JSON" ]; then
        print_status "💾 Raw Data: $LATEST_JSON" "success"
    fi
    
    # Check for visualizations
    VIZ_COUNT=$(find ${RESULTS_DIR} -name "*.png" 2>/dev/null | wc -l)
    if [ "$VIZ_COUNT" -gt 0 ]; then
        print_status "📈 Generated $VIZ_COUNT visualization charts" "success"
        echo "   📁 Charts location: ${RESULTS_DIR}/"
    elif [ "$NO_VIZ" != true ]; then
        print_status "📈 Generate visualizations manually: python results.py $LATEST_JSON" "info"
    fi
    
    echo ""
    echo "═══════════════════════════════════════════════════════════════"
    print_status "Thank you for using the AI CLI Tools Testing Framework!" "success"
    echo "═══════════════════════════════════════════════════════════════"
}

cleanup() {
    # Deactivate virtual environment if active
    if [ -n "$VIRTUAL_ENV" ]; then
        deactivate 2>/dev/null || true
    fi
}

# Trap to ensure cleanup on exit
trap cleanup EXIT

# Main execution flow
main() {
    # 1. Check prerequisites
    print_status "Step 1: Checking prerequisites..." "header"
    check_python
    check_node
    echo ""
    
    # 2. Setup environment
    print_status "Step 2: Setting up environment..." "header"
    setup_environment
    echo ""
    
    # 3. Install dependencies
    print_status "Step 3: Installing dependencies..." "header"
    install_dependencies
    echo ""
    
    # 4. Check API keys
    print_status "Step 4: Checking configuration..." "header"
    check_api_keys
    echo ""
    
    # 5. Install AI tools
    print_status "Step 5: Installing AI CLI tools..." "header"
    install_ai_tools
    echo ""
    
    # 6. Clone test repositories
    print_status "Step 6: Cloning test repositories..." "header"
    clone_test_repositories
    echo ""
    
    # 7. Run tests
    print_status "Step 7: Running tests..." "header"
    run_tests
    echo ""
    
    # 8. Show results
    print_status "Step 8: Results summary..." "header"
    show_results
}

# Execute main function
main "$@"
