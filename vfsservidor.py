import zmq
import os
import base64
context = zmq.Context()
s= context.socket(zmq.REP)
s.bind('tcp://*:8001') #protocol://*:puerto     * significa:

def enviar(username,orden,nombreArchivo,direccion):
    f = open(direccion, 'rb')# R lee el archivo en modo binario B
    while True:
        print('enviando...')
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


def recibir(orden):
    #tamanoArchivo=os.path.getsize('C:\\Users\\Sofia\\Documents\\utp\\arquitectura\\semana5\\'+orden[2])
    while True:
        print("recibiendo...")
        image_64_decode = base64.decodebytes(orden[3])
        if image_64_decode==b'0':
            s.send_multipart(['termino'.encode()])
            break
        else:
            image_result = open('C:\\Users\\Sofia\\Documents\\utp\\arquitectura\\semana5\\servidor\\'+orden[0]+'\\'+orden[2], 'ab')#Cambiar con respecto al usuario,escritura y binario
            image_result.write(image_64_decode)
            size_file = os.path.getsize('C:\\Users\\Sofia\\Documents\\utp\\arquitectura\\semana5\\servidor\\'+orden[0]+'\\'+orden[2])
            mensaje='documento cargado'+ str(size_file)
            #print(size_file,tamanoArchivo)
            print(size_file)
            s.send_multipart([mensaje.encode()])
            m=s.recv_multipart()
            orden=[m[0].decode("utf-8"),m[1].decode("utf-8"),m[2].decode("utf-8"),m[3]]

while True:
    print("calculando...")
    m=s.recv_multipart()
    orden=[m[0].decode("utf-8"),m[1].decode("utf-8"),m[2].decode("utf-8"),m[3]]
    if orden[1]=='upload':
        recibir(orden)
    if orden[1]=='download' or orden[1]=='downloadlink':
        enviar(orden[0],orden[1],orden[2],'C:\\Users\\Sofia\\Documents\\utp\\arquitectura\\semana5\\servidor\\'+orden[0]+'\\'+orden[2])
    if orden[1]=='sharelink':
        mensaje='C:\\Users\\Sofia\\Documents\\utp\\arquitectura\\semana5\\servidor\\'+orden[0]+'\\'+orden[2]
        s.send_multipart([mensaje.encode()])
    if orden[1]=='list':
        list = os.listdir("servidor/"+orden[0]) # dir is your directory path
        mensaje="archivos: "+ str(list)
        s.send_multipart([mensaje.encode()])
