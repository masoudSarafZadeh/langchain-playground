# Autonomous SQL Agent with Self-Correction & Query Optimization

This sub-repository contains an advanced, state-driven SQL Agent built using **LangGraph** and **LangChain**. It connects to a PostgreSQL database (hosted via Supabase), translates natural language user requests into syntactically correct SQL queries, validates them for errors, and yields structured payloads ready for frontend mobile applications.

## Agent Architecture

Unlike standard text-to-SQL workflows that fail silently when a query throws an error or returns empty results, this agent implements a reflective loop with automatic fallback mechanics and grading routines.

Here is the exact runtime execution graph generated dynamically by LangGraph:

![SQL Agent Architecture Graph](sql_agent_graph.png)

### Dynamic Workflow Breakdown

1. **Database Discovery (`list_tables` ➔ `call_get_schema` ➔ `get_schema`)**: The agent dynamically bootstraps itself by inspecting the database dialect, retrieving available tables, and loading schema constraints so it knows exactly what columns exist.
2. **Query Generation (`generate_query`)**: The LLM constructs a precise SQL statement targeting the `goods` table using domain-specific business logic guidelines.
3. **Syntax Guardrails (`check_query`)**: A specialized SQL expert node intercepts the query before execution, checking for common pitfalls like exclusive ranges, null handling bugs, or datatype mismatches.
4. **Resilient Query Execution (`run_query`)**: Runs the SQL statement.
5. **Relevance Assessment & Query Rewriting**: 
   * The database payload is evaluated by a structured binary grader tool.
   * If the returned records match the semantic intent of the question, it moves to **`generate_answer`**.
   * If the data is deemed irrelevant or empty, it routes to **`rewrite_question`**, where conversational fillers are stripped out, and a cleaner search term is pushed back into `generate_query` to start a corrective loop.
6. **Polished Response (`generate_answer`)**: Formulates an engaging, user-facing sales assistant response written entirely in Persian.

## Project Structure

```text
SQL-agent/
├── sql_agent_graph.png    # Dynamic architecture layout visualization
├── main.py                # Core graph definitions, node logic, and execution loop
├── example.env            # Environment configuration template
├── requirements.txt       # Module dependencies (LangGraph, OpenRouter, Psycopg2)
└── README.md              # Project documentation and architectural overview
```
## 🚀 Setup & Installation

### 1. Navigate to the Directory
```bash
cd SQL-agent
```
### 2. Install Dependencies
Ensure you have a virtual environment active, then run:

```bash
pip install -r requirements.txt
```
### 3. Environment Configuration
Copy the sample environment file to create a live .env file:

```bash
cp example.env .env
Open the .env file and fill in your respective credentials:
```
```Plaintext
OPENROUTER_API_KEY=your_openrouter_api_key_here
DATABASE_URL=postgresql://postgres.your_project_id:your_password@aws-host.pooler.supabase.com:5432/postgres
```
### 4. Running the Agent
Run the main script to watch the streaming node steps and inspect the final dual-layered device output payload:

```bash
python main.py
```
## 📱 Mobile-Ready Output Layer

The script aggregates the conversational text response along with uncleaned database elements (such as item metadata and product image URLs) into a standardized application JSON structure:

```json
{
  "llm_response": "سرآغاز پاسخ صمیمانه به زبان فارسی...",
  "products": [
    {
      "id": 1,
      "product_name": "رب گوجه فرنگی",
      "price_after_off": 45000,
      "image": "[https://supabase-storage-url.com/tomato_paste.png](https://supabase-storage-url.com/tomato_paste.png)"
    }
  ]
}
```
