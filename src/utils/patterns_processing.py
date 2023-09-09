import re
from .constants import *
from .general import is_defined
from .ui import printb, printg, printr, printy

def get_first_node_and_relationship(string):
    """
    Extracts and returns the initial node and its relationship from a Cypher pattern.

    This function extracts the first node and its connecting relationship from a given Cypher 
    pattern string. It does not include the next node in the result.

    Parameters:
    - string (str): A Cypher pattern string. 
      E.g., "(nodeA)-[:REL]->(nodeB)" or "(nodeA)-->(nodeB)".

    Returns:
    - str: A substring containing the first node and its relationship.
      E.g., For the input "(nodeA)-[:REL]->(nodeB)", the output would be "(nodeA)-[:REL]->".

    Examples:
    ```python
    result = get_first_node_and_relationship("(nodeA)-[:REL]->(nodeB)")
    print(result)  # Outputs: "(nodeA)-[:REL]->"
    ```

    """
    # in example for (nodeA)-[:REL]->(nodeB), returns only (nodeA)-[:REL]->
    # for (nodeA)-->(nodeB), returns only (nodeA)-->
    first_node_and_relationship = '(' + string.split('(')[1]
    return first_node_and_relationship

def search_for_classes(variable, query):
    """
    Searches for the classes (labels) associated with a given variable within a Cypher query.

    This function looks for node patterns in the Cypher query that are associated 
    with the provided variable, and extracts the class or classes (labels) assigned 
    to that node.

    Parameters:
    - variable (str): The variable whose classes (labels) are to be identified.
    - query (str): The Cypher query string where the search is to be performed.

    Returns:
    - list[str] or None: A list of classes (labels) associated with the variable, 
      or None if no match is found.

    Examples:
    ```python
    classes = search_for_classes("a", "(a:Person:Employee)-[:WORKS_AT]->(b:Company)")
    print(classes)  # Outputs: ['Person', 'Employee']
    ```

    """
    # Example (a:Person)
    pattern_str = f'{create_pattern_node_with_variable(variable,"classesNames")}'
    pattern = re.compile(pattern_str)
    
    matches = pattern.finditer(query)
    
    for match in matches:
        # Get the match string
        full_match_string = match.group()
        
        # Get the groups
        node_classes = match.group('classesNames') and match.group('classesNames').replace(':','', 1).replace('`','').split(':')
        
        return node_classes

    return None

def pattern_exists_in_schema_multiple(source_classes_names, target_classes_names, rels_names, schema, source_classes_is_defined, target_classes_is_defined, rels_names_is_defined):
    """
    Determines if a given pattern with multiple possible combinations exists within the schema.

    This function checks for a match of the provided pattern components (source classes, target 
    classes, and relationships) against the provided schema. It does so by iterating through all 
    possible combinations of the given pattern components and checks if any of those combinations 
    match with the schema.

    Parameters:
    - source_classes_names (list[str]): List of possible source class names.
    - target_classes_names (list[str]): List of possible target class names.
    - rels_names (list[str]): List of possible relationship names.
    - schema (list[dict]): The schema against which the pattern is checked.
    - source_classes_is_defined (bool): Whether the source classes are defined.
    - target_classes_is_defined (bool): Whether the target classes are defined.
    - rels_names_is_defined (bool): Whether the relationships are defined.

    Returns:
    - bool: True if a matching pattern is found, otherwise False.

    """
    # source, relationship and target
    if source_classes_is_defined and target_classes_is_defined and rels_names_is_defined:
        for source_class_name in source_classes_names:
            for target_class_name in target_classes_names:
                for rel_name in rels_names:
                    if pattern_exists_in_schema(source_class_name, target_class_name, rel_name, schema, source_classes_is_defined, target_classes_is_defined, rels_names_is_defined):
                        return True
    # source and target only
    if source_classes_is_defined and target_classes_is_defined and not rels_names_is_defined:
        for source_class_name in source_classes_names:
            for target_class_name in target_classes_names:
                if pattern_exists_in_schema(source_class_name, target_class_name, None, schema, source_classes_is_defined, target_classes_is_defined, rels_names_is_defined):
                    return True
    # source and relationship only
    if source_classes_is_defined and not target_classes_is_defined and rels_names_is_defined:
        for source_class_name in source_classes_names:
            for rel_name in rels_names:
                if pattern_exists_in_schema(source_class_name, None, rel_name, schema, source_classes_is_defined, target_classes_is_defined, rels_names_is_defined):
                    return True
    # source only
    if source_classes_is_defined and not target_classes_is_defined and not rels_names_is_defined:
        for source_class_name in source_classes_names:
            if pattern_exists_in_schema(source_class_name, None, None, schema, source_classes_is_defined, target_classes_is_defined, rels_names_is_defined):
                return True
    # target and relationship only
    if not source_classes_is_defined and target_classes_is_defined and rels_names_is_defined:
        for target_class_name in target_classes_names:
            for rel_name in rels_names:
                if pattern_exists_in_schema(None, target_class_name, rel_name, schema, source_classes_is_defined, target_classes_is_defined, rels_names_is_defined):
                    return True
    # target only
    if not source_classes_is_defined and target_classes_is_defined and not rels_names_is_defined:
        for target_class_name in target_classes_names:
            if pattern_exists_in_schema(None, target_class_name, None, schema, source_classes_is_defined, target_classes_is_defined, rels_names_is_defined):
                return True
    
    return False
    
