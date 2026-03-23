import input_handling
import common

from text_formatting import END, color

from typing import Callable, Optional

class Alignment:
    LEFT = "<"
    RIGHT = ">"
    CENTER = "^"

class Style:
    def __init__(self, width: int = 20, alignment: str = Alignment.LEFT, margin_left: int = 0):
        self.alignment = alignment
        self.width = width
        self.margin_left = margin_left


class Element:
    def render(self, ui: UIState, style: Style):
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
        print("+" + "-" * self.style.width + "+")
        for e in self.elements:
            print(" "*self.style.margin_left, end="")
            e.render(ui, self.style)
        print("+" + "-" * self.style.width + "+")

    def element_count(self):
        return len(self.elements)


class UIState:
    def __init__(self):
        self.currently_selected = 0
        self.ui_to_navigate = None
        self.ui_to_display = None

    def change_ui(self, new_ui_to_display: Container, new_ui_to_navigate: Container):
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

        match key:
            case b'\xe0H' | "\x1b[A": # arrow down
                self.currently_selected = (self.currently_selected - 1) % self.ui_to_navigate.element_count()
            case b'\xe0P' | "\x1b[B": # arrow up
                self.currently_selected = (self.currently_selected + 1) % self.ui_to_navigate.element_count()
            case b'\r' | "\n": # enter
                self.ui_to_navigate.elements[self.currently_selected].pressed()


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
        print(self.button_func())

    def button_func(self) -> str:
        if self.position == self.ui_state.currently_selected:
            return f"{color(90, 79, 102, True)}{self.text:{self.style.alignment}{self.style.width-4}}{END}"

        return f"{self.text:{self.style.alignment}{self.style.width-4}}"

    def __str__(self) -> str:
        return self.button_func()


class Label(Element):
    def __init__(self, text: str):
        self.text = text

    def render(self, ui: UIState, style: Style):
        print(f"{str(self.text):{style.alignment}{style.width}}")