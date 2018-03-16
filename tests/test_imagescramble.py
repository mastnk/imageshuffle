#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from imageshuffle import imagescramble

import numpy as np
from PIL import Image


write_image = 'SC_'
#write_image = None

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
	def test_Rand(self):
		ar0 = self.ar
		
		imScramble = imagescramble.Rand( 567 )
		
		roiSize = imScramble.calcRoiSize( ar0 )
		self.assertEqual( roiSize, (512,512,3) )
		
		ar1 = imScramble.enc( ar0 )
		ar2 = imScramble.dec( ar1 )
		
		if( write_image is not None ):
			Image.fromarray( ar0 ).save( write_image+'Rand0.png' )
			Image.fromarray( ar1 ).save( write_image+'Rand1.png' )
			Image.fromarray( ar2 ).save( write_image+'Rand2.png' )
		
		self.assertTrue( ( ar0 == ar2 ).all() )

###################################################################
	def test_RandBlock(self):
		ar0 = self.ar
		
		imScramble = imagescramble.RandBlock( 567, (8,8), ord2rev = False )
		
		roiSize = imScramble.calcRoiSize( ar0 )
		self.assertEqual( roiSize, (512,512,3) )
		
		ar1 = imScramble.enc( ar0 )
		ar2 = imScramble.dec( ar1 )
		if( write_image is not None ):
			Image.fromarray( ar0 ).save( write_image+'RandBlock0.png' )
			Image.fromarray( ar1 ).save( write_image+'RandBlock1.png' )
			Image.fromarray( ar2 ).save( write_image+'RandBlock2.png' )		
		self.assertTrue( ( ar0 == ar2 ).all() )
		
		imScramble = imagescramble.RandBlock( 123, (7,9), ord2rev = True )
		ar1 = imScramble.enc( ar0 )
		ar2 = imScramble.dec( ar1 )
		if( write_image is not None ):
			Image.fromarray( ar1 ).save( write_image+'RandBlock3.png' )
			Image.fromarray( ar2 ).save( write_image+'RandBlock4.png' )
		self.assertTrue( ( ar0 == ar2 ).all() )

		imScramble = imagescramble.RandBlock( 123, (7,9), ord2rev = True, bit_split = True )
		ar1 = imScramble.enc( ar0 )
		ar2 = imScramble.dec( ar1 )
		if( write_image is not None ):
			Image.fromarray( ar1 ).save( write_image+'RandBlock5.png' )
			Image.fromarray( ar2 ).save( write_image+'RandBlock6.png' )
		self.assertTrue( ( ar0 == ar2 ).all() )
		


###################################################################
	def suite():
		suite = unittest.TestSuite()
		suite.addTests(unittest.makeSuite(test_ImageShffleRand))
		return suite
  
if( __name__ == '__main__' ):
	unittest.main()
