import tkinter as tk
from tkinter import ttk  # Importa ttk para estilos mejorados
from tkinter import messagebox
from tabulate import tabulate

def recorta(lista):
    # Inicializa una lista vacía para almacenar elementos recortados.
    elementos_recortados = []
    
    # Itera a través de los elementos de la lista de entrada.
    for i in lista:
        # Extiende la lista 'elementos_recortados' con los elementos de 'lista[i]'.
        elementos_recortados.extend(lista[i])
    
    # Devuelve la lista 'elementos_recortados'.
    return elementos_recortados

def buscaMinterminos(mt):
    # Cuenta cuántos guiones tiene la cadena 'mt'.
    guiones = mt.count('-')
    
    # Si no hay guiones en 'mt', convierte 'mt' a decimal y devuelve en una lista.
    if guiones == 0:
        return [str(int(mt, 2))]
    
    # Crea una lista 'opciones' que contiene representaciones binarias de números con 'guiones' dígitos.
    opciones = [bin(i)[2:].zfill(guiones) for i in range(pow(2, guiones))]
    
    # Inicializa una lista temporal.
    temporal = []
    
    # Itera a través de las opciones binarias.
    for i in range(pow(2, guiones)):
        # Crea una copia de 'mt' llamada 'temporal2'.
        temporal2 = mt[:]
        
        # Inicializa una variable 'indice' en -1.
        indice = -1
        
        # Itera a través de los dígitos en la primera opción.
        for j in opciones[0]:
            # Encuentra la siguiente posición de '-' en 'temporal2'.
            if indice != -1:
                indice += temporal2[indice+1:].find('-') + 1
            else:
                indice = temporal2[indice+1:].find('-')
            
            # Reemplaza el primer '-' encontrado con el valor de 'j' (0 o 1).
            temporal2 = temporal2[:indice] + j + temporal2[indice+1:]
        
        # Convierte 'temporal2' a decimal y agrega a la lista 'temporal'.
        temporal.append(str(int(temporal2, 2)))
        
        # Elimina la primera opción de 'opciones'.
        opciones.pop(0)
    
    # Devuelve la lista 'temporal' con los minterminos en formato decimal.
    return temporal

def diferencias(mt1, mt2):
    # Inicializa un contador de diferencias en 0.
    contador = 0
    
    # Inicializa una variable 'indice' en 0.
    indice = 0
    
    # Itera a través de los caracteres de 'mt1' y 'mt2'.
    for i in range(len(mt1)):
        # Compara los caracteres en la misma posición.
        if mt1[i] != mt2[i]:
            # Si son diferentes, actualiza 'indice' con la posición de la diferencia.
            indice = i
            # Incrementa el contador de diferencias en 1.
            contador += 1
            
            # Si hay más de una diferencia, retorna (False, -1).
            if contador > 1:
                return (False, -1)
    
    # Después de recorrer ambas cadenas, si el contador de diferencias es 1, retorna (True, indice).
    return (True, indice)

def convertir(mintermino):
    # Inicializa una lista 'var_formula' para almacenar variables de la fórmula resultante.
    var_formula = []
    
    # Itera a través de los caracteres en 'mintermino'.
    for i in range(len(mintermino)):
        # Si el carácter es '1', agrega la variable correspondiente (A, B, C, ...) a 'var_formula'.
        if mintermino[i] == '1':
            var_formula.append(chr(i + 65))  # 65 es el código ASCII de 'A', 66 es el de 'B', y así sucesivamente.
        # Si el carácter es '0', agrega la variable negada (A', B', C', ...) a 'var_formula'.
        elif mintermino[i] == '0':
            var_formula.append(chr(i + 65) + "'")
    
    # Devuelve la lista 'var_formula' con las variables de la fórmula resultante.
    return var_formula

def buscar_implicantes_unicos(tabla):
    # Inicializa una lista vacía 'implicantes_unicos' para almacenar implicantes únicos.
    implicantes_unicos = []
    
    # Itera a través de las claves (índices) en el diccionario 'tabla'.
    for i in tabla:
        # Verifica si la longitud de la lista en 'tabla[i]' es igual a 1.
        if len(tabla[i]) == 1:
            # Si es 1, verifica si el implicante no está en 'implicantes_unicos'.
            if tabla[i][0] not in implicantes_unicos:
                # Agrega el implicante a 'implicantes_unicos'.
                implicantes_unicos.append(tabla[i][0])
    
    # Devuelve la lista 'implicantes_unicos' con los implicantes únicos encontrados.
    return implicantes_unicos

def ingresar_minterminos():
    # Imprime un encabezado.
    print("\nQUINE MCCLUSKEY\n")
    print("Ingrese los términos separados por un espacio. \n")
    
    # Lee la entrada del usuario y la convierte en una lista de enteros.
    mt = [int(i) for i in input("Ingrese los mintérminos: ").strip().split()]
    
    # Ordena los minterminos.
    mt.sort()
    
    # Devuelve la lista ordenada.
    return mt

