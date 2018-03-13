#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

import util
import imageshuffle

import numpy as np
from PIL import Image


write_image = True

class test_ImageShffleRand( unittest.TestCase ):
###################################################################
	@classmethod
	def setUpClass(cls): # it is called before test starting
		pass

	@classmethod
	def tearDownClass(cls): # it is called before test ending
		pass

	def setUp(self): # it is called before each test
		im = Image.open('tests/lena.png')
		self.ar = np.asarray( im )
		pass

	def tearDown(self): # it is called after each test
		pass
                
###################################################################
	def test_logisticmap(self):
		key = 123
		
		myrand = util.logisticmap( float(key)/4294967295.0 * (1.0-2.0E-12 ) + 1.0E-12 )
		imShffule = imageshuffle.Rand( key )
		imShffule.rand_init()

		for i in range(10):
			self.assertTrue( myrand.get() == imShffule.rand() )

	def test_enc_dec_process(self):
		src = np.array(list(range(8)))
		ord = [4,5,6,7, 0,1,2,3]
		dst = np.zeros( (8) )
		rec = np.zeros( (8) )
		
		dst = util._enc_process( src, ord )
		rec = util._dec_process( dst, ord )

		self.assertTrue( ( dst == ord ).all() )
		self.assertTrue( ( rec == src ).all() )

	def test_paddingBlockSize(self):
		X = np.array(list(range(16)))
		X = np.reshape( X, (4,4,1) )
		
		blockSize = (3,2)
		XX = util.paddingBlockSize( X, blockSize )
		
		YY = np.array( [ 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,12,13,14,15,12,13,14,15] )
		YY = np.reshape( YY, (6,4,1) )
		
		self.assertEqual( XX.shape, (6,4,1) )
		self.assertTrue( (XX == YY).all() )

	def test_uint8(self):
		X = np.array( [0x00, 0x01, 0x10, 0x11], dtype=np.uint8 )
		X = np.reshape( X, (2,2,1) )
		
		XX = util.split_uint8( X )
		Y = util.join_uint8( XX )
		
		YY0 = np.reshape( np.array([0,0,1,1], dtype=np.uint8), (2,2))
		YY1 = np.reshape( np.array([0,1,0,1], dtype=np.uint8), (2,2))
		
		self.assertTrue( (XX[:,:,0] == YY0).all() )
		self.assertTrue( (XX[:,:,1] == YY1).all() )
		self.assertTrue( (X == Y).all() )
		

###################################################################
	def suite():
		suite = unittest.TestSuite()
		suite.addTests(unittest.makeSuite(test_ImageShffleRand))
		return suite
  
if( __name__ == '__main__' ):
	unittest.main()
