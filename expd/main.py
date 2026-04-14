# main_script.py

from expd.config import Config
from expd.core import ExperimentRunner
from expd.interface import AppInterface

# 設定ファイル名
CONFIG_FILE = "config.yaml"
# 結果を保存するCSVファイル名
RESULTS_FILE = "experiment_results.csv"


def main() -> None:
    """メイン処理"""
    print("探索的プログラミング支援ツールを開始します。")

    try:
        # 1. 設定ファイルの読み込み
        config = Config(CONFIG_FILE)
        print(f"設定ファイルを読み込みました: {CONFIG_FILE}")
    except Exception as e:
        print(f"エラー: 設定ファイルの読み込みに失敗しました。詳細: {e}")
        return

    target_script = config.target_script

    # 2. 外部スクリプトのインターフェースの初期化
    app_interface = AppInterface(target_script=target_script)

    # 3. 実験ランナーの初期化
    runner = ExperimentRunner(config=config, app_interface=app_interface)

    # 4. 実験の実行
    runner.run(results_file=RESULTS_FILE)


if __name__ == "__main__":
    main()
