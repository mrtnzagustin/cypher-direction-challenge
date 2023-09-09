
import csv
from .constants import CONST_SOURCE_CLASS_KEY, CONST_TARGET_CLASS_KEY, CONST_RELATIONSHIP_KEY, CONST_SCHEMA_KEY, CYPHER_QUERIES_CSV_FILE_PATH

def process_schema(input_str):
    """Process the schema string into a list of dictionaries with the following structure: sourceClass, relationship, targetClass"""
    
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
    """Parse CSV file containing cypher queries to be processed"""
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