# ADK Crash Course

これは Google の Agent Development Kit (ADK) を使用した簡単な挨拶エージェントのサンプルプロジェクトです。

## 概要

このプロジェクトでは、ADK を使用して基本的なエージェントを実装しています。エージェントはユーザーに名前を尋ね、その名前を使って挨拶を返します。

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
uv pip install -e .
```

注: [uv](https://github.com/astral-sh/uv) は高速な Python パッケージインストーラーです。事前に以下のコマンドで uv をインストールしてください：

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## プロジェクト構成

```
.
├── pyproject.toml    # プロジェクト設定ファイル
├── README.md         # このファイル
└── greeting_agent/   # エージェントの実装
    ├── __init__.py
    └── agent.py      # エージェントの主要なコード
```

## ライセンス

このプロジェクトは MIT ライセンスの下で公開されています。詳細については `LICENSE` ファイルを参照してください。
