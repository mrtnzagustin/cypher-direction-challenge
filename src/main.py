from utils import *
import re

def process_general_pattern(query, schema):
    """Process the general pattern, with relationship name. Examples: (varA:classA)-[relVar:relName]->(varB:classB) or (varA:classA)<-[relVar:relName]-(varB:classB)"""
    # Strucutre of the pattern: (varA:classA){leftArrow}-[relVar:relName]-{rightArrow}(varB:classB)
    pattern_str = f'{create_pattern_node("varA","classA")}{create_pattern_relationship("relVar","relName","leftArrow","rightArrow")}{create_pattern_node("varB","classB")}'
    pattern = re.compile(pattern_str)
    
    matches = pattern.finditer(query)
    
    for match in matches:
        # Get the match string
        full_match_string = match.group()
        
        printb(f'Processing match {full_match_string}')
        
        # Get the groups
        node_var_a = match.group('varA')
        node_class_a = match.group('classA') and match.group('classA').replace(':','').replace('`','')
        node_var_b = match.group('varB')
        node_class_b = match.group('classB') and match.group('classB').replace(':','').replace('`','')
        rel_var = match.group('relVar')
        rel_name = match.group('relName') and match.group('relName').replace(':','').replace('`','')
        left_arrow = match.group('leftArrow')
        right_arrow = match.group('rightArrow')
        
        # If the relationship name is present, check if relationship exists in the schema
        rel_name_is_defined = rel_name != '' and rel_name != None
        if rel_name_is_defined and not relationship_exists_in_schema(rel_name, schema):
            printy(f'No schema item found for relationship {rel_name} in match {full_match_string}')
            return ''
        
        # If node a has a class, checks if the class exists in the schema
        class_a_is_defined = node_class_a != '' and node_class_a != None
        if class_a_is_defined and not class_exists_in_schema(node_class_a, schema):
            printy(f'No schema item found for class {node_class_a} in match {full_match_string}')
            return ''
        
        # If node b has a class, checks if the class exists in the schema
        class_b_is_defined = node_class_b != '' and node_class_b != None
        if class_b_is_defined and not class_exists_in_schema(node_class_b, schema):
            printy(f'No schema item found for class {node_class_b} in match {full_match_string}')
            return ''
        
        # If there is no direction (right or left arrow) do nothing
        left_arrow_is_defined = left_arrow != '' and left_arrow != None
        right_arrow_is_defined = right_arrow != '' and right_arrow != None
        if not left_arrow_is_defined and not right_arrow_is_defined:
            printy(f'No direction found in match {full_match_string}, continuing')
            continue
        
        # If both directions are defined, that is an error
        if not left_arrow_is_defined and not right_arrow_is_defined:
            printy(f'Both directions are defined in {full_match_string}')
            return ''
    
        # If both classes are not defined, there is nothing to validate, continue
        # TODO: The class could be in other step inside the query    
        if not class_a_is_defined and not class_b_is_defined:
            printy(f'No classes are defined in {full_match_string}')
            continue
        
        # Identifies source and destination classes
        if left_arrow_is_defined:
            source_class_is_defined, target_class_is_defined = class_b_is_defined, class_a_is_defined
            source_class_name, target_class_name = node_class_b, node_class_a
        elif right_arrow_is_defined:
            source_class_is_defined, target_class_is_defined = class_a_is_defined, class_b_is_defined
            source_class_name, target_class_name = node_class_a, node_class_b
        else:
            source_class_is_defined = target_class_is_defined = False
            source_class_name = target_class_name = None
    
        if not pattern_exists_in_schema(source_class_name, target_class_name, rel_name, schema, source_class_is_defined, target_class_is_defined, rel_name_is_defined):
            # Then, checks if the opposite pattern exists in the schema
            if pattern_exists_in_schema(target_class_name, source_class_name, rel_name, schema, target_class_is_defined, source_class_is_defined, rel_name_is_defined):
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
                
            else:
                print(f'No schema item found for pattern {source_class_name} {rel_name} {target_class_name} in match {full_match_string}')
                return ''
    
    return query
            
