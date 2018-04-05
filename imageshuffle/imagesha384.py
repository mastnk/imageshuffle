#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import hashlib


def md5( data ):
	b0 = hashlib.md5(data[  0:128]).digest()
	b1 = hashlib.md5(data[128:256]).digest()
	b2 = hashlib.md5(data[256:384]).digest()
	
	return bytes( bytearray(b0) + bytearray(b1) + bytearray(b2) )

def shake128( data ):
	return hashlib.shake_128(data).digest(48) # 48 bytes = 384 bits

def shake256( data ):
	return hashlib.shake_256(data).digest(48) # 48 bytes = 384 bits

def sha384( data ):
	return hashlib.sha384(data).digest()

def sha3_384( data ):
	return hashlib.sha3_384(data).digest()

def dec( src, salt = None, sha = 'sha2' ):
	assert( src.shape[0] % 4 == 0 )
	assert( src.shape[1] % 4 == 0 )
	assert( src.shape[2] == 3 )
	assert( src.dtype == np.uint8 )
	
	if( salt is not None ):
		x = salt
		salt = []
		while( x > 0 ):
			salt.append( x % 256 )
			x = x // 256
		salt = np.asarray( salt, dtype=np.uint8 )
	
	if( sha.lower() == 'sha3' ):
		sha_func = sha3_384
	elif( sha.lower() == 'sha2' ):
		sha_func = sha384
	elif( sha.lower() == 'md5' ):
		sha_func = md5
	elif( sha.lower() == 'shake256' ):
		sha_func = shake256
	elif( sha.lower() == 'shake128' ):
		sha_func = shake128
	else:
		msg = 'Unsported algorithm: {}'.format(sha)
		raise ValueError(msg)
	
	s = src.shape
	nb_blocks0 = s[0] // 4
	nb_blocks1 = s[1] // 4
	
	dst = np.zeros( s, dtype=np.uint8 )
	for r in range(nb_blocks0):
		for c in range(nb_blocks1):
			data = np.reshape( src[ r*4:(r+1)*4, c*4:(c+1)*4, : ], [4*4*3] )
			if( salt is not None ):
				data = np.concatenate((salt,data))
			data = sha_func( data )
			data = np.asarray( bytearray(data), dtype=np.uint8 )
			dst[ r*4:(r+1)*4, c*4:(c+1)*4, : ] = np.reshape( data, [4,4,3] )
	return dst
