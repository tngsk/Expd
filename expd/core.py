"""
Core experiment execution functionality.
"""

import itertools
import os
from datetime import datetime
from typing import Any, Dict, List

import pandas as pd

from expd.config import Config
from expd.interface import AppInterface


class ExperimentRunner:
    """Handles the execution of experiments with external applications."""

    def __init__(self, config: Config, app_interface: AppInterface):
        self.config = config
        self.app_interface = app_interface

    def _generate_param_combinations(self) -> List[Dict[str, Any]]:
        """Generate all parameter combinations from configuration."""
        parameters_config = self.config.get("parameters")
        if not parameters_config:
            print("警告: パラメータ設定が空です。")
            return []

        fixed_params = parameters_config.get("fixed_params", {})
        grid_params_config = parameters_config.get("grid_params", {})

        if not grid_params_config:
            if fixed_params:
                print("グリッドパラメータはなく、固定パラメータのみで実行します。")
                return [fixed_params.copy()]
            else:
                print("警告: 固定パラメータもグリッドパラメータも指定されていません。")
                return []

        param_names = list(grid_params_config.keys())
        value_lists = [
            (
                grid_params_config[name]
                if isinstance(grid_params_config[name], list)
                else [grid_params_config[name]]
            )
            for name in param_names
        ]

        combinations = []
        for values_combination in itertools.product(*value_lists):
            current_params = fixed_params.copy()
            for name, value in zip(param_names, values_combination):
                current_params[name] = value
            combinations.append(current_params)

        print(f"{len(combinations)} 通りのパラメータの組み合わせを生成しました。")
        return combinations

    def run(self, results_file: str = "experiment_results.csv") -> None:
        """Execute experiments based on configuration."""
        experiment_name = self.config.experiment_name
        param_combinations = self._generate_param_combinations()

        if not param_combinations:
            print("実行するパラメータの組み合わせがありません。処理を終了します。")
            return

        all_results = []
        start_time_experiment = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n実験開始: {experiment_name} (開始時刻: {start_time_experiment})")

        for i, params in enumerate(param_combinations):
            print(f"\n試行 {i+1}/{len(param_combinations)}: パラメータ = {params}")

            cmd = self.app_interface.build_command(params)
            stdout, error = self.app_interface.execute(cmd)

            accuracy = None
            loss = None
            if stdout is not None:
                accuracy, loss = self.app_interface.parse_results(stdout)

            current_result = {
                "experiment_name": experiment_name,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                **params,
                "accuracy": accuracy,
                "loss": loss,
            }
            all_results.append(current_result)

        if all_results:
            self._save_results(all_results, results_file)
        else:
            print("記録する結果がありませんでした。")

        end_time_experiment = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n実験終了: {experiment_name} (終了時刻: {end_time_experiment})")
        print(
            f"全 {len(param_combinations)} 件の試行が完了しました。結果は '{results_file}' を確認してください。"
        )

    def _save_results(self, results_list: List[Dict[str, Any]], filepath: str) -> None:
        """Save experiment results to a CSV file."""
        df = pd.DataFrame(results_list)
        if os.path.exists(filepath):
            print(f"結果を既存のファイル '{filepath}' に追記します。")
            df.to_csv(
                filepath, mode="a", header=False, index=False, encoding="utf-8-sig"
            )
        else:
            print(f"結果を新しいファイル '{filepath}' に保存します。")
            df.to_csv(filepath, index=False, encoding="utf-8-sig")
