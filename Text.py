# Pygame Dynamic Text - Text

# ================================================================================================ #
# Imports

from typing import Callable, Optional

import pygame as pg

# ================================================================================================ #
# Text Class

class Text:
	def __init__(self, **kwargs):
		# Background Color
		background_color_kwarg = kwargs.get('background_color')
		self._background_color: Callable[[], tuple[int, int, int]] = (
			background_color_kwarg
			if isinstance(background_color_kwarg, Callable)
			else lambda: background_color_kwarg # type: ignore
		)
		self._last_background_color: Optional[tuple[int, int, int]] = None

		# Center
		center_kwarg = kwargs.get('center')
		self._center: Callable[[], tuple[float, float]] = (
			center_kwarg
			if isinstance(center_kwarg, Callable)
			else lambda: center_kwarg # type: ignore
		)
		self._last_center: Optional[tuple[float, float]] = self.center

		# Color
		color_kwarg = kwargs.get('color', (255, 255, 255))
		self._color: Callable[[], tuple[int, int, int]] = (
			color_kwarg
			if isinstance(color_kwarg, Callable)
			else lambda: color_kwarg # type: ignore
		)
		self._last_color: tuple[int, int, int] = self.color
		
		# Text
		text_kwarg = kwargs.get('text', 'Text')
		self._text: Callable[[], str] = (
			text_kwarg
			if isinstance(text_kwarg, Callable)
			else lambda: str(text_kwarg)
		)
		self._last_text: str = '' # Forces self._check_for_update() to return True on first run

		# Generate Surface & Rect
		self._update_surface()

	# ================================================== #
	# Property Methods

	@property
	def background_color(self) -> Optional[tuple[int, int, int]]:
		return self._background_color()

	@property
	def center(self) -> Optional[tuple[float, float]]:
		return self._center()

	@property
	def color(self) -> tuple[int, int, int]:
		return self._color()

	@property
	def frect(self) -> pg.FRect:
		return self._background_rect

	@property
	def surf(self) -> pg.Surface:
		return self._background_surf

	@property
	def text(self) -> str:
		return self._text()

	# ================================================== #

	def _check_for_update(self) -> bool:
		update_needed = False

		# Background Color

		background_color = self.background_color
		if background_color != self._last_background_color:
			self._last_background_color = background_color
			update_needed = True

		# Center
		center = self.center
		if center != self._last_center:
			self._last_center = center
			update_needed = True

		# Color
		color = self.color
		if color != self._last_color:
			self._last_color = color
			update_needed = True

		# Text
		text = self.text
		if text != self._last_text:
			self._last_text = text
			update_needed = True

		return update_needed

	def _update_surface(self):
		self._text_surf: pg.Surface = pg.font.Font(pg.font.get_default_font(), 20).render(self._last_text, True, self._last_color)
		self._text_rect: pg.FRect = self._text_surf.get_frect()

		if self._last_background_color is None:
			self._background_surf: pg.Surface = pg.surface.Surface(self._text_rect.size, pg.SRCALPHA)
		else:
			self._background_surf: pg.Surface = pg.surface.Surface(self._text_rect.size)
			self._background_surf.fill(self._last_background_color)

		self._background_rect: pg.FRect = self._background_surf.get_frect()

		self._text_rect.center = self._background_rect.center
		self._background_surf.blit(self._text_surf, self._text_rect)

		if self._last_center is not None:
			self._background_rect.center = self._last_center

	def display(self, target_surface: pg.Surface) -> None:
		if self._check_for_update():
			self._update_surface()
		
		target_surface.blit(self.surf, self.frect)

# ================================================================================================ #
# Test

if __name__ == '__main__':
	from datetime import datetime
	from math import cos, sin, tau
	from sys import exit
	from time import time

	def time_based_color() -> tuple[int, int, int]:
		return (
			round(2 * time() % 255),
			round(3 * time() % 255),
			round(5 * time() % 255)
		)

	pg.init()
	clock = pg.time.Clock()

	window_surf = pg.display.set_mode((500, 500))
	window_rect = window_surf.get_rect()

	pg.display.set_caption('Example Text Object')

	fps_text = Text(
		text = lambda: 'FPS: ' + str(round(clock.get_fps())) + ' / 240'
	)

	time_text = Text(
		background_color = (0, 127, 0),
		center = lambda: (
			window_rect.centerx + 100 * cos(time() * tau / 10),
			window_rect.centery + 100 * sin(time() * tau / 10)
		),
		color = time_based_color,
		text = lambda: datetime.fromtimestamp(time()).strftime("%Y-%m-%d %H:%M:%S")
	)

	while True:
		clock.tick(240)

		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.QUIT
				exit()

		window_surf.fill((63, 63, 63))
		fps_text.display(window_surf)
		time_text.display(window_surf)
		pg.display.flip()