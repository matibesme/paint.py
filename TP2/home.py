import gamelib
import png

ANCHO, ALTO, TAM_CELDA = 10,10,15
#Algunas claves de diccionarios para que sea menos vulnerable
SELECCIONADO, PINTANDO, COLOR = "color_sel", "Pintando","color"
BLANCO,NEGRO="#FFFFFF","#000000"
PNG,PPM=".png",".ppm"



def paint_nuevo(ancho, alto):
    '''inicializa el estado del programa con una imagen vacía de ancho x alto pixels'''
    paint=[]
    for i in range(alto):
      lista=[]
      for j in range(ancho):
        lista.append(BLANCO)
      paint.append(lista)
    return paint

def paint_mostrar(nuevo_paint):
    '''dibuja la interfaz de la aplicación en la ventana'''
    gamelib.draw_begin()
    
    nuevo_paint.estado["Ancho"],nuevo_paint.estado["Alto"]=len(nuevo_paint.paint[0]),len( nuevo_paint.paint)
    nueva_dim=dimensiones( nuevo_paint.estado["Ancho"], nuevo_paint.estado["Alto"])
    dim_min=dimensiones(300/nueva_dim.ancho,300/nueva_dim.alto)
    #Siempre el gadmelib mantiene la misma dimensiones lo que varia es la plantilla
    #defino tamano de celda
    if nueva_dim.ancho == nueva_dim.alto:
         nuevo_paint.estado["Celda"]=dim_min.ancho
    else:
        if dim_min.ancho>dim_min.alto:
             nuevo_paint.estado["Celda"]=dim_min.alto
        else:
             nuevo_paint.estado["Celda"]=dim_min.ancho

    tam_celda=  nuevo_paint.estado["Celda"]

    #Diseno de plantilla
    for i in range(nueva_dim.alto):
      for j in range(nueva_dim.ancho):
        fill_color= nuevo_paint.paint[i][j]
        gamelib.draw_rectangle(j*tam_celda, tam_celda*i, (j+1)*tam_celda, (i+1)*tam_celda, outline=NEGRO, fill=fill_color)
    #Diseno de paleta    
    for i in range(len( nuevo_paint.paleta)):
        fill_color =  nuevo_paint.paleta[i][COLOR]
        outline= nuevo_paint.paleta[i]['outline']
        x1=10 + i * 35
        x2=30 + i * 35
        y1= 320
        y2=340
        gamelib.draw_rectangle(x1,y1, x2, y2, fill=fill_color, outline=outline)
    #Texto de guardado o cargra
    texto="'c': Cargar PPM\n'd': Guardar PPM\n'g': Guardar PNG "
    gamelib.draw_text(texto, 52, 370, size=10, fill=BLANCO)
    gamelib.draw_end()


def pintar_pixel(paint,x,y,color):
   """Recibe una plantilla una posicion y un color, y lo pinta de ese color"""
   paint[y][x]=color
   

def guardar_img_ppm(imagen,estado):
    """Recibe una plantilla y la gurda en formato .ppm"""
    archivo = gamelib.input("Nombre del archivo .ppm:")
    #Verifico que haya archivo y cumpla con la direccion correcta
    if archivo and archivo[-4:]==PPM:
        with open (archivo, 'w') as salida:
            ancho,alto= estado["Ancho"],estado["Alto"]
            salida.write(f'P3\n{ancho} {alto}\n255\n')
            for i in range(alto):
                for j in range(ancho):
                    r,g,b=hexadecimal_a_decimal(imagen[i][j])
                    salida.write(f'{r} {g} {b} ')
                salida.write('\n')
    else:
        gamelib.say("Ingrese un archivo en el formato valido") 

def cargar_img_ppm(archivo):
    """carga una plantilla en formato .ppm, la funcion devuelve una nueva plantilla adaptada a el cambio de dimensiones."""
    with open(archivo, 'r') as entrada:
        entrada.readline()

        dimensiones = entrada.readline().split()
        ancho = int(dimensiones[0])
        alto = int(dimensiones[1])
        entrada.readline()

        imagen = []
        for linea in entrada:
            valores = linea.split()
            fila = []

            for j in range(0, len(valores), 3):
                r = int(valores[j])
                g = int(valores[j+1])
                b = int(valores[j+2])
                fila.append((r,g,b))
            imagen.append(fila)

    nuevo_paint = paint_nuevo(ancho, alto)
    for i in range(alto):
        for j in range(ancho):
            nuevo_paint[i][j] = decimal_a_hexadecimal(imagen[i][j])

    return nuevo_paint

def guardar_img_png(paint,paleta):
    """Guarda la imagen en un format .png"""
    archivo = gamelib.input("Nombre del archivo .png:")
    #Verifico que haya archivo y cumpla con la direccion correcta
    if archivo and archivo[-4:]==PNG:
        lista_colores=[]
       
        for indice in paleta:
            color_temp=hexadecimal_a_decimal(paleta[indice][COLOR])
            lista_colores.append(color_temp)
        imagen=[]
        for i in range(len(paint)):
            lista=[]
            for j in range(len(paint[0])):
                color=hexadecimal_a_decimal(paint[i][j])
                if color in lista_colores:
                    lista.append(lista_colores.index(color))
            imagen.append(lista)
        png.escribir(archivo,lista_colores,imagen)
        


