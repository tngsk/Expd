# target_script.py
# これはパラメータを受け取って処理を実行し、結果を標準出力するサンプルスクリプトです。
# 実際の探索対象のスクリプトに置き換えてください。

import argparse
import random
import time

def main():
    parser = argparse.ArgumentParser(description="探索対象のサンプルスクリプト")
    # config.yaml の parameters で定義したキー名と合わせる
    parser.add_argument("--learning_rate", type=float, default=0.01, help="学習率")
    parser.add_argument("--optimizer", type=str, default="adam", help="オプティマイザ")
    parser.add_argument("--epochs", type=int, default=50, help="エポック数")
    parser.add_argument("--batch_size", type=int, default=32, help="バッチサイズ")
    parser.add_argument("--dataset_size", type=int, default=1000, help="データセットサイズ")
    # 必要に応じて他のパラメータも追加

    args = parser.parse_args()

    print(f"--- target_script.py 実行開始 ---")
    print(f"パラメータ:")
    print(f"  Learning Rate: {args.learning_rate}")
    print(f"  Optimizer: {args.optimizer}")
    print(f"  Epochs: {args.epochs}")
    print(f"  Batch Size: {args.batch_size}")
    print(f"  Dataset Size: {args.dataset_size}")

    # ここで実際の処理（例: モデルの訓練、シミュレーションなど）を行う
    # このサンプルでは、ダミーの計算とランダムな結果を出力します
    print("\n処理中...")
    time.sleep(random.uniform(0.5, 2.0)) # ダミーの処理時間

    # ダミーの精度と損失を計算
    # learning_rate が高いほど精度が上がりやすいが、高すぎると不安定になる、といった傾向を模擬
    # optimizer によってベースの精度が変わる、などを模擬
    base_accuracy = 0.6
    if args.optimizer == "adam":
        base_accuracy = 0.7
    elif args.optimizer == "sgd":
        base_accuracy = 0.65

    # learning_rate の影響 (単純な例)
    accuracy_offset = (args.learning_rate * 10) if args.learning_rate < 0.05 else - (args.learning_rate * 5)
    accuracy = base_accuracy + accuracy_offset + random.uniform(-0.05, 0.05)
    accuracy = min(max(accuracy, 0.1), 0.99) # 0.1 から 0.99 の範囲に収める

    loss = (1.0 - accuracy) + random.uniform(-0.1, 0.1)
    loss = max(loss, 0.01)

    print(f"\n結果:")
    print(f"Accuracy: {accuracy:.4f}") # この形式で出力すると main_script.py で抽出しやすい
    print(f"Loss: {loss:.4f}")         # 同上
    print(f"--- target_script.py 実行終了 ---")

if __name__ == "__main__":
    main()
