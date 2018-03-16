#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from imageshuffle import imagesha384

import numpy as np
from PIL import Image


write_image = 'SH_'
#write_image = None

class test_ImageSHA384( unittest.TestCase ):
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
	def test_SHA384(self):
		ar0 = self.ar
		ar1 = imagesha384.dec( ar0 )
		ar2 = imagesha384.dec( ar0, 888 )
		ar3 = imagesha384.dec( ar0, sha = 'sha3' )
		ar4 = imagesha384.dec( ar0, 888, sha = 'sha3' )
		ar5 = imagesha384.dec( ar0, sha = 'md5' )
		ar6 = imagesha384.dec( ar0, 888, sha = 'md5' )
		ar7 = imagesha384.dec( ar0, sha = 'shake256' )
		ar8 = imagesha384.dec( ar0, 888, sha = 'shake256' )
		
		if( write_image is not None ):
			Image.fromarray( ar1 ).save( write_image+'SHA384.png' )
			Image.fromarray( ar2 ).save( write_image+'SHA384_888.png' )
			Image.fromarray( ar3 ).save( write_image+'SHA3_384.png' )
			Image.fromarray( ar4 ).save( write_image+'SHA3_384_888.png' )
			Image.fromarray( ar5 ).save( write_image+'MD5_384.png' )
			Image.fromarray( ar6 ).save( write_image+'MD5_384_888.png' )
			Image.fromarray( ar5 ).save( write_image+'shake_384.png' )
			Image.fromarray( ar6 ).save( write_image+'shake_384_888.png' )

###################################################################
	def suite():
		suite = unittest.TestSuite()
		suite.addTests(unittest.makeSuite(test_ImageSHA384))
		return suite
  
if( __name__ == '__main__' ):
	unittest.main()
