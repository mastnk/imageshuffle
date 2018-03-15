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

def split_uint8(X):
	assert(X.dtype == np.uint8)
	X1 = X >> 4
	X0 = X & 0x0F
	return np.concatenate( (X1, X0), axis=2 )

def join_uint8(X):
	assert(X.dtype == np.uint8)
	assert(X.shape[2] % 2 == 0)
	s = X.shape[2]//2
	X1 = X[:,:,:s]
	X0 = X[:,:,s:]
	return ( X1 << 4 ) + X0
