
import csv
import re

CYPHER_QUERIES_CSV_FILE_PATH = "examples.csv"

CONST_SOURCE_CLASS_KEY = "sourceClass"
CONST_TARGET_CLASS_KEY = "targetClass"
CONST_RELATIONSHIP_KEY = "relationship"
CONST_SCHEMA_KEY = "schema"
CONST_STATEMENT_KEY = "statement"
CONST_CORRECT_QUERY_KEY = "correct_query"

CONST_SIMPLE_ARROW_LEFT_TO_RIGHT = "]->"
CONST_SIMPLE_ARROW_RIGHT_TO_LEFT = "<-["
CONST_LARGE_ARROW_LEFT_TO_RIGHT = "-->"
CONST_LARGE_ARROW_RIGHT_TO_LEFT = "<--"
CONST_NO_ARROW_LEFT_SIDE = "-["
CONST_NO_ARROW_RIGHT_SIDE = "]-"

# To match properties, wrapped by double quotes, in example:
# { name: "John", age: "20" }
CONST_PATTERN_ANY_SPACE = '\s*'
CONST_PATTERN_PROPERTIES = CONST_PATTERN_ANY_SPACE + '(?:\{\s*[a-zA-Z]+:\s*["\'][^"]*["\']\s*(?:\s*,\s*[a-zA-Z]+:\s*["\'][^"]*["\'])*\s*\})?' + CONST_PATTERN_ANY_SPACE

CONST_COLOR_BLUE = "\033[34m"
CONST_COLOR_RED = "\033[31m"
CONST_COLOR_GREEN = "\033[32m"
CONST_COLOR_YELLOW = "\033[33m"
CONST_COLOR_NORMAL = "\033[0m"

def printb(text):
    """Print text in blue"""
    print(CONST_COLOR_BLUE + text)

def printg(text):
    """Print text in green"""
    print(CONST_COLOR_GREEN + text)
    
def printr(text):
    """Print text in red"""
    print(CONST_COLOR_RED + text)

def printn(text):
    """Print text in normal color"""
    print(CONST_COLOR_NORMAL + text)
    
def printy(text):
    """Print text in yellow"""
    print(CONST_COLOR_YELLOW + text)
    
def search_for_class(variable, query):
    """Search for the class of the given variable in the query"""
    # Example (a:Person)
    pattern_str = f'{create_pattern_node_with_variable(variable,"className")}'
    pattern = re.compile(pattern_str)
    
    matches = pattern.finditer(query)
    
    for match in matches:
        # Get the match string
        full_match_string = match.group()
        
        # Get the groups
        node_class = match.group('className') and match.group('className').replace(':','').replace('`','')
        
        return node_class

    return None

def pattern_exists_in_schema(source_class_name, target_class_name, rel_name, schema, source_class_is_defined, target_class_is_defined, rel_name_is_defined):
    """Check if the given pattern exists in the schema"""
    # source, relationship and target
    if source_class_is_defined and target_class_is_defined and rel_name_is_defined:
        return any(
            item[CONST_SOURCE_CLASS_KEY] == source_class_name and
            item[CONST_TARGET_CLASS_KEY] == target_class_name and
            item[CONST_RELATIONSHIP_KEY] == rel_name
            for item in schema)
    # source and target only
    if source_class_is_defined and target_class_is_defined and not rel_name_is_defined:
        return any(
            item[CONST_SOURCE_CLASS_KEY] == source_class_name and
            item[CONST_TARGET_CLASS_KEY] == target_class_name
            for item in schema)
    # source and relationship only
    if source_class_is_defined and not target_class_is_defined and rel_name_is_defined:
        return any(
            item[CONST_SOURCE_CLASS_KEY] == source_class_name and
            item[CONST_RELATIONSHIP_KEY] == rel_name
            for item in schema)
    # source only
    if source_class_is_defined and not target_class_is_defined and not rel_name_is_defined:
        return any(
            item[CONST_SOURCE_CLASS_KEY] == source_class_name
            for item in schema)
    # target and relationship only
    if not source_class_is_defined and target_class_is_defined and rel_name_is_defined:
        return any(
            item[CONST_TARGET_CLASS_KEY] == target_class_name and
            item[CONST_RELATIONSHIP_KEY] == rel_name
            for item in schema)
    # target only
    if not source_class_is_defined and target_class_is_defined and not rel_name_is_defined:
        return any(
            item[CONST_TARGET_CLASS_KEY] == target_class_name
            for item in schema)

