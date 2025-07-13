# NL2SQL Sample Project

自然言語をSQLクエリに変換するシンプルなサンプルプロジェクトです。

## 機能

- 自然言語クエリをSQLに変換
- Google Vertex AI (Gemini)を使用した高精度な変換
- SQLiteデータベースでのクエリ実行
- サンプルデータ（商品、顧客、注文）を含む

## セットアップ

1. 依存関係のインストール:
```bash
pip install -r requirements.txt
```

2. Google Cloud認証の設定:
```bash
# Google Cloud SDKをインストール
gcloud auth application-default login

# プロジェクトIDを環境変数に設定
export GOOGLE_CLOUD_PROJECT="your-project-id"
```

または、`.env`ファイルを作成:
```
GOOGLE_CLOUD_PROJECT=your-project-id
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