def pattern_exists_in_schema(source_class_name, target_class_name, rel_name, schema, source_class_is_defined, target_class_is_defined, rel_name_is_defined):
    """
    Determines if a given pattern exists within the schema.

    This function checks if the provided pattern components (source class, target class, and 
    relationship) match any entry in the provided schema.

    Parameters:
    - source_class_name (str or None): The name of the source class.
    - target_class_name (str or None): The name of the target class.
    - rel_name (str or None): The name of the relationship.
    - schema (list[dict]): The schema against which the pattern is checked.
    - source_class_is_defined (bool): Whether the source class is defined.
    - target_class_is_defined (bool): Whether the target class is defined.
    - rel_name_is_defined (bool): Whether the relationship is defined.

    Returns:
    - bool: True if a matching pattern is found, otherwise False.

    """
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

def classes_exists_in_schema(classes_name, schema):
    """
    Determines if any of the specified classes exist within the provided schema.

    Parameters:
    - classes_name (list[str]): List of class names to check.
    - schema (list[dict]): The schema against which the classes are checked.

    Returns:
    - bool: True if any class from the list is found in the schema, otherwise False.
    """
    return any (class_name in list_classes(schema) for class_name in classes_name)

def relationships_exists_in_schema(relationships_names, schema):
    """
    Determines if any of the specified relationships exist within the provided schema.

    Parameters:
    - relationships_names (list[str]): List of relationship names to check.
    - schema (list[dict]): The schema against which the relationships are checked.

    Returns:
    - bool: True if any relationship from the list is found in the schema, otherwise False.
    """
    return any (relationship_name in list_unique_relationships(schema) for relationship_name in relationships_names)

def create_pattern_node(variable_group_name, class_group_name):
    """
    Generates a regex pattern for a node, including optional properties.
    
    This pattern can represent nodes like: (variable:ClassName), (:ClassName), or ().

    Parameters:
    - variable_group_name (str): Name for the regex group capturing the variable name.
    - class_group_name (str): Name for the regex group capturing the class name(s).

    Returns:
    - str: Regex pattern for the node.
    """
    return f'(?:\({create_pattern_variable(variable_group_name)}{create_pattern_classes(class_group_name)}'+CONST_PATTERN_PROPERTIES+'\))'

def create_pattern_node_with_variable(variable_name, classes_group_name):
    """
    Generates a regex pattern for a node that mandates both the variable and class.
    
    The pattern represents nodes like: 
    (variable:ClassName) or (variable:ClassName:OtherClass)
    The node may also include optional properties.

    Parameters:
    - variable_name (str): Name for the regex group capturing the variable name.
    - classes_group_name (str): Name for the regex group capturing the mandatory class names.

    Returns:
    - str: Regex pattern for the node with a mandatory variable and class.
    """
    return f'(?:\({variable_name}{create_pattern_classes_must(classes_group_name)}'+CONST_PATTERN_PROPERTIES+'\))'

def create_pattern_variable(variable_group_name):
    """
    Generates a regex pattern for a single variable name.
    
    The pattern represents a variable name consisting only of words without spaces.
    The variable could be empty.

    Parameters:
    - variable_group_name (str): Name for the regex group capturing the variable name.

    Returns:
    - str: Regex pattern for the variable name.
    """
    return f'(?P<{variable_group_name}>[a-zA-Z]*)'

