import socket
import pickle
import time

start = time.time()

def master_client(host,data):
    #print('aggr_client_v1_3 start: %.2f'%(time.time()-start))
    host = host
    #data = data.astype('float16')
    port = 65432
    datasend = pickle.dumps(data)
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_addr = (host, port)
    s.connect(server_addr)
    total_sent = 0
    while len(datasend):
        sent = s.send(datasend)
        total_sent += sent
        datasend = datasend[sent:]
    #print('aggr_client_v1_3 end: %.2f'%(time.time()-start))
    s.close()
    
