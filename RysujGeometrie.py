import numpy as np
import matplotlib.pyplot as plt

def RysujGeometrie(NODES, ELEMS, WB):
   
    fh = plt.figure()

    plt.plot(NODES[:,1], np.zeros( (np.shape(NODES)[0], 1) ), '-b|' )
        
    nodeNo = np.shape(NODES)[0]
        
    for ii in np.arange(0,nodeNo):
        
        ind = NODES[ii,0]
        x = NODES[ii,1]
        plt.text(x, 0.01, str( int(ind) ), c="b")
        plt.text(x, -0.01, str(x))
     
    elemNo = np.shape(ELEMS)[0]
    for ii in np.arange(0,elemNo):

        wp = ELEMS[ii,1]
        wk = ELEMS[ii,2]

        x = (NODES[wp-1,1] + NODES[wk-1,1] ) / 2  
        plt.text(x, 0.01, str(ii+1), c="r")

    plt.show()
    return fh