def class_exists_in_schema(class_name, schema):
    """Check if the given class exists in the schema"""
    return class_name in list_classes(schema)

def relationship_exists_in_schema(relationship_name, schema):
    """Check if the given relationship exists in the schema"""
    return relationship_name in list_unique_relationships(schema)

# (variable:ClassName) or (:ClassName) or (), including possible properties
def create_pattern_node(variable_group_name, class_group_name):
    return f'(?:\({create_pattern_variable(variable_group_name)}{create_pattern_class(class_group_name)}'+CONST_PATTERN_PROPERTIES+'\))'

# (variable:ClassName) or (:ClassName) or (), including possible properties, variable and class are mandatory
def create_pattern_node_with_variable(variable_name, class_group_name):
    return f'(?:\({variable_name}{create_pattern_class_must(class_group_name)}'+CONST_PATTERN_PROPERTIES+'\))'

# a single variable name using words only, no spaces, it could be empty
def create_pattern_variable(variable_group_name):
    return f'(?P<{variable_group_name}>[a-zA-Z]*)'

# :ClassName or :`ClassName`
def create_pattern_class(class_group_name):
    return f'(?P<{class_group_name}>:`?[a-zA-Z]*`?)?'

# :ClassName or :`ClassName`
def create_pattern_class_must(class_group_name):
    return f'(?P<{class_group_name}>:`?[a-zA-Z]*`?)+'

# :REL_TYPE or :`REL_TYPE` 
def create_pattern_relationship_name(relationship_type_group_name):
    return f'(?P<{relationship_type_group_name}>:`?[a-zA-Z_]*`?)?'

# :ClassName
def create_pattern_multiple_class(class_group_name):
    # TODO: Complete
    return f'(?P<{class_group_name}>:[a-zA-Z]*)*'

# -[variable:REL_TYPE]- or -[variable:`REL_TYPE`]- or -[:`REL_TYPE`]- including possible properties and arrow directions
def create_pattern_relationship(relationship_variable_group_name, relationship_type_group_name, left_arrow_name, right_arrow_name):
    return f'(?P<{left_arrow_name}><)?-\[{create_pattern_variable(relationship_variable_group_name)}{create_pattern_relationship_name(relationship_type_group_name)}{CONST_PATTERN_PROPERTIES}\]-(?P<{right_arrow_name}>>)?'

# <-- or -->
def create_pattern_relationship_short(left_arrow_name, right_arrow_name):
    return f'(?P<{left_arrow_name}><)?--(?P<{right_arrow_name}>>)?'

def list_classes(schema):
    """List all the classes that are present in the schema"""
    classes_set = {item[CONST_SOURCE_CLASS_KEY] for item in schema}
    classes_set.update({item[CONST_TARGET_CLASS_KEY] for item in schema})
    classes_list = list(classes_set)
    return classes_list

def list_source_classes(schema):
    """List all the classes that are source classes at least once in the schema"""
    source_classes_set = {item[CONST_SOURCE_CLASS_KEY] for item in schema}
    source_classes_list = list(source_classes_set)
    return source_classes_list

def list_target_classes(schema):
    """List all the classes that are target classes at least once in the schema"""
    target_classes_set = {item[CONST_TARGET_CLASS_KEY] for item in schema}
    target_classes_list = list(target_classes_set)
    return target_classes_list

def list_unique_relationships(schema):
    """List the unique relationships in the schema"""
    predicates_set = {item[CONST_RELATIONSHIP_KEY] for item in schema}
    predicates_list = list(predicates_set)
    return predicates_list

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