from collections import defaultdict

# Input data
data = [
    "hello world",
    "hello mapreduce",
    "world of mapreduce"
]

# Mapper function: Split sentences into (word, 1) pairs
def mapper(input_data):
    mapped_data = []
    for line in input_data:
        words = line.split()
        for word in words:
            mapped_data.append((word, 1))  # Emit (word, 1)
    return mapped_data

# Reducer function: Combine counts for each word
def reducer(mapped_data):
    reduced_data = defaultdict(int)
    for word, count in mapped_data:
        reduced_data[word] += count  # Sum up counts for each word
    return reduced_data

# Step 1: Map phase
mapped = mapper(data)
print("Mapped Data:", mapped)

# Step 2: Shuffle and Sort (simulate by grouping the same keys)
# Group by word (key)
grouped_data = defaultdict(list)
for word, count in mapped:
    grouped_data[word].append(count)

# Step 3: Reduce phase
final_result = reducer(mapped)
print("Word Count:", dict(final_result))
