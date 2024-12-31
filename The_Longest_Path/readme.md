

### Command 
```
python3 longest_path_mrjob.py input.txt
```

### Mapper
- Reads each file path from the input.
- Emits key-value pairs: `("path", file_path)`.
- Example Input: `/home/user/docs/report.pdf`
- Example Output: `("path", "/home/user/docs/report.pdf")`

### Shuffle and Sort
- Groups all paths by the common key "path".
- Example Output: `"path": ["/home/user/docs/report.pdf", "/home/user/music/playlist.m3u", "/home/user/videos/movie.mp4"]`

### Reducer
Finds the longest file path from the grouped paths.
Emits: `("Longest Path", longest_path)`.
- Example Input: `"path": ["/home/user/docs/report.pdf", "/home/user/music/playlist.m3u", "/home/user/videos/movie.mp4"]`
- Example Output: `("Longest Path", "/home/user/music/playlist.m3u")`

[?] Where is Shuffle and Sort in the Code?
In the MapReduce framework, Shuffle and Sort is not explicitly written in the code. Instead, it is automatically handled by the MapReduce framework, such as mrjob.

### Pesudocode

```py
DEFINE CLASS LongestPath INHERITING FROM MRJob:
    # Mapper function
    FUNCTION mapper(_, line):
        file_path = line.strip()  # Clean the input
        EMIT("path", file_path)  # Emit the key-value pair

    # Reducer function
    FUNCTION reducer(_, paths):
        paths = list(paths)  # Convert paths to a list
        longest_path = max(paths, key=len)  # Find the longest path
        EMIT("Longest Path", longest_path)  # Emit the result

    # Entry point for running the MapReduce job
    FUNCTION main():
        CALL LongestPath.run()  # Trigger the MapReduce pipeline
```
