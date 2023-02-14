import socket

def isConnected():
    try:
        # connect to the host -- tells us if the host is actually
        # reachable
        sock = socket.create_connection(("www.google.com", 80))
        if sock is not None:
            print('Internet connected......')
            sock.close
        return True
    except OSError:
        print("Internet not connected....")
    return False