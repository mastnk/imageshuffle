#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

import imageshuffle

import numpy as np
from PIL import Image


write_image = 'SH_'
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
		
		imShuffle = imageshuffle.Rand( 567 )
		
		roiSize = imShuffle.calcRoiSize( ar0 )
		self.assertEqual( roiSize, (512,512,3) )
		
		ar1 = imShuffle.enc( ar0 )
		ar2 = imShuffle.dec( ar1 )
		
		if( write_image is not None ):
			Image.fromarray( ar0 ).save( write_image+'Rand0.png' )
			Image.fromarray( ar1 ).save( write_image+'Rand1.png' )
			Image.fromarray( ar2 ).save( write_image+'Rand2.png' )

		self.assertTrue( ( ar0 == ar2 ).all() )
		
	def test_RandBlock(self):
		ar0 = self.ar
		
		imShuffle = imageshuffle.RandBlock( 567, (8,7) )
		roiSize = imShuffle.calcRoiSize( ar0 )
		self.assertEqual( roiSize, (512,511,3) )
		
		
		ar1 = imShuffle.enc( ar0 )
		ar2 = imShuffle.dec( ar1 )
		
		if( write_image is not None ):
			Image.fromarray( ar0 ).save( write_image+'RandBlock0.png' )
			Image.fromarray( ar1 ).save( write_image+'RandBlock1.png' )
			Image.fromarray( ar2 ).save( write_image+'RandBlock2.png' )

		self.assertTrue( ( ar0 == ar2 ).all() )

	def test_CatMap(self):
		ar0 = self.ar
		
		imShuffle = imageshuffle.CatMap( 8910, channel_shuffle = False )
		roiSize = imShuffle.calcRoiSize( ar0 )
		self.assertEqual( roiSize, (512,512,3) )
		
		ar1 = imShuffle.enc( ar0 )
		ar2 = imShuffle.dec( ar1 )
		
		if( write_image ):
			Image.fromarray( ar0 ).save( write_image+'CatMap0.png' )
			Image.fromarray( ar1 ).save( write_image+'CatMap1.png' )
			Image.fromarray( ar2 ).save( write_image+'CatMap2.png' )

		self.assertTrue( ( ar0 == ar2 ).all() )
		

	def test_CatMapComb(self):
		ar0 = self.ar
		
		imShuffle = imageshuffle.CatMapComb( 7683 )
		roiSize = imShuffle.calcRoiSize( ar0 )
		self.assertEqual( roiSize, (512,512,3) )
		
		ar1 = imShuffle.enc( ar0 )
		ar2 = imShuffle.dec( ar1 )
		
		if( write_image ):
			Image.fromarray( ar0 ).save( write_image+'CatMapComb0.png' )
			Image.fromarray( ar1 ).save( write_image+'CatMapComb1.png' )
			Image.fromarray( ar2 ).save( write_image+'CatMapComb2.png' )

		self.assertTrue( ( ar0 == ar2 ).all() )



###################################################################
	def suite():
		suite = unittest.TestSuite()
		suite.addTests(unittest.makeSuite(test_ImageShffleRand))
		return suite
  
if( __name__ == '__main__' ):
	unittest.main()
