#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import math

MAX_UINT8 = 255
MAX_UINT16 = 65535
MAX_UINT32 = 4294967295

def _logisticmap( x0, a=4-1E-12, init_itr=100 ):
	x = x0
	for i in range(init_itr):
		x = a*x*(1-x)
	while( True ):
		x = a*x*(1-x)
		yield x

class logisticmap:
	def __init__( self, x0, a=4-1E-12, init_itr=100 ):
		self.generator = _logisticmap( x0, a, init_itr )
	def get( self ):
		return self.generator.__next__()

def _enc_process( src, ord ):
	dst = np.copy(src)
	dst[ ord ] = src
	return dst
	
def _dec_process( src, ord ):
	return src[ord]

def paddingBlockSize( X, blockSize ):
	s = X.shape
	
	t = s[0] / blockSize[0]
	d = t - math.floor(t)
	if( d > 0 ):
		paddingSize = blockSize[0] * ( math.floor(t) + 1 ) - s[1]
		padding = X[-1:,:,:]
		padding = np.tile( padding, (paddingSize, 1, 1 ) )
		X = np.concatenate( (X, padding), axis = 0 )

	t = s[1] / blockSize[1]
	d = t - math.floor(t)
	if( d > 0 ):
		paddingSize = blockSize[1] * ( math.floor(t) + 1 ) - s[2]
		padding = X[:,-1:,:]
		padding = np.tile( padding, (1, paddingSize, 1 ) )
		X = np.concatenate( (X, padding), axis = 1 )
	
	return X	

def split_uint8(X, nb_bits):
	assert(X.dtype == np.uint8)
	
	if( nb_bits == 1 ):
		X7 = X >> 7
		X6 = X >> 6
		X5 = X >> 5
		X4 = X >> 4
		X3 = X >> 3
		X2 = X >> 2
		X1 = X >> 1
		Y = np.concatenate( (X7, X6, X5, X4, X3, X2, X1, X), axis=-1 ) & 0x01
		
	elif( nb_bits == 2 ):
		X6 = X >> 6
		X4 = X >> 4
		X2 = X >> 2
		Y = np.concatenate( (X6, X4, X2, X), axis=-1 ) & 0x03
	
	elif( nb_bits == 4 ):
		X4 = X >> 4
		Y = np.concatenate( (X4, X), axis=-1 ) & 0x0F

	elif( nb_bits == 8 ):
		Y = np.copy(X)
		
	else:
		raise ValueError('Invalide value of nb_bits: {nb_bits:d}'.format(nb_bits=nb_bits))
	
	return Y

def join_uint8(X, nb_bits):
	assert(X.dtype == np.uint8)
	
	s0 = X.shape
	N = np.prod(s0[:-1])
	Z = np.reshape(X, (N,s0[-1]))
	
	if( nb_bits == 1 ):
		if( X.shape[-1] % 8 != 0 ):
			msg = 'X.shape[-1] should be multiples of 8. But, it is {}.'.format(X.shape[-1])
			raise ValueError(msg)
			
		s = X.shape[-1]//8
	
		Z7 = Z[:,   :s]
		Z6 = Z[:,  s:2*s]
		Z5 = Z[:,2*s:3*s]
		Z4 = Z[:,3*s:4*s]
		Z3 = Z[:,4*s:5*s]
		Z2 = Z[:,5*s:6*s]
		Z1 = Z[:,6*s:7*s]
		Z0 = Z[:,7*s:]
		Y = ( Z7 << 7 ) + ( Z6 << 6 ) + ( Z5 << 5 ) + ( Z4 << 4 ) + ( Z3 << 3 ) + ( Z2 << 2 ) + ( Z1 << 1 ) + Z0
		
	elif( nb_bits == 2 ):
		if( X.shape[-1] % 4 != 0 ):
			msg = 'X.shape[-1] should be multiples of 4. But, it is {}.'.format(X.shape[-1])
			raise ValueError(msg)

		s = X.shape[-1]//4

		Z6 = Z[:,   :s]
		Z4 = Z[:,  s:2*s]
		Z2 = Z[:,2*s:3*s]
		Z0 = Z[:,3*s:4*s]
		Y = ( Z6 << 6 ) + ( Z4 << 4 ) + ( Z2 << 2 ) + Z0
	
	elif( nb_bits == 4 ):
		if( X.shape[-1] % 2 != 0 ):
			msg = 'X.shape[-1] should be multiples of 2. But, it is {}.'.format(X.shape[-1])
			raise ValueError(msg)

		s = X.shape[-1]//2

		Z4 = Z[:,:s]
		Z0 = Z[:,s:]
		Y = ( Z4 << 4 ) + Z0

	elif( nb_bits == 8 ):
		return np.copy(X)
		
	else:
		raise ValueError('Invalide value of nb_bits: {nb_bits:d}'.format(nb_bits=nb_bits))

	Y = np.reshape( Y, s0[:-1]+(s,) )

	return Y