def create_pattern_classes(classes_group_name):
    """
    Generates a regex pattern for class names in nodes.
    
    The pattern represents class names in various formats, such as:
    :ClassName or :`ClassName`
    Multiple class names (like :Class1:Class2) are also matched.

    Parameters:
    - classes_group_name (str): Name for the regex group capturing the class names.

    Returns:
    - str: Regex pattern for class names in nodes.
    """
    return f'(?P<{classes_group_name}>(:`?[\w]+`?)*)'

def create_pattern_classes_must(classes_group_name):
    """
    Generates a regex pattern for mandatory class names in nodes.
    
    The pattern represents class names in various formats, such as:
    :ClassName or :`ClassName`
    Unlike the 'create_pattern_classes' function, this ensures that at least one class name exists.

    Parameters:
    - classes_group_name (str): Name for the regex group capturing the mandatory class names.

    Returns:
    - str: Regex pattern for mandatory class names in nodes.
    """
    return f'(?P<{classes_group_name}>(:`?[\w]+`?)+)'

def create_pattern_relationship_name(relationships_type_group_name):
    """
    Generates a regex pattern for relationship names.
    
    The pattern represents relationship names in various formats, including optional negation, such as:
    :REL_TYPE or :`REL_TYPE` or :!REL_TYPE 
    Multiple relationship types separated by '|' are also matched.

    Parameters:
    - relationships_type_group_name (str): Name for the regex group capturing the relationship types.

    Returns:
    - str: Regex pattern for relationship names.
    """
    return f'(?P<{relationships_type_group_name}>(?::!?`?[a-zA-Z_]*`?)?(?:\|!?`?[a-zA-Z_]+`?)*)?'

def create_pattern_relationship(relationship_variable_group_name, relationship_type_group_name, left_arrow_name, right_arrow_name):
    """
    Generates a regex pattern for relationships in a graph pattern.
    
    The pattern represents relationships in various formats, such as:
    -[variable:REL_TYPE]-, -[variable:`REL_TYPE`]-, or -[:`REL_TYPE`]-.
    It also accounts for optional arrow directions (e.g., -> or <-), variable names, relationship types, and properties.

    Parameters:
    - relationship_variable_group_name (str): Name for the regex group capturing the relationship variable (e.g., "rel" in -[rel:REL_TYPE]-).
    - relationship_type_group_name (str): Name for the regex group capturing the relationship type (e.g., "REL_TYPE" in -[:REL_TYPE]-).
    - left_arrow_name (str): Name for the regex group capturing the optional left arrow direction (<).
    - right_arrow_name (str): Name for the regex group capturing the optional right arrow direction (>).

    Returns:
    - str: Regex pattern for relationships in a graph pattern.
    """
    return f'(?P<{left_arrow_name}><)?-\[{create_pattern_variable(relationship_variable_group_name)}{create_pattern_relationship_name(relationship_type_group_name)}{CONST_PATTERN_PROPERTIES}\]-(?P<{right_arrow_name}>>)?'

def create_pattern_relationship_short(left_arrow_name, right_arrow_name):
    """
    Generates a simplified regex pattern for relationships without specified types or properties.
    
    The pattern matches short relationship patterns, such as:
    --> or <--.
    
    Parameters:
    - left_arrow_name (str): Name for the regex group capturing the optional left arrow direction (<).
    - right_arrow_name (str): Name for the regex group capturing the optional right arrow direction (>).

    Returns:
    - str: Regex pattern for simplified relationships in a graph pattern.
    """
    return f'(?P<{left_arrow_name}><)?--(?P<{right_arrow_name}>>)?'

def list_classes(schema):
    """
    Retrieves a list of unique classes present in the given schema.

    This function combines both source and target classes and returns a unique list 
    of all class names that appear in the schema.

    Parameters:
    - schema (list of dict): A list of dictionary items representing the graph schema.

    Returns:
    - list of str: A list of unique class names.
    """
    classes_set = {item[CONST_SOURCE_CLASS_KEY] for item in schema}
    classes_set.update({item[CONST_TARGET_CLASS_KEY] for item in schema})
    classes_list = list(classes_set)
    return classes_list

