
import csv
from .constants import CONST_SOURCE_CLASS_KEY, CONST_TARGET_CLASS_KEY, CONST_RELATIONSHIP_KEY, CONST_SCHEMA_KEY, CYPHER_QUERIES_CSV_FILE_PATH

def process_schema(input_str):
    """
    Converts a schema string representation into a list of dictionaries.

    This function processes an input schema string and transforms it into a structured 
    list of dictionaries, where each dictionary represents a single schema definition 
    with keys: `sourceClass`, `relationship`, and `targetClass`.

    Parameters:
    - input_str (str): The string representation of the schema, 
      e.g. "(ClassA,REL,ClassB),(ClassC,REL,ClassD)".

    Returns:
    - list[dict]: A list of dictionaries where each dictionary has the structure:
      {
        CONST_SOURCE_CLASS_KEY: "ClassA",
        CONST_RELATIONSHIP_KEY: "REL",
        CONST_TARGET_CLASS_KEY: "ClassB"
      }

    Example:
    ```python
    input_schema = "(ClassA,REL,ClassB),(ClassC,REL,ClassD)"
    processed = process_schema(input_schema)
    ```

    """
    
    # Split the string into separate schema definitions
    schema_definitions = [s.strip() for s in input_str.split('),') if s]

    # Extract sourceClass, relationship, and targetClass for each schema
    result = []
    for schema_definition in schema_definitions:
        # Remove opening and closing parentheses
        schema_definition = schema_definition.strip('()')

        # Split the schema into its components
        components = [component.strip() for component in schema_definition.split(',')]

        # Add the components to a dictionary
        schema_dict = {
            CONST_SOURCE_CLASS_KEY: components[0],
            CONST_RELATIONSHIP_KEY: components[1],
            CONST_TARGET_CLASS_KEY: components[2]
        }
        result.append(schema_dict)

    return result

def parse_csv_with_cypher_queries():
    """
    Parses a CSV file containing Cypher queries and returns them as a list of dictionaries.

    This function reads a predefined CSV file containing Cypher queries. Each row 
    of the CSV file corresponds to a Cypher query and its associated schema. The function 
    processes each row's schema into a structured dictionary before appending it to the results.

    Returns:
    - list[dict]: A list of dictionaries where each dictionary represents a row from the 
      CSV and has the processed schema along with the Cypher query.

    Example:
    ```python
    queries = parse_csv_with_cypher_queries()
    ```

    """
    cypher_queries = []
    
    # Open the CSV file and read it line by line
    with open(CYPHER_QUERIES_CSV_FILE_PATH, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        # For each row in the csv
        for row in csv_reader:
            # Pre-process the schema
            row[CONST_SCHEMA_KEY] = process_schema(row[CONST_SCHEMA_KEY])
            cypher_queries.append(row)
    
    return cypher_queries