# -*- coding: utf-8 -*-
# Импортируем все необходимые библиотеки:
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from loader import *
from shadows import *
from math import *
import sys

# Объявляем все глобальные переменные
global xrot  # Величина вращения по оси x
global yrot  # Величина вращения по оси y
global ambient  # рассеянное освещение
global lightpos  # Положение источника освещения
global obj
global color
global obj2
global textureMapID
global angleAdj
global program

# Процедура инициализации
def init():
    global xrot  # Величина вращения по оси x
    global yrot  # Величина вращения по оси y
    global ambient  # Рассеянное освещение
    global lightpos  # Положение источника освещения
    global obj
    global obj2
    global color
    global textureMapID
    global angleAdj

    xrot = -128.0  # Величина вращения по оси x = 0
    yrot = -120.0  # Величина вращения по оси y = 0
    angleAdj = 8.0
    ambient = (0.5, 0.5, 0.5, 0.)  # Первые три числа цвет в формате RGB, а последнее - яркость
    lightpos = (0.0, 250.0, 40.0)  # Положение источника освещения по осям xyz

    glClearColor(0.2, 0.8, 0.1, 1.0)  # Серый цвет для первоначальной закраски
    # glOrtho(-20.0, 120.0, -20.0, 120.0, -120., 120.)  # Определяем границы рисования по горизонтали и вертикали
    # glRotatef(-90, 1.0, 0.0, 0.0)                   # Сместимся по оси Х на 90 градусов
    # glTranslatef(10,0,0)
    # glTranslatef(0,10,0)
    color = (1, 1, 1, 1)
#     glLightModelfv(GL_LIGHT_MODEL_AMBIENT, ambient) # Определяем текущую модель освещения
#     glEnable(GL_LIGHTING)                           # Включаем освещение
#     glEnable(GL_LIGHT0)                             # Включаем один источник света
#     glLightfv(GL_LIGHT0, GL_POSITION, lightpos)     # Определяем положение источника света
#     #glLightfv(GL_LIGHT0, GL_DIFFUSE, ambient)
#     glLightModeli(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE)
    glEnable(GL_NORMALIZE)
    glClearDepth(1.0)
    glEnable(GL_LIGHTING)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    glDepthFunc(GL_LEQUAL)
    
    glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    glEnable(GL_COLOR_MATERIAL)
    obj = OBJ(sys.argv[1], swapyz=True, color=(1., 1., 1., 1.), list=1)
    obj2 = OBJ(sys.argv[2], swapyz=True, color=(1.0, 0.0, 0.0, 1.), list=2)
    # shadow Map
    textureMapID = CreateTextureShadow()    
    

def cameraLoop():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-20.0, 120.0, -20.0, 120.0, -250., 250.)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    pickObjX, pickObjY, pickObjZ = (0, 0, -1)
    radius = 100.
    eyeX = radius * cos(xrot / 180.) * sin(yrot / 180.)
    eyeY = radius * sin(xrot / 180.) * sin(yrot / 180.)
    eyeZ = radius * cos(yrot / 180.)
    print xrot,yrot
    gluLookAt(eyeX, eyeY, eyeZ, pickObjX, pickObjY, pickObjZ, 0, 1, 0)
    modelMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
    print modelMatrix
    
def debugLightView():
    global lightpos
    glLoadIdentity()
    gluPerspective(spotFOV, 1.0, 0.1, 300.0)


    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(  lightpos[0], 
                lightpos[1],
                lightpos[2],
                0.0, 10.0, 0.0, 
                0.0, 1.0, 0.0 )

def lightLoop():
    'light which change position every frame'
    global lightpos
    position = list(lightpos)
    position.append(1.0)
#     glMatrixMode(GL_MODELVIEW)
#     glPushMatrix()
#     glDisable(GL_LIGHTING)
#     glPointSize(5.0)
#     glBegin(GL_POINTS)
#     glColor4f(1.0, 1.0, 1.0, 1.0)
#     glVertex4fv(position)
#     glEnd()
#     glPopMatrix() 

    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))  # Setup The Diffuse Light 
    glLightfv(GL_LIGHT0, GL_SPECULAR, (0.6, 0.6, 0.6, 1.0))  # Setup The Specular Light
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.5, 0.5, 0.5, 1.0))  # Setup The Ambient Light 
    glLightfv(GL_LIGHT0, GL_POSITION, position)  # Position of The Light  

    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 1.0)
    glEnable(GL_LIGHT0)
    
    glEnable(GL_LIGHTING)

# Процедура обработки специальных клавиш
def specialkeys(key, x, y):
    global xrot
    global yrot
    global angleAdj
    # Обработчики для клавиш со стрелками
    if key == GLUT_KEY_UP:  # Клавиша вверх
        xrot -= angleAdj  # Уменьшаем угол вращения по оси Х
    if key == GLUT_KEY_DOWN:  # Клавиша вниз
        xrot += angleAdj  # Увеличиваем угол вращения по оси Х
    if key == GLUT_KEY_LEFT:  # Клавиша влево
        yrot -= angleAdj  # Уменьшаем угол вращения по оси Y
    if key == GLUT_KEY_RIGHT:  # Клавиша вправо
        yrot += angleAdj  # Увеличиваем угол вращения по оси Y

    glutPostRedisplay()  # Вызываем процедуру перерисовки



def makeRotations():
    pass
#     global xrot
#     global yrot
#     glTranslatef(10, 10, 0)
#     glRotatef(xrot, 1.0, 0.0, 0.0)  # Вращаем по оси X на величину xrot
#     glRotatef(yrot, 0.0, 1.0, 0.0)  # Вращаем по оси Y на величину yrot

