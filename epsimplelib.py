"""
ePaperLibrary for Waveshare e-Paper 2.7" Raspberry HAT

Github: https://github.com/lyoko17220/ePaperLibrary
"""

from PIL import Image, ImageFont, ImageDraw, ImageChops

import waveshare_library.epd2in7

# Default font
FONT_PATH            = 'FreeMonoBold.ttf'
FONT_SMALL_MAX       = ImageFont.truetype(FONT_PATH, 12)
FONT_SMALL           = ImageFont.truetype(FONT_PATH, 14)
FONT_NORMAL          = ImageFont.truetype(FONT_PATH, 18)
FONT_BIG             = ImageFont.truetype(FONT_PATH, 22)

# Colors
BLACK                = 0
WHITE                = 255

# Size (Portrait mode)
DEVICE_WIDTH         = 176
DEVICE_HEIGHT        = 264


class EPScreen():
	"""
	Manager of the screen
	"""

	def __init__(self, screen_orientation: object) -> object:
		self.device = waveshare_library.epd2in7.EPD()
		self.device.init()

		self.width = None
		self.height = None

		self.image_live = None
		self.image_old = None
		self.draw = None

		if screen_orientation in ('landscape', 'portrait'):
			self.screen_orientation = screen_orientation
			self.init_image()
		else:
			raise Exception('Screen orientation not recognized')

	def init_image(self):
		"""
		Set width and height according to screen orientation and generate empty Image and draw
		"""

		if self.screen_orientation == 'portrait':
			self.width = DEVICE_WIDTH
			self.height = DEVICE_HEIGHT
		elif self.screen_orientation == 'landscape':
			self.width = DEVICE_HEIGHT
			self.height = DEVICE_WIDTH

		self.image_live = Image.new('1', (self.width, self.height), 255)
		self.draw = ImageDraw.Draw(self.image_live)

	def update_screen(self):
		"""
		Send the new image to HAT
		:return: Screen reloaded or not
		"""

		if self.image_old is None or self.need_to_refresh():
			if self.screen_orientation == 'landscape':
				self.device.display_frame(self.device.get_frame_buffer(self.image_live.rotate(90, expand=1)))
			else:
				self.device.display_frame(self.device.get_frame_buffer(self.image_live))
			self.image_old = self.image_live
			self.init_image()
			return True

	def need_to_refresh(self):
		"""
		Return if difference between previous image and the newest
		:return False or True
		"""

		return ImageChops.difference(self.image_live, self.image_old).getbbox() is None

	def get_width(self):
		"""
		Return width
		:return: Width
		"""
		return self.width

	def get_height(self):
		"""
		Return height
		:return: Height
		"""

		return self.height

	## Drawing functions

	def add_text_middle(self, y, text, font, fill, width=-1, offset_x=0):
		"""
		Add text to middle of block
		:param y: y in screen
		:param text: text to add
		:param font: font to use
		:param fill: fill of text
		:param width: width of block
		:param offset_x: offset in x of the block
		:return:
		"""

		if width == -1:
			width = self.get_width()

		h_origin = font.getsize('a')[1]
		w, h = font.getsize(text)

		# Vertical offset for symbol fonts
		offset_y = 0
		if h - h_origin > 5:
			offset_y = h - h_origin

		self.draw.text((offset_x + (width) / 2 - w / 2, y - offset_y), text, font=font, fill=fill)

	def set_title(self, text):
		"""
		Add title to screen
		:param text:
		:return:
		"""

		self.draw.rectangle((0, 0, self.width, 28), fill=BLACK)
		self.add_text_middle(5, text, FONT_NORMAL, WHITE)

	def add_text(self, pos, text, font=FONT_NORMAL):
		"""
		Add simple text
		:param pos: (x,y)
		:param text: Text to add
		:param font: Font to use
		:return:
		"""

		self.draw.text(pos, text, font=font, fill=BLACK)

	def add_line(self, pos):
		"""
		Add line
		:param pos: Position xy start/end point
		:return:
		"""

		self.draw.line((pos[0], pos[1], pos[2], pos[3]), fill=BLACK)
