import argparse
import random
import time

def main():
    parser = argparse.ArgumentParser(description="機械学習モデルの学習を模したデモスクリプト")
    parser.add_argument("--learning_rate", type=float, default=0.01, help="学習率")
    parser.add_argument("--batch_size", type=int, default=32, help="バッチサイズ")
    parser.add_argument("--dropout", type=float, default=0.5, help="ドロップアウト率")
    parser.add_argument("--optimizer", type=str, default="adam", help="オプティマイザ")

    args = parser.parse_args()

    print(f"--- demo_target.py 実行開始 ---")
    print(f"パラメータ: lr={args.learning_rate}, batch_size={args.batch_size}, dropout={args.dropout}, optimizer={args.optimizer}")

    # 意図的に最適なパラメータを設定
    optimal_lr = 0.005
    optimal_batch_size = 64
    optimal_dropout = 0.3

    print("\nモデルの学習をシミュレーションしています...")
    time.sleep(1.0) # ダミーの処理時間

    # パラメータと最適値の距離を計算（簡易的）
    lr_diff = abs(args.learning_rate - optimal_lr) / optimal_lr
    batch_size_diff = abs(args.batch_size - optimal_batch_size) / optimal_batch_size
    dropout_diff = abs(args.dropout - optimal_dropout) / optimal_dropout

    # 総合的なペナルティ
    penalty = lr_diff * 0.4 + batch_size_diff * 0.3 + dropout_diff * 0.3

    # オプティマイザによる微小な違い
    optimizer_bonus = 0.05 if args.optimizer == "adam" else 0.0

    # 精度と損失の計算
    base_accuracy = 0.95
    accuracy = base_accuracy - (penalty * 0.5) + optimizer_bonus + random.uniform(-0.02, 0.02)
    accuracy = min(max(accuracy, 0.1), 0.99)

    base_loss = 0.05
    loss = base_loss + (penalty * 1.5) - optimizer_bonus + random.uniform(-0.01, 0.01)
    loss = max(loss, 0.01)

    print(f"\n結果:")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Loss: {loss:.4f}")
    print(f"--- demo_target.py 実行終了 ---")

if __name__ == "__main__":
    main()