def list_source_classes(schema):
    """
    Retrieves a list of unique source classes from the given schema.

    This function examines the source classes from the schema and returns a list 
    of unique class names that have been used as sources.

    Parameters:
    - schema (list of dict): A list of dictionary items representing the graph schema.

    Returns:
    - list of str: A list of unique source class names.
    """
    source_classes_set = {item[CONST_SOURCE_CLASS_KEY] for item in schema}
    source_classes_list = list(source_classes_set)
    return source_classes_list

def list_target_classes(schema):
    """
    Retrieves a list of unique target classes from the given schema.

    This function examines the target classes from the schema and returns a list 
    of unique class names that have been used as targets.

    Parameters:
    - schema (list of dict): A list of dictionary items representing the graph schema.

    Returns:
    - list of str: A list of unique target class names.
    """
    target_classes_set = {item[CONST_TARGET_CLASS_KEY] for item in schema}
    target_classes_list = list(target_classes_set)
    return target_classes_list

def list_unique_relationships(schema):
    """
    Retrieves a list of unique relationships present in the given schema.

    This function examines the relationships (or predicates) from the schema and 
    returns a list of unique names.

    Parameters:
    - schema (list of dict): A list of dictionary items representing the graph schema.

    Returns:
    - list of str: A list of unique relationship names.
    """
    predicates_set = {item[CONST_RELATIONSHIP_KEY] for item in schema}
    predicates_list = list(predicates_set)
    return predicates_list

