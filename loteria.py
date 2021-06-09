import requests
from bs4 import BeautifulSoup

# obtener datos de la web <-------------------------------------------------------------------------------

URL = 'https://lotoluck.com/botes'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')

# listas almacenar info
list_concursos = []
list_fechas = []
list_premios = []

# busqueda de concursos
concursos = soup.find_all("span", "bj_nombre")

inicio = len('<span class="bj_nombre">')
for concur in concursos:
	final = len(str(concur)) - len("</span>")
	#print(str(concur)[inicio:final])
	list_concursos.append(str(concur)[inicio:final])

# busqueda de fechas
fechas = soup.find_all("div", "b_fecha", "<span>")

inicio = len('<div class="b_bote"><span> ')
for fecha in fechas:
	final = len(str(fecha)) - len("</span></div>")
	#print(str(fecha)[inicio:final])
	list_fechas.append(str(fecha)[inicio:final])


# busqueda de premios 
premios = soup.find_all("div", "b_bote", "<span>")

inicio = len('<div class="b_bote"><span>')
for resultado in premios:
	final = len(str(resultado)) - len("</span></div>")
	#print(str(resultado)[inicio:final])
	list_premios.append(str(resultado)[inicio:final])

# imprime elementos de las listas ordenados
#for n in range(len(list_premios)):
#	print (list_concursos[n], list_fechas[n], list_premios[n])

# calculos <-------------------------------------------------------------------------------

#premio = 400000 # premio
#eur_jugado = 20 # euros apostados

exento = 40000 # libre de impuestos
retencion = 0.2 # retencion de 40000 en adelante

participantes = 0 # participantes

def calcular_neto(exento, premio):
    neto = exento + (premio - exento)*(1-retencion)
    return neto

def calcular_impuestos(exento, premio):
    impuestos = (premio - exento)*(retencion)
    return impuestos

def premio_participes(participantes, exento, premio):
	if participantes == 1:
	    print("Premio neto: " + str(calcular_neto(exento, premio)))
	    print("Impuestos pagados " + str(calcular_impuestos(exento, premio)))
	else:
	    print("Premio neto total: " + str(calcular_neto(exento, premio)) 
	        + ". Impuestos totales: " + str(calcular_impuestos(exento, premio)))
	    print("Para cada uno de los " + str(participantes) + " participes:")
	    print("  -Premio neto: " + str(calcular_neto(exento, premio) / participantes))
	    print("  -Impuestos pagados: " + str(calcular_impuestos(exento, premio) / participantes))

# PREGUNTAR Y MOSTRAR INFO AL USUARIO<-------------------------------------------------------------------------------
# preguntar al usuario que premio y cuantos partices son
premio = input("¿Premio?: ") 
participantes = int(input("¿Participantes?: "))

info_premio = list_concursos.index(premio)

# imprimir el jeugo seleccionado: Euromillones
print(list_concursos[info_premio], "=> Fecha: ", list_fechas[info_premio], "Premio: ", list_premios[info_premio])
premio_participes(int(participantes), float(exento), float(list_premios[info_premio].replace(".","").replace(",",".")))
