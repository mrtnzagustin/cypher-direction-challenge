# ==============================
# UI Color Constants
# ==============================
CONST_COLOR_BLUE = "\033[34m"
CONST_COLOR_RED = "\033[31m"
CONST_COLOR_GREEN = "\033[32m"
CONST_COLOR_YELLOW = "\033[33m"
CONST_COLOR_NORMAL = "\033[0m"

# ==============================
# CSV File Configuration Constants
# Describes the paths and key structure for example Cypher queries CSV file
# ==============================
CYPHER_QUERIES_CSV_FILE_PATH = "files/examples.csv"
CONST_SOURCE_CLASS_KEY = "sourceClass"
CONST_TARGET_CLASS_KEY = "targetClass"
CONST_RELATIONSHIP_KEY = "relationship"
CONST_SCHEMA_KEY = "schema"
CONST_STATEMENT_KEY = "statement"
CONST_CORRECT_QUERY_KEY = "correct_query"

# ==============================
# Cypher Pattern Constants
# These constants represent different arrow notations in Cypher query patterns
# and other pattern-related configurations
# ==============================
CONST_SIMPLE_ARROW_LEFT_TO_RIGHT = "]->"
CONST_SIMPLE_ARROW_RIGHT_TO_LEFT = "<-["
CONST_LARGE_ARROW_LEFT_TO_RIGHT = "-->"
CONST_LARGE_ARROW_RIGHT_TO_LEFT = "<--"
CONST_NO_ARROW_LEFT_SIDE = "-["
CONST_NO_ARROW_RIGHT_SIDE = "]-"
CONST_PATTERN_ANY_SPACE = '\s*'
# Matches property assignments in Cypher queries; e.g., { name: "John", age: "20" }
CONST_PATTERN_PROPERTIES = (CONST_PATTERN_ANY_SPACE +
                            '(?:\{\s*[a-zA-Z]+:\s*["\'][^"]*["\']\s*'
                            '(?:\s*,\s*[a-zA-Z]+:\s*["\'][^"]*["\'])*\s*\})?'
                            + CONST_PATTERN_ANY_SPACE)

# ==============================
# Miscellaneous Constants
# ==============================
CONST_EMPTY_STRING = ''
