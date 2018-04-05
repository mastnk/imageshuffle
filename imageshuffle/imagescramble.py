#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

from imageshuffle.util import MAX_UINT32, MAX_UINT8
from imageshuffle.util import logisticmap
from imageshuffle.util import _enc_process, _dec_process
from imageshuffle.util import split_uint8, join_uint8

from imageshuffle import imageshuffle

REV_NONE = 0
REV_RAND = 1
REV_ORD  = 2

class Rand:
	def __init__( self, key, nb_bits = 4, rev_mode = REV_ORD, rev_ratio = 0.5 ):
		self.key = key
		self.ord = None
		self.rev = None
		self.roiSize = None
		self.nb_bits = nb_bits
		self.rev_mode = rev_mode
		self.rev_ratio = rev_ratio
		self.rand_init()
		
		if( self.rev_ratio < 0 ):
			self.rev_ratio = 0
		if( self.rev_ratio > 1 ):
			self.rev_ratio = 1
		
		if( self.rev_mode < 0 or self.rev_mode > 2 ):
			msg = 'rev_mode should be 0, 1, or 2. (REV_NONE, REV_RADND, or REV_ORD)'
			raise ValueError(msg)
		
		
		if( nb_bits == 1 ):
			self.rev_max = 1
		elif( nb_bits == 2 ):
			self.rev_max = 3
		elif( nb_bits == 4 ):
			self.rev_max = 15
		elif( nb_bits == 8 ):
			self.rev_max = 255
		else:
			msg = 'nb_bits is {nb_bits:d}, but it should be 1, 2, 4, or 8.'.format(nb_bits=nb_bits)
			raise ValueError(msg)
		
	
	def rand_init( self ):
		self.rand_generator = logisticmap( float(self.key)/MAX_UINT32 * (1.0-2.0E-12 ) + 1.0E-12 )
	
	def rand( self ):
		return self.rand_generator.get()
	
	def setOrdRev( self, roiSize ):
		if( self.roiSize != roiSize ):
			self.roiSize = roiSize
			self.rand_init()
			self.ord, self.rev = self.calcOrdRev()
	
	def process( self, input, func ):
		assert( input.dtype == np.uint8 )
		roiSize = self.calcRoiSize( input )
		self.setOrdRev( roiSize )
		
		src = np.copy( input[:roiSize[0], :roiSize[1], :] )
		
		src = np.reshape( src, (roiSize[0]*roiSize[1]*roiSize[2]) )
		
		if( self.rev_mode > 0 ):
			src[ self.rev ] = self.rev_max - src[ self.rev ]

		dst = func( src, self.ord )

		if( self.rev_mode > 0 ):
			dst[ self.rev ] = self.rev_max - dst[ self.rev]
		
		output = np.copy( input )
		output[ :roiSize[0], :roiSize[1], : ] = np.reshape( dst, roiSize )
		
		return output
	
	def enc( self, input ):
		return join_uint8( self.process( split_uint8( input, self.nb_bits ), _enc_process ), self.nb_bits )

	def dec( self, input ):
		return join_uint8( self.process( split_uint8( input, self.nb_bits ), _dec_process ), self.nb_bits )
		
	######
	def calcRoiSize( self, input ):
		return input.shape

	def calcOrdRev( self ):
		ord = np.argsort( np.array( [ self.rand() for i in range(self.roiSize[0] * self.roiSize[1] * self.roiSize[2]) ] ) )
		
		if( self.rev_mode == REV_ORD ):
			rev = ( ord > self.roiSize[0] * self.roiSize[1] * self.roiSize[2] * self.rev_ratio )
		else:
			rev = np.array( [ self.rand() for i in range(self.roiSize[0] * self.roiSize[1] * self.roiSize[2]) ] ) > self.rev_ratio
			
		return  ( ord, rev )


class RandBlock(Rand):
	def __init__( self, key, blockSize, nb_bits = 4, rev_mode = REV_ORD, rev_ratio = 0.5 ):
		super(RandBlock, self).__init__(key, nb_bits, rev_mode, rev_ratio )
		self.blockSize = blockSize

	######
	def calcRoiSize( self, input ):
		inputshape = input.shape
		
		s0 = (inputshape[0] // self.blockSize[0]) * self.blockSize[0]
		s1 = (inputshape[1] // self.blockSize[1]) * self.blockSize[1]
		
		return (s0,s1,inputshape[2])

	def calcOrdRev( self ):
		imShuffle = imageshuffle.Rand( self.key )
		
		ord = np.array( list(range(self.roiSize[0] * self.roiSize[1] * self.roiSize[2])) )
		ord = np.reshape( ord, self.roiSize )
		
		rev = np.array( [False] * self.roiSize[0] * self.roiSize[1] * self.roiSize[2] )
		rev = np.reshape( rev, self.roiSize )
		
		nb_blocks0 = self.roiSize[0] // self.blockSize[0]
		nb_blocks1 = self.roiSize[1] // self.blockSize[1]
		
		if( self.rev_mode == REV_ORD ):
			row=0
			col=0
			imShuffle.enc( ord[row*self.blockSize[0]:(row+1)*self.blockSize[0], col*self.blockSize[1]:(col+1)*self.blockSize[1], :] )
			_rev = imShuffle.ord > imShuffle.ord.size * self.rev_ratio
			_rev = np.reshape( _rev, (self.blockSize[0], self.blockSize[1], self.roiSize[2]) )
			
		else:
			_rev = np.array( [ self.rand() for i in range(self.blockSize[0] * self.blockSize[1] * self.roiSize[2]) ] ) > self.rev_ratio
			_rev = np.reshape( _rev, (self.blockSize[0], self.blockSize[1], self.roiSize[2]) )
		
		for row in range(nb_blocks0):
			for col in range(nb_blocks1):
				ord[row*self.blockSize[0]:(row+1)*self.blockSize[0], col*self.blockSize[1]:(col+1)*self.blockSize[1], :] = \
				imShuffle.enc( ord[row*self.blockSize[0]:(row+1)*self.blockSize[0], col*self.blockSize[1]:(col+1)*self.blockSize[1], :] )
				
				rev[row*self.blockSize[0]:(row+1)*self.blockSize[0], col*self.blockSize[1]:(col+1)*self.blockSize[1], :] = _rev
		
		ord = np.reshape( ord, (self.roiSize[0] * self.roiSize[1] * self.roiSize[2]) )
		rev = np.reshape( rev, (self.roiSize[0] * self.roiSize[1] * self.roiSize[2]) )
		
		return ord, rev
