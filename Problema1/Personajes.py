import random

class personajes:
    personajes={} #Diccionario de la forma Nombre Personaje: Características (Caracteristicas es un diccionario de la forma Tipo Caracteristica: Caracteristica)
    caracteristicasFisicas={}
    caracteristicasFisicas['pelo']=["Azul","Negro","Amarillo","Rojo","Cafe","Violeta","Gris","Verde","Plateado","Rosa"] #Color de pelo
    caracteristicasFisicas['complexion']=["Delgado","Flaco","Gordo","Morbido","Atletico","Robusto","Perfecto","Esqueletico","Normal","Amorfo"] #Complexión
    caracteristicasFisicas['estatura']=["Alto","Bajo","Enano","Gigante","Godzilla","Liliputiense","Microscopico","Planeta","Subatomico","Enorme"]#Estatura
    caracteristicasFisicas['piel']=["Blanco","Cafe","Negro","Rojo","Azul","Verde","Morado","Rosa","Amarillo","Carton"] #Color de piel
    caracteristicasFisicas['raza']=["Humano","Monstruo","Vampiro","Depredador","Robot","Reptiliano","Atlante","Demonio","Alien","Marciano"]#Diccionario constante con las caracteristicas fisicas posibles para los personajes (Tipo de Caracteristica: lista de caracteristicas)
    
    caracteristicasSobresalientes={}
    caracteristicasSobresalientes['arte']=["Arquitectura","Cine","Pintura","Escultura","Poesia","Musica","Danza"] #Artes
    caracteristicasSobresalientes['deporte']=["Futbol","Beisbol","Basquetbol","Automovilismo","Pesca","Arqueria"] #Deportes
    caracteristicasSobresalientes['ciencia']=["Quimica","Fisica","Biologia","Computacion","Economia","Epidemiologia","Farmacologia"] #/Ciencia
    caracteristicasSobresalientes['grado']=["Licenciado","Ingeniero","Maestro","Doctor","Empresario","Bachiller"] #Grado
    caracteristicasSobresalientes['pasatiempo']=["Rompecabezas","Acuarios","Terrarios","Legos","Caminata","Maquetas","Dormir"]#Diccionario constante con las caracteristicas sobresalientes posibles para los personajes (Tipo de Caracteristica: lista de caracteristicas)
	
    nombres=["Pedro", "Alex", "Ricardo", "Maria", "Sofia", "Karen", "Valentina", "Cecilia", "Diana", "Fidel"] #Lista constante con los nombres posibles para los personajes (10 nombres cualesquiera)
	
    correcto="" #Nombre del personaje a adivinar (se escoge al azar al terminar de llenar el diccionario de personajes)
    ganador=False
    ultimaJugada=[]
    turnos=[]
    def __init__(self):
        #Constructor de la clase personajes aquí se llenará el diccionario personajes al azar
        self.correcto=self.nombres[int(random.random()*len(self.nombres))]
        self.generaCaracteristicas()
        print(self.correcto)
	
    def generaCaracteristicas(self):
        numero=random.random()
        if numero<=0.7 and numero>=0.2:
            diccionario=self.caracteristicasFisicas
        else:
            diccionario=self.caracteristicasSobresalientes
        for i in range(0,10):
            caracteristicas={}
            for key in diccionario:
                numero2=int(random.random()*len(diccionario[key]))
                caracteristicas[key]=diccionario[key][numero2]
            numero2=int(random.random()*len(self.nombres))
            llave=self.nombres.pop(numero2)
            self.personajes[llave]=caracteristicas #aqui se añade el personaje con las carcateristicas generadas

    def getGanador(self):
        return (self.correcto,self.personajes[self.correcto])


