from django.core.paginator import Paginator

class paginate:
    def __init__(self,queryList,requestData):
        self.paginator=Paginator(queryList)
        self.requestData=requestData
    def getPage(self):
        page=self.paginator.get_page(1)
        if self.requestData.get("page"):
            page=self.paginator.get_page(self.requestData.get("page"))
        
        return page