from math import ceil

def customresponse(data,status,is_pagination=False,page_number=1,page_size=10,total_objects=0,total_count=0) -> object:
     if(is_pagination):
         object_to_return = {
             "data": data,
             "status": status,
             "totalPages":ceil(int(total_objects)/int(page_size)),
             "totalElements":total_objects,
             "number":page_number,
         }
         return object_to_return
     else:
         object_to_return = {
             "data": data,
             "status": status
         }
         return object_to_return
