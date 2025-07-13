SYSTEM_PROMPT = """あなたは自然言語をSQLクエリに変換する専門家です。
以下のデータベーススキーマに基づいて、ユーザーの質問を適切なSQLクエリに変換してください。

データベーススキーマ:
{schema}

重要な注意事項:
1. SQLiteの構文を使用してください
2. 日付の比較にはdatetime()関数を使用してください
3. 必要に応じてJOINを使用してください
4. 集計関数（COUNT, SUM, AVG等）を適切に使用してください
5. SQLクエリのみを返し、説明は含めないでください
6. 必ずセミコロン(;)でクエリを終了してください
7. 一覧表を要求された場合は、適切な項目でソートしてください：
   - 商品一覧: 名前(name)またはカテゴリ(category)でソート
   - 顧客一覧: 名前(name)でソート
   - 注文一覧: 日付(order_date)の降順でソート
   - 金額に関する一覧: 金額の降順でソート
   - その他の場合: 最も意味のある項目でソート
8. 人名での検索時の注意：
   - 「〇〇さん」という表現は通常、姓のみを指します
   - 日本人の名前検索では、姓での部分一致検索（LIKE '姓%'）を使用してください
   - 例: 「田中さん」→ name LIKE '田中%'（田中太郎、田中花子などにマッチ）
"""

FEW_SHOT_EXAMPLES = [
    {
        "input": "価格が1000円以上の商品を教えて",
        "output": "SELECT * FROM products WHERE price >= 1000;"
    },
    {
        "input": "在庫が10個以下の商品は？",
        "output": "SELECT * FROM products WHERE stock <= 10;"
    },
    {
        "input": "最近1週間の注文を表示",
        "output": "SELECT * FROM orders WHERE order_date >= datetime('now', '-7 days');"
    },
    {
        "input": "顧客ごとの購入金額合計",
        "output": """SELECT c.name, SUM(o.total_price) as total_spent
FROM customers c
JOIN orders o ON c.id = o.customer_id
GROUP BY c.id, c.name
ORDER BY total_spent DESC;"""
    },
    {
        "input": "電子機器カテゴリの商品で在庫がある商品",
        "output": "SELECT * FROM products WHERE category = '電子機器' AND stock > 0 ORDER BY name;"
    },
    {
        "input": "今月の売上合計",
        "output": "SELECT SUM(total_price) as monthly_sales FROM orders WHERE order_date >= datetime('now', 'start of month');"
    },
    {
        "input": "文房具の商品一覧",
        "output": "SELECT * FROM products WHERE category = '文房具' ORDER BY name;"
    },
    {
        "input": "商品の価格一覧を高い順に",
        "output": "SELECT name, price FROM products ORDER BY price DESC;"
    },
    {
        "input": "田中さんの注文履歴",
        "output": """SELECT o.*, p.name as product_name, c.name as customer_name
FROM orders o
JOIN customers c ON o.customer_id = c.id
JOIN products p ON o.product_id = p.id
WHERE c.name LIKE '田中%'
ORDER BY o.order_date DESC;"""
    },
    {
        "input": "山田さんが購入した商品",
        "output": """SELECT DISTINCT p.name, p.category, p.price
FROM products p
JOIN orders o ON p.id = o.product_id
JOIN customers c ON o.customer_id = c.id
WHERE c.name LIKE '山田%';"""
    }
]

def format_schema(table_info: dict) -> str:
    """Format table info for prompt"""
    schema_text = ""
    for table, columns in table_info.items():
        schema_text += f"\nTable: {table}\n"
        schema_text += "Columns:\n"
        for col_name, col_type in columns:
            schema_text += f"  - {col_name} ({col_type})\n"
    return schema_text

def create_prompt(query: str, table_info: dict) -> str:
    """Create prompt for NL2SQL conversion"""
    schema = format_schema(table_info)
    
    # Add few-shot examples
    examples_text = "\n例:\n"
    for example in FEW_SHOT_EXAMPLES[:3]:  # Use first 3 examples
        examples_text += f"質問: {example['input']}\n"
        examples_text += f"SQL: {example['output']}\n\n"
    
    prompt = SYSTEM_PROMPT.format(schema=schema)
    prompt += examples_text
    prompt += f"\n質問: {query}\nSQL: "
    
    return prompt