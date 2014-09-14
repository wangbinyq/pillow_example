#Pillow 初级教程

2014-09-14 翻译 [http://pillow.readthedocs.org/en/latest/handbook/tutorial.html](http://pillow.readthedocs.org/en/latest/handbook/tutorial.html "翻译") 

Pillow由PIL而来，所以该导入该库使用import PIL

##Image类
Pillow中最重要的类就是Image，该类存在于同名的模块中。可以通过以下几种方式实例化：从文件中读取图片，处理其他图片得到，或者直接创建一个图片。

使用Image模块中的open函数打开一张图片：
    
	>>> from PIL import Image
	>>> im = Image.open("lena.ppm")

如果打开成功，返回一个Image对象，可以通过对象属性检查文件内容

	>>> from __future__ import print_function
	>>> print(im.format, im.size, im.mode)
	PPM (512, 512) RGB

format属性定义了图像的格式，如果图像不是从文件打开的，那么该属性值为None；size属性是一个tuple，表示图像的宽和高（单位为像素）；mode属性为表示图像的模式，常用的模式为：L为灰度图，RGB为真彩色，CMYK为pre-press图像。

如果文件不能打开，则抛出IOError异常。

当有一个Image对象时，可以用Image类的各个方法进行处理和操作图像，例如显示图片：

	>>> im.show()

> ps：标准版本的show()方法不是很有效率，因为它先将图像保存为一个临时文件，然后使用xv进行显示。如果没有安装xv，该函数甚至不能工作。但是该方法非常便于debug和test。（windows中应该调用默认图片查看器打开）

##读写图片

Pillow库支持相当多的图片格式。直接使用Image模块中的open()函数读取图片，而不必先处理图片的格式，Pillow库自动根据文件决定格式。

Image模块中的save()函数可以保存图片，除非你指定文件格式，那么文件名中的扩展名用来指定文件格式。

**图片转成jpg格式**

	from __future__ import print_function
	import os, sys
	from PIL import Image

	for infile in sys.argv[1:]:
    	f, e = os.path.splitext(infile)
    	outfile = f + ".jpg"
    	if infile != outfile:
        	try:
            	Image.open(infile).save(outfile)
        	except IOError:
            	print("cannot convert", infile)

save函数的第二个参数可以用来指定图片格式，如果文件名中没有给出一个标准的图像格式，那么第二个参数是必须的。

**创建缩略图**

	from __future__ import print_function
	import os, sys
	from PIL import Image
	
	size = (128, 128)
	
	for infile in sys.argv[1:]:
	    outfile = os.path.splitext(infile)[0] + ".thumbnail"
	    if infile != outfile:
	        try:
	            im = Image.open(infile)
	            im.thumbnail(size)
	            im.save(outfile, "JPEG")
	        except IOError:
	            print("cannot create thumbnail for", infile)

必须指出的是除非必须，Pillow不会解码或raster数据。当你打开一个文件，Pillow通过文件头确定文件格式，大小，mode等数据，余下数据直到需要时才处理。

这意味着打开文件非常快，与文件大小和压缩格式无关。下面的程序用来快速确定图片属性：

**确定图片属性**

	from __future__ import print_function
	import sys
	from PIL import Image
	
	for infile in sys.argv[1:]:
	    try:
	        with Image.open(infile) as im:
	            print(infile, im.format, "%dx%d" % im.size, im.mode)
	    except IOError:
	        pass

##裁剪、粘贴、与合并图片
Image类包含还多操作图片区域的方法。如crop()方法可以从图片中提取一个子矩形

**从图片中复制子图像**
	
	box = im.copy() #直接复制图像
	box = (100, 100, 400, 400)
	region = im.crop(box)

区域由4-tuple决定，该tuple中信息为(left, upper, right, lower)。	Pillow左边系统的原点（0，0）为图片的左上角。坐标中的数字单位为像素点，所以上例中截取的图片大小为300*300像素^2。

**处理子图，粘贴回原图**

	region = region.transpose(Image.ROTATE_180)
	im.paste(region, box)

将子图paste回原图时，子图的region必须和给定box的region吻合。该region不能超过原图。而原图和region的mode不需要匹配，Pillow会自动处理。

另一个例子

**Rolling an image**

	def roll(image, delta):
	    "Roll an image sideways"
		
		image = image.copy() #复制图像
	    xsize, ysize = image.size
	
	    delta = delta % xsize
	    if delta == 0: return image
	
	    part1 = image.crop((0, 0, delta, ysize))
	    part2 = image.crop((delta, 0, xsize, ysize))
	    image.paste(part2, (0, 0, xsize-delta, ysize))
	    image.paste(part1, (xsize-delta, 0, xsize, ysize))
	
	    return image

**分离和合并通道**

	r, g, b = im.split()
	im = Image.merge("RGB", (b, g, r))

对于单通道图片，split()返回图像本身。为了处理单通道图片，必须先将图片转成RGB。

##几何变换

Image类有resize()、rotate()和transpose()、transform()方法进行几何变换。

**简单几何变换**

	out = im.resize((128, 128))
	out = im.rotate(45) # 顺时针角度表示

**置换图像**

	out = im.transpose(Image.FLIP_LEFT_RIGHT)
	out = im.transpose(Image.FLIP_TOP_BOTTOM)
	out = im.transpose(Image.ROTATE_90)
	out = im.transpose(Image.ROTATE_180)
	out = im.transpose(Image.ROTATE_270)

transpose()和象的rotate()没有性能差别。

更通用的图像变换方法可以使用[transform()](http://pillow.readthedocs.org/en/latest/reference/Image.html#PIL.Image.Image.transform)

##模式转换

[convert()](http://pillow.readthedocs.org/en/latest/reference/Image.html#PIL.Image.Image.convert)方法

**模式转换**

	im = Image.open('lena.ppm').convert('L')

##图像增强

###Filter
[ImageFilter](http://pillow.readthedocs.org/en/latest/reference/ImageFilter.html#module-PIL.ImageFilter)模块包含很多预定义的增强filters，通过[filter()](http://pillow.readthedocs.org/en/latest/reference/Image.html#PIL.Image.Image.filter)方法使用

**应用filters**

	from PIL import ImageFilter
	out = im.filter(ImageFilter.DETAIL)	

##像素点处理

[point()](http://pillow.readthedocs.org/en/latest/reference/Image.html#PIL.Image.Image.point)方法通过一个函数或者查询表对图像中的像素点进行处理（例如对比度操作）。

**像素点变换**

	# multiply each pixel by 1.2
	out = im.point(lambda i: i * 1.2)

上述方法可以利用简单的表达式进行图像处理，通过组合point()和paste()还能选择性地处理图片的某一区域。

**处理单独通道**

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
	im = Image.merge(im.mode, source)

注意到创建mask的语句：

	mask = source[R].point(lambda i: i < 100 and 255)

该句可以用下句表示

	imout = im.point(lambda i: expression and 255)

如果expression为假则返回expression的值为0（因为and语句已经可以得出结果了），否则返回255。（[mask](http://pillow.readthedocs.org/en/latest/reference/Image.html#PIL.Image.Image.point)参数用法：当为0时，保留当前值，255为使用paste进来的值，中间则用于transparency效果）

##高级图片增强

对其他高级图片增强，应该使用[ImageEnhance](http://pillow.readthedocs.org/en/latest/reference/ImageEnhance.html#module-PIL.ImageEnhance)模块
。一旦有一个Image对象，应用ImageEnhance对象就能快速地进行设置。
可以使用以下方法调整对比度、亮度、色平衡和锐利度。

**图像增强**

	from PIL import ImageEnhance
	
	enh = ImageEnhance.Contrast(im)
	enh.enhance(1.3).show("30% more contrast")

**动态图**

Pillow支持一些动态图片的格式如FLI/FLC，GIF和其他一些处于实验阶段的格式。TIFF文件同样可以包含数帧图像。

当读取动态图时，PIL自动读取动态图的第一帧，可以使用seek和tell方法读取不同帧。

	from PIL import Image
	
	im = Image.open("animation.gif")
	im.seek(1) # skip to the second frame
	
	try:
	    while 1:
	        im.seek(im.tell()+1)
	        # do something to im
	except EOFError:
	    pass # end of sequence

当读取到最后一帧时，Pillow抛出EOFError异常。

当前版本只允许seek到下一帧。为了倒回之前，必须重新打开文件。

或者可以使用下述迭代器类

**动态图迭代器类**

	class ImageSequence:
	    def __init__(self, im):
	        self.im = im
	    def __getitem__(self, ix):
	        try:
	            if ix:
	                self.im.seek(ix)
	            return self.im
	        except EOFError:
	            raise IndexError # end of sequence
	
	for frame in ImageSequence(im):
	    # ...do something to frame...


##Postscript Printing

Pillow允许通过Postscript Printer在图片上添加images、text、graphics。

**Drawing Postscript**

	from PIL import Image
	from PIL import PSDraw
	
	im = Image.open("lena.ppm")
	title = "lena"
	box = (1*72, 2*72, 7*72, 10*72) # in points
	
	ps = PSDraw.PSDraw() # default is sys.stdout
	ps.begin_document(title)
	
	# draw the image (75 dpi)
	ps.image(box, im, 75)
	ps.rectangle(box)
	
	# draw centered title
	ps.setfont("HelveticaNarrow-Bold", 36)
	w, h, b = ps.textsize(title)
	ps.text((4*72-w/2, 1*72-h), title)
	
	ps.end_document()

> ps：textsize不能用，有谁知道吗

##更多读取图片方法

之前说到Image模块的open()函数已经足够日常使用。该函数的参数也可以是一个文件对象。

**从string中读取**

	import StringIO
	
	im = Image.open(StringIO.StringIO(buffer))

**从tar文件中读取**

	from PIL import TarIO
	
	fp = TarIO.TarIO("Imaging.tar", "Imaging/test/lena.ppm")
	im = Image.open(fp)

##草稿模式

draft()方法允许在不读取文件内容的情况下尽可能（可能不会完全等于给定的参数）地将图片转成给定模式和大小，这在生成缩略图的时候非常有效（速度要求比质量高的场合）。

**draft模式**

	from __future__ import print_function
	im = Image.open(file)
	print("original =", im.mode, im.size)
	
	im.draft("L", (100, 100))
	print("draft =", im.mode, im.size)


#参考
[PIL中的Image模块](http://www.cnblogs.com/way_testlife/archive/2011/04/20/2022997.html)