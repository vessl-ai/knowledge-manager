
class Document:
    def __init__(self, id, filename, content, created_at, updated_at):
        self.id = id
        self.filename = filename
        self.content = content
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return f'<Document {self.id}>'