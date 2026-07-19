class DocumentCorpus:
    
    def __init__(self):
        self.documents = []
        
    def add_document(self,document)->None:
        self.documents.append(document)
        
    def get_documents(self)->list[str]:
        return self.documents
    
    def total_documents(self)->int:
        return len(self.documents)