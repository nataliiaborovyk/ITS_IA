import numpy as np

import random



def simulazione(num_lanci, campo):

    media = [0]*num_lanci

    res_lancio = np.random.randint(1, campo+1, num_lanci)
    res_lancio2 = np.random.randint(1, campo+1, num_lanci)

    somma = res_lancio + res_lancio2

    facce, fequenza = np.unique(somma, return_counts=True)


        
