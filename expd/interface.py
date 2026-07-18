"""
Interface module for connecting with external applications.
"""

import re
import subprocess
from typing import Any, Dict, List, Optional, Tuple


class AppInterface:
    """Interface for external application integration."""

    def __init__(
        self, target_script: str, metrics_config: Optional[Dict[str, str]] = None
    ):
        self.target_script = target_script
        self.metrics_config = metrics_config or {}

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

    def parse_results(self, output: str) -> Dict[str, float]:
        """Parse dynamically configured metrics from application output."""
        results: Dict[str, float] = {}
        if not output:
            return results

        for metric_name, pattern in self.metrics_config.items():
            match = re.search(pattern, output)
            if match:
                try:
                    results[metric_name] = float(match.group(1))
                except ValueError:
                    print(
                        f"  警告: メトリクス '{metric_name}' の値 "
                        f"'{match.group(1)}' を数値に変換できませんでした。"
                    )
        return results
