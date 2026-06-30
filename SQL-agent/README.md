# Autonomous SQL Agent with Self-Correction & Query Optimization

This sub-repository contains an advanced, state-driven SQL Agent built using **LangGraph** and **LangChain**. It connects to a PostgreSQL database (hosted via Supabase), translates natural language user requests into syntactically correct SQL queries, validates them for errors, and yields structured payloads ready for frontend mobile applications.

## 📊 Agent Architecture

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

## 📂 Project Structure

```text
SQL-agent/
├── sql_agent_graph.png    # Dynamic architecture layout visualization
├── main.py                # Core graph definitions, node logic, and execution loop
├── example.env            # Environment configuration template
├── requirements.txt       # Module dependencies (LangGraph, OpenRouter, Psycopg2)
└── README.md              # Project documentation and architectural overview
