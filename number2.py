# Quine McCluskey
# Stiven Castro Soto
# Tomas Castro Cacante

# Función que concatena todos los elementos dentro de una lista y retorna una nueva lista
def recorta(lista):
    elementos_recortados = []
    for sublista in lista:
        elementos_recortados.extend(lista[sublista])
    return elementos_recortados

# Función que convierte una cadena binaria con caracteres "-" en una lista de todas las combinaciones posibles de posiciones rellenas con ceros y unos
def buscaMinterminos(mt):
    guiones = mt.count('-')
    if guiones == 0:
        return [mt]
    opciones = [bin(i)[2:].zfill(guiones) for i in range(pow(2, guiones))]
    temporal = []
    for i in range(pow(2, guiones)):
        temporal2 = mt[:]
        indice = -1
        for j in opciones[0]:
            if indice != -1:
                indice += temporal2[indice+1:].find('-')+1
            else:
                indice = temporal2[indice+1:].find('-')
            temporal2 = temporal2[:indice] + j + temporal2[indice+1:]
        temporal.append(temporal2)
        opciones.pop(0)
    return temporal

# Función que compara dos listas de minterminos y devuelve información sobre sus diferencias
def diferencias(mt1, mt2):
    contador = 0
    indice = 0
    for i in range(len(mt1)):
        if mt1[i] != mt2[i]:
            indice = i
            contador += 1
            if contador > 1:
                return (False, -1)
    return (True, indice)

# Función que convierte una cadena binaria en variables y sus negaciones
def convertir(mintermino):
    var_formula = []
    for i in range(len(mintermino)):
        if mintermino[i] == '1':
            var_formula.append(chr(i + 65))  # CODIGO ASCII 65 = A, 66= B, 67 = C,...
        elif mintermino[i] == '0':
            var_formula.append(chr(i + 65) + "'")
    return var_formula

# Función que busca los implicantes únicos en una tabla representada como un diccionario
def buscar_implicantes_unicos(tabla):
    implicantes_unicos = []
    for i in tabla:
        if len(tabla[i]) == 1: # Único implicante en la columna
            if tabla[i][0] not in implicantes_unicos:
                implicantes_unicos.append(tabla[i][0])
    return implicantes_unicos

# Inicio del programa
print("\nQUINE MCCLUSKEY\n")
print("Ingrese los términos separados por un espacio. \n")
mt = [int(i) for i in input("Ingrese los mintérminos: ").strip().split()]
mt.sort() # Ordenamos los minterminos
minterminos = mt
max_minterm = len(bin(minterminos[-1])) - 2
grupos = {}
implicantes = set()

# Comenzamos la agrupación primaria
for minterm in minterminos:
    count = bin(minterm).count('1')
    minterm_str = bin(minterm)[2:].zfill(max_minterm)

    if count in grupos:
        grupos[count].append(minterm_str)
    else:
        grupos[count] = [minterm_str]
# Término de la agrupación primaria

# Proceso para crear las tablas y encontrar los implicantes primos
while True:
    temporal = grupos.copy()
    grupos = {}
    n = 0
    marcados = set()
    debo_parar = True
    lclaves = sorted(list(temporal.keys()))
    for i in range(len(lclaves) - 1):
        for j in temporal[lclaves[i]]:
            for k in temporal[lclaves[i+1]]:
                cambio = diferencias(j, k)
                if cambio[0]:
                    minterm_cambio = j[:cambio[1]] + '-' + j[cambio[1]+1:]
                    if n in grupos:
                        if minterm_cambio not in grupos[n]:
                            grupos[n].append(minterm_cambio)
                    else:
                        grupos[n] = [minterm_cambio]
                    debo_parar = False
                    marcados.add(j)
                    marcados.add(k)
        n += 1
    desmarcados_local = set(recorta(temporal)).difference(marcados)
    implicantes = implicantes.union(desmarcados_local)
    if debo_parar:
        break

tabla = {}
for i in implicantes:
    minterminos_mezclados = buscaMinterminos(i)
    for j in minterminos_mezclados:
        if j in tabla:
            if i not in tabla[j]:
                tabla[j].append(i)
        else:
            tabla[j] = [i]

# Búsqueda de implicantes únicos y compartidos en la tabla generada
implicantes_unicos = buscar_implicantes_unicos(tabla)

reducir_tabla = {}
for i in tabla:
    for j in implicantes_unicos:
        if j in tabla[i]:
            reducir_tabla[i] = tabla[i]

nueva_tabla = {}
for i in tabla:
    if i not in reducir_tabla:
        nueva_tabla[i] = tabla[i]

dos_marcas = []
for i in nueva_tabla:
    if len(nueva_tabla[i]) == 2:
        dos_marcas.append(int(i))
dos_marcas.sort()

# Función recursiva para marcar implicantes compartidos en la tabla
def marcar_todos(dos, tabla, confirmados):
    if len(tabla) > 0:
        dos.sort()
        temporal = set(dos)
        nueva_tabla = dict(tabla)
        for i in dos:
            opciones = tabla[str(i)]
            x = -1
            y = -1
            for j in tabla:
                if (opciones[0] in tabla[j]) and (str(i) != j):
                    x = j
                elif (opciones[1] in tabla[j]) and (str(i) != j):
                    y = j
            if int(x) == -1 and int(y) == -1:
                confirmados.add(opciones[0])
            elif int(x) == -1 and int(y) > 0:
                confirmados.add(opciones[1])
                nueva_tabla.pop(y)
            elif int(y) == -1 and int(x) > 0:
                confirmados.add(opciones[0])
                nueva_tabla.pop(x)
            elif len(tabla[str(x)]) > len(tabla[str(y)]):
                confirmados.add(opciones[0])
                nueva_tabla.pop(x)
            elif len(tabla[str(x)]) < len(tabla[str(y)]):
                confirmados.add(opciones[1])
                nueva_tabla.pop(y)
            temporal.discard(i)
            nueva_tabla.pop(str(i))
            marcar_todos(list(temporal), nueva_tabla, confirmados)

complemento = set()
marcar_todos(dos_marcas, nueva_tabla, complemento)

formula_final = list(complemento) + implicantes_unicos
formato_ecuacion = []
for i in range(len(formula_final)):
    formato_ecuacion.append(convertir(formula_final[i]))

# Impresión del resultado final
print("\nSOLUCION: \n")
for i in range(len(formato_ecuacion)):
    for j in formato_ecuacion[i]:
        print(j, end='')
    if i < len(formato_ecuacion) - 1:
        print(" + ", end='')    
print("\n")
