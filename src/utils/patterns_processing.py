import re
from .constants import *
from .general import is_defined
from .ui import printb, printg, printr, printy

def get_first_node_and_relationship(string):
    """Returns the first node and relationship from the string"""
    # in example for (nodeA)-[:REL]->(nodeB), returns only (nodeA)-[:REL]->
    # for (nodeA)-->(nodeB), returns only (nodeA)-->
    first_node_and_relationship = '(' + string.split('(')[1]
    return first_node_and_relationship

def search_for_classes(variable, query):
    """Search for the classes of the given variable in the query"""
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
    """Check if the given pattern exists in the schema, but with many possible classes (target and source), relationships and directions"""
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
    """Check if the given pattern exists in the schema. In example Person, WORKS_AT, Organization"""
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
    """Check if at least one of the given classes exists in the schema"""
    return any (class_name in list_classes(schema) for class_name in classes_name)

def relationships_exists_in_schema(relationships_names, schema):
    """Check if at least one of the given relationship exists in the schema"""
    return any (relationship_name in list_unique_relationships(schema) for relationship_name in relationships_names)

# (variable:ClassName) or (:ClassName) or (), including possible properties
def create_pattern_node(variable_group_name, class_group_name):
    return f'(?:\({create_pattern_variable(variable_group_name)}{create_pattern_classes(class_group_name)}'+CONST_PATTERN_PROPERTIES+'\))'

# (variable:ClassName) or (variable:ClassName:OtherClass) including possible properties, variable and class are mandatory
def create_pattern_node_with_variable(variable_name, classes_group_name):
    return f'(?:\({variable_name}{create_pattern_classes_must(classes_group_name)}'+CONST_PATTERN_PROPERTIES+'\))'

# a single variable name using words only, no spaces, it could be empty
def create_pattern_variable(variable_group_name):
    return f'(?P<{variable_group_name}>[a-zA-Z]*)'

# :ClassName or :`ClassName`
def create_pattern_classes(classes_group_name):
    return f'(?P<{classes_group_name}>(:`?[\w]+`?)*)'

# :ClassName or :`ClassName`
def create_pattern_classes_must(classes_group_name):
    return f'(?P<{classes_group_name}>(:`?[\w]+`?)+)'

# :REL_TYPE or :`REL_TYPE` or :!REL_TYPE 
def create_pattern_relationship_name(relationships_type_group_name):
    return f'(?P<{relationships_type_group_name}>(?::!?`?[a-zA-Z_]*`?)?(?:\|!?`?[a-zA-Z_]+`?)*)?'

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

def process_general_pattern(query, schema):
    """Process the general pattern, with relationship name. Examples: (varA:classA)-[relVar:relName]->(varB:classB) or (varA:classA)<-[relVar:relName]-(varB:classB)"""
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
            if not left_arrow_is_defined and not right_arrow_is_defined:
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
    """Process the short pattern, with no relationship name. Examples: (varA:classA)--(varB:classB) or (varA:classA)<--(varB:classB)"""
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
            if not left_arrow_is_defined and not right_arrow_is_defined:
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