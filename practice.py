

array = ["Juan", "Lucas", "marcelo"] 

def mostrar_estudiantes(lista_estudiantes):
    estudiantes = lista_estudiantes
    return estudiantes

print("LIsta de estdiantes: " + str(mostrar_estudiantes(array)))

diccionario = {"valor1": 20, "valor2": 300, "valor3": 240, "valor4": 500}

dicc = dict({"valor1": 20, "valor2": 300, "valor3": 240, "valor4": 500})

def mostrar_precios(lista_precios):
    return lista_precios

print("Lista de precios: " + str(mostrar_precios(diccionario)))

class Persona():
    #constructor de la clase persona
    #constructor sobrecargado
    def __init__(self, nombre, apellido, edad):

        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad
    
    def mostrar_datos(nombre, apellido):
        return nombre + " " + apellido


persona = Persona("Fatima", "Espindola", 22)
datos = persona.mostrar_datos(persona.nombre, persona.apellido)
print(str(datos))
