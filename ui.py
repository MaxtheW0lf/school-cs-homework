#from __future__ import annotations

import input_handling
import common

from typing import Callable, Optional

import text_formatting



class Alignment:
	LEFT = "<"
	RIGHT = ">"
	CENTER = "^"

class Style:
	def __init__(self, width: int = 20, alignment: str = Alignment.LEFT, margin_left: int = 0):
		self.alignment = alignment
		self.width = width
		self.margin_left = margin_left


class UIState:
	def __init__(self):
		self.currently_selected = 0
		self.ui_to_navigate = None
		self.ui_to_display = None

	def change_ui(self, new_ui_to_display: 'Container', new_ui_to_navigate: 'Container'):
		self.currently_selected = 0
		self.ui_to_navigate = new_ui_to_navigate
		self.ui_to_display = new_ui_to_display
		common.clear()

	def update(self):
		common.reset()

		if self.ui_to_display is None:
			return

		self.ui_to_display.render(self)

		key = input_handling.get_key()

		if key in (b'\x03', '\x03'): # Ctrl+C
			raise KeyboardInterrupt
		
		if self.ui_to_navigate is None:
			return

		element: Element = self.ui_to_navigate.elements[self.currently_selected]

		match key:
			case "UP": # arrow down
				self.currently_selected = (self.currently_selected - 1) % self.ui_to_navigate.element_count()
			case "DOWN": # arrow up
				self.currently_selected = (self.currently_selected + 1) % self.ui_to_navigate.element_count()
		
		element.handle_input(key)


class Element:
	def render(self, ui: UIState, style: Style):
		pass
				
	def handle_input(self, key):
		pass


class Container:
	def __init__(self, style: Style, *elements: Element):
		self.elements = list(elements)
		self.style = style

	def set_style(self, style):
		self.style = style

	def add_element(self, element: Element):
		self.elements.append(element)

	def render(self, ui: UIState):
		print("+" + "-" * (self.style.width-2 + self.style.margin_left) + "+")
		for e in self.elements:
			print(" "*self.style.margin_left, end="")
			e.render(ui, self.style)
			print()
		print("+" + "-" * (self.style.width-2 + self.style.margin_left) + "+")

	def element_count(self):
		return len(self.elements)


class HorizontalSection(Element):
	def __init__(self, style: Style, *elements: Element):
		self.elements = list(elements)
		self.style = style

	def set_style(self, style):
		self.style = style

	def add_element(self, element: Element):
		self.elements.append(element)

	def render(self, ui: UIState, style: Style):
		for e in self.elements:
			print(" "*self.style.margin_left, end="")
			e.render(ui, self.style)

	def element_count(self):
		return len(self.elements)

class Button(Element):
	def __init__(self, text: str, position: int, ui_state: UIState, on_press: Optional[Callable] = None, style: Optional[Style] = None):
		self.text = text
		self.on_press = on_press
		self.position = position
		self.ui_state = ui_state
		self.style = style

	def pressed(self):
		if self.on_press:
			common.clear()
			self.on_press()
	
	def render(self, ui: UIState, style: Style):
		self.style = style
		print(self.button_func(), end="")
	
	def handle_input(self, key):
		if key in ("\n", "\r"):
			self.pressed()

	def button_func(self) -> str:
		if self.style is None:
			return ""
		
		if self.position == self.ui_state.currently_selected:
			return f"{common.color(90, 79, 102, True)}{self.text:{self.style.alignment}{self.style.width}}{common.END}"

		return f"{self.text:{self.style.alignment}{self.style.width}}"

	def __str__(self) -> str:
		return self.button_func()


class Label(Element):
	def __init__(self, text: str):
		self.text = text

	def render(self, ui: UIState, style: Style):
		print(f"{str(self.text):{style.alignment}{style.width}}", end="")


