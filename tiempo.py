#   Práctica 1: Análisis del tiempo
##  Realizado por María Mateos López y Andrea Sayago Butrón
# librerías
import os
import requests
import json
from datetime import datetime, timedelta, timezone
import pandas as pd

# %%
def EsEntero(num):
    try:
        k = int(num)
        return k
    except:
        return -1

# %%
# EsEntero("ssss")

# %%
def PintarMenu(listaOpc):
    seguir = True
    while(seguir):
        for i,opcion in enumerate(listaOpc):
             print(f"{i}.-{opcion}")
        cad = input("Inserte una opción: ")
        k = EsEntero(cad)
        if 0<=k and k< len(listaOpc):
            return k 
        elif k == -1:
            print("\nDebe insertar un número entero.\n")
        else:
            print(f"\nEl número debe estar entre 0 y {len(listaOpc)-1}.\n")

# %%
def ExisteApiKey():
    try:
        fich=open("./datos/keyAEMET.key","r")
        fich.close()
        return True
    except:
        return False

# %%
def ConvertirListaEstaciones():
    with open("./datos/estaciones.txt", "r") as f:
        lineas = [line.strip() for line in f]
    texto = "\n".join(lineas)
    # Quitar posibles caracteres raros
    texto = texto.strip()
    # Convertir a JSON
    datos = json.loads(texto)
    datos_ordenados = sorted(
        datos,
        key=lambda diccionario: diccionario['provincia']
    )
    return datos_ordenados

# %%
#ConvertirListaEstaciones()

# %%
def ConvertirListaObservaciones():
    with open("./datos/observacionactual.txt", "r") as f:
        lineas = [line.strip() for line in f]
    texto = "\n".join(lineas)
    # Quitar posibles caracteres raros
    texto = texto.strip()
    # Convertir a JSON
    datos = json.loads(texto)
    datos_ordenados = sorted(
        datos,
        key=lambda diccionario: diccionario['idema']
    )
    return datos_ordenados

# %%
#ConvertirListaObservaciones()

