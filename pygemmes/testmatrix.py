import numpy as np
M1 = np.array([
#   BRE FLO W+  W-  CER  ENE
    [ 0, 1 , 1 , 0 , 0 , 1 ], # BREAD
    [ 0, 0 , 0 , 0 , 1 , 1 ], # FLOUR
    [ 0, 0 , 0 , 1 , 0 , 1 ], # GOOD WATER
    [ 0, 0 , 0 , 0 , 0 , 0.1 ], # BAD WATER
    [ 0, 0 , 0 , 0 , 0 , 0.1 ], # CEREAL
    [ 0, 0 , 0 , 0 , 0 , .01 ] , # ENERGY
])


I = np.eye(6)

M0 = M1
M2 = np.matmul(M0,M1)
M3 = np.matmul(M0,M2)
M4 = np.matmul(M0,M3)
M5 = np.matmul(M0,M4)
M6 = np.matmul(M0,M5)
M7 = M6-I