# Процедура перерисовки
def drawFrame():
    global lightpos
    global program
    
    # first pass, compute texture
    textureMatrix = CreateShadowBefore(position=lightpos)
    drawModels()
    CreateShadowAfter(textureMapID)
    # draw all objects
    cameraLoop()
    drawLighting()
    glUseProgram(program)
    drawModels()
    glUseProgram(0)
    # render only obj(s) where shadows cast
    RenderShadowCompareBefore(textureMapID, textureMatrix)
    drawModels()
    RenderShadowCompareAfter()
    glutSwapBuffers() 


def drawLighting():
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    makeRotations()
    lightLoop()  # Источник света вращаем тоже
    glPopMatrix()  # Возвращаем сохраненное положение "камеры"
    
def drawModels():
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    makeRotations()
    drawObjModels()
    drawFloor()
    glPopMatrix()  # Возвращаем сохраненное положение "камеры"
    

def drawObjModels():
    global obj
    global obj2
    glDisable(GL_COLOR_MATERIAL)
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, (0.95,0.95,0.95))
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, (0.6,0.6,0.6))
    #glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, (0.7,0.7,0.7))
    #glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 0.25 * 128.0)
    glCallList(obj.gl_list)
    glEnable(GL_COLOR_MATERIAL)
    #glMaterialfv(GL_FRONT, GL_SPECULAR, (0.992157,0.941176,0.807843))
    #glMaterialf(GL_FRONT, GL_SHININESS, 0.21794872 * 128.0)
    glCallList(obj2.gl_list)
    
    
# Процедура подготовки шейдера (тип шейдера, текст шейдера)
def create_shader(shader_type, source):
    # Создаем пустой объект шейдера
    shader = glCreateShader(shader_type)
    # Привязываем текст шейдера к пустому объекту шейдера
    glShaderSource(shader, source)
    # Компилируем шейдер
    glCompileShader(shader)
    # Возвращаем созданный шейдер
    return shader
    
def phongVertex():
    return """
varying vec3 N;
varying vec3 v;
void main(void)  
{     
   v = vec3(gl_ModelViewMatrix * gl_Vertex);       
   N = normalize(gl_NormalMatrix * gl_Normal);
   gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;  
}"""
            
def phongFragment():
    return """
varying vec3 N;
varying vec3 v;    
void main (void)  
{  
   vec3 L = normalize(gl_LightSource[0].position.xyz - v);   
   vec3 E = normalize(-v); // we are in Eye Coordinates, so EyePos is (0,0,0)  
   vec3 R = normalize(-reflect(L,N));  
 
   //calculate Ambient Term:  
   vec4 Iamb = gl_FrontLightProduct[0].ambient;    

   //calculate Diffuse Term:  
   vec4 Idiff = gl_FrontLightProduct[0].diffuse * max(dot(N,L), 0.0);
   Idiff = clamp(Idiff, 0.0, 1.0);     
   
   // calculate Specular Term:
   vec4 Ispec = gl_FrontLightProduct[0].specular 
                * pow(max(dot(R,E),0.0),0.3*gl_FrontMaterial.shininess);
   Ispec = clamp(Ispec, 0.0, 1.0); 
   // write Total Color:  
   gl_FragColor = gl_FrontLightModelProduct.sceneColor + Iamb + Idiff + Ispec;     
}"""


def drawFloor():
    #glDisable(GL_COLOR_MATERIAL)
    #glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, (0.5,0.5,0.5))
    #glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, (0.2,0.2,0.2))
    glColor3f(0.5, 0.5, 0.5)
    glBegin(GL_QUADS)
    glNormal3f(0.0, 1.0, 0.0)
    glVertex3f(-250.0, 0, -250.0)
    glVertex3f(-250.0, 0, 250)
    glVertex3f(250.0, 0, 250) 
    glVertex3f(250, 0, -250.0)
    glEnd()
    #glEnable(GL_COLOR_MATERIAL)

if len(sys.argv) < 2:
    sys.argv.append("cup.obj")
if len(sys.argv) < 3:
    sys.argv.append("handler.obj")
    
# Здесь начинается выполнение программы
# Использовать двойную буферизацию и цвета в формате RGB (Красный, Зеленый, Синий)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
# Указываем начальный размер окна (ширина, высота)
glutInitWindowSize(1024, 1024)
# Указываем начальное положение окна относительно левого верхнего угла экрана
glutInitWindowPosition(50, 50)
# Инициализация OpenGl
glutInit(sys.argv)
# Создаем окно с заголовком
glutCreateWindow(b"cup")
# Определяем процедуру, отвечающую за перерисовку
glutDisplayFunc(drawFrame)
# Определяем процедуру, отвечающую за обработку клавиш
glutSpecialFunc(specialkeys)
# Вызываем нашу функцию инициализации
init()
vertex = create_shader(GL_VERTEX_SHADER, phongVertex())
# Создаем фрагментный шейдер:
# Определяет цвет каждого фрагмента как "смешанный" цвет его вершин
fragment = create_shader(GL_FRAGMENT_SHADER, phongFragment())
# Создаем пустой объект шейдерной программы
program = glCreateProgram()
# Приcоединяем вершинный шейдер к программе
glAttachShader(program, vertex)
# Присоединяем фрагментный шейдер к программе
glAttachShader(program, fragment)
# "Собираем" шейдерную программу
glLinkProgram(program)
# Сообщаем OpenGL о необходимости использовать данную шейдерну программу при отрисовке объектов
#glUseProgram(program)
# Запускаем основной цикл
glutMainLoop()
