#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

from util import MAX_UINT32
from util import logisticmap
from util import _enc_process, _dec_process

def _enc_process( src, ord ):
	dst = np.copy(src)
	dst[ ord ] = src
	return dst
	
def _dec_process( src, ord ):
	return src[ord]
	
class Rand:
	def __init__( self, key ):
		self.key = key
		self.ord = None
		self.roiSize = None
		self.rand_init()
	
	def rand_init( self ):
		self.rand_generator = logisticmap( float(self.key)/MAX_UINT32 * (1.0-2.0E-12 ) + 1.0E-12 )
	
	def rand( self ):
		return self.rand_generator.get()
	
	def setOrd( self, roiSize ):
		if( self.roiSize != roiSize ):
			self.roiSize = roiSize
			self.rand_init()
			self.ord = self.calcOrd()
	
	def process( self, input, func ):
		roiSize = self.calcRoiSize( input )
		self.setOrd( roiSize )
		
		src = np.copy( input[:roiSize[0], :roiSize[1], :] )
		
		src = np.reshape( src, (roiSize[0]*roiSize[1]*roiSize[2]) )
		dst = func( src, self.ord )
		
		output = np.copy( input )
		output[ :roiSize[0], :roiSize[1], : ] = np.reshape( dst, roiSize )
		
		return output
	
	def enc( self, input ):
		return self.process( input, _enc_process )

	def dec( self, input ):
		return self.process( input, _dec_process )
		
		
	######
	def calcRoiSize( self, input ):
		return input.shape

	def calcOrd( self ):
		return np.argsort( np.array( [ self.rand() for i in range(self.roiSize[0] * self.roiSize[1] * self.roiSize[2]) ] ) )


