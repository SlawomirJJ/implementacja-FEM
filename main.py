import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as spint

from GeoDef import *
from AutomatycznyGeneratorGeometrii import *
from RysujGeometrie import *
from Alokacja import *
from FunkcjeBazowe import *
from Aij import *
from RysujRozwiazanie import *

if __name__ == '__main__':
    
    
    ## parametry sterujace
    c = 0 
    f = lambda x: 0*x # wymuszenie


    #Geometria
    #   Definicja
    # WEZLY, ELEMENTY, WB = GeoDef()
    # n = np.shape(WEZLY)[0]
    
    # Automatyczne wygenerowanie geometrii   
    x_a =  0 
    x_b =  1
    n = 15
    WEZLY, ELEMENTY = AutomatycznyGeneratorGeometrii(x_a,x_b,n)
    
    WB    = [{"ind": 1, "typ":'D', "wartosc":1}, 
              {"ind": n, "typ":'D', "wartosc":2}]
    
    
    RysujGeometrie(WEZLY, ELEMENTY, WB)


    A,b = Alokacja(n)
    
    stopien_fun_bazowych = 1
    phi, dphi = FunkcjeBazowe(stopien_fun_bazowych)
    
    #PROCESSING

    
    for ee in np.arange(0, np.shape(ELEMENTY)[0] ):
        
        elemRowInd = ee
        elemGlobalInd = ELEMENTY[ee,0]        
        elemWezel1 = ELEMENTY[ee,1]     # indeks wezla poczatkowego elemntu ee
        elemWezel2 = ELEMENTY[ee,2]     # indeks wezla koncowego elemntu ee
        indGlobalneWezlow = np.array([elemWezel1, elemWezel2 ])
    
        x_a = WEZLY[ elemWezel1-1 ,1]
        x_b = WEZLY[ elemWezel2-1 ,1]
        
        Ml = np.zeros( [stopien_fun_bazowych+1, stopien_fun_bazowych+1] )
        
        J = (x_b-x_a)/2
        
        m = 0; n = 0 ;
        Ml[m,n] = J * spint.quad( Aij(dphi[m], dphi[n], c, phi[m],phi[n]), -1, 1)[0]
        
        m = 0; n = 1 ;
        Ml[m,n] = J * spint.quad( Aij(dphi[m], dphi[n], c, phi[m],phi[n]), -1, 1)[0]
        
        m = 1; n = 0 ;
        Ml[m,n] = J * spint.quad( Aij(dphi[m], dphi[n], c, phi[m],phi[n]), -1, 1)[0]
        
        m = 1; n = 1 ;
        Ml[m,n] = J * spint.quad( Aij(dphi[m], dphi[n], c, phi[m],phi[n]), -1, 1)[0]
                
       
        A[np.ix_(indGlobalneWezlow-1, indGlobalneWezlow-1  ) ] =  \
            A[np.ix_(indGlobalneWezlow-1, indGlobalneWezlow-1  ) ] + Ml

        
        
    print(WB)
        
    
    # UWZGLEDNIENIE WARUNKOW BRZEGOWYCH
    if WB[0]['typ'] == 'D':
        ind_wezla = WB[0]['ind']
        wart_war_brzeg = WB[0]['wartosc']
        
        iwp = ind_wezla - 1
        
        WZMACNIACZ = 10**14
        
        b[iwp] = A[iwp,iwp]*WZMACNIACZ*wart_war_brzeg
        A[iwp, iwp] = A[iwp,iwp]*WZMACNIACZ
        
        
    if WB[1]['typ'] == 'D':
        ind_wezla = WB[1]['ind']
        wart_war_brzeg = WB[1]['wartosc']
        
        iwp = ind_wezla - 1
        
        WZMACNIACZ = 10**14
        
        b[iwp] = A[iwp,iwp]*WZMACNIACZ*wart_war_brzeg
        A[iwp, iwp] = A[iwp,iwp]*WZMACNIACZ        
       
    
    
    # Rozwiazanie ukladu rownan liniowych    
    u = np.linalg.solve(A,b)
    
    RysujRozwiazanie(WEZLY, ELEMENTY, WB, u)
    
    
    
    
    