def process_general_pattern(query, schema):
    """
    Process a general Cypher pattern query against the given graph schema.

    This function examines a Cypher query to ensure it matches the provided graph schema.
    If the pattern does not match, the function attempts to correct the query.
    In certain conditions (e.g. undirected relationships or unmatched patterns), 
    it might return an empty string, based on challenge guidelines.

    Examples of handled patterns:
    - (varA:classA)-[relVar:relName]->(varB:classB)
    - (varA:classA)<-[relVar:relName]-(varB:classB)

    Parameters:
    - query (str): The Cypher query pattern to be processed.
    - schema (list of dict): A list of dictionary items representing the graph schema.

    Returns:
    - str: The processed query if it's valid according to the schema, 
           otherwise an empty string.
    
    Note:
    The function uses regular expressions to identify nodes and relationships 
    in the query. After identifying patterns in the query, it checks the validity
    of the pattern with the provided schema and tries to correct any discrepancies.
    """
    return_empty_response = False # flag used to return an empty string based on challenge guidelines
    # Strucutre of the pattern: (varA:classA){leftArrow}-[relVar:relName]-{rightArrow}(varB:classB)
    pattern_str = f'{create_pattern_node("varA","classesA")}{create_pattern_relationship("relVar","relsNames","leftArrow","rightArrow")}{create_pattern_node("varB","classesB")}'
    pattern = re.compile(pattern_str)
    
    # Every time some match is found, we store it to remove it later
    # This is done to be able to match other aparitions like: (nodeA)-[:REL]->(nodeB)-[:REL2]->(nodeC)
    # where we need to match (nodeA)-[:REL]->(nodeB) and (nodeB)-[:REL2]->(nodeC)
    # after we match (nodeA)-[:REL]->(nodeB), we remove it from a copy of the query, and then we look for other patterns (nodeB)-[:REL2]->(nodeC)
    matches_to_remove = []
    query_copy = query
    
    # Do while loop that ends when there is no more matches to analyze
    while True:
        
        # If there is some match to remove, remove it from the query
        for match_to_remove in matches_to_remove:
            query_copy = query_copy.replace(match_to_remove, CONST_EMPTY_STRING)
        
        # Reset the matches to remove
        matches_to_remove = []
        
        # Search for the pattern in the copy of the query
        matches = pattern.finditer(query_copy)
        
        for match in matches:
            # Get the match string
            full_match_string = match.group()
            
            # Store the first node and rel from the match string to remove it later
            matches_to_remove.append(get_first_node_and_relationship(full_match_string))
            
            printb(f'Processing match {full_match_string}')
            
            # Get the groups
            node_var_a = match.group('varA')
            node_a_classes = match.group('classesA') and match.group('classesA').replace(':',CONST_EMPTY_STRING, 1).replace('`',CONST_EMPTY_STRING).split(':')
            node_var_b = match.group('varB')
            node_b_classes = match.group('classesB') and match.group('classesB').replace(':',CONST_EMPTY_STRING, 1).replace('`',CONST_EMPTY_STRING).split(':')
            rel_var = match.group('relVar')
            rels_names = match.group('relsNames') and match.group('relsNames').replace(':',CONST_EMPTY_STRING).replace('!',CONST_EMPTY_STRING).replace('`',CONST_EMPTY_STRING).split('|')
            left_arrow = match.group('leftArrow')
            right_arrow = match.group('rightArrow')
            
            # If the relationships name is present, check if relationship exists in the schema
            rels_names_is_defined = is_defined(rels_names)
            if rels_names_is_defined and not relationships_exists_in_schema(rels_names, schema):
                printy(f'No schema item found for relationships {rels_names} in match {full_match_string}')
                return_empty_response = True
            
            # If node a has classes, checks that at least one of the classes exists in the schema
            classes_a_is_defined = is_defined(node_a_classes)
            if classes_a_is_defined and not classes_exists_in_schema(node_a_classes, schema):
                printy(f'No schema item found for classes {node_a_classes} in match {full_match_string}')
                return_empty_response = True
            
            # If node b has classes, checks that at least one of the classes exists in the schema
            classes_b_is_defined = is_defined(node_b_classes)
            if classes_b_is_defined and not classes_exists_in_schema(node_b_classes, schema):
                printy(f'No schema item found for classes {node_b_classes} in match {full_match_string}')
                return_empty_response = True
            
            # If there is no direction (right or left arrow) do nothing
            left_arrow_is_defined = is_defined(left_arrow)
            right_arrow_is_defined = is_defined(right_arrow)
            # based on guideline: "If the input query has an undirected relationship in the pattern, we do not correct it."
            if not left_arrow_is_defined and not right_arrow_is_defined:
                printy(f'No direction found in match {full_match_string}, continuing')
                continue
            
            # If both directions are defined, that is an error
            if left_arrow_is_defined and right_arrow_is_defined:
                printy(f'Both directions are defined in {full_match_string}')
                return_empty_response = True
        
            # If at least one class is not defined
            # The class could be in other part of the query
            node_var_a_is_defined = is_defined(node_var_a)
            node_var_b_is_defined = is_defined(node_var_b)
            
            # search classes for node a
            if not classes_a_is_defined:
                if node_var_a_is_defined:
                    node_a_classes = search_for_classes(node_var_a, query)
                    classes_a_is_defined = is_defined(node_a_classes)
            
            # search classes for node b
            if not classes_b_is_defined:
                if node_var_b_is_defined:
                    node_b_classes = search_for_classes(node_var_b, query)
                    classes_b_is_defined = is_defined(node_b_classes)
                
            # If both classes are still not defined, there is nothing to validate, continue
            if not classes_a_is_defined and not classes_b_is_defined:    
                printy(f'No classes are defined in {full_match_string}')
                continue
            
            # Identifies source and destination classes
            if left_arrow_is_defined:
                source_class_is_defined, target_class_is_defined = classes_b_is_defined, classes_a_is_defined
                source_classes_names, target_classes_names = node_b_classes, node_a_classes
            elif right_arrow_is_defined:
                source_class_is_defined, target_class_is_defined = classes_a_is_defined, classes_b_is_defined
                source_classes_names, target_classes_names = node_a_classes, node_b_classes
            else:
                source_class_is_defined = target_class_is_defined = False
                source_classes_names = target_classes_names = None
        
            # only tries to fix the query if the pattern is not found in the schema
            if not pattern_exists_in_schema_multiple(source_classes_names, target_classes_names, rels_names, schema, source_class_is_defined, target_class_is_defined, rels_names_is_defined):
                # Then, checks if the opposite pattern exists in the schema
                if pattern_exists_in_schema_multiple(target_classes_names, source_classes_names, rels_names, schema, target_class_is_defined, source_class_is_defined, rels_names_is_defined):
                    # If it exists, the direction is wrong, so it changes it
                    printg(f'Pattern found in schema, but with opposite direction in match {full_match_string}, fixing the query')
                    correct_full_match_string = match.group()
                    
                    if left_arrow_is_defined:
                        correct_full_match_string = correct_full_match_string.replace(CONST_SIMPLE_ARROW_RIGHT_TO_LEFT, CONST_NO_ARROW_LEFT_SIDE)
                        correct_full_match_string = correct_full_match_string.replace(CONST_NO_ARROW_RIGHT_SIDE, CONST_SIMPLE_ARROW_LEFT_TO_RIGHT)
                    elif right_arrow_is_defined:
                        correct_full_match_string = correct_full_match_string.replace(CONST_SIMPLE_ARROW_LEFT_TO_RIGHT, CONST_NO_ARROW_RIGHT_SIDE)
                        correct_full_match_string = correct_full_match_string.replace(CONST_NO_ARROW_LEFT_SIDE, CONST_SIMPLE_ARROW_RIGHT_TO_LEFT)
                    
                    query = query.replace(full_match_string, correct_full_match_string)
                # if the opposite pattern doesnt exists in schema                
                else:
                    # this response is based on the guideline: "If the given pattern in a Cypher statement doesn't fit the graph schema, simply return an empty string"
                    printy(f'No schema item found for opposite pattern {source_classes_names} {rels_names} {target_classes_names} in match {full_match_string}')
                    printy(f'Schema: {schema}')
                    return_empty_response = True
        
        # no more matches to analyze
        if len(matches_to_remove) == 0:
            break
    
    if return_empty_response:
        return CONST_EMPTY_STRING
    else:
        return query
            
