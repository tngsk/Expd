# main_script.py

import yaml
import subprocess
import itertools
import pandas as pd
import os
import re
from datetime import datetime

# 設定ファイル名
CONFIG_FILE = 'config.yaml'
# 結果を保存するCSVファイル名
RESULTS_FILE = 'experiment_results.csv'
# 実行対象のスクリプト名
TARGET_SCRIPT = 'target_script.py'

def load_config(config_path):
    """設定ファイルを読み込む"""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        print(f"設定ファイルを読み込みました: {config_path}")
        return config
    except FileNotFoundError:
        print(f"エラー: 設定ファイル '{config_path}' が見つかりません。")
        return None
    except yaml.YAMLError as e:
        print(f"エラー: 設定ファイル '{config_path}' の形式が正しくありません。詳細: {e}")
        return None

def generate_param_combinations(parameters_config):
    """
    パラメータ設定から全ての組み合わせを生成する。
    'fixed_params' は固定値として扱い、'grid_params' で指定された値の組み合わせを生成する。
    """
    if not parameters_config:
        print("警告: パラメータ設定が空です。")
        return []

    fixed_params = parameters_config.get('fixed_params', {})
    grid_params_config = parameters_config.get('grid_params', {})

    if not grid_params_config: # グリッドサーチするパラメータがない場合
        if fixed_params:
             print("グリッドパラメータはなく、固定パラメータのみで実行します。")
             return [fixed_params.copy()] # 固定パラメータのみの組み合わせを返す
        else:
            print("警告: 固定パラメータもグリッドパラメータも指定されていません。")
            return []


    # グリッドパラメータのキーと値のリストを準備
    param_names = list(grid_params_config.keys())
    value_lists = [grid_params_config[name] if isinstance(grid_params_config[name], list) else [grid_params_config[name]] for name in param_names]

    combinations = []
    for values_combination in itertools.product(*value_lists):
        current_params = fixed_params.copy() # 固定パラメータをベースにする
        for name, value in zip(param_names, values_combination):
            current_params[name] = value
        combinations.append(current_params)

    print(f"{len(combinations)} 通りのパラメータの組み合わせを生成しました。")
    return combinations

def run_target_script(script_name, params):
    """
    指定されたパラメータで対象スクリプトを実行し、標準出力を返す。
    パラメータはコマンドライン引数として '--key value' の形式で渡される。
    """
    cmd = ['python', script_name]
    for key, value in params.items():
        cmd.append(f'--{key}')
        cmd.append(str(value))

    print(f"  実行中: {' '.join(cmd)}")
    try:
        process = subprocess.run(cmd, capture_output=True, text=True, check=True, encoding='utf-8')
        # 簡単な例として、標準出力から 'Accuracy: X.XX' のような形式の値を抽出
        # より複雑な抽出ロジックが必要な場合は、ここを修正してください。
        match = re.search(r"Accuracy:\s*([0-9.]+)", process.stdout)
        accuracy = float(match.group(1)) if match else None

        match_loss = re.search(r"Loss:\s*([0-9.]+)", process.stdout)
        loss = float(match_loss.group(1)) if match_loss else None

        print(f"  実行完了。Accuracy: {accuracy}, Loss: {loss}")
        return process.stdout, accuracy, loss
    except subprocess.CalledProcessError as e:
        print(f"  エラー: スクリプト '{script_name}' の実行に失敗しました。")
        print(f"  コマンド: {' '.join(e.cmd)}")
        print(f"  リターンコード: {e.returncode}")
        print(f"  標準出力: {e.stdout}")
        print(f"  標準エラー: {e.stderr}")
        return e.stdout, None, None # エラー時も標準出力を返す
    except FileNotFoundError:
        print(f"  エラー: 対象スクリプト '{script_name}' が見つかりません。")
        return None, None, None
    except Exception as e:
        print(f"  予期せぬエラーが発生しました: {e}")
        return None, None, None


def save_results(results_list, filepath):
    """実験結果をCSVファイルに保存または追記する"""
    df = pd.DataFrame(results_list)
    if os.path.exists(filepath):
        print(f"結果を既存のファイル '{filepath}' に追記します。")
        df.to_csv(filepath, mode='a', header=False, index=False, encoding='utf-8-sig')
    else:
        print(f"結果を新しいファイル '{filepath}' に保存します。")
        df.to_csv(filepath, index=False, encoding='utf-8-sig')

def main():
    """メイン処理"""
    print("探索的プログラミング支援ツールを開始します。")

    # 1. 設定ファイルの読み込み
    config = load_config(CONFIG_FILE)
    if not config:
        return

    experiment_name = config.get('experiment_name', 'default_experiment')
    parameters_config = config.get('parameters')
    target_script_to_run = config.get('target_script', TARGET_SCRIPT) # 設定ファイルから対象スクリプト名を取得、なければデフォルト

    if not parameters_config:
        print("エラー: 設定ファイルに 'parameters' セクションが見つかりません。")
        return

    # 2. パラメータの組み合わせを生成
    param_combinations = generate_param_combinations(parameters_config)
    if not param_combinations:
        print("実行するパラメータの組み合わせがありません。処理を終了します。")
        return

    all_results = []
    start_time_experiment = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"\n実験開始: {experiment_name} (開始時刻: {start_time_experiment})")

    # 3. 各パラメータの組み合わせでスクリプトを実行
    for i, params in enumerate(param_combinations):
        print(f"\n試行 {i+1}/{len(param_combinations)}: パラメータ = {params}")

        stdout, accuracy, loss = run_target_script(target_script_to_run, params)

        current_result = {
            'experiment_name': experiment_name,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            **params, # パラメータを展開して辞書に含める
            'accuracy': accuracy,
            'loss': loss,
            # 'raw_stdout': stdout # 必要であれば標準出力全体も保存
        }
        all_results.append(current_result)

    # 4. 結果をCSVファイルに保存
    if all_results:
        save_results(all_results, RESULTS_FILE)
    else:
        print("記録する結果がありませんでした。")

    end_time_experiment = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"\n実験終了: {experiment_name} (終了時刻: {end_time_experiment})")
    print(f"全 {len(param_combinations)} 件の試行が完了しました。結果は '{RESULTS_FILE}' を確認してください。")

if __name__ == '__main__':
    main()