# %%
def GuardarDatos(apikey, url):
    querystring = {"api_key":apikey}
    headers = {'cache-control': "no-cache"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    
    dic1=json.loads(response.text)
    dic1['datos'] # contiene la dirección web a la que nos tenemos que conectar

    #nos conectamos a la anterior dirección web y pintamos su respuesta
    r2 = requests.request("GET", dic1['datos'], headers=headers, params=querystring)
    return r2.text

# %%
# 1 GUARDAR API KEY

def Guardar_API_key():
    API_key=input("Introduce tu API key de AEMET: \n").strip() #input recibe lo que se escribe, strip elimina espacios alante y atrás
    carpeta="datos/"
    os.makedirs(carpeta, exist_ok=True) # Crea carpeta si no existe 
    ruta_archivo = os.path.join(carpeta, "keyAEMET.key") #Construye ruta de archivo donde guardamos apikey
    with open(ruta_archivo, "w") as f: #Abre archivo en modo escritura w(si existe, borra lo que tiene y escribe la apikey; si no existe, lo crea y escribe la apikey)con with el archivo se cierra al terminar
        f.write(API_key) #Escribe apikey en el archivo
    print(f"Tu API key ha sido guardada correctamente en {ruta_archivo}")


# %%
# 2 MOSTRAR EL LISTADO DE ESTACIONES POR PROVINCIA

def GuardarEstacionesProvinciaPrimeraVez(apikey):
    url = "https://opendata.aemet.es/opendata/api/valores/climatologicos/inventarioestaciones/todasestaciones"
    querystring = {"api_key":apikey}
    headers = {'cache-control': "no-cache"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    
    dic1=json.loads(response.text)
    dic1['datos'] # contiene la dirección web a la que nos tenemos que conectar

    #nos conectamos a la anterior dirección web y pintamos su respuesta
    r2 = requests.request("GET", dic1['datos'], headers=headers, params=querystring)
    return r2.text

# %%
def MostrarProvincias(listadic):
    listaprovincias = []
    listaprovincias.append(listadic[0]['provincia'])
    print(f'\n{1} - {listaprovincias[0]}')
    i = 1
    aux = 0
    
    while i<len(listadic):
        if listadic[i]['provincia'] == listaprovincias[aux]:
            i = i+1
        else:
            listaprovincias.append(listadic[i]['provincia'])
            aux = aux + 1
            print(f'{aux+1} - {listaprovincias[aux]}')
            i = i+1
    return listaprovincias
        

# %%
def Provincias(listadic):
    listaprovincias = []
    listaprovincias.append(listadic[0]['provincia'])
    i = 1
    aux = 0
    
    while i<len(listadic):
        if listadic[i]['provincia'] == listaprovincias[aux]:
            i = i+1
        else:
            listaprovincias.append(listadic[i]['provincia'])
            aux = aux + 1
            i = i+1
    return listaprovincias

# %%
def MostrarEstacionesPorProvincia(listadic):
    listaprovincias = Provincias(listadic)
    estacionesporprovincia = [[] for _ in range(len(listaprovincias))]
    j = 0
    for i in range(0,len(listaprovincias)-1):
        print(f"ESTACIONES DE {listaprovincias[i]}:")
        while listaprovincias[i] == listadic[j]["provincia"]:
            estacionesporprovincia[i].append(listadic[j]["nombre"])
            print(f"\t-{listadic[j]['nombre']}")
            j = j+1
    #return(estacionesporprovincia)

# %%
# 3 Mostrar datos meteorológicos de una provincia actual

# %%
def Datos_Metereologicos_12h_AEMET(idema):

    # Comprobar si existe la API key usando la función común
    if not ExisteApiKey():
        print("No se ha encontrado la API key. Por favor, introdúcela primero (opción 1 del menú).")
        return

    # Leer la API key
    with open("./datos/keyAEMET.key", "r") as fich:
        api_key = fich.read().strip()

    # Llamada a la API para obtener la URL de los datos
    url = f"https://opendata.aemet.es/opendata/api/observacion/convencional/datos/estacion/{idema}"
    headers = {"api_key": api_key}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data_api = response.json()
    except Exception as e:
        print("Error al obtener los datos de la API:", e)
        return

    # Obtener la URL real de los datos
    if 'datos' not in data_api:
        print("Error en la respuesta de la API AEMET:")
        print(data_api.get('descripcion', 'Error desconocido'))
        return

    datos_url = data_api['datos']

    try:
        response_datos = requests.get(datos_url)
        response_datos.raise_for_status()
        observaciones = response_datos.json()
    except Exception as e:
        print("Error al descargar los datos meteorológicos:", e)
        return

    # Filtrar las últimas 12 horas
    now = datetime.now(timezone.utc)
    last_12h = now - timedelta(hours=12)

    ultimas_12h = []
    for obs in observaciones:
        try:
            fecha_obs = datetime.strptime(obs['fint'], "%Y-%m-%dT%H:%M:%S%z")
            if fecha_obs >= last_12h:
                ultimas_12h.append(obs)
        except:
            continue

    # Mostrar resultados
    print("\n\t\t=== DATOS METEOROLÓGICOS DE LAS ÚLTIMAS 12 HORAS ===")
    if not ultimas_12h:
        print("No hay observaciones en las últimas 12 horas.")
    else:
        for obs in ultimas_12h:
            print(f"Fecha: {obs['fint']}")
            print(f"Temperatura: {obs.get('ta', 'N/A')} °C")
            print(f"Humedad: {obs.get('hr', 'N/A')} %")
            print(f"Precipitación: {obs.get('prec', 'N/A')} mm")
            print(f"Viento: {obs.get('vv', 'N/A')} km/h, dirección: {obs.get('dv', 'N/A')}")
            print(f"Presión: {obs.get('pres', 'N/A')} hPa")
            print("-" * 40)

# %%
# 3 CONSULTAR DATOS ACTUALES DE UNA ESTACIÓN
def Elegir_provincia_estacion(listaprovincias, listadic):
    # Elegir provincia
    while True:
        try:
            op = int(input("\nElige una provincia: ")) #muestra mensaje y espera a que escriba,concierte a entero
            if 1 <= op <= len(listaprovincias): #para que el usuario ponga un nuemro de la lista
                provincia_elegida = listaprovincias[op - 1] #pues el 1 sera el 0 en la lista
                break
            else:
                print("Número fuera de rango.")
        except:
            print("Introduce un número válido.")

    # Filtrar estaciones de la provincia elegida
    estaciones = [x for x in listadic if x['provincia'] == provincia_elegida]#nueva lista donde vamos a guardadr solo las estaciones de la provincia elegida

    # Mostrar estaciones
    print(f"\n\t\t=== ESTACIONES EN {provincia_elegida} ===")
    for i, est in enumerate(estaciones, 1): #muestra la lista estaciones enumerada
        print(f"{i}. {est['nombre']}")

    # Elegir estación
    while True:
        try:
            op2 = int(input("\nElige una estación: "))
            if 1 <= op2 <= len(estaciones):
                estacion_elegida = estaciones[op2 - 1]
                break
            else:
                print("Número fuera de rango.")
        except:
            print("Introduce un número válido.")

    # Mostrar datos de la estación elegida
    idema = estacion_elegida['indicativo']
    print("\n\t\t=== DATOS ELEGIDOS ===")
    print(f"Provincia:      {estacion_elegida['provincia']}")
    print(f"Estación:       {estacion_elegida['nombre']}")
    print(f"Idema:          {estacion_elegida['indicativo']}")
    Datos_Metereologicos_12h_AEMET(idema)

# %%
#datos_ordenados = ConvertirListaEstaciones()
#MostrarEstacionesPorProvincia(datos_ordenados)

# %%
def QuitarVacios(lista):
    return [x for x in lista if x]

# %%
def MinimaLongitud(lista):
    listadelong = []
    for i,_ in enumerate(lista):
        if lista[i] != []:
            listadelong.append(len(lista[i]))
    return min(listadelong)

# %%
def HallarMedias(lista):
    listamedia = []
    lonlista = len(lista)
    minimalon = MinimaLongitud(lista)
    for i in range(0,minimalon):
        t = 0
        for est in lista:
            if  est != [] and est[i] != None:
                t = t + est[i]
            elif i == 0:
                lonlista = lonlista - 1
        listamedia.append(t/lonlista)
    return listamedia

# %%
import matplotlib.pyplot as plt

def GraficarDatos(datos,parametro,unidades):

    ejeY1 = datos 
    ejeX1 = [f"{x}:00" for x in range(len(ejeY1))] 
        
    fig, ax = plt.subplots(figsize=(8, 5)) 

    ax.plot(ejeX1, ejeY1, 
            marker='o',         
            linestyle='-',      
            color='#34495e')   
    
    ax.set_title(f"Gráfica de {parametro}", 
                 fontsize=14, 
                 fontweight='bold')
    ax.set_ylabel(f"{parametro} ({unidades})", 
                  fontsize=12)
    ax.set_xlabel(f"Hora", 
                  fontsize=12)

    ax.grid(True, linestyle='--', alpha=0.6) 
    
    plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout() 
    
    plt.show()  

# %%
#GraficarDatos([10.2,13.6,16.3,11.7],"temperatura","ºC")

# %%
# 4 CALCULAR MEDIAS DE VALORES DE ESTACIONES POR PROVINCIA

def CalcularMedias(listadic, apikey):
    listaprovincias = MostrarProvincias(listadic)
    seguir = True
    
    while seguir:
        n = input("\nElija una de las provincia (indique el número): ")
        k = EsEntero(n)
        if 0<=k and k<= 54:
            seguir = False
        elif k == -1:
            print("Debe insertar un número entero.")
        else:
            print("El número debe estar entre 1 y 54.")
    provincia = listaprovincias[k-1]
    print(f"\nProvincia seleccionada: {provincia}\n")
    
    i = 0
    listaestaciones = []
    indicativos = []
    
    for estacion in listadic:
        if estacion.get("provincia") == provincia:
            listaestaciones.append({
                "estacion": estacion.get("nombre"),
                "indicativo": estacion.get("indicativo")
            })
            indicativos.append(estacion.get("indicativo"))
    
    dicindicativoindice = {
        indicativo: idx for idx, indicativo in enumerate(indicativos)
    }
    
    with open("./datos/observacionactual.txt", "w") as fich:
        fich.write(GuardarDatos(apikey,"https://opendata.aemet.es/opendata/api/observacion/convencional/todas"))
    fich.close()
    
    lista_dic_observaciones = ConvertirListaObservaciones()
    
    if not lista_dic_observaciones:
        print("[INFO] No se encontraron datos de observación para procesar.")
        return None
    
    fechaprimerahora = lista_dic_observaciones[0]["fint"]
    num_estaciones = len(listaestaciones)
    temperatura = [[] for _ in range(num_estaciones)]
    humedadre = [[] for _ in range(num_estaciones)]
    pres = [[] for _ in range(num_estaciones)]
    preci = [[] for _ in range(num_estaciones)]
    vv = [[] for _ in range(num_estaciones)]
    rv = [[] for _ in range(num_estaciones)]
    
    estacionescondatos = set()
    
    for observacion in lista_dic_observaciones:
        idema = observacion.get("idema")
        if idema in dicindicativoindice:
            indice = dicindicativoindice[idema]
            estacionescondatos.add(idema)
            temperatura[indice].append(observacion.get("ta"))
            humedadre[indice].append(observacion.get("hr"))
            pres[indice].append(observacion.get("pres"))
            preci[indice].append(observacion.get("prec"))
            vv[indice].append(observacion.get("vv"))
            rv[indice].append(observacion.get("vmax"))
    
    for estacion in listaestaciones:
        if not estacion["indicativo"] in estacionescondatos: 
            print(f"[INFO] Estación {estacion['indicativo']} ({estacion['estacion']}) no tuvo observaciones en las últimas 12 horas.")
    input("Presiona Enter para continuar...")
    print("[INFO] En las últimas 12 horas no se han recogido los siguientes datos de las siguientes estaciones:")
    for estacion in estacionescondatos:
        indice = dicindicativoindice[estacion]
        print(f"\tEstación: {listaestaciones[indice]['estacion']}")
        if temperatura[indice][0] == None:
            print("\t\t- Faltan las temperaturas.")
        if humedadre[indice][0] == None:
            print("\t\t- Faltan las humedades.")
        if pres[indice][0] == None:
            print("\t\t- Faltan las presiones.")
        if preci[indice][0] == None:
            print("\t\t- Faltan las precipitaciones.")
        if vv[indice][0] == None:
            print("\t\t- Faltan las velocidades del viento.")
        if rv[indice][0] == None:
            print("\t\t- Faltan las rachas de viento.") 
    input("Presiona Enter para continuar...")
    print("\n\t\t=== RESUMEN DE VALORES MEDIOS EN LAS ÚLTIMAS 12 HORAS ===")
    print("\t\t----------------------------------------------------------\n")
    
    print(f"Provincia: {provincia} (últimas 12 horas)")
    print(f"Número de estaciones: {len(listaestaciones)}\n")
    
    print(f"Temperatura media: {round(sum(HallarMedias(temperatura))/len(HallarMedias(temperatura)),2)} ºC")
    print(f"Humedad relativa media: {round(sum(HallarMedias(humedadre))/len(HallarMedias(humedadre)),2)} %")
    print(f"Presión media: {round(sum(HallarMedias(pres))/len(HallarMedias(pres)),2)} hPa")
    print(f"Precipitación media: {round(sum(HallarMedias(preci))/len(HallarMedias(preci)),2)} mm")
    print(f"Velocidad del viento media: {round(sum(HallarMedias(vv))/len(HallarMedias(vv)),2)} m/s")
    print(f"Rachas de viento media: {round(sum(HallarMedias(rv))/len(HallarMedias(rv)),2)} m/s\n")
    input("Presiona Enter para continuar...")
    seguir = True
    while seguir:
        listaOpciones = ["Salir",
                        "Temperatura",
                        "Humedad relativa",
                        "Presión", 
                        "Precipitación",
                        "Velocidad del viento",
                        "Rachas de viento"]
        print("¿Quiere graficar algún valor medio a lo largo de las últimas 12 horas?\n")
        k = PintarMenu(listaOpciones)
        
        match k:
            case 0:
                print("\nSaliendo...\n")
                seguir = False
            case 1:
                GraficarDatos(HallarMedias(temperatura),"temperatura","ºC")
            case 2:
                GraficarDatos(HallarMedias(humedadre),"humedad relativa","%")
            case 3:
                GraficarDatos(HallarMedias(pres),"presión","hPa")
            case 4:
                GraficarDatos(HallarMedias(preci),"precipitación","mm")
            case 5:
                GraficarDatos(HallarMedias(vv),"velocidad del viento","m/s")
            case 6:
                GraficarDatos(HallarMedias(rv),"rachas de viento","m/s")    
    
    

# %%
#5 CONSULTRAR PREDICCIONES METEREOLÓGICAS DE MUNICIPIOS
def Asegurar_Diccionario_Municipios():
    ruta = "./datos/diccionario24.xlsx"
    url = "https://www.ine.es/daco/daco42/codmun/diccionario24.xlsx"

    if not os.path.exists("./datos"):
        os.mkdir("./datos")

    if os.path.exists(ruta):
        return True

    print("Descargando diccionario de municipios del INE...")
    try:
        r = requests.get(url)
        r.raise_for_status()
        with open(ruta, "wb") as f:
            f.write(r.content)
        print("Diccionario descargado correctamente.")
        return True
    except Exception as e:
        print("Error al descargar el diccionario de municipios:")
        print(e)
        return False


# %%
def Leer_Diccionario_Municipios():
    if not Asegurar_Diccionario_Municipios():
        return None

    try:
        columnas = ["CODAUTO", "CPRO", "CMUN", "DC", "NOMBRE"]
        df = pd.read_excel("./datos/diccionario24.xlsx", header=0, names=columnas)

        df = df[df["CPRO"].apply(lambda x: str(x).isdigit())]
        df = df[df["CMUN"].apply(lambda x: str(x).isdigit())]

        df["CPRO"] = df["CPRO"].astype(int)
        df["CMUN"] = df["CMUN"].astype(int)

        return df
    except Exception as e:
        print("Error al leer el fichero diccionario24.xlsx")
        print(e)
        return None

# %%
codigos_provincias = {
    1: "Álava", 
    2: "Albacete", 
    3: "Alicante", 
    4: "Almería",
    5: "Ávila", 
    6: "Badajoz", 
    7: "Islas Baleares", 
    8: "Barcelona",
    9: "Burgos", 
    10: "Cáceres", 
    11: "Cádiz", 
    12: "Castellón",
    13: "Ciudad Real", 
    14: "Córdoba", 
    15: "A Coruña", 
    16: "Cuenca",
    17: "Girona", 
    18: "Granada", 
    19: "Guadalajara", 
    20: "Guipúzcoa",
    21: "Huelva", 
    22: "Huesca", 
    23: "Jaén", 
    24: "León", 
    25: "Lleida",
    26: "La Rioja", 
    27: "Lugo", 
    28: "Madrid", 
    29: "Málaga", 
    30: "Murcia",
    31: "Navarra", 
    32: "Ourense", 
    33: "Asturias", 
    34: "Palencia", 
    35: "Las Palmas",
    36: "Pontevedra", 
    37: "Salamanca", 
    38: "Santa Cruz de Tenerife", 
    39: "Cantabria",
    40: "Segovia", 
    41: "Sevilla", 
    42: "Soria", 
    43: "Tarragona", 
    44: "Teruel",
    45: "Toledo", 
    46: "Valencia", 
    47: "Valladolid", 
    48: "Vizcaya", 
    49: "Zamora",
    50: "Zaragoza", 
    51: "Ceuta", 
    52: "Melilla"
}

# %%
def Mostrar_Provincias_Municipios(df):
    provincias_cod = sorted(df["CPRO"].unique())
    print("\nListado de provincias:\n")
    for i, cod in enumerate(provincias_cod):
        nombre = codigos_provincias.get(cod, f"Provincia {cod}")
        print(f"{i} - {nombre} ({cod-1})")
    return provincias_cod

# %%
def Elegir_Provincia_Municipios(df):
    provincias = Mostrar_Provincias_Municipios(df)
    while True:
        try:
            op = int(input("Elige una provincia(pon el número): "))
            if 0 <= op < len(provincias):
                return provincias[op] 
            else:
                print("Opción incorrecta")
        except:
            print("Debes introducir un número")
# %%
def Mostrar_Municipios_Provincia(df, provincia):
    municipios = df[df["CPRO"] == provincia].sort_values("NOMBRE")
    print("\nListado de municipios:\n")
    for _, fila in municipios.iterrows():
        print(f"{fila['NOMBRE']} (INE: {fila['CMUN']})")
    return municipios

# %%
def Elegir_Municipio(df, provincia):
    municipios = df[df["CPRO"] == provincia]

    while True:
        cod = input("Introduce el código INE del municipio: ")

        if cod.isdigit() and int(cod) in municipios["CMUN"].values:
            cmun = int(cod)
            cpro = provincia
            codigo_municipio = cpro * 1000 + cmun

            return codigo_municipio
        else:
            print("Código de municipio incorrecto")
# %%
def Consultar_Prediccion_Municipio(cod_municipio):
    if not ExisteApiKey():
        print("Debes introducir primero la API key (Pulsa 1).")
        return

    with open("./datos/keyAEMET.key", "r") as fich:
        api_key = fich.read().strip()

    url = f"https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/diaria/{cod_municipio}"
    headers = {"api_key": api_key}

    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        data_api = r.json()
    except Exception as e:
        print("Error al conectar con AEMET:", e)
        return

    if "datos" not in data_api:
        print("Error en la respuesta de AEMET:")
        print(data_api.get("descripcion", "Error desconocido"))
        return

    try:
        r2 = requests.get(data_api["datos"])
        r2.raise_for_status()
        pred = r2.json()
    except Exception as e:
        print("Error al descargar la predicción:", e)
        return

    print("\n=== PREDICCIÓN METEOROLÓGICA ===\n")

    dias = pred[0]["prediccion"]["dia"]
    for d in dias:
        print(f"Fecha: {d['fecha']}")

        tmax = d["temperatura"]["maxima"]
        tmin = d["temperatura"]["minima"]
        print(f"Temperatura máxima: {tmax} °C")
        print(f"Temperatura mínima: {tmin} °C")
        print(f"Temperatura media: {(tmax + tmin) / 2:.1f} °C")

        print(f"Humedad máxima: {d['humedadRelativa']['maxima']} %")
        print(f"Humedad mínima: {d['humedadRelativa']['minima']} %")

        if "probPrecipitacion" in d and d["probPrecipitacion"]:
            print(f"Prob. precipitación: {d['probPrecipitacion'][0]['value']} %")

        if "estadoCielo" in d and d["estadoCielo"]:
            print(f"Cielo: {d['estadoCielo'][0]['descripcion']}")

        if "viento" in d and d["viento"]:
            v = d["viento"][0]
            print(f"Viento: {v.get('velocidad', 'N/A')} km/h {v.get('direccion', '')}")

        print(f"Horas de sol: {d.get('horasSol', 'N/A')}")

        print(f"Índice UV: {d.get('uvMax', 'N/A')}")

        print("-" * 40)

# %%
#datos_ordenados = ConvertirListaEstaciones()
#apikey = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhbmRyZWEuc2F5YWdvYnV0cm9uQGFsdW0udWNhLmVzIiwianRpIjoiNTNlYzllY2YtZWY1MS00ZmQ2LTk3MzktNDY1NzJmMDY4OGRmIiwiaXNzIjoiQUVNRVQiLCJpYXQiOjE3NjI3NzE4OTMsInVzZXJJZCI6IjUzZWM5ZWNmLWVmNTEtNGZkNi05NzM5LTQ2NTcyZjA2ODhkZiIsInJvbGUiOiIifQ.2V2S519YdRnGaXy9WP55AgPtB_qI7UmkZ3bzRhWmaLI"
#CalcularMedias(datos_ordenados,apikey)

# %%
#apikey = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhbmRyZWEuc2F5YWdvYnV0cm9uQGFsdW0udWNhLmVzIiwianRpIjoiNTNlYzllY2YtZWY1MS00ZmQ2LTk3MzktNDY1NzJmMDY4OGRmIiwiaXNzIjoiQUVNRVQiLCJpYXQiOjE3NjI3NzE4OTMsInVzZXJJZCI6IjUzZWM5ZWNmLWVmNTEtNGZkNi05NzM5LTQ2NTcyZjA2ODhkZiIsInJvbGUiOiIifQ.2V2S519YdRnGaXy9WP55AgPtB_qI7UmkZ3bzRhWmaLI"
#print(MostrarEstacionesProvinciaPrimeraVez(apikey))

# %%
def main():
    print("---- P R Á C T I C A  1 : A N Á L I S I S  D E L  T I E M P O ----\n\nTrabajo realizado por : \n\tMaría Mateos López \n\tAndrea Sayago Butrón")
    print("\n╔══════════════════════════════════╗")
    print("║              MENÚ                ║")
    print("╚══════════════════════════════════╝")
    seguir = True
    apikey = 0
    #apikey = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhbmRyZWEuc2F5YWdvYnV0cm9uQGFsdW0udWNhLmVzIiwianRpIjoiNTNlYzllY2YtZWY1MS00ZmQ2LTk3MzktNDY1NzJmMDY4OGRmIiwiaXNzIjoiQUVNRVQiLCJpYXQiOjE3NjI3NzE4OTMsInVzZXJJZCI6IjUzZWM5ZWNmLWVmNTEtNGZkNi05NzM5LTQ2NTcyZjA2ODhkZiIsInJvbGUiOiIifQ.2V2S519YdRnGaXy9WP55AgPtB_qI7UmkZ3bzRhWmaLI"
    while seguir:
        listaOpciones = ["Salir",
                        "Introducir API key",
                        "Mostrar el listado de estaciones por provincia",
                        "Consultar datos actuales de una estación", 
                        "Calcular medias de valores de estaciones por provincia",
                        "Consultar predicciones meteorológicas de municipios"]
        k = PintarMenu(listaOpciones)
        print(f"\nOpción elegida: {listaOpciones[k]}\n")
        match k:
            case 0:
                print("\nSaliendo...\n")
                seguir = False
            case 1:
                if ExisteApiKey():
                    seguir2 = True
                    while seguir2:
                        x = input("Ya existe una API key, ¿quieres volver a introducirla?\n 0 - No\n1 - Sí\n")
                        try:
                            x = int(x)
                            if x:
                                Guardar_API_key()
                                seguir2 = False
                            elif x == 0:
                                seguir2 = False
                            else:
                                print("Debes poner 0 o 1")
                        except:
                            print("Debes poner 0 o 1")
                else: 
                    Guardar_API_key()
            case 2:
                if ExisteApiKey():
                    fich = open("./datos/keyAEMET.key","r")
                    apikey = fich.read()
                    fich.close()
                    try:
                        fich=open("./datos/estaciones.txt","r")
                        fich.close()
                        datos_ordenados = ConvertirListaEstaciones()
                        MostrarEstacionesPorProvincia()
                    except:
                        with open("./datos/estaciones.txt", "w") as fich:
                            fich.write(GuardarEstacionesProvinciaPrimeraVez(apikey))
                            fich.close()
                            datos_ordenados = ConvertirListaEstaciones()
                            MostrarEstacionesPorProvincia(datos_ordenados)
                else:
                    print("Debes introducir primero la API key (opción 1).")
                
            case 3:
                datos_ordenados = ConvertirListaEstaciones()
                listaprovincias = MostrarProvincias(datos_ordenados)
                Elegir_provincia_estacion(listaprovincias, datos_ordenados)
            case 4:
                if ExisteApiKey():
                    fich = open("./datos/keyAEMET.key","r")
                    apikey = fich.read()
                    fich.close()
                    datos_ordenados = ConvertirListaEstaciones()
                    CalcularMedias(datos_ordenados,apikey)
                else:
                    print("Debes introducir primero la API key (opción 1).")
            case 5:
                df =Leer_Diccionario_Municipios()
                if df is not None:
                    provincia = Elegir_Provincia_Municipios(df)
                    Mostrar_Municipios_Provincia(df, provincia)
                    cod_municipio = Elegir_Municipio(df, provincia)
                    Consultar_Prediccion_Municipio(cod_municipio)
            

# %%
if __name__ == '__main__':
    main()

# %%