class RandBlock(Rand):
	def __init__( self, key, blockSize ):
		super(RandBlock, self).__init__(key)
		self.blockSize = blockSize

	######
	def calcRoiSize( self, input ):
		inputshape = input.shape
		
		s0 = (inputshape[0] // self.blockSize[0]) * self.blockSize[0]
		s1 = (inputshape[1] // self.blockSize[1]) * self.blockSize[1]
		
		return (s0,s1,inputshape[2])

	def calcOrd( self ):
		imShuffle = Rand( self.key )
		
		ord = np.array( list(range(self.roiSize[0] * self.roiSize[1] * self.roiSize[2])) )
		ord = np.reshape( ord, self.roiSize )
		
		nb_blocks0 = self.roiSize[0] // self.blockSize[0]
		nb_blocks1 = self.roiSize[1] // self.blockSize[1]
		
		for row in range(nb_blocks0):
			for col in range(nb_blocks1):
				ord[row*self.blockSize[0]:(row+1)*self.blockSize[0], col*self.blockSize[1]:(col+1)*self.blockSize[1], :] = \
				imShuffle.enc( ord[row*self.blockSize[0]:(row+1)*self.blockSize[0], col*self.blockSize[1]:(col+1)*self.blockSize[1], :] )
		
		return np.reshape( ord, (self.roiSize[0] * self.roiSize[1] * self.roiSize[2]) )


def genCatMapInd( size, rowroll, colroll, p, q, r ):
	rind = np.reshape( np.array(list(range(size))), (size, 1, 1) )
	rind = np.tile( rind, (1, size, 1) )
	rind = np.roll( rind, rowroll, axis=0 )
	
	cind = np.reshape( np.array(list(range(size))), (1, size, 1) )
	cind = np.tile( cind, (size, 1, 1) )
	cind = np.roll( cind, colroll, axis=1 )
	
	ind = np.concatenate( (rind, cind), axis=2 )
	
	'''
	a00 = 1.
	a01 = p
	a10 = q
	a11 = 1. + p*q
	'''
	
	for i in range(r):
		ind0 = np.copy(ind)
		ind[:,:,0] = np.mod( ind0[:,:,0] + p * ind0[:,:,1], size )
		ind[:,:,1] = np.mod( q * ind0[:,:,0] + (1.+p*q) * ind0[:,:,1], size )
	
	return ind

def genArnoldCatMapInd( size, r ):
	return genCatMapInd( size, 0, 0, 1, 1, r )


class CatMap(Rand):
	def __init__( self, key, Arnold = False, channel_shuffle = True ):
		super(CatMap, self).__init__(key)
		self.Arnold = Arnold
		self.channel_shuffle = channel_shuffle

	######
	def calcRoiSize( self, input ):
		inputshape = input.shape
		s = min( inputshape[0], inputshape[1] )
		return (s,s,inputshape[2])

	def calcOrd( self ):
		ord = np.array( list(range(self.roiSize[0] * self.roiSize[1] * self.roiSize[2])) )
		ord = np.reshape( ord, self.roiSize )
		ord0 = np.copy( ord )

		if( self.channel_shuffle ):
			for row in range(self.roiSize[0]):
				for col in range(self.roiSize[1]):
					roll = int(self.rand()*self.roiSize[2])
					ord0[row,col,:] = np.roll( ord0[row,col,:], roll, axis=0 )
		
		s = self.roiSize[0]
		for cha in range(self.roiSize[2]):
			if( self.Arnold ):
				rowroll = int(self.rand() * s)
				colroll = int(self.rand() * s)
				p = int(self.rand() * s)
				q = int(self.rand() * s)
			else:
				rowroll = 0
				colroll = 0
				p = 1
				q = 1
			
			r = 2 + int(self.rand()*8)
			ind = genCatMapInd( s, rowroll, colroll, p, q, r )
			for row in range(self.roiSize[0]):
				for col in range(self.roiSize[1]):
					row1 = ind[row,col,0]
					col1 = ind[row,col,1]
					ord[row1,col1,cha] = ord0[row,col,cha]
		
		return np.reshape( ord, (self.roiSize[0] * self.roiSize[1] * self.roiSize[2]) )


class CatMapComb(CatMap):
	def __init__( self, key, Arnold = False, channel_shuffle = True ):
		super(CatMapComb, self).__init__(key, Arnold, channel_shuffle )
	
	######
	def calcRoiSize( self, input ):
		inputshape = input.shape
		s = min( inputshape[0], inputshape[1] )
		return (s,s,inputshape[2])
	
	def calcOrd( self ):
		ord = np.array( list(range(self.roiSize[0] * self.roiSize[1] * self.roiSize[2])) )
		ord = np.reshape( ord, self.roiSize )
		ord0 = np.copy( ord )
		
		s = self.roiSize[0] // 2
		
		imShuffle = CatMap( self.rand()*MAX_UINT32, self.Arnold, self.channel_shuffle )
		ord[:s, :s, :] = imShuffle.enc( ord[:s, :s, :] )
		
		imShuffle = CatMap( self.rand()*MAX_UINT32, self.Arnold, self.channel_shuffle )
		ord[:s, -s:, :] = imShuffle.enc( ord[:s, -s:, :] )

		imShuffle = CatMap( self.rand()*MAX_UINT32, self.Arnold, self.channel_shuffle )
		ord[-s:, :s, :] = imShuffle.enc( ord[-s:, :s, :] )
		
		imShuffle = CatMap( self.rand()*MAX_UINT32, self.Arnold, self.channel_shuffle )
		ord[-s:, -s:, :] = imShuffle.enc( ord[-s:, -s:, :] )

		ind0 = range(0, self.roiSize[0], 2 )
		ind1 = range(1, self.roiSize[0], 2 )
		
		ord0 = np.copy( ord )
		ord[ind0, :, :] = ord0[:len(ind0), :, :]
		ord[ind1, :, :] = ord0[len(ind0):, :, :]

		ord0 = np.copy( ord )
		ord[:, ind0, :] = ord0[:, :len(ind0), :]
		ord[:, ind1, :] = ord0[:, len(ind0):, :]

		imShuffle = CatMap( self.rand()*MAX_UINT32, self.Arnold, self.channel_shuffle )
		ord = imShuffle.enc( ord )


		return np.reshape( ord, (self.roiSize[0] * self.roiSize[1] * self.roiSize[2]) )
