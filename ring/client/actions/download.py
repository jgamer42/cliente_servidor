import os
import io
import sys
import json
from dotenv import load_dotenv
load_dotenv()
utils_path:str=os.getenv("PROJECT_UTILS","")
if utils_path:
    sys.path.append(utils_path)
else:
    print(".env not configured killing the server")
    sys.exit(1)
from file_utils import read_file,write_file
from zmq_utils import get_send_socket
class Download:
    def execute(self,context,file:str,host:str,output:str,*args,**kwargs):
        chunks_to_find,_ = read_file(file)
        data_structure = json.loads(chunks_to_find)
        data_from_file = self.download_chunks(data_structure["chunks"],context,host)
        write_file(data_from_file,output)

    def download_chunks(self,chunks,context,host):
        data = io.BytesIO()
        for chunk in chunks.keys():
            known_host = host
            finded = False
            while not finded:
                message = {
                    "action":"download",
                    "payload":{
                        "file":chunks[chunk]
                    }
                }
                socket = get_send_socket(context,known_host)
                socket.send_multipart([json.dumps(message).encode("utf-8")])
                raw_response = socket.recv_multipart()
                status = json.loads(raw_response[0])
                finded = status["stored"]
                if finded:
                    chunk_aux = raw_response[1]
                else:
                    known_host = status["host"]
            data_from_chunk = chunk_aux
            data.write(data_from_chunk)
        return data.getvalue()