import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk

def recorta(lista):
    elementos_recortados = []
    for i in lista:
        elementos_recortados.extend(lista[i])
    return elementos_recortados

def buscaMinterminos(mt):
    guiones = mt.count('-')  # Cuenta cuántos guiones tiene el argumento 'mt'
    if guiones == 0:
        return [str(int(mt, 2))]  # Si no tiene ningún guión, devuelve el número decimal que corresponde al binario ingresado
    
    opciones = [bin(i)[2:].zfill(guiones) for i in range(pow(2, guiones))]
    # Aquí se crea una lista llamada 'opciones' que contiene representaciones binarias de números en forma de cadenas.
    # Estos números van desde 0 hasta 2^guiones - 1. 
    # 'bin(i)[2:]' convierte 'i' a binario y omite el prefijo '0b', y 'zfill(guiones)' rellena con ceros a la izquierda para que tengan la misma longitud que 'mt'.

    temporal = []
    for i in range(pow(2, guiones)):
        temporal2 = mt[:]  # Crea una copia de 'mt' para modificarla
        indice = -1
        for j in opciones[0]:
            if indice != -1:
                indice += temporal2[indice+1:].find('-') + 1
            else:
                indice = temporal2[indice+1:].find('-')
            # Encuentra la siguiente posición de '-' en 'temporal2'
            # (si ya se encontró uno, se busca después de la última posición encontrada)
            temporal2 = temporal2[:indice] + j + temporal2[indice+1:]
            # Reemplaza el primer '-' encontrado con el valor de 'j' (0 o 1)

        temporal.append(str(int(temporal2, 2)))
        opciones.pop(0)
    # Convierte la cadena modificada 'temporal2' a decimal y la agrega a la lista 'temporal'
    # Luego, elimina la primera opción de 'opciones' para procesar la siguiente iteración.

    return temporal  # Devuelve una lista de minterminos en formato decimal

def diferencias(mt1, mt2):
    contador = 0  # Inicializa un contador para llevar un registro de las diferencias encontradas.
    indice = 0  # Inicializa una variable 'indice' para rastrear la posición de la diferencia.

    for i in range(len(mt1)):
        # Itera a través de los índices de las cadenas 'mt1' y 'mt2'.
        
        if mt1[i] != mt2[i]:
            # Compara los caracteres en el mismo índice en ambas cadenas.

            indice = i  # Si los caracteres son diferentes, actualiza 'indice' con la posición de la diferencia.
            contador += 1  # Incrementa el contador de diferencias en 1.

            if contador > 1:
                # Si se encuentran más de una diferencia, retorna (False, -1).
                # Esto indica que las cadenas 'mt1' y 'mt2' tienen más de una diferencia y no son adecuadas para el propósito actual.
                return (False, -1)

    # Después de recorrer ambas cadenas, si el contador de diferencias es igual a 1, significa que hay una sola diferencia.
    # En ese caso, se devuelve (True, indice) donde 'True' indica que hay una sola diferencia y 'indice' es la posición de la diferencia.
    return (True, indice)

def convertir(mintermino):
    var_formula = []  # Crea una lista vacía para almacenar las variables de la fórmula resultante.

    for i in range(len(mintermino)):
        # Itera a través de los caracteres en la cadena 'mintermino'.

        if mintermino[i] == '1':
            # Si el carácter en la posición 'i' es '1', agrega la variable correspondiente a 'var_formula'.
            # En este caso, utiliza la convención de letras mayúsculas A, B, C, ... para representar las variables.
            var_formula.append(chr(i + 65))  # 65 es el código ASCII de 'A', 66 es el de 'B', y así sucesivamente.

        elif mintermino[i] == '0':
            # Si el carácter en la posición 'i' es '0', agrega la variable negada a 'var_formula'.
            # En este caso, utiliza la misma convención de letras mayúsculas, pero agrega una comilla simple ('), como A', B', C', ...
            var_formula.append(chr(i + 65) + "'")

    return var_formula  # Devuelve la lista de variables de la fórmula resultante.


def buscar_implicantes_unicos(tabla):
    implicantes_unicos = []  # Crea una lista vacía para almacenar los implicantes únicos.

    for i in tabla:
        # Itera a través de las claves (índices) en el diccionario 'tabla'.

        if len(tabla[i]) == 1:
            # Verifica si la longitud de la lista en 'tabla[i]' es igual a 1.
            # Esto significa que hay un único implicante en la columna correspondiente a la clave 'i'.

            if tabla[i][0] not in implicantes_unicos:
                # Comprueba si el único implicante encontrado no está en la lista 'implicantes_unicos'.
                # Si no está en la lista, lo agrega.
                implicantes_unicos.append(tabla[i][0])

    return implicantes_unicos
def ingresar_minterminos():
    print("\nQUINE MCCLUSKEY\n")
    print("Ingrese los términos separados por un espacio. \n")
    mt = [int(i) for i in input("Ingrese los mintérminos: ").strip().split()]
    mt.sort()  # Ordenamos los minterminos
    return mt
