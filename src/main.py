from utils.ui import *
from utils.file_processing import *
from utils.constants import CONST_EMPTY_STRING, CONST_STATEMENT_KEY, CONST_SCHEMA_KEY, CONST_CORRECT_QUERY_KEY
from utils.patterns_processing import process_general_pattern, process_short_rel_pattern

def process_query(query, schema):
    """Process the cypher query with the given schema"""
    # Search for patterns, and check if the direction is correct by analyzing the schema
    query = process_general_pattern(query, schema)
    query = process_short_rel_pattern(query, schema)
    
    return query
    
def process_all_queries():
    # Parse the examples file with cypher queries to process them
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