def process_short_rel_pattern(query, schema):
    """Process the short pattern, with no relationship name. Examples: (varA:classA)--(varB:classB) or (varA:classA)<--(varB:classB)"""
    # Strucutre of the pattern: (varA:classA){leftArrow}--{rightArrow}(varB:classB)
    pattern_str = f'{create_pattern_node("varA","classA")}{create_pattern_relationship_short("leftArrow","rightArrow")}{create_pattern_node("varB","classB")}'
    pattern = re.compile(pattern_str)
    
    matches = pattern.finditer(query)
    
    for match in matches:
        # Get the match string
        full_match_string = match.group()
        
        printb(f'Processing match {full_match_string}')
        
        # Get the groups
        node_var_a = match.group('varA')
        node_class_a = match.group('classA') and match.group('classA').replace(':','').replace('`','')
        node_var_b = match.group('varB')
        node_class_b = match.group('classB') and match.group('classB').replace(':','').replace('`','')
        left_arrow = match.group('leftArrow')
        right_arrow = match.group('rightArrow')
        
        # Set the relationship name to not defined since the short pattern does not have it
        rel_name = None
        rel_name_is_defined = False
        
        # If node a has a class, checks if the class exists in the schema
        class_a_is_defined = node_class_a != '' and node_class_a != None
        if class_a_is_defined and not class_exists_in_schema(node_class_a, schema):
            printr(f'No schema item found for class {node_class_a} in match {full_match_string}')
            return ''
        
        # If node b has a class, checks if the class exists in the schema
        class_b_is_defined = node_class_b != '' and node_class_b != None
        if class_b_is_defined and not class_exists_in_schema(node_class_b, schema):
            printr(f'No schema item found for class {node_class_b} in match {full_match_string}')
            return ''
        
        # If there is no direction (right or left arrow) do nothing
        left_arrow_is_defined = left_arrow != '' and left_arrow != None
        right_arrow_is_defined = right_arrow != '' and right_arrow != None
        if not left_arrow_is_defined and not right_arrow_is_defined:
            printb(f'No direction found in match {full_match_string}, continuing')
            continue
        
        # If both directions are defined, that is an error
        if not left_arrow_is_defined and not right_arrow_is_defined:
            printr(f'Both directions are defined in {full_match_string}')
            return ''
    
        # If both classes are not defined, there is nothing to validate, continue
        # TODO: The class could be in other step inside the query    
        if not class_a_is_defined and not class_b_is_defined:
            print(f'No classes are defined in {full_match_string}')
            continue
        
        if left_arrow_is_defined:
            source_class_is_defined, target_class_is_defined = class_b_is_defined, class_a_is_defined
            source_class_name, target_class_name = node_class_b, node_class_a
        elif right_arrow_is_defined:
            source_class_is_defined, target_class_is_defined = class_a_is_defined, class_b_is_defined
            source_class_name, target_class_name = node_class_a, node_class_b
        else:
            source_class_is_defined = target_class_is_defined = False
            source_class_name = target_class_name = None
    
        if not pattern_exists_in_schema(source_class_name, target_class_name, rel_name, schema, source_class_is_defined, target_class_is_defined, rel_name_is_defined):
            # Then, checks if the opposite pattern exists in the schema
            if pattern_exists_in_schema(target_class_name, source_class_name, rel_name, schema, target_class_is_defined, source_class_is_defined, rel_name_is_defined):
                # If it exists, the direction is wrong, so it changes it
                printg(f'Pattern found in schema, but with opposite direction in match {full_match_string}, fixing the query')
                correct_full_match_string = match.group()
                
                if left_arrow_is_defined:
                    correct_full_match_string = correct_full_match_string.replace(CONST_LARGE_ARROW_RIGHT_TO_LEFT, CONST_LARGE_ARROW_LEFT_TO_RIGHT)
                elif right_arrow_is_defined:
                    correct_full_match_string = correct_full_match_string.replace(CONST_LARGE_ARROW_LEFT_TO_RIGHT, CONST_LARGE_ARROW_RIGHT_TO_LEFT)
                
                query = query.replace(full_match_string, correct_full_match_string)
                
            else:
                print(f'No schema item found for pattern {source_class_name} {rel_name} {target_class_name} in match {full_match_string}')
                return ''
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
            correct_count+=1
        elif result_query == '':
            printr(f'Query process worked with some warnings, check previous messages')
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