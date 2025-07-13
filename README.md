# NL2SQL Sample Project

- 自然言語をSQLクエリに変換するシンプルなサンプルプロジェクトです。
- サンプルデータ（商品、顧客、注文）を含みます。

## 機能

- Google Vertex AI (Gemini 2.5 Flash)で自然言語をSQLクエリに変換
- PythonでSQLiteデータベースに対してSQLを実行し、データを取得

## 前提条件

### Google Cloud / Vertex AI環境
このプロジェクトを実行する前に、以下の環境を事前に準備してください：

1. **Google Cloudプロジェクトの作成**
   - [Google Cloud Console](https://console.cloud.google.com/)でプロジェクトを作成
   - Vertex AI APIを有効化
   - 課金設定を有効化（Gemini 2.5 Flash利用のため）

2. **認証の設定**
   - Google Cloud SDKをインストール
   - `gcloud auth application-default login`で認証

3. **Vertex AI Gemini APIへのアクセス確認**
   - プロジェクトでVertex AI Gemini APIが利用可能であることを確認

### 開発環境
- Python 3.12以上
- [uv](https://docs.astral.sh/uv/)（Pythonパッケージマネージャー）

## セットアップ

1. **リポジトリをクローン**:
```bash
git clone https://github.com/YOUR_USERNAME/nl2sql-sample.git
cd nl2sql-sample
```

2. **仮想環境の作成と依存関係のインストール**:
```bash
# uvで仮想環境を作成
uv venv

# 仮想環境をアクティベート
source .venv/bin/activate  # macOS/Linux
# または
.venv\Scripts\activate     # Windows

# 依存関係をインストール
uv pip install -r requirements.txt
```

3. **環境変数の設定**:
`.env`ファイルを作成:
```bash
cp .env.example .env
```

`.env`ファイルを編集してプロジェクトIDを設定:
```
GOOGLE_CLOUD_PROJECT='your-actual-project-id'
```

## 使用方法

### サンプルクエリの実行

```bash
# プロジェクトルートディレクトリから実行
python3 examples/sample_queries.py

# またはモジュールとして実行
python3 -m examples.sample_queries
```

### Pythonコードでの使用

```python
from src.nl2sql_agent import NL2SQLAgent

# エージェントの初期化
agent = NL2SQLAgent()
agent.initialize_database()

# 自然言語クエリの実行
result = agent.execute_nl_query("価格が1000円以上の商品を教えて")

# 結果の表示
print(f"SQL: {result['sql_query']}")
print(f"結果: {result['dataframe']}")
```

## データベーススキーマ

### products（商品）
- id: 商品ID
- name: 商品名
- category: カテゴリ
- price: 価格
- stock: 在庫数

### customers（顧客）
- id: 顧客ID
- name: 名前
- email: メールアドレス
- created_at: 登録日時

### orders（注文）
- id: 注文ID
- customer_id: 顧客ID
- product_id: 商品ID
- quantity: 数量
- order_date: 注文日時
- total_price: 合計金額

## サンプルクエリ

- 「価格が5000円以上の商品を教えて」
- 「在庫が10個以下の商品は？」
- 「最近1週間の注文を表示」
- 「顧客ごとの購入金額合計」
- 「電子機器カテゴリの商品一覧」