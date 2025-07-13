#!/usr/bin/env python3
import sys
from pathlib import Path

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.nl2sql_agent import NL2SQLAgent
import pandas as pd

def print_results(result: dict):
    """Pretty print query results"""
    print("\n" + "="*80)
    print(f"自然言語クエリ: {result['natural_language']}")
    print(f"生成されたSQL: {result['sql_query']}")
    print(f"実行結果: {'成功' if result['success'] else '失敗'}")
    
    if result['success']:
        print(f"取得件数: {result['row_count']}件")
        if result['dataframe'] is not None and not result['dataframe'].empty:
            print("\n結果:")
            print(result['dataframe'].to_string(index=False))
    else:
        print(f"エラー: {result['error']}")
    print("="*80)

def main():
    # Initialize agent
    print("NL2SQL エージェントを初期化中...")
    agent = NL2SQLAgent()
    
    # Initialize database
    print("データベースを初期化中...")
    agent.initialize_database()
    
    # Sample queries
    sample_queries = [
        "価格が5000円以上の商品を教えて",
        "在庫が10個以下の商品は？",
        "最近1週間の注文を表示して",
        "顧客ごとの購入金額合計を見せて",
        "電子機器カテゴリの商品で在庫がある商品を表示",
        "文房具の商品一覧",
        "田中さんの注文履歴",
        "佐藤さんが買った商品を教えて",
        "一番高い商品は何？",
        "在庫切れの商品があるか確認",
        "今月の売上合計金額"
    ]
    
    print("\n\n*** サンプルクエリの実行 ***")
    
    for query in sample_queries:
        result = agent.execute_nl_query(query)
        print_results(result)
        
    # Interactive mode
    print("\n\n*** インタラクティブモード ***")
    print("自然言語でデータベースに質問してください。終了するには 'exit' と入力してください。")
    
    while True:
        user_query = input("\nクエリ> ").strip()
        
        if user_query.lower() in ['exit', 'quit', '終了']:
            print("終了します。")
            break
            
        if not user_query:
            continue
            
        result = agent.execute_nl_query(user_query)
        print_results(result)

if __name__ == "__main__":
    main()