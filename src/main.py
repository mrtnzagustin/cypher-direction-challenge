from utils import *
import re

def process_general_pattern(query, schema):
    """Process the general pattern, with relationship name. Examples: (varA:classA)-[relVar:relName]->(varB:classB) or (varA:classA)<-[relVar:relName]-(varB:classB)"""
    return_empty_response = False # flag used to return an empty string
    # Strucutre of the pattern: (varA:classA){leftArrow}-[relVar:relName]-{rightArrow}(varB:classB)
    pattern_str = f'{create_pattern_node("varA","classesA")}{create_pattern_relationship("relVar","relsNames","leftArrow","rightArrow")}{create_pattern_node("varB","classesB")}'
    pattern = re.compile(pattern_str)
    
    matches = pattern.finditer(query)
    
    for match in matches:
        # Get the match string
        full_match_string = match.group()
        
        printb(f'Processing match {full_match_string}')
        
        # Get the groups
        node_var_a = match.group('varA')
        node_a_classes = match.group('classesA') and match.group('classesA').replace(':','', 1).replace('`','').split(':')
        node_var_b = match.group('varB')
        node_b_classes = match.group('classesB') and match.group('classesB').replace(':','', 1).replace('`','').split(':')
        rel_var = match.group('relVar')
        rels_names = match.group('relsNames') and match.group('relsNames').replace(':','').replace('`','').split('|')
        left_arrow = match.group('leftArrow')
        right_arrow = match.group('rightArrow')
        
        # If the relationships name is present, check if relationship exists in the schema
        rels_names_is_defined = rels_names != '' and rels_names != None
        if rels_names_is_defined and not relationships_exists_in_schema(rels_names, schema):
            printy(f'No schema item found for relationships {rels_names} in match {full_match_string}')
            return_empty_response = True
        
        # If node a has classes, checks that at least one of the classes exists in the schema
        classes_a_is_defined = node_a_classes != '' and node_a_classes != None
        if classes_a_is_defined and not classes_exists_in_schema(node_a_classes, schema):
            printy(f'No schema item found for classes {node_a_classes} in match {full_match_string}')
            return_empty_response = True
        
        # If node b has classes, checks that at least one of the classes exists in the schema
        classes_b_is_defined = node_b_classes != '' and node_b_classes != None
        if classes_b_is_defined and not classes_exists_in_schema(node_b_classes, schema):
            printy(f'No schema item found for classes {node_b_classes} in match {full_match_string}')
            return_empty_response = True
        
        # If there is no direction (right or left arrow) do nothing
        left_arrow_is_defined = left_arrow != '' and left_arrow != None
        right_arrow_is_defined = right_arrow != '' and right_arrow != None
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
        node_var_a_is_defined = node_var_a != '' and node_var_a != None
        node_var_b_is_defined = node_var_b != '' and node_var_b != None 
        
        if not classes_a_is_defined:
            if node_var_a_is_defined:
                node_a_classes = search_for_classes(node_var_a, query)
                classes_a_is_defined = node_a_classes != '' and node_a_classes != None
        
        if not classes_b_is_defined:
            if node_var_b_is_defined:
                node_b_classes = search_for_classes(node_var_b, query)
                classes_b_is_defined = node_b_classes != '' and node_b_classes != None
            
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
    
    if return_empty_response:
        return ''
    else:
        return query
            
def process_short_rel_pattern(query, schema):
    """Process the short pattern, with no relationship name. Examples: (varA:classA)--(varB:classB) or (varA:classA)<--(varB:classB)"""
    return_empty_response = False # flag used to return an empty string
    # Strucutre of the pattern: (varA:classA){leftArrow}--{rightArrow}(varB:classB)
    pattern_str = f'{create_pattern_node("varA","classesA")}{create_pattern_relationship_short("leftArrow","rightArrow")}{create_pattern_node("varB","classesB")}'
    pattern = re.compile(pattern_str)
    
    matches = pattern.finditer(query)
    
    for match in matches:
        # Get the match string
        full_match_string = match.group()
        
        printb(f'Processing match {full_match_string}')
        
        # Get the groups
        node_var_a = match.group('varA')
        node_a_classes = match.group('classesA') and match.group('classesA').replace(':','', 1).replace('`','').split(':')
        node_var_b = match.group('varB')
        node_b_classes = match.group('classesB') and match.group('classesB').replace(':','', 1).replace('`','').split(':')
        left_arrow = match.group('leftArrow')
        right_arrow = match.group('rightArrow')
        
        # Set the relationship name to not defined since the short pattern does not have it
        rels_names = None
        rels_names_is_defined = False
        
        # If node a has classes, checks that at least one of the classes exists in the schema
        classes_a_is_defined = node_a_classes != '' and node_a_classes != None
        if classes_a_is_defined and not classes_exists_in_schema(node_a_classes, schema):
            printr(f'No schema item found for classes {node_a_classes} in match {full_match_string}')
            return_empty_response = True
        
        # If node b has classes, checks that at least one of the classes exists in the schema
        classes_b_is_defined = node_b_classes != '' and node_b_classes != None
        if classes_b_is_defined and not classes_exists_in_schema(node_b_classes, schema):
            printr(f'No schema item found for classes {node_b_classes} in match {full_match_string}')
            return_empty_response = True
        
        # If there is no direction (right or left arrow) do nothing
        left_arrow_is_defined = left_arrow != '' and left_arrow != None
        right_arrow_is_defined = right_arrow != '' and right_arrow != None
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
        node_var_a_is_defined = node_var_a != '' and node_var_a != None
        node_var_b_is_defined = node_var_b != '' and node_var_b != None 
        
        if not classes_a_is_defined:
            if node_var_a_is_defined:
                node_a_classes = search_for_classes(node_var_a, query)
                classes_a_is_defined = node_a_classes != '' and node_a_classes != None
        
        if not classes_b_is_defined:
            if node_var_b_is_defined:
                node_b_classes = search_for_classes(node_var_b, query)
                classes_b_is_defined = node_b_classes != '' and node_b_classes != None
            
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
    
    if return_empty_response:
        return ''
    else:
        return query
        
def process_query(query, schema):
    """Process the cypher query with the given schema"""
    # General process, search for patterns, and check if the direction is correct
    # by analyzing the schema
    # If the direction is wrong, it changes it
    # If the pattern is not found in the schema, it returns an empty string
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
        printb(f'')
        printb(f'-------------------------')
        printb(f'Processing query {query[CONST_STATEMENT_KEY]}')
        result_query = process_query(query[CONST_STATEMENT_KEY], query[CONST_SCHEMA_KEY])
        
        if result_query == query[CONST_CORRECT_QUERY_KEY]:
            printg(f'Query process worked correctly')
            printg(f'Final query: {result_query}')
            correct_count+=1
        elif result_query == '':
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
    printn('')
    
    process_query(
        """ (:Organization)-->(:Person) RETURN o.name AS name """,
        [
            {
                'sourceClass': 'Person',
                'relationship': 'KNOWS',
                'targetClass': 'Person'
            },
            {
                'sourceClass': 'Person',
                'relationship': 'WORKS_AT',
                'targetClass': 'Organization'
            }
        ])
    
    correct_count, incorrect_count, correct_with_warnings_count, total_count = process_all_queries()
    
    printn('')    
    printn(f'Process finished')
    printg(f'Correct queries: {correct_count}/{total_count}')
    printr(f'Incorrect queries: {incorrect_count}/{total_count}')
    printy(f'Correct with warnings: {correct_with_warnings_count}/{total_count}')
    printn('')
    
if __name__ == "__main__":
    main()