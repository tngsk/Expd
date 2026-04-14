# EXPD デモ: 調整しながら最適化する

このデモでは、EXPD ツールを使用して、外部スクリプトのパラメータを探索し、MLflow で結果を確認しながら最適化していくプロセスを体験できます。

## 概要

`demo_target.py` は、機械学習モデルの学習を模したスクリプトです。内部にはある特定の「最適なパラメータ」が設定されており、与えられたパラメータがそれに近いほど高い `Accuracy` (精度) と低い `Loss` (損失) を出力します。

## 手順 1: 初期探索（広範囲のグリッドサーチ）

まず、事前に用意されている `demo_config.yaml` を使って、大まかなパラメータ探索を実行します。

この設定ファイルでは、以下のパラメータの組み合わせを試します：
- `learning_rate`: `[0.01, 0.005, 0.001]`
- `batch_size`: `[32, 64, 128]`
- `dropout`: `[0.3, 0.5, 0.7]`
- 固定: `optimizer` は `adam`

### 実行方法

`main.py` 内の `CONFIG_FILE` のパスが `demo_config.yaml` に向くように書き換えるか、今回はデモ用に以下のコマンドを実行して設定を上書きしてください。（※ `config.yaml` を一時的に `demo_config.yaml` の内容で上書きするか、プログラムで指定します）

今回は、便宜上 `config.yaml` を `demo_config.yaml` で置き換えて実行します。

```bash
cp demo_config.yaml config.yaml
uv run python expd/main.py
```

実行が完了すると、`experiment_results.csv` に結果が保存され、同時に MLflow にも記録されます。

## 手順 2: MLflow で結果を確認し、最適化の方針を立てる

MLflow UI を起動して、結果を視覚的に確認します。

```bash
uv run python scripts.py mlflow
```

ブラウザで `http://localhost:5000` を開き、以下の点を確認します。
1. **Accuracy の高い順にソート**: どのパラメータの組み合わせが良かったか確認します。
2. **Parallel Coordinates Plot (平行座標プロット)** を作成し、各パラメータが Accuracy にどのように影響しているかを観察します。
   - `learning_rate` は 0.005 が良さそう？
   - `batch_size` は 64 が良さそう？
   - `dropout` は 0.3 が良さそう？

## 手順 3: 範囲を絞って再探索（最適化）

MLflow での観察に基づいて、`config.yaml` を編集し、より細かい範囲でパラメータを探索します。
例えば、`learning_rate` を 0.005 付近で細かくし、`batch_size` は 64 に固定するなどです。

`config.yaml` を以下のように書き換えてみてください。

```yaml
experiment_name: "demo_optimization_process_fine"

target_script: "demo_target.py"

parameters:
  fixed_params:
    optimizer: "adam"
    batch_size: 64      # 最も良かった 64 に固定
    dropout: 0.3        # 最も良かった 0.3 に固定

  grid_params:
    # 0.005 の周辺を細かく探索
    learning_rate: [0.004, 0.005, 0.006]
```

再度、実験を実行します。

```bash
uv run python expd/main.py
```

MLflow で `demo_optimization_process_fine` の結果を確認し、より高い Accuracy が得られたか（調整によって最適化が進んだか）を確認します。
