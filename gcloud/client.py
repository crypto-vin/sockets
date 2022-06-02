import socket            
s = socket.socket()        
port = 3389              
s.connect(('130.211.116.77', port))
print (s.recv(1024).decode())
s.close()