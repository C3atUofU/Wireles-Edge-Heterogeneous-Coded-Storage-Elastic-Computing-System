import selectors
import socket
import pickle
import numpy as np
import types
isImported = True

def client(data,host):
    
    keep_running = True
    datasend = pickle.dumps(data)   			# Searalizes the object 'data' and returns the bytes of the object
    port = 65432    
    
    sel = selectors.DefaultSelector()			# Waits for I/O readiness on file objects
    
    server_addr = (host, port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_addr) #.connect_ex()
    sock.setblocking(0) # vs False
    sel.register(sock, selectors.EVENT_WRITE)

    while keep_running:
        #print('waiting for connection')
        for key, mask in sel.select(timeout=None): #changed from 1 to None 11Nov
            conn = key.fileobj

        totalsent = 0
        while len(datasend):
            sent = conn.send(datasend)
            totalsent += sent
            datasend = datasend[sent:]
            #print('sending data',totalsent)

        print('data sent')
        keep_running = False
                
    #print('shutting down')
    sel.unregister(conn)
    conn.close()
    sel.close()
    #return portionSent

## Use for testing. Currently will not run with values in here.
if not isImported:
	host = '192.168.0.14' #!Wrong IP !
	tau = 2
	messageType = np.ones(784) #messageType = np.zeros(784)
	fn = np.zeros(tau)
	messageType, fn = NodeSvm.NodeSVM(messageType,N) # run SVM on node, N is nodenum !Wrong Notation!
	data = client(messageType,fn,host)
