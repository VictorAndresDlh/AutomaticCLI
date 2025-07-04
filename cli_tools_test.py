"""
AI CLI Tools Automated Testing Framework
Tests Claude Code, OpenAI Codex, and Google Gemini CLI

CORRECTED CONFIGURATIONS (Based on Official Documentation):
- Claude Code: npm install -g @anthropic-ai/claude-code, command: claude
- OpenAI Codex: npm install -g @openai/codex, command: codex  
- Google Gemini CLI: npm install -g @google/gemini-cli, command: gemini

UPDATED CLI USAGE PATTERNS:
- Claude Code: Uses --print, --debug, --model, --output-format flags for non-interactive mode
- Codex: Uses --full-auto, --ask-for-approval, --model flags, supports exec mode
- Gemini CLI: Uses --prompt, --model, --sandbox, --all_files, --yolo flags

MCP CONFIGURATIONS:
- Claude Code: .claude/config.json with mcpServers
- Codex: .codex/config.toml with mcp_servers
- Gemini CLI: .gemini/settings.json with mcpServers

All configurations verified against official repositories and documentation.
"""

import subprocess
import json
import time
import os
import sys
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import tempfile
import argparse
import git
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

class CLIToolTester:
    """Automated testing framework for AI CLI tools"""
    
    def __init__(self, results_dir: str = "test_results", generate_viz: bool = True, repos_dir: str = "test_repositories"):
        self.results_dir = Path(results_dir)
        self.results_dir.mkdir(exist_ok=True)
        self.repos_dir = Path(repos_dir)
        self.test_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.generate_viz = generate_viz
        
        # Initialize LangChain evaluator with fallback models
        # o3 is preferred for complex evaluation tasks, but fallback to gpt-4o if not available
        self.evaluator = ChatOpenAI(
            model="o3",
        )
        
        # Tool configurations
        self.tools = {
            "claude_code": {
                "command": "claude",
                "name": "Claude Code",
                "setup_check": "claude --version",
                "installation": "npm install -g @anthropic-ai/claude-code",
                "unique_features": ["agentic_reasoning", "mcp_support", "file_editing", "web_search", "git_operations"],
                "cli_flags": {
                    "print": "--print",  # Non-interactive mode
                    "debug": "--debug",
                    "model": "--model",
                    "output_format": "--output-format",
                    "continue": "--continue",
                    "mcp_config": "--mcp-config"
                }
            },
            "codex": {
                "command": "codex",
                "name": "OpenAI Codex",
                "setup_check": "codex --version",
                "installation": "npm install -g @openai/codex",
                "unique_features": ["sandboxing", "approval_modes", "full_auto", "exec_mode"],
                "cli_flags": {
                    "model": "--model",
                    "approval": "--ask-for-approval", 
                    "full_auto": "--full-auto",
                    "exec": "exec",  # Non-interactive mode
                    "cd": "--cd"
                }
            },
            "gemini_cli": {
                "command": "gemini",
                "name": "Google Gemini CLI",
                "setup_check": "gemini --version",
                "installation": "npm install -g @google/gemini-cli",
                "unique_features": ["large_context", "multimodal", "mcp_support", "sandbox_execution", "tools_system"],
                "cli_flags": {
                    "prompt": "--prompt",
                    "model": "--model",
                    "sandbox": "--sandbox",
                    "debug": "--debug",
                    "all_files": "--all_files",
                    "yolo": "--yolo"  # Auto-accept all actions
                }
            }
        }
        
        # Test repositories
        self.test_repos = {
            "small_python": "https://github.com/miguelgrinberg/flasky.git",
            "react_app": "https://github.com/gothinkster/react-redux-realworld-example-app.git",
            "cli_tool": "https://github.com/httpie/httpie.git",
            "data_science": "https://github.com/jakevdp/PythonDataScienceHandbook.git",
            "microservice": "https://github.com/microsoft/vscode.git"
        }
        
        # Test definitions
        self.tests = self._define_tests()
        
    def _define_tests(self) -> List[Dict]:
        """Define comprehensive tests using real repositories"""
        return [
            {
                "id": "test_1_codebase_understanding",
                "name": "Complex Codebase Analysis & Architecture Understanding",
                "description": "Tests ability to understand and document a real Flask application",
                "repo": "small_python",
                "prompts": {
                    "claude_code": "Analyze this Flask application and CREATE THREE SEPARATE FILES: 1) ARCHITECTURE.md - comprehensive architecture document covering data models, API endpoints, authentication flow, and database schema. 2) SECURITY_AUDIT.md - identify potential security issues with detailed explanations. 3) IMPROVEMENTS.md - suggest specific improvements and fixes. You must create these files, not just provide analysis in text.",
                    "codex": "Analyze this Flask codebase completely. CREATE THREE FILES: ARCHITECTURE.md (document the architecture including models, routes, authentication, and database design), SECURITY_AUDIT.md (find security vulnerabilities), and IMPROVEMENTS.md (suggest fixes). Write the actual files, don't just output text.",
                    "gemini_cli": "Perform a deep analysis of this Flask application and CREATE FILES: ARCHITECTURE.md (complete architecture, API endpoints, auth system), SECURITY_AUDIT.md (security issues with solutions), IMPROVEMENTS.md (recommended improvements). Create the actual markdown files."
                },
                "evaluation_criteria": [
                    "architecture_accuracy",
                    "security_findings",
                    "improvement_suggestions",
                    "documentation_quality",
                    "code_understanding"
                ],
                "expected_outputs": ["ARCHITECTURE.md", "SECURITY_AUDIT.md", "IMPROVEMENTS.md"]
            },
            
            {
                "id": "test_2_feature_implementation",
                "name": "Real Feature Addition to Existing Codebase",
                "description": "Tests ability to add a complex feature to a React application",
                "repo": "react_app",
                "prompts": {
                    "claude_code": "Add a dark mode feature to this React application. CREATE THE FOLLOWING FILES: 1) src/components/DarkModeToggle.jsx - toggle component for header, 2) src/styles/dark-theme.css - CSS variables and dark theme styles, 3) tests/darkMode.test.js - unit tests for the feature. The feature should: persist preference in localStorage, apply theme globally with smooth transitions. Create the actual files.",
                    "codex": "Add complete dark mode support to this React app. CREATE FILES: components/DarkModeToggle.jsx (header toggle), styles/dark-theme.css (global theme with CSS variables and transitions), tests/darkMode.test.js (unit tests). Implement localStorage persistence and smooth CSS transitions. Write the actual files.",
                    "gemini_cli": "Implement a dark mode feature for this React application. CREATE FILES: DarkModeToggle component, dark-theme.css file, and test file. Add toggle button in header, save preference to localStorage, apply dark theme globally with CSS variables, add smooth transitions. Create the actual files, don't just describe them."
                },
                "evaluation_criteria": [
                    "feature_completeness",
                    "code_integration",
                    "ui_implementation",
                    "state_management",
                    "test_coverage"
                ],
                "expected_outputs": ["components/DarkModeToggle.jsx", "styles/dark-theme.css", "tests/darkMode.test.js"]
            },
            
            {
                "id": "test_3_bug_fixing",
                "name": "Bug Detection and Fixing in Production Code",
                "description": "Tests ability to find and fix bugs in a real CLI tool",
                "repo": "cli_tool",
                "prompts": {
                    "claude_code": "Analyze the HTTPie codebase for bugs and CREATE FILES: 1) bug_fixes.patch - Git patch file with actual fixes, 2) tests/test_bug_fixes.py - tests to prevent regression, 3) BUG_REPORT.md - detailed bug analysis. Focus on: error handling in network requests, input validation vulnerabilities, memory leaks or performance issues. Fix at least 3 bugs and create the actual files.",
                    "codex": "Find and fix bugs in this HTTPie CLI tool. CREATE FILES: bug_fixes.patch (Git patch with fixes), tests/test_bug_fixes.py (regression tests), BUG_REPORT.md (bug analysis). Check error handling, input validation, and performance issues. Create the actual files with real fixes.",
                    "gemini_cli": "Debug this HTTPie codebase and CREATE FILES: bug_fixes.patch, test_bug_fixes.py, BUG_REPORT.md. Identify issues with error handling, input validation, and performance. Fix the most critical bugs and create tests to verify the fixes. Generate the actual files."
                },
                "evaluation_criteria": [
                    "bug_identification",
                    "fix_correctness",
                    "test_quality",
                    "code_safety",
                    "performance_impact"
                ],
                "expected_outputs": ["bug_fixes.patch", "tests/test_bug_fixes.py", "BUG_REPORT.md"]
            },
            
            {
                "id": "test_4_mcp_filesystem_search",
                "name": "Large Codebase Analysis with MCP Filesystem Server",
                "description": "Tests ability to use MCP filesystem server for searching and analyzing code",
                "repo": "data_science",
                "setup_mcp": True,
                "prompts": {
                    "claude_code": "Connect to the filesystem MCP server running on this repository. Use the MCP search functionality to: 1) Find all Python files containing 'matplotlib', 2) Search for data processing patterns across notebooks, 3) Identify duplicate code across files, 4) Generate a comprehensive analysis report with visualizations of code structure. Use the MCP server's search and read capabilities extensively.",
                    "codex": "Use the filesystem search capabilities to analyze this codebase. Find all files using matplotlib, identify common data processing patterns, detect code duplication, and create an analysis report with code structure visualization. Search recursively through all notebooks and Python files.",
                    "gemini_cli": "Analyze this repository using filesystem search capabilities. Search for: matplotlib usage, data processing patterns, and duplicate code. Use Google Search to find best practices for the patterns you discover. Create a detailed analysis report with recommendations."
                },
                "evaluation_criteria": [
                    "mcp_usage",
                    "search_effectiveness",
                    "pattern_identification",
                    "analysis_depth",
                    "tool_integration"
                ],
                "expected_outputs": ["analysis_report.md", "code_patterns.json", "duplication_report.md", "visualization.html"]
            },
            
            {
                "id": "test_5_refactoring",
                "name": "Large-Scale Refactoring of Data Science Code",
                "description": "Tests ability to refactor and modernize Jupyter notebooks",
                "repo": "data_science",
                "prompts": {
                    "claude_code": "Refactor the Python Data Science Handbook notebooks into a modern, modular Python package. Extract reusable functions, add type hints, create a proper package structure, and include documentation. Make it pip-installable.",
                    "codex": "Convert these Jupyter notebooks into a well-structured Python package. Extract common functions, add typing, create proper modules, write documentation, and make it installable.",
                    "gemini_cli": "Refactor all notebooks in this repository into a clean Python package. Modularize the code, add type annotations, create clear package structure, document everything, and add setup.py."
                },
                "evaluation_criteria": [
                    "refactoring_quality",
                    "code_organization",
                    "type_safety",
                    "documentation_completeness",
                    "package_structure"
                ],
                "expected_outputs": ["setup.py", "src/__init__.py", "README.md", "docs/"]
            },
            
            {
                "id": "test_6_testing_automation",
                "name": "Comprehensive Test Suite Creation",
                "description": "Tests ability to create full test coverage for a large TypeScript codebase",
                "repo": "microservice",
                "prompts": {
                    "claude_code": "Using TDD principles: Create a comprehensive test suite for this VS Code TypeScript codebase. Include unit tests, integration tests, and end-to-end tests. Achieve at least 80% code coverage. Add CI/CD configuration.",
                    "codex": "Create complete test coverage for this VS Code TypeScript project. Write unit, integration, and e2e tests. Set up CI/CD pipeline with GitHub Actions. Target 80%+ coverage.",
                    "gemini_cli": "Build a full test suite for this VS Code TypeScript codebase. Create unit tests, integration tests, and end-to-end tests. Configure CI/CD with test automation. Achieve high code coverage."
                },
                "evaluation_criteria": [
                    "test_coverage",
                    "test_types",
                    "ci_cd_setup",
                    "test_quality",
                    "edge_cases"
                ],
                "expected_outputs": ["tests/", ".github/workflows/test.yml", "coverage_report.html"]
            }
        ]
    
    def clone_repository(self, repo_key: str, target_dir: Path) -> bool:
        """Copy a pre-cloned test repository to target directory"""
        # Ensure target directory is clean
        if target_dir.exists():
            shutil.rmtree(target_dir)
        
        # Look for pre-cloned repository first
        pre_cloned_path = self.repos_dir / repo_key
        
        if pre_cloned_path.exists():
            try:
                print(f"  Copying {repo_key} from pre-cloned repository...")
                shutil.copytree(pre_cloned_path, target_dir, ignore=shutil.ignore_patterns('.git'))
                return True
            except Exception as e:
                print(f"  Error copying pre-cloned repository: {e}")
                # Fall back to direct cloning
        
        # Fallback: clone directly from GitHub
        repo_url = self.test_repos.get(repo_key)
        if not repo_url:
            print(f"Unknown repository: {repo_key}")
            return False
            
        try:
            print(f"  Cloning {repo_key} from {repo_url} (fallback)...")
            git.Repo.clone_from(repo_url, target_dir, depth=1)
            return True
        except Exception as e:
            print(f"  Error cloning repository: {e}")
            return False
    
    def check_tool_availability(self) -> Dict[str, bool]:
        """Check which tools are installed and available"""
        available = {}
        for tool_id, tool_config in self.tools.items():
            try:
                result = subprocess.run(
                    tool_config["setup_check"].split(),
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                available[tool_id] = result.returncode == 0
            except:
                available[tool_id] = False
        return available
        
    def setup_mcp_filesystem_server(self, test_dir: Path) -> Dict[str, str]:
        """Setup filesystem MCP server for testing"""
        print("  Setting up filesystem MCP server...")
        
        # Create MCP configurations for different tools
        
        # Claude Code - uses .claude directory and config
        claude_dir = test_dir / ".claude"
        claude_dir.mkdir(exist_ok=True)
        claude_config = {
            "mcpServers": {
                "filesystem": {
                    "command": "npx",
                    "args": ["-y", "@modelcontextprotocol/server-filesystem", str(test_dir)]
                }
            }
        }
        with open(claude_dir / "config.json", "w") as f:
            json.dump(claude_config, f, indent=2)
        
        # Codex - uses ~/.codex/config.toml format
        codex_config_toml = f'''[mcp_servers.filesystem]
command = "npx"
args = ["-y", "@modelcontextprotocol/server-filesystem", "{test_dir}"]
'''
        codex_dir = test_dir / ".codex"
        codex_dir.mkdir(exist_ok=True)
        with open(codex_dir / "config.toml", "w") as f:
            f.write(codex_config_toml)
        
        # Gemini CLI - uses .gemini/settings.json
        gemini_dir = test_dir / ".gemini"
        gemini_dir.mkdir(exist_ok=True)
        gemini_config = {
            "mcpServers": {
                "filesystem": {
                    "command": "npx",
                    "args": ["-y", "@modelcontextprotocol/server-filesystem", str(test_dir)],
                    "env": {}
                }
            }
        }
        with open(gemini_dir / "settings.json", "w") as f:
            json.dump(gemini_config, f, indent=2)
            
        # Create helper script for tools that don't have native MCP support
        filesystem_api_script = f'''#!/usr/bin/env python3
"""Filesystem search API for tools without MCP support"""
import os
import re
import json
from pathlib import Path

def search_files(pattern, file_extension=None):
    """Search for files containing pattern"""
    results = []
    root_dir = Path("{test_dir}")
    
    for file_path in root_dir.rglob("*"):
        if file_path.is_file():
            if file_extension and not str(file_path).endswith(file_extension):
                continue
            try:
                content = file_path.read_text(errors='ignore')
                if re.search(pattern, content, re.IGNORECASE):
                    results.append({{
                        "file": str(file_path.relative_to(root_dir)),
                        "matches": len(re.findall(pattern, content, re.IGNORECASE))
                    }})
            except:
                pass
    return results

def find_duplicates(min_lines=5):
    """Find duplicate code blocks"""
    # Simplified duplicate detection
    code_blocks = {{}}
    duplicates = []
    
    for file_path in Path("{test_dir}").rglob("*.py"):
        try:
            lines = file_path.read_text().splitlines()
            for i in range(len(lines) - min_lines):
                block = "\\n".join(lines[i:i+min_lines])
                if block.strip():
                    if block in code_blocks:
                        duplicates.append({{
                            "block": block[:100] + "...",
                            "files": [code_blocks[block], str(file_path)]
                        }})
                    else:
                        code_blocks[block] = str(file_path)
        except:
            pass
    return duplicates

# Example usage
if __name__ == "__main__":
    print("Searching for matplotlib usage...")
    matplotlib_files = search_files("matplotlib", ".py")
    print(json.dumps(matplotlib_files, indent=2))
'''
        
        # Save filesystem API script
        api_script_path = test_dir / "filesystem_search.py"
        api_script_path.write_text(filesystem_api_script)
        api_script_path.chmod(0o755)
        
        # Instructions for each tool
        instructions = {
            "claude_code": f"MCP filesystem server configured in .claude/config.json. It should automatically discover and connect.",
            "codex": f"MCP filesystem server configured in .codex/config.toml. Use the filesystem tools to search and analyze code.",
            "gemini_cli": f"MCP filesystem server configured in .gemini/settings.json. Use /mcp command to see available tools, then use filesystem tools for searching."
        }
        
        return instructions
    
    def execute_test(self, tool_id: str, test: Dict, test_dir: Path) -> Dict:
        """Execute a single test for a specific tool"""
        print(f"\n  Executing {test['name']} with {self.tools[tool_id]['name']}...")
        
        # Clone the repository
        if not self.clone_repository(test["repo"], test_dir):
            return {
                "success": False,
                "error": "Failed to clone repository",
                "outputs": {}
            }
        
        # Setup MCP if needed
        mcp_instructions = {}
        if test.get("setup_mcp"):
            mcp_instructions = self.setup_mcp_filesystem_server(test_dir)
            print(f"  MCP setup complete. Instructions: {mcp_instructions.get(tool_id, 'N/A')}")
            
        # Prepare command
        tool_config = self.tools[tool_id]
        prompt = test["prompts"][tool_id]
        
        # Add MCP instructions to prompt if applicable
        if tool_id in mcp_instructions:
            prompt = f"{mcp_instructions[tool_id]} {prompt}"
        
        # Enhanced prompt for Gemini to ensure action execution
        if tool_id == "gemini_cli":
            # Add explicit action instruction for Gemini
            action_prompt = f"""IMPORTANT: You must actually CREATE the files, not just describe them. Use file creation actions to write the content.

{prompt}

Remember: Execute the file creation actions. I need the actual files created in the current directory."""
            prompt = action_prompt
        
        # Create execution script based on tool and test type
        tool_config = self.tools[tool_id]
        cli_flags = tool_config.get("cli_flags", {})
        
        if tool_id == "claude_code":
            # Claude Code uses --print for non-interactive mode and --dangerously-skip-permissions for file creation
            exec_script = f'''#!/bin/bash
cd {test_dir}
export ANTHROPIC_API_KEY="{os.environ.get('ANTHROPIC_API_KEY', '')}"
{tool_config['command']} --print --dangerously-skip-permissions "{prompt}" 2>&1
'''
        elif tool_id == "codex":
            # Always use exec mode for non-interactive execution
            # Filter out verbose logging and extract just the response
            exec_script = f'''#!/bin/bash
cd {test_dir}
export OPENAI_API_KEY="{os.environ.get('OPENAI_API_KEY', '')}"
# Run codex and filter output to extract just the response
{tool_config['command']} exec --skip-git-repo-check "{prompt}" 2>&1 | awk '
BEGIN {{ capturing = 0 }}
/^\\[.*\\] codex$/ {{ capturing = 1; next }}
/^\\[.*\\] tokens used:/ {{ capturing = 0; next }}
capturing == 1 {{ print }}
'
'''
        else:  # gemini_cli - Enhanced execution patterns
            # Suppress Node.js deprecation warnings more effectively
            node_env = 'NODE_NO_WARNINGS=1 NODE_OPTIONS="--no-deprecation --no-warnings"'
            
            if test.get("setup_mcp"):
                # For MCP tests, use specific MCP commands
                exec_script = f'''#!/bin/bash
cd {test_dir}
export OPENAI_API_KEY="{os.environ.get('OPENAI_API_KEY', '')}"
{node_env} {tool_config['command']} {cli_flags.get('prompt', '')} "{prompt}" 2>&1
'''
            elif test["id"] in ["test_1_codebase_understanding"]:
                # Use all_files flag and yolo mode for comprehensive analysis
                # Add explicit instructions for file creation
                exec_script = f'''#!/bin/bash
cd {test_dir}
export OPENAI_API_KEY="{os.environ.get('OPENAI_API_KEY', '')}"
echo "Executing Gemini with action enforcement..."
{node_env} {tool_config['command']} --all_files --yolo --prompt "{prompt}" 2>&1
'''
            else:
                # Standard prompt mode with enhanced action enforcement
                exec_script = f'''#!/bin/bash
cd {test_dir}
export OPENAI_API_KEY="{os.environ.get('OPENAI_API_KEY', '')}"
{node_env} {tool_config['command']} --yolo --prompt "{prompt}" 2>&1
'''
            
        script_path = test_dir / "execute.sh"
        script_path.write_text(exec_script)
        script_path.chmod(0o755)
        
        # Take snapshot of existing files before execution
        existing_files = set()
        file_timestamps = {}
        for file_path in test_dir.rglob("*"):
            if file_path.is_file() and ".git" not in str(file_path):
                rel_path = str(file_path.relative_to(test_dir))
                existing_files.add(rel_path)
                file_timestamps[rel_path] = file_path.stat().st_mtime

        # Execute with timeout
        start_time = time.time()
        try:
            result = subprocess.run(
                str(script_path),
                shell=True,
                capture_output=True,
                text=True,
                timeout=600  # 10 minute timeout for complex tasks
            )
            execution_time = time.time() - start_time
            
            # Detect file changes after execution
            created_files = []
            modified_files = []
            
            for file_path in test_dir.rglob("*"):
                if file_path.is_file() and ".git" not in str(file_path):
                    rel_path = str(file_path.relative_to(test_dir))
                    
                    if rel_path not in existing_files:
                        # New file created
                        created_files.append(rel_path)
                    elif rel_path in file_timestamps:
                        # Check if file was modified
                        new_mtime = file_path.stat().st_mtime
                        if new_mtime > file_timestamps[rel_path]:
                            modified_files.append(rel_path)
            
            # Check if continuation is needed for Gemini
            needs_continuation = self._check_needs_continuation(tool_id, result.stdout, created_files, test.get("expected_outputs", []))
            
            if needs_continuation and tool_id == "gemini_cli":
                print(f"  Gemini seems to need continuation - attempting follow-up...")
                continuation_result = self._attempt_continuation(tool_id, test, test_dir, result.stdout)
                if continuation_result.get("continuation_attempted"):
                    result.stdout = continuation_result["stdout"]
                    result.stderr = continuation_result.get("stderr", result.stderr)
                    
                    # Re-scan for created files after continuation
                    for file_path in test_dir.rglob("*"):
                        if file_path.is_file() and ".git" not in str(file_path):
                            rel_path = str(file_path.relative_to(test_dir))
                            if rel_path not in existing_files and rel_path not in created_files:
                                created_files.append(rel_path)
            
            # Collect outputs from expected files
            outputs = {}
            for expected_file in test.get("expected_outputs", []):
                # Check for file in various locations
                possible_paths = [
                    test_dir / expected_file,
                    test_dir / Path(expected_file).name,
                    *list(test_dir.rglob(Path(expected_file).name))
                ]
                
                for file_path in possible_paths:
                    if file_path.exists() and file_path.is_file():
                        try:
                            outputs[expected_file] = file_path.read_text(encoding='utf-8', errors='ignore')[:5000]  # First 5000 chars
                        except Exception as e:
                            outputs[expected_file] = f"Error reading file: {e}"
                        break
            
            # Collect samples of created files for validation
            created_files_content = {}
            for file_path in created_files[:10]:  # Limit to first 10 created files
                try:
                    full_path = test_dir / file_path
                    content = full_path.read_text(encoding='utf-8', errors='ignore')
                    created_files_content[file_path] = {
                        "size": len(content),
                        "preview": content[:500] + "..." if len(content) > 500 else content,
                        "lines": content.count('\n') + 1 if content else 0
                    }
                except Exception as e:
                    created_files_content[file_path] = {"error": str(e)}
                    
            return {
                "success": result.returncode == 0,
                "execution_time": execution_time,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "outputs": outputs,
                "created_files": created_files,
                "modified_files": modified_files,
                "created_files_content": created_files_content,
                "expected_files_found": [f for f in test.get("expected_outputs", []) if f in outputs],
                "task_completion_indicators": self._analyze_task_completion(result.stdout, test, created_files, outputs)
            }
            
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "execution_time": 600,
                "error": "Test timed out after 10 minutes",
                "outputs": {},
                "created_files": [],
                "modified_files": [],
                "created_files_content": {},
                "expected_files_found": [],
                "task_completion_indicators": {"completion_score": 0, "has_meaningful_output": False}
            }
        except Exception as e:
            return {
                "success": False,
                "execution_time": time.time() - start_time,
                "error": str(e),
                "outputs": {},
                "created_files": [],
                "modified_files": [],
                "created_files_content": {},
                "expected_files_found": [],
                "task_completion_indicators": {"completion_score": 0, "has_meaningful_output": False}
            }
            
    def evaluate_results_with_llm(self, test: Dict, results: Dict[str, Dict]) -> Dict[str, Dict]:
        """Evaluate test results using o3 via LangChain"""
        evaluations = {}
        
        for tool_id, tool_result in results.items():
            # Prepare evaluation prompt
            system_prompt = """You are an expert software engineering evaluator. Your task is to objectively assess AI coding assistant performance.

IMPORTANT: You are evaluating the TASK COMPLETION and CODE QUALITY, not the tool brand or provider. Focus on:
- Actual deliverables produced
- Code quality and correctness
- Task understanding and completion
- Technical accuracy
- Practical utility

Ignore tool names, providers, or any branding. Judge only on the technical merit of the output.

Score each criterion from 0-10 where:
- 0-2: Poor/Failed - Task not understood or major failures
- 3-4: Below Average - Partial understanding, significant issues
- 5-6: Average - Basic task completion with some issues
- 7-8: Good - Task completed well with minor issues
- 9-10: Excellent - Exceptional completion, high quality

Output your evaluation as JSON with this structure:
{
    "scores": {
        "criterion_name": score,
        ...
    },
    "reasoning": {
        "criterion_name": "explanation",
        ...
    },
    "overall_assessment": "summary of performance"
}"""

            # Build evaluation prompt
            eval_prompt = f"""Evaluate this coding assistant's performance on the given task:

TASK DESCRIPTION:
{test['description']}
Specific Request: {test['prompts'][tool_id]}

EXECUTION RESULTS:
- Process completed: {tool_result['success']}
- Execution time: {tool_result['execution_time']:.2f} seconds
- Files created: {len(tool_result.get('created_files', []))}
- Files modified: {len(tool_result.get('modified_files', []))}
- Expected outputs found: {len(tool_result.get('expected_files_found', []))}

TASK COMPLETION INDICATORS:
{json.dumps(tool_result.get('task_completion_indicators', {}), indent=2)}

EXPECTED DELIVERABLES:
{json.dumps(test['expected_outputs'], indent=2)}

ACTUAL FILES CREATED:
{json.dumps(tool_result.get('created_files', [])[:20], indent=2)}

CREATED FILES CONTENT SAMPLES:
{json.dumps(tool_result.get('created_files_content', {}), indent=2)}

EXPECTED OUTPUT CONTENT:
{json.dumps({k: v[:500] + '...' if len(v) > 500 else v for k, v in tool_result.get('outputs', {}).items()}, indent=2)}

ASSISTANT OUTPUT (last 2000 chars):
{tool_result.get('stdout', '')[-2000:]}

EVALUATION CRITERIA:
{json.dumps(test['evaluation_criteria'], indent=2)}

Focus on WHAT was delivered, not WHO delivered it. Evaluate task completion, code quality, and technical accuracy."""

            try:
                # Call LLM for evaluation
                messages = [
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=eval_prompt)
                ]
                
                response = self.evaluator.invoke(messages)
                
                # Parse JSON response
                eval_data = json.loads(response.content)
                
                evaluations[tool_id] = {
                    "scores": eval_data.get("scores", {}),
                    "reasoning": eval_data.get("reasoning", {}),
                    "overall_assessment": eval_data.get("overall_assessment", ""),
                    "average_score": sum(eval_data.get("scores", {}).values()) / len(eval_data.get("scores", {})) if eval_data.get("scores") else 0,
                    "execution_time": tool_result["execution_time"],
                    "success": tool_result["success"]
                }
                
            except Exception as e:
                print(f"  LLM evaluation error for {tool_id}: {e}")
                # Fallback to basic scoring
                evaluations[tool_id] = self._fallback_evaluation(test, tool_result)
                
        return evaluations
    
    def _fallback_evaluation(self, test: Dict, tool_result: Dict) -> Dict:
        """Fallback evaluation if LLM fails"""
        scores = {}
        completion_indicators = tool_result.get("task_completion_indicators", {})
        
        for criterion in test["evaluation_criteria"]:
            base_score = 3  # Lower baseline
            
            if not tool_result["success"]:
                scores[criterion] = 1  # Failed execution
            else:
                # Improved heuristic scoring based on actual deliverables
                completion_score = completion_indicators.get("completion_score", 0) * 4  # 0-4 points
                
                # Bonus for creating expected files
                expected_files_bonus = len(tool_result.get("expected_files_found", [])) * 1.5
                
                # Bonus for creating any files (capped)
                created_files_bonus = min(2, len(tool_result.get("created_files", [])) * 0.5)
                
                # Time penalty for very slow execution
                time_penalty = 1 if tool_result["execution_time"] > 300 else 0  # 5+ minutes
                
                final_score = base_score + completion_score + expected_files_bonus + created_files_bonus - time_penalty
                scores[criterion] = min(10, max(1, final_score))
                
        return {
            "scores": scores,
            "reasoning": {
                "fallback": f"LLM evaluation failed. Heuristic based on: completion_score={completion_indicators.get('completion_score', 0):.2f}, expected_files={len(tool_result.get('expected_files_found', []))}, created_files={len(tool_result.get('created_files', []))}"
            },
            "overall_assessment": "Fallback evaluation used - scores may be less accurate",
            "average_score": sum(scores.values()) / len(scores) if scores else 0,
            "execution_time": tool_result["execution_time"],
            "success": tool_result["success"]
        }
        
    def generate_report(self, all_results: Dict):
        """Generate comprehensive comparison report"""
        report_path = self.results_dir / f"report_{self.test_timestamp}.md"
        
        with open(report_path, "w") as f:
            f.write("# AI CLI Tools Comparison Report\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Tool availability
            f.write("## Tool Availability\n\n")
            for tool_id, available in all_results["availability"].items():
                status = "✅ Available" if available else "❌ Not Available"
                f.write(f"- **{self.tools[tool_id]['name']}**: {status}\n")
            f.write("\n")
            
            # Test repositories used
            f.write("## Test Repositories\n\n")
            for repo_key, repo_url in self.test_repos.items():
                f.write(f"- **{repo_key}**: {repo_url}\n")
            f.write("\n")
            
            # Test results summary
            f.write("## Test Results Summary\n\n")
            
            # Create summary table
            f.write("| Test | " + " | ".join([self.tools[t]["name"] for t in self.tools]) + " |\n")
            f.write("|------|" + "|".join(["------" for _ in self.tools]) + "|\n")
            
            for test_id, test_results in all_results["tests"].items():
                test_name = next(t["name"] for t in self.tests if t["id"] == test_id)
                scores = []
                for tool_id in self.tools:
                    if tool_id in test_results["evaluations"]:
                        avg_score = test_results["evaluations"][tool_id]["average_score"]
                        scores.append(f"{avg_score:.1f}/10")
                    else:
                        scores.append("N/A")
                f.write(f"| {test_name[:40]}... | " + " | ".join(scores) + " |\n")
                
            # Detailed results
            f.write("\n## Detailed Test Results\n\n")
            for test in self.tests:
                test_id = test["id"]
                if test_id not in all_results["tests"]:
                    continue
                    
                f.write(f"### {test['name']}\n\n")
                f.write(f"**Description**: {test['description']}\n")
                f.write(f"**Repository**: {test['repo']} ({self.test_repos[test['repo']]})\n\n")
                
                test_results = all_results["tests"][test_id]
                
                for tool_id, tool_config in self.tools.items():
                    if tool_id not in test_results["evaluations"]:
                        continue
                        
                    f.write(f"#### {tool_config['name']}\n\n")
                    eval_data = test_results["evaluations"][tool_id]
                    raw_result = test_results["results"][tool_id]
                    
                    f.write(f"- **Success**: {'✅' if eval_data['success'] else '❌'}\n")
                    f.write(f"- **Execution Time**: {eval_data['execution_time']:.2f}s\n")
                    f.write(f"- **Average Score**: {eval_data['average_score']:.1f}/10\n")
                    
                    # New file tracking metrics
                    f.write(f"- **Files Created**: {len(raw_result.get('created_files', []))}\n")
                    f.write(f"- **Files Modified**: {len(raw_result.get('modified_files', []))}\n")
                    f.write(f"- **Expected Files Found**: {len(raw_result.get('expected_files_found', []))}/{len(test.get('expected_outputs', []))}\n")
                    
                    # Task completion indicators
                    completion_indicators = raw_result.get("task_completion_indicators", {})
                    completion_score = completion_indicators.get("completion_score", 0)
                    f.write(f"- **Task Completion Score**: {completion_score:.2f}/1.0\n")
                    
                    # Show which expected files were found
                    if raw_result.get('expected_files_found'):
                        f.write(f"- **Expected Files Created**: {', '.join(raw_result['expected_files_found'])}\n")
                    
                    # Show created files sample
                    if raw_result.get('created_files'):
                        f.write(f"- **Sample Created Files**: {', '.join(raw_result['created_files'][:5])}\n")
                        if len(raw_result['created_files']) > 5:
                            f.write(f"  (and {len(raw_result['created_files']) - 5} more)\n")
                    
                    f.write("\n")
                    
                    f.write("**Scores by Criteria**:\n")
                    for criterion, score in eval_data["scores"].items():
                        reasoning = eval_data.get("reasoning", {}).get(criterion, "")
                        f.write(f"- {criterion}: {score}/10\n")
                        if reasoning:
                            f.write(f"  - *{reasoning}*\n")
                    
                    if eval_data.get("overall_assessment"):
                        f.write(f"\n**Overall Assessment**: {eval_data['overall_assessment']}\n")
                    
                    # Add task completion breakdown
                    if completion_indicators:
                        f.write("\n**Task Completion Analysis**:\n")
                        for indicator, value in completion_indicators.items():
                            if indicator != "completion_score":
                                status = "✅" if value else "❌"
                                f.write(f"- {indicator.replace('_', ' ').title()}: {status}\n")
                    
                    f.write("\n")
                    
            # Overall recommendations
            f.write("## Overall Analysis\n\n")
            
            # Calculate overall scores
            overall_scores = {}
            for tool_id in self.tools:
                tool_scores = []
                for test_id in all_results["tests"]:
                    if tool_id in all_results["tests"][test_id]["evaluations"]:
                        tool_scores.append(all_results["tests"][test_id]["evaluations"][tool_id]["average_score"])
                overall_scores[tool_id] = sum(tool_scores) / len(tool_scores) if tool_scores else 0
                
            # Sort by score
            sorted_tools = sorted(overall_scores.items(), key=lambda x: x[1], reverse=True)
            
            f.write("### Overall Performance Ranking\n\n")
            for i, (tool_id, score) in enumerate(sorted_tools, 1):
                f.write(f"{i}. **{self.tools[tool_id]['name']}**: {score:.1f}/10\n")
                
            f.write("\n### Recommendations by Use Case\n\n")
            f.write("Based on the test results:\n\n")
            f.write("- **Complex Reasoning & Architecture**: Best tool based on test_1_codebase_understanding\n")
            f.write("- **Feature Development**: Best tool based on test_2_feature_implementation\n")
            f.write("- **Bug Fixing**: Best tool based on test_3_bug_fixing\n")
            f.write("- **Code Refactoring**: Best tool based on test_4_refactoring\n")
            f.write("- **Test Automation**: Best tool based on test_5_testing_automation\n")
            f.write("- **External Integrations**: Best tool based on test_6_mcp_integration\n")
            
        print(f"\nReport generated: {report_path}")
        return report_path
        
    def run_all_tests(self, selected_tools: Optional[List[str]] = None):
        """Run all tests for selected tools"""
        print("Starting AI CLI Tools Comparison Tests...")
        print("Using real repositories for testing")
        
        # Check tool availability
        availability = self.check_tool_availability()
        print("\nTool Availability:")
        for tool_id, available in availability.items():
            print(f"  {self.tools[tool_id]['name']}: {'✅' if available else '❌'}")
            
        # Filter tools based on availability and selection
        tools_to_test = []
        for tool_id in self.tools:
            if availability.get(tool_id, False):
                if selected_tools is None or tool_id in selected_tools:
                    tools_to_test.append(tool_id)
                    
        if not tools_to_test:
            print("\nNo tools available for testing!")
            return
            
        print(f"\nTesting {len(tools_to_test)} tools across {len(self.tests)} tests...")
        
        all_results = {
            "availability": availability,
            "tests": {}
        }
        
        # Run each test
        for test in self.tests:
            print(f"\n{'='*60}")
            print(f"Running Test: {test['name']}")
            print(f"Repository: {test['repo']}")
            print(f"{'='*60}")
            
            test_results = {}
            
            for tool_id in tools_to_test:
                # Create isolated test directory
                with tempfile.TemporaryDirectory() as temp_dir:
                    test_dir = Path(temp_dir)
                    
                    # Execute test
                    result = self.execute_test(tool_id, test, test_dir)
                    test_results[tool_id] = result
                    
                    # Save outputs
                    output_dir = self.results_dir / test["id"] / tool_id
                    output_dir.mkdir(parents=True, exist_ok=True)
                    
                    # Save execution log
                    log_data = {
                        "test": test,
                        "result": result,
                        "timestamp": datetime.now().isoformat()
                    }
                    with open(output_dir / "execution_log.json", "w") as f:
                        json.dump(log_data, f, indent=2)
                            
            # Evaluate results using LLM
            print("\n  Evaluating results with o3...")
            evaluations = self.evaluate_results_with_llm(test, test_results)
            
            all_results["tests"][test["id"]] = {
                "results": test_results,
                "evaluations": evaluations
            }
            
        # Generate report
        report_path = self.generate_report(all_results)
        
        # Save raw results
        results_json_path = self.results_dir / f"results_{self.test_timestamp}.json"
        with open(results_json_path, "w") as f:
            json.dump(all_results, f, indent=2, default=str)
            
        print(f"\nResults saved: {results_json_path}")
        
        # Optional: Generate visualizations
        if self.generate_viz:
            self._generate_visualizations(results_json_path)
        else:
            print(f"\n📈 Skipping visualization generation (--no-viz flag used)")
            print(f"   Run manually: python results.py {results_json_path}")
        
        print("\nTesting complete!")
        
        return all_results
    
    def _generate_visualizations(self, results_json_path: Path):
        """Generate visualizations if matplotlib is available"""
        try:
            # Try to import visualization dependencies
            import matplotlib
            import seaborn
            
            # Import the results visualizer
            from pathlib import Path
            import subprocess
            
            print("\n📈 Generating visualizations...")
            
            # Run the results.py script
            result = subprocess.run([
                sys.executable, "results.py", str(results_json_path)
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                print("✅ Visualizations generated successfully!")
                print("📁 Check the test_results directory for charts")
            else:
                print(f"⚠️  Visualization generation failed: {result.stderr}")
                
        except ImportError:
            print("\n📈 Visualization libraries not available.")
            print("   Install with: pip install matplotlib seaborn")
            print(f"   Then run: python results.py {results_json_path}")
        except subprocess.TimeoutExpired:
            print("⚠️  Visualization generation timed out")
        except Exception as e:
            print(f"⚠️  Could not generate visualizations: {e}")
            print(f"   Run manually: python results.py {results_json_path}")
    
    def _analyze_task_completion(self, stdout: str, test: Dict, created_files: List[str], outputs: Dict) -> Dict:
        """Analyze indicators of task completion"""
        indicators = {
            "has_meaningful_output": len(stdout.strip()) > 100,
            "created_expected_files": len([f for f in test.get("expected_outputs", []) if any(f in cf for cf in created_files)]) > 0,
            "found_expected_content": len(outputs) > 0,
            "shows_progress_or_completion": any(keyword in stdout.lower() for keyword in [
                "created", "generated", "implemented", "added", "completed", "done", "finished",
                "analysis complete", "documentation", "test", "file", "component"
            ]),
            "appears_to_understand_task": any(keyword in stdout.lower() for keyword in [
                test.get("repo", "").lower(), "application", "code", "architecture", "feature"
            ]),
            "provides_structured_response": any(marker in stdout for marker in ["#", "```", "1.", "-", "*"]),
            "shows_code_analysis": any(keyword in stdout.lower() for keyword in [
                "function", "class", "variable", "import", "module", "endpoint", "route"
            ])
        }
        
        # Calculate completion score
        completion_score = sum(1 for v in indicators.values() if v) / len(indicators)
        indicators["completion_score"] = completion_score
        
        return indicators
    
    def _check_needs_continuation(self, tool_id: str, stdout: str, created_files: List[str], expected_outputs: List[str]) -> bool:
        """Check if the tool seems to need a continuation prompt"""
        if tool_id != "gemini_cli":
            return False
            
        # Enhanced indicators that Gemini might need continuation
        incomplete_indicators = [
            "would you like me to" in stdout.lower(),
            "shall i" in stdout.lower(),
            "do you want me to" in stdout.lower(),
            "should i" in stdout.lower(),
            "i'll start by" in stdout.lower() and "complete" not in stdout.lower()[-500:],
            "let me know if" in stdout.lower(),
            "i will now create" in stdout.lower() and len(created_files) == 0,
            "based on my analysis" in stdout.lower() and len(created_files) == 0,
            "first, i will analyze" in stdout.lower(),
            # New indicators specific to the logs we see
            "i will perform a deep analysis" in stdout.lower() and len(created_files) == 0,
            "i will now create the files" in stdout.lower() and len(created_files) == 0
        ]
        
        # Check if no expected files were created
        no_expected_files = len([f for f in expected_outputs if any(f.lower() in cf.lower() for cf in created_files)]) == 0
        
        has_incomplete_indicator = any(indicator for indicator in incomplete_indicators)
        
        # More aggressive continuation check for Gemini
        short_response_with_promise = len(stdout.strip()) < 500 and any([
            "create" in stdout.lower(),
            "analysis" in stdout.lower(),
            "files" in stdout.lower()
        ])
        
        return has_incomplete_indicator or (no_expected_files and (len(stdout.strip()) < 2000 or short_response_with_promise))
    
    def _attempt_continuation(self, tool_id: str, test: Dict, test_dir: Path, previous_stdout: str) -> Dict:
        """Attempt to continue a task if the tool seems to have stopped mid-task"""
        print(f"  Attempting continuation for {tool_id}...")
        
        tool_config = self.tools[tool_id]
        cli_flags = tool_config.get("cli_flags", {})
        
        # Create a more specific continuation prompt for Gemini
        if "create the files" in previous_stdout.lower() or "i will now create" in previous_stdout.lower():
            continuation_prompt = f"""You said you would create the files but I don't see them yet. Please ACTUALLY CREATE these files now:

{', '.join(test.get('expected_outputs', []))}

Use file creation actions to write the actual files with the analysis content. Don't just describe what you would put in them - CREATE THE ACTUAL FILES."""
        else:
            continuation_prompt = f"""Please continue with the task and CREATE the actual files: {', '.join(test.get('expected_outputs', []))}. 

Don't just analyze or describe - use file creation actions to write the files with your analysis content. I need the actual markdown files created."""
        
        # Execute continuation with better environment setup
        if tool_id == "gemini_cli":
            node_env = 'NODE_NO_WARNINGS=1 NODE_OPTIONS="--no-deprecation --no-warnings"'
            exec_script = f'''#!/bin/bash
cd {test_dir}
export OPENAI_API_KEY="{os.environ.get('OPENAI_API_KEY', '')}"
echo "Attempting continuation with explicit file creation request..."
{node_env} {tool_config['command']} --yolo {cli_flags.get('prompt', '')} "{continuation_prompt}" 2>&1
'''
        else:
            # For other tools, use standard approach
            exec_script = f'''#!/bin/bash
cd {test_dir}
export ANTHROPIC_API_KEY="{os.environ.get('ANTHROPIC_API_KEY', '')}"
{tool_config['command']} "{continuation_prompt}" 2>&1
'''
        
        script_path = test_dir / "continue.sh"
        script_path.write_text(exec_script)
        script_path.chmod(0o755)
        
        try:
            result = subprocess.run(
                str(script_path),
                shell=True,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout for continuation
            )
            
            return {
                "success": result.returncode == 0,
                "stdout": previous_stdout + "\n\n--- CONTINUATION ---\n\n" + result.stdout,
                "stderr": result.stderr,
                "continuation_attempted": True
            }
            
        except Exception as e:
            return {
                "success": False,
                "stdout": previous_stdout,
                "stderr": f"Continuation failed: {e}",
                "continuation_attempted": True
            }
    
def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description="AI CLI Tools Testing Framework")
    parser.add_argument("--repos-dir", default="test_repositories", 
                        help="Directory containing test repositories")
    parser.add_argument("--results-dir", default="test_results", 
                        help="Directory to store test results")
    parser.add_argument("--tools", nargs="+", 
                        choices=["claude_code", "codex", "gemini_cli"],
                        help="Specific tools to test (default: all available)")
    parser.add_argument("--quick", action="store_true", 
                        help="Run only first 3 tests for quick evaluation")
    parser.add_argument("--no-viz", action="store_true",
                        help="Skip visualization generation")
    
    args = parser.parse_args()
    
    # Initialize tester
    tester = CLIToolTester(
        results_dir=args.results_dir,
        generate_viz=not args.no_viz,
        repos_dir=args.repos_dir
    )
    
    # Filter tests if quick mode
    if args.quick:
        original_tests = tester.tests
        tester.tests = original_tests[:3]  # First 3 tests
        print(f"Running in quick mode: {len(tester.tests)} tests")
    
    # Run tests
    try:
        results = tester.run_all_tests(selected_tools=args.tools)
        print(f"\n✅ Testing completed successfully!")
        return 0
    except KeyboardInterrupt:
        print(f"\n⚠️  Testing interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ Testing failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit(main())