"""
Interface module for connecting with external applications.
"""

import re
import subprocess
from typing import Any, Dict, List, Optional, Tuple


class AppInterface:
    """Interface for external application integration."""

    def __init__(self, target_script: str):
        self.target_script = target_script

    def build_command(self, params: Dict[str, Any]) -> List[str]:
        """Build command line from parameters."""
        cmd = ["python", self.target_script]
        for key, value in params.items():
            cmd.append(f"--{key}")
            cmd.append(str(value))
        return cmd

    def execute(self, cmd: List[str]) -> Tuple[Optional[str], Optional[Exception]]:
        """Execute external application with given command."""
        print(f"  実行中: {' '.join(cmd)}")
        try:
            process = subprocess.run(
                cmd, capture_output=True, text=True, check=True, encoding="utf-8"
            )
            return process.stdout, None
        except subprocess.CalledProcessError as e:
            print("  エラー: コマンドの実行に失敗しました。")
            print(f"  コマンド: {' '.join(e.cmd)}")
            print(f"  リターンコード: {e.returncode}")
            print(f"  標準出力: {e.stdout}")
            print(f"  標準エラー: {e.stderr}")
            return e.stdout, e
        except Exception as e:
            print(f"  予期せぬエラーが発生しました: {e}")
            return None, e

    def parse_results(self, output: str) -> Tuple[Optional[float], Optional[float]]:
        """Parse results from application output."""
        accuracy = None
        loss = None
        if output:
            match = re.search(r"Accuracy:\s*([0-9.]+)", output)
            if match:
                accuracy = float(match.group(1))

            match_loss = re.search(r"Loss:\s*([0-9.]+)", output)
            if match_loss:
                loss = float(match_loss.group(1))
        return accuracy, loss
