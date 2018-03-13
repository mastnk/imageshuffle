#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

from util import MAX_UINT32, MAX_UINT8
from util import logisticmap
from util import _enc_process, _dec_process
from util import split_uint8, join_uint8

import imageshuffle

class Rand:
	def __init__( self, key, bit_split = False ):
		self.key = key
		self.ord = None
		self.rev = None
		self.roiSize = None
		self.bit_split = bit_split
		self.rand_init()
		
	
	def rand_init( self ):
		self.rand_generator = logisticmap( float(self.key)/MAX_UINT32 * (1.0-2.0E-12 ) + 1.0E-12 )
	
	def rand( self ):
		return self.rand_generator.get()
	
	def setOrdRev( self, roiSize ):
		if( self.roiSize != roiSize ):
			self.roiSize = roiSize
			self.rand_init()
			self.ord, self.rev = self.calcOrdRev()
	
	def process( self, input, func, rev_max ):
		assert( input.dtype == np.uint8 )
		roiSize = self.calcRoiSize( input )
		self.setOrdRev( roiSize )
		
		src = np.copy( input[:roiSize[0], :roiSize[1], :] )
		
		src = np.reshape( src, (roiSize[0]*roiSize[1]*roiSize[2]) )
		
		src[ self.rev ] = rev_max - src[ self.rev ]
		dst = func( src, self.ord )
		dst[ self.rev ] = rev_max - dst[ self.rev]
		
		output = np.copy( input )
		output[ :roiSize[0], :roiSize[1], : ] = np.reshape( dst, roiSize )
		
		return output
	
	def enc( self, input ):
		if( self.bit_split ):
			return join_uint8( self.process( split_uint8( input ), _enc_process, 15 ) )
		else:
			return self.process( input, _enc_process, 255 )

	def dec( self, input ):
		if( self.bit_split ):
			return join_uint8( self.process( split_uint8( input ), _dec_process, 15 ) )
		else:
			return self.process( input, _dec_process, 255 )
		
		
	######
	def calcRoiSize( self, input ):
		return input.shape

	def calcOrdRev( self ):
		ord = np.argsort( np.array( [ self.rand() for i in range(self.roiSize[0] * self.roiSize[1] * self.roiSize[2]) ] ) )
		rev = np.array( [ self.rand() for i in range(self.roiSize[0] * self.roiSize[1] * self.roiSize[2]) ] ) > 0.5
		return  ( ord, rev )


class RandBlock(Rand):
	def __init__( self, key, blockSize, ord2rev = True, rev_ratio = 0.5, bit_split = False  ):
		super(RandBlock, self).__init__(key, bit_split)
		self.blockSize = blockSize
		self.ord2rev = ord2rev
		self.rev_ratio = rev_ratio

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
		
		_rev = np.array( list(range(self.blockSize[0] * self.blockSize[1] * self.roiSize[2])) ) > self.rev_ratio
		_rev = np.reshape( _rev, (self.blockSize[0], self.blockSize[1], self.roiSize[2]) )
		
		for row in range(nb_blocks0):
			for col in range(nb_blocks1):
				ord[row*self.blockSize[0]:(row+1)*self.blockSize[0], col*self.blockSize[1]:(col+1)*self.blockSize[1], :] = \
				imShuffle.enc( ord[row*self.blockSize[0]:(row+1)*self.blockSize[0], col*self.blockSize[1]:(col+1)*self.blockSize[1], :] )
				
				if( self.ord2rev ):
					_rev = imShuffle.ord > imShuffle.ord.size * self.rev_ratio
					_rev = np.reshape( _rev, (self.blockSize[0], self.blockSize[1], self.roiSize[2]) )
					rev[row*self.blockSize[0]:(row+1)*self.blockSize[0], col*self.blockSize[1]:(col+1)*self.blockSize[1], :] = \
					_rev
				else:
					rev[row*self.blockSize[0]:(row+1)*self.blockSize[0], col*self.blockSize[1]:(col+1)*self.blockSize[1], :] = \
					_rev
		
		ord = np.reshape( ord, (self.roiSize[0] * self.roiSize[1] * self.roiSize[2]) )
		rev = np.reshape( rev, (self.roiSize[0] * self.roiSize[1] * self.roiSize[2]) )
		
		return ord, rev
