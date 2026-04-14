#!/usr/bin/env python3
"""
Development task runner for EXPD project.
Usage: uv run python scripts.py <task>
"""

import subprocess
import sys


def run_command(cmd, cwd=None):
    """Run shell command and return result."""
    try:
        result = subprocess.run(
            cmd, shell=True, cwd=cwd, check=True, capture_output=True, text=True
        )
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
        return False


def task_install():
    """Install dependencies."""
    print("📦 Installing dependencies...")
    return run_command("uv sync")


def task_test():
    """Run tests."""
    print("🧪 Running tests...")
    return run_command("uv run pytest -v")


def task_format():
    """Format code with black and isort."""
    print("🎨 Formatting code...")
    success = True
    success &= run_command("uv run black expd/ scripts.py")
    success &= run_command("uv run isort expd/ scripts.py")
    return success


def task_lint():
    """Run linting with flake8."""
    print("🔍 Running linting...")
    return run_command("uv run flake8 expd/ scripts.py")


def task_type_check():
    """Run type checking with mypy."""
    print("🔍 Running type checks...")
    return run_command("uv run mypy expd/")


def task_check():
    """Run all checks (format, lint, type check)."""
    print("✅ Running all checks...")
    success = True
    success &= task_format()
    success &= task_lint()
    success &= task_type_check()
    return success


def task_experiment():
    """Run sample experiment with existing code."""
    print("🔬 Running sample experiment...")
    return run_command("uv run python expd/main.py")


def task_mlflow():
    """Start MLflow UI server."""
    print("📊 Starting MLflow UI...")
    print("MLflow UI will be available at: http://localhost:5000")
    return run_command("uv run mlflow ui --host 127.0.0.1 --port 5000")


def task_clean():
    """Clean build artifacts and cache."""
    print("🧹 Cleaning build artifacts...")
    artifacts = [
        ".venv",
        "build",
        "dist",
        "*.egg-info",
        "expd/__pycache__",
        "**/__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        "mlruns",
    ]

    for pattern in artifacts:
        run_command(f"rm -rf {pattern}")

    print("✨ Clean complete!")
    return True


def task_dev_deps():
    """Install development dependencies."""
    print("🛠️ Installing development dependencies...")
    return run_command("uv add --dev pytest black isort flake8 mypy")


def task_gui_deps():
    """Install GUI dependencies (Streamlit)."""
    print("🖥️ Installing GUI dependencies...")
    return run_command("uv add streamlit")


def task_optimization_deps():
    """Install optimization dependencies (Optuna)."""
    print("⚡ Installing optimization dependencies...")
    return run_command("uv add optuna")


def task_help():
    """Show available tasks."""
    tasks = {
        "install": "Install dependencies",
        "test": "Run tests",
        "format": "Format code with black and isort",
        "lint": "Run linting with flake8",
        "type-check": "Run type checking with mypy",
        "check": "Run all checks (format, lint, type check)",
        "experiment": "Run sample experiment",
        "mlflow": "Start MLflow UI server",
        "clean": "Clean build artifacts and cache",
        "dev-deps": "Install development dependencies",
        "gui-deps": "Install GUI dependencies",
        "optimization-deps": "Install optimization dependencies",
        "help": "Show this help message",
    }

    print("📋 Available tasks:")
    print()
    for task, description in tasks.items():
        print(f"  {task:<20} {description}")
    print()
    print("Usage: uv run python scripts.py <task>")
    return True


def main():
    """Main task runner."""
    if len(sys.argv) < 2:
        task_help()
        sys.exit(1)

    task_name = sys.argv[1].replace("-", "_")
    task_func = globals().get(f"task_{task_name}")

    if not task_func:
        print(f"❌ Unknown task: {sys.argv[1]}")
        task_help()
        sys.exit(1)

    success = task_func()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
