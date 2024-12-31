## MapReduce WordCount

MapReduce is a programming model and processing technique for handling and analyzing large datasets in a distributed and parallel computing environment.

### Core Ideal
1. Map Phase:
Processes input data in parallel and transforms it into intermediate key-value pairs.
2. Reduce Phase:
Aggregates or summarizes the intermediate key-value pairs to produce the final result.

### Key Features
1. Scalability:
Handles petabytes of data across thousands of machines.
2. Fault Tolerance:
Automatically re-executes failed tasks on different nodes.
3. Simplified Programming:
Developers focus on "what to do" (map and reduce functions), while the framework handles "how to do it" (data distribution, parallelization, fault recovery).
4. Distributed Computing:
Runs on clusters of commodity hardware, making it cost-effective.

### Command
```
python3 wordcount_mrjob.py input.txt
```

mrjob: Easy to implement and debug locally, with the potential to scale to larger systems.

input.txt
`three witches watch three swatch watches which witch watches which swatch watch`

output.txt
```
"witch" 1
"swatch"        2
"witches"       1
"which" 2
"watch" 2
"watches"       2
"three" 2
```

### Pseudo Code
```py
function WordCount(input_file):
    Initialize MapperOutput as empty list

    # Step 1: Mapper
    for each line in input_file:
        for each word in line.split():
            word_lower = word.to_lowercase()
            MapperOutput.append((word_lower, 1))

    # Step 2: Shuffle and Sort (Tự động thực hiện)
    GroupedOutput = group_by_key(MapperOutput)

    # Step 3: Reducer
    for each (word, values) in GroupedOutput:
        count = sum(values)
        print(word, count)
```

### Mapper and Reducer work
Mapper Function
- Processes each line of the input file.
- Splits the line into words.
- Emits key-value pairs where the key is a word, and the value is 1.

Input:
- A line of text (e.g., "hello world").

Output:
- Key-value pairs (e.g., ("hello", 1), ("world", 1)).

Reducer Function
- Aggregates the key-value pairs emitted by the mapper.
- Counts the occurrences of each word.

Input:
- Grouped key-value pairs (e.g., ("hello", [1, 1, 1])).

Output:
- The total count for each word (e.g., ("hello", 3)).


### Roles in MapReduce Workflow
1. Mapper:

Reads input data and processes it to emit key-value pairs.

Example: `"hello hello world" → [("hello", 1), ("hello", 1), ("world", 1)]`.

2. Shuffle and Sort (Framework):

Groups and sorts key-value pairs by their key.

Example: `[("hello", 1), ("hello", 1), ("world", 1)] → [("hello", [1, 1]), ("world", [1])]`.

3. Reducer:

Aggregates values for each key to produce the final result.

Example: `[("hello", [1, 1]), ("world", [1])] → [("hello", 2), ("world", 1)]`.