def process_short_rel_pattern(query, schema):
    """
    Process a Cypher query pattern with short (unlabeled) relationships.
    
    This function corrects the direction of relationships in the given Cypher
    query pattern based on the provided schema. It identifies patterns that don't 
    fit the schema and attempts to correct them. If a pattern cannot be 
    corrected or identified within the schema, an empty string is returned.
    
    Args:
        query (str): The input Cypher query string.
        schema (object): The schema against which the query is validated.
        
    Returns:
        str: Corrected Cypher query or an empty string if the query doesn't 
             fit the graph schema.
        
    Example patterns:
        (varA:classA)--(varB:classB) or (varA:classA)<--(varB:classB)
    
    Notes:
        - The function assumes that the relationship name is not provided 
          in the pattern.
        - If a query contains an undirected relationship, the function does not 
          correct it.
        - If a given pattern doesn't fit the graph schema, the function 
          returns an empty string.
    """
    return_empty_response = False # flag used to return an empty string based on challenge guidelines
    # Strucutre of the pattern: (varA:classA){leftArrow}--{rightArrow}(varB:classB)
    pattern_str = f'{create_pattern_node("varA","classesA")}{create_pattern_relationship_short("leftArrow","rightArrow")}{create_pattern_node("varB","classesB")}'
    pattern = re.compile(pattern_str)
    
    # Every time some match is found, we store it to remove it later
    # This is done to be able to match other aparitions like: (nodeA)-->(nodeB)-->(nodeC)
    # where we need to match (nodeA)-->(nodeB) and (nodeB)-->(nodeC)
    # after we match (nodeA)-->(nodeB), we remove it from a copy of the query, and then we look for other patterns (nodeB)-->(nodeC)
    matches_to_remove = []
    query_copy = query
    
    # Do while loop that ends when there is no more matches to analyze
    while True: 
        
        # If there is some match to remove, remove it from the query
        for match_to_remove in matches_to_remove:
            query_copy = query_copy.replace(match_to_remove, CONST_EMPTY_STRING)
        
        # Reset the matches to remove
        matches_to_remove = []
        
        # Search for the pattern in the copy of the query
        matches = pattern.finditer(query_copy)
        
        for match in matches:
            # Get the match string
            full_match_string = match.group()
            
            printb(f'Processing match {full_match_string}')
            
            # Store the first node and rel from the match string to remove it later
            matches_to_remove.append(get_first_node_and_relationship(full_match_string))
            
            # Get the groups
            node_var_a = match.group('varA')
            node_a_classes = match.group('classesA') and match.group('classesA').replace(':',CONST_EMPTY_STRING, 1).replace('`',CONST_EMPTY_STRING).split(':')
            node_var_b = match.group('varB')
            node_b_classes = match.group('classesB') and match.group('classesB').replace(':',CONST_EMPTY_STRING, 1).replace('`',CONST_EMPTY_STRING).split(':')
            left_arrow = match.group('leftArrow')
            right_arrow = match.group('rightArrow')
            
            # Set the relationship name to not defined since the short pattern does not have it
            rels_names = None
            rels_names_is_defined = False
            
            # If node a has classes, checks that at least one of the classes exists in the schema
            classes_a_is_defined = is_defined(node_a_classes)
            if classes_a_is_defined and not classes_exists_in_schema(node_a_classes, schema):
                printr(f'No schema item found for classes {node_a_classes} in match {full_match_string}')
                return_empty_response = True
            
            # If node b has classes, checks that at least one of the classes exists in the schema
            classes_b_is_defined = is_defined(node_b_classes)
            if classes_b_is_defined and not classes_exists_in_schema(node_b_classes, schema):
                printr(f'No schema item found for classes {node_b_classes} in match {full_match_string}')
                return_empty_response = True
            
            # If there is no direction (right or left arrow) do nothing
            left_arrow_is_defined = is_defined(left_arrow)
            right_arrow_is_defined = is_defined(right_arrow)
            # based on guideline: "If the input query has an undirected relationship in the pattern, we do not correct it."
            if not left_arrow_is_defined and not right_arrow_is_defined:
                printb(f'No direction found in match {full_match_string}, continuing')
                continue
            
            # If both directions are defined, that is an error
            if left_arrow_is_defined and right_arrow_is_defined:
                printr(f'Both directions are defined in {full_match_string}')
                return_empty_response = True
        
            # If at least one class is not defined
            # The class could be in other part of the query  
            node_var_a_is_defined = is_defined(node_var_a)
            node_var_b_is_defined = is_defined(node_var_b)
            
            # search classes for node a
            if not classes_a_is_defined:
                if node_var_a_is_defined:
                    node_a_classes = search_for_classes(node_var_a, query)
                    classes_a_is_defined = is_defined(node_a_classes)
            
            # search classes for node b
            if not classes_b_is_defined:
                if node_var_b_is_defined:
                    node_b_classes = search_for_classes(node_var_b, query)
                    classes_b_is_defined = is_defined(node_b_classes)
                
            # If both classes are still not defined, there is nothing to validate, continue
            if not classes_a_is_defined and not classes_b_is_defined:    
                printy(f'No classes are defined in {full_match_string}')
                continue
            
            # Identifies source and destination classes
            if left_arrow_is_defined:
                source_class_is_defined, target_class_is_defined = classes_b_is_defined, classes_a_is_defined
                source_classes_names, target_classes_names = node_b_classes, node_a_classes
            elif right_arrow_is_defined:
                source_class_is_defined, target_class_is_defined = classes_a_is_defined, classes_b_is_defined
                source_classes_names, target_classes_names = node_a_classes, node_b_classes
            else:
                source_class_is_defined = target_class_is_defined = False
                source_classes_names = target_classes_names = None
        
            # only tries to fix the query if the pattern is not found in the schema
            if not pattern_exists_in_schema_multiple(source_classes_names, target_classes_names, rels_names, schema, source_class_is_defined, target_class_is_defined, rels_names_is_defined):
                # Then, checks if the opposite pattern exists in the schema
                if pattern_exists_in_schema_multiple(target_classes_names, source_classes_names, rels_names, schema, target_class_is_defined, source_class_is_defined, rels_names_is_defined):
                    # If it exists, the direction is wrong, so it changes it
                    printg(f'Pattern found in schema, but with opposite direction in match {full_match_string}, fixing the query')
                    correct_full_match_string = match.group()
                    
                    if left_arrow_is_defined:
                        correct_full_match_string = correct_full_match_string.replace(CONST_LARGE_ARROW_RIGHT_TO_LEFT, CONST_LARGE_ARROW_LEFT_TO_RIGHT)
                    elif right_arrow_is_defined:
                        correct_full_match_string = correct_full_match_string.replace(CONST_LARGE_ARROW_LEFT_TO_RIGHT, CONST_LARGE_ARROW_RIGHT_TO_LEFT)
                    
                    query = query.replace(full_match_string, correct_full_match_string)
                # if the opposite pattern doesnt exists in schema                
                else:
                    # this response is based on the guideline: "If the given pattern in a Cypher statement doesn't fit the graph schema, simply return an empty string"
                    printy(f'No schema item found for opposite pattern {source_classes_names} {rels_names} {target_classes_names} in match {full_match_string}')
                    printy(f'Schema: {schema}')
                    return_empty_response = True
        
        # no more matches to analyze
        if len(matches_to_remove) == 0:
            break
    
    if return_empty_response:
        return CONST_EMPTY_STRING
    else:
        return query