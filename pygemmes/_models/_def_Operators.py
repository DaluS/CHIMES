import numpy as np

# ######################## OPERATORS ####################################
'''Those are operators that can be used to do multisectoral operations : 
coupling, transposition, sums...'''
class Operators :

    ### Matrix operations (Coupling sectors) ##########################

    # Scalar products 
    def sprod(X,Y):
        ''' Scalar product between vector X and Y.
        Z=sprod(X,Y) so Z_i=\sum X_i Y_i'''
        return np.matmul(np.moveaxis(X,-1,-2),Y)
    def ssum(X):
        ''' Scalar product between vector X and Y.
        Z=ssum(X) so Z_i=\sum X_i'''
        return np.matmul(np.moveaxis(X,-1,-2),X*0+1)
    def ssum2(X):
        '''
        Z_i=ssum_j(X_{ij}) so Z_i=\sum_j X_{ij}'''
        return np.sum(X, axis=-1)[...,np.newaxis]

    # Multiplications
    def transpose(X):
        '''Transposition of X :
        Y=transpose(X)  Y_ij=X_ji'''
        return np.moveaxis(X, -1, -2)
    def matmul(M,V):
        '''Matrix product Z=matmul(M,V) Z_i = \sum_j M_{ij} V_j'''
        return np.matmul(M,V)

    ### Regional operations (Coupling regions) #########################
    def ssumR(X):
        return np.sum(X,axis=-2)[...,np.newaxis]
    def transposeR(X):
        '''Transposition of X :
        Y=transpose(X)  Y_ijk=X_jik'''
        return np.moveaxis(X, -2, -3)
    def Rmatmul(nabla,C):
        '''Matrix product but with the axis of Regions rather than multisectoral'''
        return np.matmul(np.swapaxes(nabla, -3, -1),
                         np.swapaxes(C    , -3, -2))

    ### Matrix generation ##############################################
    def Identity(X):
        '''generate an identity matrix of the same size a matrix X'''
        return np.eye(np.shape(X)[-1])
    def distXY(self,x,y):
        '''x and y vector of position, z=distXY(x,y) is the matrix of distance
        between each particle of position x,y :
        z_ij= \sqrt{ (x_i-x_j)^2 + (y_i-y_j)^2}'''
        return np.sqrt((x - self.transpose(x)) ** 2 + (y - self.transpose(y)) ** 2)


# ########################################################################