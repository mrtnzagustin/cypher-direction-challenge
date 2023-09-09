from utils.ui import *
from utils.file_processing import *
from utils.constants import CONST_EMPTY_STRING, CONST_STATEMENT_KEY, CONST_SCHEMA_KEY, CONST_CORRECT_QUERY_KEY
from utils.patterns_processing import process_general_pattern, process_short_rel_pattern

def process_query(query, schema):
    """
    Processes and adjusts the provided Cypher query based on the given schema.

    This function takes a Cypher query and a schema as input. It searches for 
    specific patterns within the query and verifies the direction of relationships 
    based on the provided schema. If any discrepancies are found, the function 
    adjusts the query to align with the schema.

    Parameters:
    - query (str): The Cypher query to be processed.
    - schema (object): The schema against which the query is to be validated and corrected.

    Returns:
    - str: The processed and corrected Cypher query.

    Example:
    ```python
    query = "MATCH (a)-[r]->(b) RETURN a, b"
    processed_query = process_query(query, my_schema)
    ```

    Note:
    - The function calls two internal methods:
      1. process_general_pattern: For general pattern checking and correction.
      2. process_short_rel_pattern: For checking and correcting short relationship patterns.
    """
    # Search for patterns, check if the direction is correct by analyzing the schema and corrects it whenever is needed
    query = process_general_pattern(query, schema)
    query = process_short_rel_pattern(query, schema)
    
    return query
    
def process_all_queries():
    """
    Processes all Cypher queries from a predefined CSV file and validates their correctness.
    
    This function parses a CSV file containing example Cypher queries. For each query, 
    it attempts to process and correct it. It then validates the processed query against 
    a provided correct version. The results of the processing are printed to the console, 
    and counters for various outcomes (correct, incorrect, etc.) are maintained.

    Note: 
    - The function assumes the CSV file has columns for the statement, schema, and correct query.
    - Helper functions and constants like `parse_csv_with_cypher_queries`, `printb`, `printg`, 
      `printy`, and `printr` are utilized for various operations and console output.

    Returns:
    - tuple: A tuple containing counts of:
      1. Correctly processed queries.
      2. Incorrectly processed queries.
      3. Queries processed with warnings.
      4. Total number of queries processed.

    Example:
    ```python
    correct, incorrect, with_warnings, total = process_all_queries()
    print(f"Correct: {correct}, Incorrect: {incorrect}, With Warnings: {with_warnings}, Total: {total}")
    ```

    """
    cypher_queries = parse_csv_with_cypher_queries()
    correct_count = 0
    incorrect_count = 0
    correct_with_warnings_count = 0
    
    for query in cypher_queries:
        printb(CONST_EMPTY_STRING)
        printb(f'-------------------------')
        printb(f'Processing query {query[CONST_STATEMENT_KEY]}')
        result_query = process_query(query[CONST_STATEMENT_KEY], query[CONST_SCHEMA_KEY])
        
        if result_query == query[CONST_CORRECT_QUERY_KEY]:
            printg(f'Query process worked correctly')
            printg(f'Final query: {result_query}')
            correct_count+=1
        elif result_query == CONST_EMPTY_STRING:
            printy(f'Query process worked with some warnings, check previous messages')
            correct_with_warnings_count+=1
        elif result_query != query[CONST_CORRECT_QUERY_KEY]:
            printr(f'Fixed query and correct query are different, something failed')
            printr(f'Final query: {result_query}')
            printr(f'Correct query: {query[CONST_CORRECT_QUERY_KEY]}')
            incorrect_count+=1
    return correct_count, incorrect_count, correct_with_warnings_count, len(cypher_queries)
            
def main():
    printn('Starting process')
    printn(CONST_EMPTY_STRING)
    
    correct_count, incorrect_count, correct_with_warnings_count, total_count = process_all_queries()
    
    printn(CONST_EMPTY_STRING)    
    printn(f'Process finished')
    printg(f'Correct queries: {correct_count}/{total_count}')
    printr(f'Incorrect queries: {incorrect_count}/{total_count}')
    printy(f'Correct with warnings: {correct_with_warnings_count}/{total_count}')
    printn(CONST_EMPTY_STRING)
    
if __name__ == "__main__":
    main()