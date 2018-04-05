imagedegrade
====

It is a python package to degrade image data.

## Usage

### imageshuffle.Rand
It shuffles pixels.
Any kind of data type of numpy.ndarray is supoorted.

- **\_\_init\_\_**( **key** )
	- Constructor
	- **key** (uint32): key
	- **output**: instance
- **enc**( **input** )
	- encryption
	- **input**(numpy.ndarray): Three dimensional array. (Height, Width, Channel)
	- **output**(numpy.ndarray): encrypted array.
- **dec**( **input** )
	- decryption
	- **input**(numpy.ndarray): Three dimensional array.
	- **output**(numpy.ndarray): decrypted array.

---

### imageshuffle.RandBlock
It shuffles pixels block-by-block.
Any kind of data type of numpy.ndarray is supoorted.
Size of input array shuld be multiples of block size.

- **\_\_init\_\_**( **key**, **blockSize** )
	- Constructor
	- **key** (uint32): key
	- **blockSize**: size of each block [Height, Width]
	- **output**: instance
- **enc**( **input** )
	- encryption
	- **input**(numpy.ndarray): Three dimensional array. (Height, Width, Channel). Height and Width should be multiples of blockSize.
	- **output**(numpy.ndarray): encrypted array.
- **dec**( **input** )
	- decryption
	- **input**(numpy.ndarray): Three dimensional array.
	- **output**(numpy.ndarray): decrypted array.

---

### imagescramble.Rand
It scrambles image. It only supports *numpy.uint8*.
First, the input data is splited. 
Then, reverse operation, pixel shuffling, and reverse operation are applied.

- **\_\_init\_\_**( **key**, **nb_bits** = 4, **rev_mode** = imagescramble.REV_ORD, **rev_ratio** = 0.5 )
	- Constructor
	- **key** (uint32): key
	- **nb_bits**: number of splited data bits. For instance, data is splited to two if nb_bits equals 4.
	- **rev_mode**: tye reverse mode
		- imagescramble.**REV_NONE**: not applied the reverse operation
		- imagescramble.**REV_RAND**: randomly applied the reverse operation
		- imagescramble.**REV_ORD**: the pixel to be applied the reverse operation is calculated with shuffleing order.
	- **rev_ratio**(float): the ratio to apply reverse operation. If it is out of [0,1]. 
	- **output**: instance
- **enc**( **input** )
	- encryption
	- **input**(numpy.ndarray): Three dimensional array. (Height, Width, Channel)
	- **output**(numpy.ndarray): encrypted array.
- **dec**( **input** )
	- decryption
	- **input**(numpy.ndarray): Three dimensional array.
	- **output**(numpy.ndarray): decrypted array.

---

### ImageScramble.RandBlock
It scrambles image block-by-block.
Size of input data should be multiples of size of block.

- **\_\_init\_\_**( **key**, **blockSize**, **nb_bits** = 4, **rev_mode** = imagescramble.REV_ORD, **rev_ratio** = 0.5 )
	- Constructor
	- **key** (uint32): key
	- **blockSize**: size of each block [Height, Width]
	- **nb_bits**: number of splited data bits. For instance, data is splited to two if nb_bits equals 4.
	- **rev_mode**: tye reverse mode
		- imagescramble.**REV_NONE**: not applied the reverse operation
		- imagescramble.**REV_RAND**: randomly applied the reverse operation
		- imagescramble.**REV_ORD**: the pixel to be applied the reverse operation is calculated with shuffleing order.
	- **rev_ratio**(float): the ratio to apply reverse operation. If it is out of [0,1]. 
	- **output**: instance
- **enc**( **input** )
	- encryption
	- **input**(numpy.ndarray): Three dimensional array. (Height, Width, Channel). Height and Width should be multiples of blockSize.
	- **output**(numpy.ndarray): encrypted array.
- **dec**( **input** )
	- decryption
	- **input**(numpy.ndarray): Three dimensional array.
	- **output**(numpy.ndarray): decrypted array.

---

### Image SHA 384 methods
It encrypt image block-by-block. The block size is 4x4.
It only supports _numpy.uint8_ and three channel data array.
4x4x3x8=384 bits. Then, it apply Secure Hash Algorithm (SHA) for 384 bits block-by-block.

- **dec**( **input**, **salt** = None, **sha** = 'sha2' )
	- encryption
	- **input** (numpy.ndarray): Three dimensional array. (Height, Width, Channel). Height and Width should be multiples of four. Channel should be three.
	- **salt**(uint32): salt for encryption.
	- **sha**: it specifies the algorithm
		- 'sha3': hashlib.sha3_384
		- 'sha2': hashlib.sha384
		- 'md5': hashlib.md5 (apply three times)
		- 'shake256': hashlib.shake_256 with 48 byte-length digest
		- 'shake128': hashlib.shake_128 with 48 byte-length digest
	- **output**(numpy.ndarray): encrypted array.

---

### Utility methods

- **paddingBlockSize**:( **X**, **blockSize** )
	- padding array with replicated manner
	- **x**(numpy.ndarray): three dimensional array
	- **blockSize**: size of block
	- **output**(numpy.ndarray): size of output is multiples of block size
	
Example

    import numpy as np
	from imageshffle.util import paddingBlockSize
	X = np.zeros((30,30))
	Y = paddingBlockSize( X, (8,8) )

---

### Sample

    from PIL import Image
    import numpy as np
    from imageshuffle import imageshuffle
    from imageshuffle import imagescramble
    
    img = Image.open('lena.png')
    ar = np.asarray(img)
    
    key = 1234
    s = imageshuffle.Rand( key )
    enc = s.enc( ar )
    dec = s.dec( enc )

    key = 5678
    s = imageshuffle.RandBlock( key, [8,8] )
    enc = s.enc( ar )
    dec = s.dec( enc )

    key = 1234
    s = imageshuffle.Rand( key )
    enc = s.enc( ar )
    dec = s.dec( enc )

    key = 5678
    s = imageshuffle.RandBlock( key, [8,8] )
    enc = s.enc( ar )
    dec = s.dec( enc )


## Install

`% pip install git+https://github.com/mastnk/imageshuffle`

## Reference

Masayuki Tanaka, Learnable Image Encryption, IEEE International Conference on Consumer Electronics TAIWAN (ICCE-TW), 2018.

## Links

[Masayuki Tanaka](https://github.com/mastnk)

[Project page](http://www.ok.sc.e.titech.ac.jp/~mtanaka/proj/imagescramble/)
