# main_script.py
import argparse

from expd.config import Config
from expd.core import ExperimentRunner
from expd.interface import AppInterface

# 結果を保存するCSVファイル名
RESULTS_FILE = "experiment_results.csv"


def main() -> None:
    """メイン処理"""
    parser = argparse.ArgumentParser(description="探索的プログラミング支援ツール")
    parser.add_argument(
        "--config", type=str, default="config.yaml", help="設定ファイルのパス"
    )
    args = parser.parse_args()

    print("探索的プログラミング支援ツールを開始します。")

    try:
        # 1. 設定ファイルの読み込み
        config = Config(args.config)
        print(f"設定ファイルを読み込みました: {args.config}")
    except Exception as e:
        print(f"エラー: 設定ファイルの読み込みに失敗しました。詳細: {e}")
        return

    target_script = config.target_script

    # 2. 外部スクリプトのインターフェースの初期化
    app_interface = AppInterface(
        target_script=target_script,
        metrics_config=config.metrics,
    )

    # 3. 実験ランナーの初期化
    runner = ExperimentRunner(config=config, app_interface=app_interface)

    # 4. 実験の実行
    runner.run(results_file=RESULTS_FILE)


if __name__ == "__main__":
    main()
