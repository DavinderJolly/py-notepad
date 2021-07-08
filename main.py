from datetime import datetime

from prompt_toolkit.application import Application
from prompt_toolkit.application.current import get_app
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import (
    ConditionalContainer,
    HSplit,
    VSplit,
    Window,
)
from prompt_toolkit.filters import Condition
from prompt_toolkit.widgets import (
    MenuContainer,
    MenuItem,
    TextArea,
)
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.styles import Style
from prompt_toolkit.lexers import PygmentsLexer
from pygments.lexers.python import PythonLexer


class ApplicationState:
    "Application state"
    show_status_bar = True


# Editing area
text_field = TextArea(
    lexer=PygmentsLexer(PythonLexer),
    scrollbar=True,
    line_numbers=True,
)


# Status bar area
def get_datetime():
    "Get opening datetime"
    return "Opened at " + datetime.now().strftime("%d/%m/%Y, %H:%M:%S")


status_bar_field = VSplit([Window(FormattedTextControl(get_datetime()))], height=1)


# UI main body
body = HSplit(
    [
        text_field,
        ConditionalContainer(
            content=status_bar_field,
            filter=Condition(lambda: ApplicationState.show_status_bar),
        ),
    ]
)


# Keybindings
bindings = KeyBindings()


@bindings.add("c-d")
def _exit(event):
    "Exit the editor"
    event.app.exit()


@bindings.add("c-c")
def _focus(event):
    "Focus on the menu"
    event.app.layout.focus(root_container.window)


# Menu items
def status_bar_handler():
    ApplicationState.show_status_bar = not ApplicationState.show_status_bar


root_container = MenuContainer(
    body=body,
    menu_items=[
        MenuItem(
            "File",
            children=[
                MenuItem("New"),
                MenuItem("Save"),
                MenuItem("Exit", handler=lambda: get_app().exit()),
            ],
        ),
        MenuItem("View", children=[MenuItem("Status Bar", handler=status_bar_handler)]),
        MenuItem("Info", children=[MenuItem("About")]),
    ],
    key_bindings=bindings,
)


layout = Layout(root_container, focused_element=text_field)

# Global style
style = Style.from_dict(
    {
        # empty for now
    }
)


application = Application(
    layout=layout,
    style=style,
    full_screen=True,
)


def run():
    application.run()


if __name__ == "__main__":
    run()