def agregar_color(paleta):
    """Pide ingresar un color y lo reemplaza en la paleta """
    color_nuevo=gamelib.input("Ingrese el colo en formato hexadecimal(#rrggbb)")
    if color_nuevo:
        paleta[0][COLOR]=color_nuevo
        gamelib.say("Color agregado con exito")

def hexadecimal_a_decimal(color):
    """Convierte un color en formato hexadecimal a decimal(Tuple)"""
    r=int(color[1:3],16)
    g=int(color[3:5],16)
    b=int(color[5:7],16)
    return r,g,b

def decimal_a_hexadecimal(color):
    """Convierte un color en formato decimal a hexadecimal"""
    r, g, b = color
    rh= f"{r:02x}"
    gh= f"{g:02x}"
    bh= f"{b:02x}"

    hexadecimal = f"#{rh}{gh}{bh}"
    return hexadecimal

def crear_paleta():
    """Devulve un diccionario de colores donde su clave es su ubicacion y su valor es otro diccionario donde podemos encontrar su color y su borde. En el caso de que su borde sea BLANCO es el color actual."""
    paleta = {
    0: {COLOR: "#ce2740","outline": "#FFFFFF"},
    1: {COLOR: "#FFFFFF","outline": "#000000"},
    2: {COLOR: "#567dfb","outline": "#000000"},
    3: {COLOR: "#f1db35","outline": "#000000"},
    4: {COLOR: "#17a339","outline": "#000000"},
    5: {COLOR: "#348b8c","outline": "#000000"},
    6: {COLOR: "#fd597e","outline": "#000000"} }
    return paleta


class dimensiones:
    """Clase dimensiones del paint, recibe un alto ancho. Ademas tiene una funcion para agregar un tamano de celda"""
    def __init__(self,ancho,alto):
        self.ancho=ancho
        self.alto=alto
        self.celda=15
    def agregar_celda(self,celda):
        self.celda=celda


class estructura_paint:
    """Clase una estructura del juego completo, recibe un paint, estado y paleta  """
    
    def __init__(self,paint,estado,paleta):
        self.paint=paint
        self.estado=estado
        self.paleta=paleta
   

def main():
    gamelib.title("AlgoPaint")
    gamelib.resize(300,400)
    estado={SELECCIONADO: 0, "Ancho": ANCHO, "Alto": ALTO, "Celda": TAM_CELDA, PINTANDO: False}
    paint = paint_nuevo(ANCHO,ALTO)
    paleta=crear_paleta()

    nuevo_paint=estructura_paint(paint,estado,paleta)


    while gamelib.loop(fps=15):

        paint_mostrar(nuevo_paint)
        dim=dimensiones( nuevo_paint.estado["Ancho"], nuevo_paint.estado["Alto"])
        dim.agregar_celda( nuevo_paint.estado["Celda"])
        


        for ev in gamelib.get_events():

            if ev.type == gamelib.EventType.ButtonPress and ev.mouse_button == 1:
                x = int(ev.x // dim.celda)
                y = int(ev.y // dim.celda)
                #si hace click dentro de la plantilla llamo a pintar_pixel
                if 0 <= x < dim.ancho and 0 <= y < dim.alto:
                    pintar_pixel(nuevo_paint.paint,x, y, nuevo_paint.paleta[nuevo_paint.estado[SELECCIONADO]][COLOR])
                    nuevo_paint.estado[PINTANDO]=True
                x2 = ev.x
                y2 = ev.y 
                #Verifico si ace click dentro de la paleta
                if 320 <= y2 <= 340:
                    for i in range(len(nuevo_paint.paleta)):
                        if 10 + i * 35 <= x2 <= 30 + i * 35:
                            nuevo_paint.paleta[nuevo_paint.estado[SELECCIONADO]]['outline'] = NEGRO
                            nuevo_paint.estado[SELECCIONADO] = i
                            nuevo_paint.paleta[i]['outline'] =BLANCO

                            if i == 0:
                                agregar_color(nuevo_paint.paleta)
                
                        
            elif ev.type == gamelib.EventType.Motion and nuevo_paint.estado[PINTANDO]:
                x =int(ev.x // dim.celda)
                y = int(ev.y // dim.celda)
                #Verifico mientras mantiene apretado
                if 0 <= x < dim.ancho and 0 <= y < dim.alto:
                    pintar_pixel( nuevo_paint.paint,x, y,  nuevo_paint.paleta[estado[SELECCIONADO]][COLOR])
               
            elif ev.type == gamelib.EventType.ButtonRelease and ev.mouse_button == 1:
                nuevo_paint.estado[PINTANDO]=False
        
            elif ev.type == gamelib.EventType.KeyPress: 
                tecla = ev.key.lower()
                try:
                    if tecla == 'c':
                        archivo = gamelib.input("Nombre del archivo .ppm:")
                        if archivo and archivo[-4:]==PPM:
                            nuevo_paint.paint=cargar_img_ppm(archivo)
                        

                    if tecla == 'd':
                        guardar_img_ppm(nuevo_paint.paint,nuevo_paint.estado)
                    if tecla == 'g':
                        guardar_img_png(nuevo_paint.paint,nuevo_paint.paleta)
                except Exception:
                    gamelib.say("Ha ocurrido un error con el archivo")





gamelib.init(main)