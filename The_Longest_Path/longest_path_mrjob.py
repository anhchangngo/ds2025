from mrjob.job import MRJob

class LongestPath(MRJob):
    def mapper(self, _, line):
        """
        Mapper: Outputs the length of the path and the path itself.
        """
        file_path = line.strip()  # Remove any extra whitespace or newlines
        yield "path", file_path  # Emit a common key ("path") for all entries

    def reducer(self, _, paths):
        """
        Reducer: Finds the absolute longest path.
        """
        # Convert generator to a list
        paths = list(paths)
        
        # Find the longest path
        longest_path = max(paths, key=len)
        
        # Emit only the longest path
        yield "Longest Path", longest_path


if __name__ == "__main__":
    LongestPath.run()
