class pornFile():
    fileType = 'all'
    rawName = None
    prodName = None
    relation = None

    def __init__(self, fileType=None, rawName=None, prodName=None, relation=None):
        self.fileType=fileType
        self.rawName = rawName
        self.prodName = prodName
        self.relation = relation


    def __repr__(self):
        return "<pornFile Type:%s FileName:%s ProductID:%s relations:%s>"% (self.fileType, self.rawName, self.prodName,
                                                                            self.relation)