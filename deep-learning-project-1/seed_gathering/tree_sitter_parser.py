from tree_sitter import Language, Parser

# Step 1: Build the Tree-Sitter library for C language
Language.build_library(
    'build/lang.so',  # Path to output the shared object file
    [
        'tree-sitter-c'  # Path to the Tree-Sitter C grammar repository
    ]
)

# Step 2: Set up the C language and parser
LANGUAGE = Language('build/lang.so', 'c')

QUERY = LANGUAGE.query("""
(function_definition) @function
""")

global_parser = Parser()
global_parser.set_language(LANGUAGE)

def get_fn_name(code, parser=global_parser):
    src = bytes(code, "utf8")
    tree = parser.parse(src)
    node = tree.root_node
    
    function_names = []
    captures = QUERY.captures(node)
    
    for cap, typ in captures:
        if typ == "function":
            function_names.append(node_to_string(src, cap))
    
    return function_names
    
def node_to_string(src: bytes, node):
    """
    Convert a Tree-Sitter node to its string representation.
    """
    return src[node.start_byte:node.end_byte].decode("utf8")

def make_parser():
    """
    Create a new Tree-Sitter parser for C.
    """
    _parser = Parser()
    _parser.set_language(LANGUAGE)
    return _parser

# Query to find return statements in C
RETURN_QUERY = LANGUAGE.query("""
(return_statement) @return
""")

def does_have_return(src, parser=global_parser):
    """
    Check if the C code contains return statements with values.
    """
    tree = parser.parse(bytes(src, "utf8"))
    root = tree.root_node
    captures = RETURN_QUERY.captures(root)
    for node, _ in captures:
        # If the return statement doesn't have an argument, it doesn't return a value
        if len(node.children) <= 1:  # Includes "return" itself
            continue
        else:
            return True
    return False

if __name__ == "__main__":
    # Complex C code for testing
    complex_code = """
    #include <stdio.h>

    // A recursive function to calculate the factorial of a number
    int factorial(int n) {
        if (n <= 1) {
            return 1;
        }
        return n * factorial(n - 1);
    }

    // Function to check if a number is prime
    int is_prime(int n) {
        if (n <= 1) {
            return 0;  // Not prime
        }
        for (int i = 2; i * i <= n; i++) {
            if (n % i == 0) {
                return 0;  // Not prime
            }
        }
        return 1;  // Prime
    }

    // Function with multiple return statements and conditions
    int process_value(int val) {
        if (val > 100) {
            return 1;  // Large value
        } else if (val < 0) {
            return -1;  // Negative value
        } else if (val == 0) {
            return 0;  // Zero value
        } else {
            return val * 2;  // Return double the value if positive but not large
        }
    }

    // A function with a loop and return statement inside
    int find_first_even(int arr[], int size) {
        for (int i = 0; i < size; i++) {
            if (arr[i] % 2 == 0) {
                return arr[i];  // Return first even number found
            }
        }
        return -1;  // Return -1 if no even number found
    }

    int main() {
        int result1 = factorial(5);  // Should return 120
        int result2 = is_prime(29);  // Should return 1 (true)
        int result3 = process_value(-10);  // Should return -1 (negative)
        int result4 = find_first_even((int[]){1, 3, 5, 6, 8}, 5);  // Should return 6

        printf("Factorial: %d\n", result1);
        printf("Is prime: %d\n", result2);
        printf("Processed value: %d\n", result3);
        printf("First even number: %d\n", result4);

        return 0;
    }
    """

    # Parse the code and print the syntax tree
    tree = global_parser.parse(bytes(complex_code, "utf8"))
    print("Syntax tree:")
    print(tree.root_node.sexp())  # Print the syntax tree in S-expression format

    # Test function name extraction
    function_names = get_fn_name(complex_code)
    print("\nExtracted function names:")
    print(function_names)

    # Test if the code has return statements
    print("\nChecking for return statements:")
    print("Has return with value (factorial):", does_have_return(complex_code))
    print("Has return with value (is_prime):", does_have_return(complex_code))
    print("Has return with value (process_value):", does_have_return(complex_code))
    print("Has return with value (find_first_even):", does_have_return(complex_code))
