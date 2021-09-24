import zmq #provee la comunicacion a traves de sockets (hulk)
import sys
import base64
import os
import json
from shasum import *
context = zmq.Context()#black box!!
link=' '
tamanoArchivo=0
llave=''
new_data={}
with open('op.json') as file:
     new_data = json.load(file) #cargo el archivo json
file.close()

def recibir(direccion,archivo):
    while True:
        print("recibiendo...")
        m=s.recv_multipart()
        orden=[m[0].decode("utf-8"),m[1].decode("utf-8"),m[2].decode("utf-8"),m[3]]
        image_64_decode = base64.decodebytes(orden[3])
        if image_64_decode==b'0':
            break
        else:
            image_result = open(direccion+archivo, 'ab')#Cambiar con respecto al usuario,escritura y binario
            image_result.write(image_64_decode)
            size_file = os.path.getsize(direccion+archivo)
            mensaje='documento cargado'+ str(size_file)
            #print(size_file,tamanoArchivo)
            print(size_file)
            s.send_multipart([mensaje.encode()])

def enviar(username,orden,nombreArchivo,direccion):
    f = open(direccion, 'rb')# R lee el archivo en modo binario B
    while True:
        archivoLeido = f.read(1024*1024)
        if not archivoLeido:
            image_64_encode = base64.encodebytes(b'0')
            s.send_multipart([username.encode(),orden.encode(),nombreArchivo.encode(),image_64_encode])
            break
        image_64_encode = base64.encodebytes(archivoLeido)
        s.send_multipart([username.encode(),orden.encode(),nombreArchivo.encode(),image_64_encode])
        respuesta=s.recv_multipart()
        print(respuesta)
    f.close()



#Crea un socket y lo conecta a traves del protocolo tcp con el equipo local en el puerto 8001
s = context.socket(zmq.REQ)
s.connect('tcp://localhost:8001')

username = sys.argv[1]
orden = sys.argv[2]
nombreArchivo = sys.argv[3]

if orden=='upload':
    direccion='C:\\Users\\Sofia\\Documents\\utp\\arquitectura\\semana5\\'+nombreArchivo
    llave=shasum('C:\\Users\\Sofia\\Documents\\utp\\arquitectura\\semana5\\'+nombreArchivo)
    if llave in new_data:
        print('ya esta el archivo')
    else:
        new_data[llave] = nombreArchivo  #agrego valores al nuevo diccionario
        with open('op.json','w') as file:
            json.dump(new_data,file)
        file.close()
        enviar(username,orden,nombreArchivo,direccion)
        respuesta=s.recv_multipart()
        print(respuesta)
else:
    if orden=='downloadlink':
        try:
            partes = nombreArchivo.split("\\")
            nombreUsuarioDueno=partes[8]
            link=partes[9]
            #tamanoArchivo=os.path.getsize(nombreArchivo)
            mensaje=' '
            print([nombreUsuarioDueno.encode(),orden.encode(),link.encode(),mensaje.encode()])
            s.send_multipart([nombreUsuarioDueno.encode(),orden.encode(),link.encode(),mensaje.encode()])
            recibir('C:\\Users\\Sofia\\Documents\\utp\\arquitectura\\semana5\\servidor\\'+username+'\\',link)
        except:
            print('no se ha cargado el archivo')
    if orden=='sharelink':
        mensaje=' '
        s.send_multipart([username.encode(),orden.encode(),nombreArchivo.encode(),mensaje.encode()])
        respuesta=s.recv_multipart()
        print(respuesta[0].decode("utf-8"))
    if orden=='download':
        try:
            #tamanoArchivo=os.path.getsize('C:\\Users\\Sofia\\Documents\\utp\\arquitectura\\semana5\\servidor\\'+username+'\\'+nombreArchivo)
            mensaje=' '
            s.send_multipart([username.encode(),orden.encode(),nombreArchivo.encode(),mensaje.encode()])
            recibir('C:\\Users\\Sofia\\Documents\\utp\\arquitectura\\semana5\\',nombreArchivo)
        except:
            print('no se ha cargado el archivo')
    if orden=='list':
        mensaje=' '
        s.send_multipart([username.encode(),orden.encode(),nombreArchivo.encode(),mensaje.encode()])
        respuesta=s.recv_multipart()
        print(respuesta[0].decode("utf-8"))