#-----------------------------------------------------
'''
    Contamos el número de unos en cada mintermino, luego guardamos el equivalente binario desde la posicion 2 para evitar '0b' que agrega la funcion
    seguido lo metemos en una cadena y rellenamos con ceros a la izquierda equivalentes al mintermino más grande. Despues validamos si ya existe
    una clave con ese número de unos, si ya existe simplemente agregamos el mintermino al grupo con esa clave, de lo contrario se crea la clave y
    se introduce de igual manera.
'''
def agrupar_minterminos(minterminos):
    max_minterm = len(bin(minterminos[-1])) - 2
    grupos = {}

    for minterm in minterminos:
        count = bin(minterm).count('1')
        minterm_str = bin(minterm)[2:].zfill(max_minterm)

        if count in grupos:
            grupos[count].append(minterm_str)
        else:
            grupos[count] = [minterm_str]

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
#------------------------------------------------------------------------------------------------------
def mostrar_resultados(resultados):
    # Crea una nueva ventana para mostrar los resultados
    result_window = tk.Toplevel()
    result_window.title("Resultados")
    result_window.geometry("800x600")  # Establece el tamaño de la ventana

    # Crea un widget de área de texto para mostrar los resultados con desplazamiento
    result_text = tk.Text(result_window, wrap=tk.WORD)
    result_text.pack(fill=tk.BOTH, expand=True)

    # Inserta los resultados en el widget de área de texto
    result_text.insert(tk.END, resultados)


def main():
    def calcular():
        mt = [int(i) for i in input_entry.get().strip().split()]
        mt.sort()
        minterminos = mt
        implicantes = set()

        # Comenzamos la agrupación primaria
        # agrupar_minterminos
        grupos = agrupar_minterminos(minterminos)
        # Término de la agrupación primaria

        # Proceso para crear las tablas y encontrar los implicantes primos 
        while True:
            temporal = grupos.copy()
            grupos = {}
            n = 0
            marcados = set()
            debo_parar = True
            lclaves = sorted(list(temporal.keys()))
            for i in range(len(lclaves)-1):
                for j in temporal[lclaves[i]]: # Iteración a través del grupo de elementos actual 
                    for k in temporal[lclaves[i+1]]: # Iteración a través del siguiente grupo de elementos
                        cambio = diferencias(j,k) # Comparamos los mintérminos
                        if cambio[0]: # Si los mintérminos difieren solamente en un bit
                            minterm_cambio = j[:cambio[1]] + '-' + j[cambio[1]+1:]
                            if n in grupos:
                                if minterm_cambio not in grupos[n]:
                                    grupos[n].append(minterm_cambio)
                            else:
                                grupos[n] = [minterm_cambio]
                            debo_parar = False
                            marcados.add(j) # Marca el elemento j
                            marcados.add(k) # Marca el elemento k

                n += 1
            desmarcados_local = set(recorta(temporal)).difference(marcados) # Desmarcamos los elementos de cada tabla
            implicantes = implicantes.union(desmarcados_local) # Agregamos el implicante primo a la lista.
            if debo_parar: # Si los mintérminos no pueden ser combinados
                break #Detenemos el ciclo

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
            
        # Calcular y formatear los resultados
        resultados = []
        for i in range(len(formato_ecuacion)):
            for j in formato_ecuacion[i]:
                resultados.append(j)
            if i < len(formato_ecuacion) - 1:
                resultados.append(" + ")

        # Mostrar los resultados en el widget de etiqueta
        result_label.config(text="Resultados:\n" + "".join(resultados))
        
        # Deshabilitar el botón de cálculo
        calculate_button.config(state=tk.DISABLED)

    # Crear una ventana Tkinter
    root = tk.Tk()
    root.title("Quine McCluskey")
    root.geometry("800x600")  # Establece el tamaño de la ventana

    # Cambiar el color de fondo de la ventana
    root.configure(bg="#3B13EE")  # Reemplaza "color_de_fondo" con el color que desees, p. ej., "white" o "#FF0000" (rojo)
    input_label = tk.Label(root, text="Quine McCluskey",justify="center", wraplength=600,bg="#3B13EE",fg="white",font=("Arial", 20))
    input_label.pack()
    # Crear y configurar etiqueta de entrada
    input_label = tk.Label(root, text="Ingrese los mintérminos (separados por espacios):",justify="center", wraplength=600,bg="#3B13EE",fg="white",font=("Arial", 15))
    input_label.pack()

    input_entry = tk.Entry(root,width=100)
    input_entry.pack()
    # Crear botón para calcular
    calculate_button = tk.Button(root, text="Calcular", command=calcular)
    calculate_button.pack()
    # Crear una etiqueta para mostrar los resultados en el centro de la ventana
    result_label = tk.Label(root, text="", justify="center", wraplength=600,bg="#3B13EE",fg="white",font=("Arial", 20))
    result_label.pack(fill="both", expand=True)

    # Ejecutar la aplicación Tkinter
    root.mainloop()
#-----------------------------------------------------------

if __name__ == "__main__":
    main()