def agrupar_minterminos(minterminos):
    # Calcula el número máximo de dígitos en los minterminos.
    max_minterm = len(bin(minterminos[-1])) - 2
    
    # Inicializa un diccionario 'grupos' para agrupar minterminos por cantidad de unos.
    grupos = {}
    
    # Itera a través de los minterminos.
    for minterm in minterminos:
        # Cuenta la cantidad de unos en el mintermino.
        count = bin(minterm).count('1')
        
        # Convierte el mintermino a una cadena binaria y rellena con ceros a la izquierda.
        minterm_str = bin(minterm)[2:].zfill(max_minterm)
        
        # Agrega el mintermino a la lista correspondiente en el diccionario 'grupos'.
        if count in grupos:
            grupos[count].append(minterm_str)
        else:
            grupos[count] = [minterm_str]
    
    # Devuelve el diccionario 'grupos' con los minterminos agrupados.
    return grupos

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
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
            marcar_todos(list(temporal),nueva_tabla,confirmados)
            break
    return confirmados


#---------------------------------------------------------------------------------------------------
def es_entero(numero):
    try:
        int(numero)
        return True
    except ValueError:
        return False
#------------------------------------------------------------------------------------------------------
def calcular():
    mt_input = input_entry.get().strip()
    if mt_input:
        minterminos = []
        for token in mt_input.split():
            if es_entero(token):
                minterminos.append(int(token))
            else:
                result_label.config(text="Por favor, ingrese Datos validos")
                return  # Salir de la función si se ingresa un valor no válido
        minterminos = set(minterminos)
        minterminos = list(minterminos)
        minterminos.sort()
        # minterminos = mt
        implicantes = set()
        grupos = agrupar_minterminos(minterminos)
        while True:
            temporal = grupos.copy()
            grupos = {}
            n = 0
            marcados = set()
            debo_parar = True
            lclaves = sorted(list(temporal.keys()))
            for i in range(len(lclaves)-1):
                for j in temporal[lclaves[i]]:
                    for k in temporal[lclaves[i+1]]:
                        cambio = diferencias(j,k)
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
        implicantes_unicos = buscar_implicantes_unicos(tabla)
        if len(implicantes_unicos) == 1 and not("0" in implicantes_unicos[0] or "1" in implicantes_unicos[0]):
            result_label.config(text="Resultados:\n 1" )
            formato_extendido = ["Terminos"]
            for i in minterminos:
                formato_extendido.append(str(i))
            longitud_formato = len(formato_extendido[1:])
            implicante_vacio = [implicantes_unicos[0]]
            for i in range(longitud_formato):
                implicante_vacio.append("X")
            print(tabulate([implicante_vacio], headers=formato_extendido))
            print("\n")
            return
        else:
            formato_extendido = ["Terminos"]
            for i in minterminos:
                formato_extendido.append(str(i)) 
            longitud_formato = len(formato_extendido[1:])
            implicante_lista = []
            for i in implicantes:
                temporal = ["".join(convertir(i))]
                for j in minterminos:
                    if i in tabla[str(j)]:
                        temporal.append("X")
                    else:
                         temporal.append(" ")   
                
                implicante_lista.append(temporal)
            #print(implicante_lista)
            print(tabulate(implicante_lista, headers=formato_extendido))
            print("\n")    
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
            complemento = set()
            marcar_todos(dos_marcas, nueva_tabla, complemento)
            formula_final = list(complemento)+implicantes_unicos
            formato_ecuacion = []
            for i in range(len(formula_final)):
                formato_ecuacion.append(convertir(formula_final[i]))
            resultados = []
            for i in range(len(formato_ecuacion)):
                for j in formato_ecuacion[i]:
                    resultados.append(j)
                if i < len(formato_ecuacion) - 1:
                    resultados.append(" + ")

            result_label.config(text="Resultados:\n" + "".join(resultados))
    else:
        result_label.config(text="Por favor, ingrese los minterminos.")

def reiniciar():
    input_entry.delete(0, tk.END)
    result_label.config(text="")

root = tk.Tk()
root.title("Quine McCluskey")
root.geometry("800x600")

color = "#2B023C"
root.configure(bg=color)

title_label = tk.Label(root, text="Quine McCluskey", justify="center", wraplength=600, bg=color, fg="white", font=("Arial", 20))
title_label.pack()

input_label = tk.Label(root, text="Ingrese los minterminos (separados por espacios):", justify="center", wraplength=600, bg=color, fg="white", font=("Arial", 15))
input_label.pack()

frame = tk.Frame(root,bg=color)
frame.pack()

# Texto antes del input
label_before = tk.Label(frame, text="(", bg=color, fg="white", font=("Arial", 20))
label_before.pack(side=tk.LEFT)

# Widget de entrada
input_entry = tk.Entry(frame, width=60, font=("Arial", 10))
input_entry.pack(side=tk.LEFT)

# Texto después del input
label_after = tk.Label(frame, text=" )", bg=color, fg="white", font=("Arial", 20))
label_after.pack(side=tk.LEFT)

# calculate_button = tk.Button(root, text="Calcular", command=calcular)
# calculate_button.pack()

# reset_button = tk.Button(root, text="Reiniciar", command=reiniciar)
# reset_button.pack()

# Cambia el estilo del botón
style = ttk.Style()
style.configure("Custom.TButton", background="#3498db", foreground="black", font=("Arial", 12))

calculate_button = ttk.Button(root, text="Calcular", command=calcular, style="Custom.TButton")
calculate_button.pack(pady=10)

reset_button = ttk.Button(root, text="Reiniciar", command=reiniciar, style="Custom.TButton")
reset_button.pack(pady=10)

result_label = tk.Label(root, text="", justify="center", wraplength=600, bg=color, fg="white", font=("Arial", 20))
result_label.pack(fill="both", expand=True)

root.mainloop()