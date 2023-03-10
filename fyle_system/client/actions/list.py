import json 
class List():
    def execute(self,connection_pool,*arg,**kwargs):
        message = {
            "action":"list",
            "payload":{
            "type":"files",
            "user":kwargs["user"]
        }}
        connection_pool["ORQUESTER"].send_multipart([json.dumps(message).encode("utf-8")])
        response = connection_pool["ORQUESTER"].recv_multipart()
        print(f"listing files {response[0].decode('utf-8')}")