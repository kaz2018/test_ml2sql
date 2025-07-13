import os
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv
import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig
from src.db_manager import DatabaseManager
from src.prompt_templates import create_prompt

load_dotenv()

class NL2SQLAgent:
    def __init__(self, project_id: Optional[str] = None, location: str = "us-central1"):
        """
        Initialize NL2SQL Agent with Google Vertex AI
        
        Args:
            project_id: Google Cloud Project ID
            location: Vertex AI location
        """
        self.project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT")
        self.location = location
        self.model = None
        self.db_manager = DatabaseManager()
        
        # Initialize Vertex AI
        if self.project_id:
            vertexai.init(project=self.project_id, location=self.location)
            self.model = GenerativeModel("gemini-2.5-flash")
        else:
            print("Warning: Google Cloud Project ID not set. Using mock mode.")
            
    def initialize_database(self):
        """Initialize database with schema and sample data"""
        with self.db_manager:
            self.db_manager.initialize_database()
            
    def convert_nl_to_sql(self, natural_language_query: str) -> str:
        """
        Convert natural language query to SQL
        
        Args:
            natural_language_query: User's query in natural language
            
        Returns:
            SQL query string
        """
        with self.db_manager:
            # Get table schema information
            table_info = self.db_manager.get_table_info()
            
            # Create prompt
            prompt = create_prompt(natural_language_query, table_info)
            
            # Generate SQL using Vertex AI
            if self.model:
                try:
                    response = self.model.generate_content(
                        prompt,
                        generation_config=GenerationConfig(
                            temperature=0.1,
                            max_output_tokens=512,
                        )
                    )
                    sql_query = response.text.strip()
                    
                    # Clean up the SQL query
                    if sql_query.startswith("```sql"):
                        sql_query = sql_query[6:]
                    if sql_query.endswith("```"):
                        sql_query = sql_query[:-3]
                    sql_query = sql_query.strip()
                    
                    # Ensure query ends with semicolon
                    if not sql_query.endswith(";"):
                        sql_query += ";"
                        
                    return sql_query
                    
                except Exception as e:
                    print(f"Error generating SQL: {e}")
                    return self._mock_generate_sql(natural_language_query)
            else:
                # Mock mode for testing without Vertex AI
                return self._mock_generate_sql(natural_language_query)
                
    def _mock_generate_sql(self, query: str) -> str:
        """Mock SQL generation for testing"""
        query_lower = query.lower()
        
        if "価格" in query and "以上" in query:
            return "SELECT * FROM products WHERE price >= 1000;"
        elif "在庫" in query and "以下" in query:
            return "SELECT * FROM products WHERE stock <= 10;"
        elif "最近" in query and "注文" in query:
            return "SELECT * FROM orders WHERE order_date >= datetime('now', '-7 days');"
        elif "顧客" in query and "合計" in query:
            return """SELECT c.name, SUM(o.total_price) as total_spent
FROM customers c
JOIN orders o ON c.id = o.customer_id
GROUP BY c.id, c.name
ORDER BY total_spent DESC;"""
        else:
            return "SELECT * FROM products;"
            
    def execute_nl_query(self, natural_language_query: str) -> Dict[str, Any]:
        """
        Convert natural language to SQL and execute the query
        
        Args:
            natural_language_query: User's query in natural language
            
        Returns:
            Dictionary with SQL query and results
        """
        # Convert to SQL
        sql_query = self.convert_nl_to_sql(natural_language_query)
        
        # Execute query
        with self.db_manager:
            try:
                results = self.db_manager.execute_query(sql_query)
                df = self.db_manager.execute_query_df(sql_query)
                
                return {
                    "success": True,
                    "natural_language": natural_language_query,
                    "sql_query": sql_query,
                    "results": results,
                    "dataframe": df,
                    "row_count": len(results)
                }
            except Exception as e:
                return {
                    "success": False,
                    "natural_language": natural_language_query,
                    "sql_query": sql_query,
                    "error": str(e),
                    "results": [],
                    "dataframe": None,
                    "row_count": 0
                }
                
    def validate_sql(self, sql_query: str) -> bool:
        """Validate SQL query by executing with EXPLAIN"""
        with self.db_manager:
            try:
                self.db_manager.execute_query(f"EXPLAIN QUERY PLAN {sql_query}")
                return True
            except:
                return False