imagedegrade
====

It is a python package to degrade image data.

## Usage

### imageshuffle.Rand

### imageshuffle.RandBlock

### imagescramble.Rand

### ImageScramble.RandBlock

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
