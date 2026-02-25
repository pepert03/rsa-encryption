from re import X
import numpy as np                      # importamos las librerías necesarias
from math import sqrt
import time
 
def es_primo(n):                        # funcion que comprueba si un número es primo o no
    if n==2:
        return True
    if not n%2:
        return False
    for i in range(3,int(sqrt(n))+1,2): # este bucle comprueba si es divisible entre los impares desde el 3 hasta la raiz de n
        if n%i==0:                      # en cuanto n sea divisibke entre i, devuelve que n no es primo
            return False                
    return True                         #si no se da el caso, significa que n es primo
 
 
def lista_primos(inicio, fin):          # lista los numeros primos entre inicio y fin
    a = [1 for _ in range(fin)]         # crea una lista de unos
    a[0],a[1]=0,0                       # 0 y 1 se introducen directamente por su multiplicidad 0*i=0 , 1*p = p por lo cual no queremos contarlo como divisor
    contador=2
    tope = sqrt(fin)                    # no hace falta recorrer todo fin, basta con recorrerlo hasta raiz(fin) por el teorema de la cota para divisores primos
    while contador<tope:
        if a[contador]==0:              # si es un número compuesto (0)
            contador+=1                 # no hace nada
        else:
            i=2                         # si no es comuesto significa que es primo
            while i*contador < fin:       # se marcaran todos los múltiplos de este primo como compuestos (0)
                a[i*contador]=0         # de esta manera los ceros son multiplos de algún primo inferior,
                i+=1                    # y los 1 significan que ningún número por debajo lo divide, marcandolo como primo
            contador+=1                
    sol = []                            # se convierte la lista de 1s y 0s en lista de primos guardando el índice
    for prime in range(inicio,len(a)):  # de cada uno de los unos de la lista original
        if a[prime] == 1:
            sol.append(prime)
    return sol
 

def f(x,c,n):
    return (x**2 + c)%n


def rho(n):
    # es eficiente a partir de n = 10**6
    fracaso = True
    c = 1
    while fracaso:
        x,y,d = 2,2,1
        while d == 1: # hace una secuencia pseudoaleatoria de x hasta que se encuentre un divisor de n
            x = f(x,c,n)
            y = f(f(y,c,n),c,n)
            d = mcd(abs(x-y),n)
        if d == n:
            if c == 100:
                fracaso = False
            c += 1
        else:
            fracaso = False
    return d 


def factorizar(n):                      # factorizar el número n en sus factores primos
    factores = {}                       # inicialmente es un diccionario vacío
    if n < 10**7:
        for i in range(2,int(n/2)+1):       # el tope es n entre dos, ya que cualquier número y por encima de esa cota debería ser
            while n % i == 0 and n!=1:      # multiplicado por 1.xxx para dar n, == la division entera n/y dejaría resto
                factores[i] = factores.get(i, 0)+1
                n//=i                       # se reduce el número del que buscamos factores a medida que los vamos encontrando
        if not factores:                    # hasta que n equivale a uno
            factores[n] = factores.get(n, 0)+1 # si no se encuentra ningún factor, el número mismo es primo
    else:
        while n != 1:
            d = rho(n)
            n //= d
            if es_primo(n):
                factores[n] = factores.get(n, 0)+1
                n = 1
            factores[d] = factores.get(d, 0)+1
    return factores
 
 
def mcd(a, b):                          # funcion que encuentra el mínimo común múltiplo de a y b
    n = a if a>b else b                 # se utiliza el algoritmo de Euclídes, que reduce a y b usándo el módulo
    m = b if a>b else a                 # de a y b reiteradamente hasta que uno de los dos es 0, momento en el cual
    while m != 0:                       # devuelve el resto final, que será el mínimo común múltiplo de a y b
        n,m = m,n%m
    return n

 
def bezout(a, b):                       # bezout busca la solución a la ecuación xa + yb = (a,b)
    n = a if a>b else b                 # se utiliza también el algoritmo de Euclídes pero en este caso
    m = b if a>b else a                 # se guardan las opercaiones necesarias para sacar x e y en un vector
    v_n,v_m = np.array([1,0],dtype=object),np.array([0,1],dtype=object)
    while m != 0:
        x = n//m
        n,m = m,n%m
        v_n,v_m = v_m,v_n-(x*v_m)
    if a>b:
        return n,v_n[0],v_n[1]
    else:
        return n,v_n[1],v_n[0]
 
 
