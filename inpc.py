'''
    # author: JOSE DANIEL
    # Script para obtener e informar el valor del INPC actual
    # date: 03/05/2021
'''
import Service
import requests
from bs4 import BeautifulSoup
from datetime import date
import pandas as pd

meses = ['ENERO','FEBRERO','MARZO','ABRIL','MAYO','JUNIO','JULIO','AGOSTO','SEPTIEMBRE','OCTUBRE','NOVIEMBRE','DICIEMBRE']
numeroDia = int(date.today().strftime('%d'))
numeroMes = int(date.today().strftime('%m'))

#metodos
def getINPC():
    URL = "https://www.elcontribuyente.mx/inpc/"
    try:
        page = requests.get(URL)
        soup = BeautifulSoup(page.content,'html.parser')
        allElements = soup.find_all('tbody')

        for element in allElements:
            listaValores = element.find_all('tr')
            if None in listaValores:
                continue
            listINPC = list(listaValores)

        cadena = str(listINPC[:1])
        stringTemp = cadena.replace('<td>','')
        stringTemp = stringTemp.replace('</td>',',')
        stringTemp = stringTemp.replace('[<tr>','')
        stringTemp = stringTemp.replace('</tr>]','')
        stringTemp = stringTemp.replace('<strong>','')
        stringTemp = stringTemp.replace('</strong>,','')
        listINPC = stringTemp.split(',')

        # sacamos el valor 2022
        listINPC.pop(0)

        datos = ['null'] * 12
        flag = 0
        for INPC in listINPC:
            datos[flag] = INPC
            flag+=1

        df = pd.DataFrame([datos],index=['2022'], columns = [meses])
        return df
    except:
        print('Hubo un error al intentar conectarse con el servidor')
        return 504

# EVALUACION
if numeroDia <= 15:
    dfINPC = getINPC()
    print('Obtener valor del INPC')
    print(dfINPC)
    if isinstance(dfINPC, pd.DataFrame):
        nombreMesINPC = meses[numeroMes-2]
        currentINPC = dfINPC.loc['2022', nombreMesINPC]
        if currentINPC.iloc[0] != 'null':
            #IF VERIFICAR SI EL EMAIL YA SE HA ENVIADO
            if Service.status_correo() != 'enviado':
                Service.enviar_correo(nombreMesINPC, currentINPC)
                Service.escribir_contenido_txt('enviado')
        else:
            Service.escribir_contenido_txt('no enviado')
            print('VALOR INPC NO ACTUALIZADO')
else:
    Service.escribir_contenido_txt('no enviado')
    print('INPC ACTUALIZADO'+'\n'+'BUEN DIA c:')
