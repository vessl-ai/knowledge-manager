
class QueryResult:
    def __init__(self, query, result):
        self.query = query
        self.result = result

    def __str__(self):
        return f'{self.query} => {self.result}'