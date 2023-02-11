import socket 
import threading
from predict import *
from funcs import *

data = pd.read_csv('Crop_recommendation.csv')
clases=data['label'].unique()


PORT = 5050
FORMAT = 'utf-8'
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

lcon= []
laddr= []
server= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    connected = True

    while connected:
     try:  
           #app sends meg in format /get/n/k/p/latitude/longitude/ph
           msg = conn.recv(1024).decode('utf-8')

           if msg.startswith("/get"):
               #getting requied features and city name from msg
               fea=getfeatures(msg)[0]
               city=getfeatures(msg)[1]
               #normalizing input recived with same variables to predict
               y=np.squeeze(model.predict(sc.transform(np.array(fea).reshape((1,7)))))
               #text to be shown in app
               pre=f'in {city} for temp {fea[3]}, precep {fea[-1]} and humidity{fea[-3]} {onehottoclass(y,clases)} are the most optimal crops'
               conn.send(pre.encode(FORMAT))
  
               
           else:
               connected= False

           

     except:
         connected= False
         
         lcon.remove(conn)
         laddr.remove(addr)

      


def start():
    server.listen()
    while 1:
        conn, addr = server.accept()
        lcon.append(conn)
        laddr.append(addr)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


print("starting........",SERVER)
start()
