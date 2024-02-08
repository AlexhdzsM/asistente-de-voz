import pyttsx3
import speech_recognition as sr
import pywhatkit
import yfinance as yf
import pyjokes
import webbrowser
import datetime
import wikipedia

#escuchar microfono y devolver el audio como texto
def audio_a_texto():
    #Almacenar recognizer en variable
    r = sr.Recognizer()

    #configurar microfono
    with sr.Microphone() as origen:

        #tiempo de espera

        r.pause_threshold = 0.8

        #informar que comenzo grabacion
        print("Ya puedes hablar")

        #Guardar audio
        audio = r.listen(origen)

        try:
            #Buscar en google lo escuchado
            pedido = r.recognize_google(audio, language = "es-mx")

            #Prueba de que se pudo ingresar

            print("Dijiste: "+ pedido)

            #devolver pedido

            return pedido
        
        #En caso de que no se entienda el audio
        except sr.UnknownValueError:

            #Prueba de que no comprendio audio
            print("No se entendio")


            #devolver error

            return "sigo esperando"
        
        #En caso de no resolver el pedido

        except sr.RequestError:
            #Prueba de que no comprendio audio
            print("No se entendio")

            #devolver error

            return "sigo esperando"
        
        #Error inesperado

        except:
            #Prueba de que no comprendio audio
            print("No hay servicio")

            #devolver error

            return "sigo esperando"
        


#Funcion para que asistente hable
        
def hablar(mensaje):

    #Encender el motor pyttsx3

    engine = pyttsx3.init()

    #pronunciar mensaje
    engine.say(mensaje)
    engine.runAndWait()



#informar dia
def pedir_dia():
    #Crear variable con datos de hoy
    dia = datetime.date.today()
    print(dia)

    #Crear variable de dia de la semana
    dia_semana = dia.weekday()
    print(dia_semana)
        

    #diccionario de dias
    calendario = {0:"Lunes",
                  1:"Martes",
                  2:"Miércoles",
                  3:"Jueves",
                  4:"Viernes",
                  5:"Sábado",
                  6:"Domingo"}
        
    #Decir el dia
    hablar(f"Hoy es {calendario[dia_semana]}")




#Informar hora

def pedir_hora():
    #Crear variable con datos de hora

    hora = datetime.datetime.now()
    hora = f"En este momento son las {hora.hour} horas con {hora.minute} minutos y {hora.second} segundos"
    
    #Decir la hora
    hablar(hora)


#Saludo inicial
    
def saludo_inicial():

    #crear variable de hora
    hora = datetime.datetime.now()
    if hora.hour < 6 or hora.hour>20:
        momento = "Buenas noches"
    elif hora.hour >= 6 and hora.hour < 13:
        momento = "Buen día"
    else:
        momento = "Buenas tardes"

    #Decir el saludo
    hablar(f"{momento}, soy el asistente Lika, en que te puedo ayudar?")

#Funcion central del asistente
    
def peticion():

    #Activar saludo inicial
    saludo_inicial()

    #Variable de corte
    comenzar = True

    #loop principal
    while comenzar:

        #activar micro y guardar pedido en string
        pedido = audio_a_texto().lower()

        if ('abrir youtube') in pedido:
            hablar("okey, abriendo youtube")
            webbrowser.open("https://www.youtube.com")
            continue
        elif ("abrir navegador") in pedido:
            hablar("Abriendo navegador")
            webbrowser.open("https://www.google.com")
            continue

        elif "qué día es" in pedido:
            pedir_dia()
            continue

        elif "qué hora es" in pedido:
            pedir_hora()
            continue

        elif "busca en wikipedia" in pedido:
            hablar("Buscando en wikipedia")
            pedido = pedido.replace("busca en wikipedia", "")
            wikipedia.set_lang("es")
            resultado = wikipedia.summary(pedido, sentences=1)
            hablar("Encontré esto en wikipedia:")
            hablar(resultado)
            continue

        elif "busca en internet" in pedido:
            hablar("buscando")
            pedido = pedido.replace("busca en internet", "")
            pywhatkit.search(pedido)
            hablar("Esto es lo que he encontrado")
            continue

        elif "reproduce" in pedido:
            hablar("okey, ya lo reproduzco")
            pywhatkit.playonyt(pedido)
            continue

        elif "chiste" in pedido:
            hablar(pyjokes.get_joke("es"))
            continue
        elif "precio de las acciones" in pedido:
            accion = pedido.split("de")[-1].strip()
            cartera = {"apple":"APPL",
                       "amazon":"AMZN",
                       "google":"GOOGL"}
            try:
                accion_buscada = cartera[accion]
                accion_buscada = yf.Ticker(accion_buscada)
                presio_actual = accion_buscada.info["regularMarketPrice"]
                hablar(f"La encontré, el precio de {accion} es {presio_actual}")
                continue
            except:
                hablar("Perdón, no pude encontrarla")
                continue

        elif "adiós" in pedido:
            hablar("adiós, llámame si me necesitas")
            break
        


peticion()