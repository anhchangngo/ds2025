from mrjob.job import MRJob

class WordCount(MRJob):
    def mapper(self, _, line):
        """
        Mapper: Tách từng dòng văn bản thành các từ và ánh xạ chúng thành các cặp (word, 1).
        """
        for word in line.split():
            yield word.lower(), 1  # Đưa từ về dạng chữ thường để tránh trùng lặp do viết hoa/viết thường

    def reducer(self, key, values):
        """
        Reducer: Tổng hợp số lần xuất hiện của mỗi từ từ các mapper.
        """
        yield key, sum(values)  # Tổng số lần xuất hiện của từ

if __name__ == '__main__':
    WordCount.run()
