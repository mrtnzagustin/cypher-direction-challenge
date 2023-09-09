# Cypher Direction Challenge Refactor

Implementation of the Tomaz Bratanic (@tomasonjo) neo4j cypher direction competition.
- **Original Repository**: [Cypher Direction Competition](https://github.com/tomasonjo/cypher-direction-competition/)

## Quickstart

### Using Python Locally
1. Ensure you have Python installed.
2. Navigate to the `src` directory.
3. Run the `main.py` script. This script will process the queries listed in the `examples.csv` file from the competition.

   ```bash
   python main.py
   ```

### Using Docker

If you'd rather not set up a local Python environment, you can utilize the Docker configuration provided in this repository.

1. Build and run the Docker container.
2. Optionally, if you're using Visual Studio Code, the solution is compatible with the Remote Container extension for a seamless development experience inside a Docker container.

## Implementation Details

### Regular Expressions
The solution primarily relies on regular expressions to parse and process Cypher query patterns.

- **Utility Functions**: Inspect the `utils` folder for a deeper dive into the utility functions and regex patterns used in this solution.
- **Regex Debugging**: If you wish to test or debug any of the regular expressions, I recommend using [regex101](https://regex101.com/).

---

With this documentation, readers can get a clear overview of the project, instructions on how to run the solution, and insight into the core mechanism used (regular expressions).