def coprimos(a, b):                     # funcion que verifica si a y b son coprimos entre si,  
    if mcd(a, b) == 1:                  # lo cual será verdad si mcd(a,b) = 1
        return True
    else:
        return False
 
 
def potencia_mod_p(base, exp, p):       # funcion que devuelve la potencia de una base en módulo p
    if exp < 0: 
        base = inversa_mod_p(base, p)
        exp = -exp        
    if exp == 0:
        return 1
    n = 1
    while exp > 0:                      # si exp es par, se eleva la base al cuadrado y se divide exp entre dos
        if exp % 2 == 0:
            base = (base * base) % p
            exp = exp//2
        else:                           # si exp es impar, guarda la base en n y se reduce exp en uno
            n *= base
            exp -= 1
    return n % p


def inversa_mod_p(n, p):                # funcion que devuelve la inversa de un número en módulo p
    (d, x, y) = bezout(n, p)            # se utiliza el algoritmo de bezout para encontrar la solución (la x en modulo p)
    if d == 1:
        return x % p
    else:
        return None
 
 
def euler(n):                           # funcion que devuelve cuantos números coprimos tiene n en (0,n)
    dik=factorizar(n)                   # en el intervalo (0,n)
    exp=list(dik.values())[0]          
    b=list(dik.keys())[0]               # utilizaremos el diccionario de factorizar n
    if len(dik)==1:                     # si el número es primo o potencia de primo solo tendrá un factor
        if exp==1:                      # si es primo, el factor esta elevado a 1 y la formula es b-1
            return b-1
        else:
            return (b-1)*(b**(exp-1))   # si es potencia de primo, devuelve esta expresión
       
    else:                                           # si es compuesto, descomponémos el número en partes coprimas
        return euler(int(n/(b**exp)))*euler(b**exp) # para usar la propiedad; Euler(nm) = Euler(n)Euler(m).Si (n,m)=1


def legendre(n, p):                       # funcion que devuelve el símbolo de legendre de n en módulo p
    if potencia_mod_p(n, (p-1)//2, p) == p-1:
        return -1 
    else:
        return potencia_mod_p(n, (p-1)//2, p) # utilizando el criterio de Euler
 
 
def resolver_sistema_congruencias(alist, blist, plist):   # funcion que resuelve un sistema de congruencias 
    N = 1                                                 # ai*x = bi (mod pi) -> x = bi/ai (mod pi)
    for p in plist:                                       # mediante el teoremade chino del resto
        N *= p                                            # se calcula el producto de todos los modulos
    x = 0
    for i in range(len(plist)):                           # x = sumatorio de bi/ai * Ni * xi (mod pi)
        Ni = N//plist[i]
        xi = inversa_mod_p(Ni, plist[i])
        x += blist[i]*Ni*xi/alist[i]
    return int(x % N), N
 

def raiz_mod_p(n, p):
    if legendre(n, p) != 1:                               # si el símbolo de legendre de n en módulo p es distinto de 1
        return None                                       # no existe raíz cuadrada de n en módulo p
    for i in range(1,p):                                  # algoritmo de Cipolla
        if legendre((i*i-n),p)==-1:
            a = i                                         # se busca un número a tal que (a^2-n) no sea un cuadrado
            w = (a*a-n)**(1/2)
            break
    x = ((a + w) ** ((p + 1) // 2))                       
    
    if type(x) == complex:
        try:
            x = float(str(x).split("(")[1].split("+")[0].split("-")[0])
        except:
            x = float(str(x).split("(")[1].split("+")[0])
    x = int(round(x))
    return x%p 


def ecuacion_cuadratica(a, b, c, p):
    x = (-b+raiz_mod_p((b**2-4*a*c)%p,p))//(2*a)
    y = (-b-raiz_mod_p((b**2-4*a*c)%p,p))//(2*a)
    return x%p,y%p

for x in range(7):
    print(legendre(x,7))