from PIL import Image, ImageFilter, ImageEnhance
import os

fn = 'lena.ppm'

im = Image.open(fn)

print im.format, im.size, im.mode


def show(newim, oldim = im):

	'''
	show origin and new image in one image.
	'''

	cm = Image.new('RGB', (512*2, 512))
	left = (0, 0, 512, 512)
	right = (512, 0, 512*2, 512)
	cm.paste(oldim, left)
	cm.paste(newim, right)
	cm.show()

'''
uncomment those lines
'''
#im.show()

def convert_to_jpg(infile):
	f, e = os.path.splitext(infile)
	outfile = f + '.jpg'
	if infile != outfile:
		try:
			Image.open(infile).save(outfile)
		except IOError:
			print 'cannot convert', infile

#convert_to_jpg(fn)

def create_thumbnails(infile):
	size = (128, 128)
	outfile = os.path.splitext(infile)[0] + ".thumbnail"
	if infile != outfile:
		try:
			im = Image.open(infile)
			im.thumbnail(size)
			im.save(outfile, "JPEG")
		except IOError:
			print "cannot create thumbnail for", infile

#create_thumbnails(fn)	

def identify_image(infile):
    try:
        im = Image.open(infile)
        print infile, im.format, "%dx%d"%im.size, im.mode
    except IOError:
        pass

#identify_image(fn)

box = (100, 100, 400, 400)
region = im.crop(box)
#region.show()

region = region.rotate(Image.ROTATE_180)
#im.paste(region, box)
#im.show()

def roll(image, delta):
    "Roll an image sideways"

    image = image.copy()
    xsize, ysize = image.size

    delta = delta % xsize
    if delta == 0: return image

    part1 = image.crop((0, 0, delta, ysize))
    part2 = image.crop((delta, 0, xsize, ysize))
    image.paste(part2, (0, 0, xsize-delta, ysize))
    image.paste(part1, (xsize-delta, 0, xsize, ysize))

    return image

newim = roll(im, 512 / 2)
#newim.show()

out = im.resize((128, 128))
#out.show()
out = im.rotate(45)
#out.show()

#im = Image.open("lena.ppm").convert("L")
#print im.format, im.size, im.mode
#im.show()

out = im.filter(ImageFilter.BLUR)
'''
ImageFilter contains those pre-define filters:


    BLUR
    CONTOUR
    DETAIL
    EDGE_ENHANCE
    EDGE_ENHANCE_MORE
    EMBOSS
    FIND_EDGES
    SMOOTH
    SMOOTH_MORE
    SHARPEN

'''

#show(out)

out = im.point(lambda x: x*2)

#show(out)

def show_bands(im):
	return im.split()


def process_individual_bands(im):
	# split the image into individual bands
	source = im.split()

	R, G, B = 0, 1, 2

	# select regions where red is less than 100
	mask = source[R].point(lambda i: i < 100 and 255)
	# process the green band
	out = source[G].point(lambda i: i * 0.7)
	
	# paste the processed band back, but only where red was < 100
	source[G].paste(out, None, mask)

	# build a new multiband image
	return Image.merge(im.mode, source)

out = process_individual_bands(im)
#show(out)

ech = ImageEnhance.Contrast(im)
#show(ech.enhance(1.3))