class InputField(Element):
	def __init__(self, placeholder: str, position: int, ui_state: UIState, default: str = ""):
		self.value = default
		self.placeholder = placeholder
		self.position = position
		self.ui_state = ui_state

	def handle_input(self, key):
		# Enter → stop editing
		if key in ("\n", "\r", "UP", "LEFT", "RIGHT",  "DOWN"):
			return

		# Backspace
		if key in (b'\x08', b'\x7f'):
			self.value = self.value[:-1]
			return

		# Only accept normal characters
		if key.isprintable():
			self.value += key

	def render(self, ui: UIState, style: Style):
		text = self.value if self.value else common.color(128,128,128) + self.placeholder + common.END

		if self.position == self.ui_state.currently_selected:
			text = f"[{text}<]"
		else:
			text = f" {text} "

		print(text_formatting.format_length(text, style.width, style.alignment), end="")

class NumberInputField(Element):
	def __init__(self, placeholder: str, position: int, ui_state: UIState, allow_float=False, allow_negative=False):
		self.value = ""
		self.placeholder = placeholder
		self.position = position
		self.ui_state = ui_state
		self.allow_float = allow_float
		self.allow_negative = allow_negative

	def handle_input(self, key):
		# Enter → stop editing
		if key in ("\n", "\r", "UP", "LEFT", "RIGHT",  "DOWN"):
			return

		# Backspace
		if key in (b'\x08', b'\x7f'):
			self.value = self.value[:-1]
			return

		try:
			if key.isdigit():
				self.value += key
				return

			# Handle decimal point
			if self.allow_float and key == "." and "." not in self.value:
				# prevent "." as first char unless you want "0."
				if self.value == "":
					self.value = "0."
				else:
					self.value += "."
				return

			# Handle negative sign
			if self.allow_negative and key == "-" and self.value == "":
				self.value = "-"
				return

		except:
			pass

	def render(self, ui: UIState, style: Style):
		text = self.value if self.value else (
			common.color(128, 128, 128) +
			self.placeholder +
			common.END
		)

		if self.position == self.ui_state.currently_selected:
			text = f"[{text}<]"
		else:
			text = f" {text} "

		print(text_formatting.format_length(text, style.width, style.alignment), end="")

class DateInputField(Element):
	def __init__(self, position: int, ui_state: UIState, default: str = ""):
		self.position = position
		self.ui_state = ui_state

		# internal fields
		self.day = NumberInputField("DD", position, ui_state)
		self.month = NumberInputField("MM", position, ui_state)
		self.year = NumberInputField("YYYY", position, ui_state)

		self.sub_index = 0  # 0=day, 1=month, 2=year
		self.value = ""
		if default:
			try:
				d, m, y = default.split("-")
				self.day.value = d
				self.month.value = m
				self.year.value = y
			except ValueError:
				pass  # ignore invalid format

	def handle_input(self, key):
		# switch between DD / MM / YYYY
		if key in (b'\t',):  # TAB
			self.sub_index = (self.sub_index + 1) % 3
			return

		if key == "LEFT":  # left arrow
			self.sub_index = (self.sub_index - 1) % 3
			return

		if key == "RIGHT":  # right arrow
			self.sub_index = (self.sub_index + 1) % 3
			return

		# delegate input
		fields = [self.day, self.month, self.year]
		fields[self.sub_index].handle_input(key)

		self.value = "-".join([self.day.value, self.month.value, self.year.value])


	def render(self, ui: UIState, style: Style):
		def fmt(field, selected):
			text = field.value if field.value else (
				common.color(128,128,128) + field.placeholder + common.END
			)
			return f"[{text}]" if selected else f" {text} "

		selected_main = (self.position == self.ui_state.currently_selected)

		parts = [
			fmt(self.day, selected_main and self.sub_index == 0),
			"/",
			fmt(self.month, selected_main and self.sub_index == 1),
			"/",
			fmt(self.year, selected_main and self.sub_index == 2),
		]

		text = "".join(parts)

		print(text_formatting.format_length(text, style.width, style.alignment), end="")