'''
    # author: DANIEL
    # Servicios que se necesitan para actualizar e informar el valor del INPC
    # date: 03/05/2021
    # pip install python-decouple
'''
from decouple import config
import  smtplib

def enviar_correo(nombreMesINPC, currentINPC):
    try:
        message = 'INPC ACTUALIZADO, QUE TENGAS UN BUEN DIA c: \n' + str(currentINPC)
        subject = 'INPC ' + nombreMesINPC
        message = 'Subject: {}\n\n{}'.format(subject, message)
        server = smtplib.SMTP(config('EMAIL_HOST'), config('EMAIL_PORT'))
        server.starttls()
        server.login(config('EMAIL_ADDRESS'), config('EMAIL_PASSWORD'))
        server.sendmail(config('EMAIL_ADDRESS'), config('EMAIL_ADDRESS_RECEIVER'), message)
        server.quit()
        print('EMAIL ENVIADO')
    except:
        print('ERROR AL ENVIAR EL EMAIL')

def status_correo():
    f = open(config('FILA_PATH'),'r')
    cadena = f.read()
    f.close()
    return cadena

def escribir_contenido_txt(cadena):
    f = open(config('FILA_PATH'),'w')
    f.write(cadena)
    f.close()
