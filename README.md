# ADK Crash Course

これは Google の Agent Development Kit (ADK) を使用した挨拶エージェントのサンプルプロジェクトです。ADK の基本的な機能から高度な使用方法まで、段階的に学ぶことができます。

以下の動画を参考にしました。

- [Agent Development Kit (ADK) Masterclass: Build AI Agents & Automate Workflows (Beginner to Pro)](https://www.youtube.com/watch?v=P4VFL9nIaIA)

## 概要

このプロジェクトは、ADK の様々な機能を学ぶためのサンプルコードを提供しています。各ブランチで異なる機能を実装しており、段階的に学習を進めることができます：

- `main`: 基本的な挨拶エージェントの実装
- `2-tool-agent`: ツールを使用するエージェントの実装
- `3-litellm-agent`: LiteLLM を使用した様々な LLM モデルの利用
- `4-structured-outputs`: 構造化された出力の生成
- `5-sessions-and-state`: セッション管理と状態の保持
- `6-persistent-storage`: 永続的なストレージの利用
- `7-multi-agent`: 複数エージェントの連携
- `8-stateful-multi-agent`: 状態を持つ複数エージェントの実装
- `9-callbacks`: コールバックを使用したイベント処理
- `10-sequential-agent`: 順次処理を行うエージェントの実装
- `11-parallel-agent`: 並列処理を行うエージェントの実装
- `12-loop-agent`: 繰り返し処理を行うエージェントの実装

## 必要要件

- Python 3.12 以上
- google-adk 1.9.0 以上
- python-dotenv 1.1.1 以上

## インストール

1. リポジトリをクローンします：

```bash
git clone https://github.com/aidiary/adk-crash-course.git
cd adk-crash-course
```

2. 依存パッケージをインストールします：

```bash
uv sync
uv venv
source .venv/bin/activate
```

注: [uv](https://github.com/astral-sh/uv) は高速な Python パッケージインストーラーです。事前に以下のコマンドで uv をインストールしてください：

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
