from functions import data

import common

from text_formatting import color, END, format_length

import ui

ui_state = ui.UIState()


style = ui.Style(20, ui.Alignment.CENTER)


students: list = data.read_data()

KEEP_RUNNING: bool = True

def stop():
    global KEEP_RUNNING
    KEEP_RUNNING = False


main_menu = ui.Container(
    style,
    ui.Button("add student", 0, ui_state),
    ui.Button("show students", 1, ui_state, lambda: show_students()),
    ui.Button("Exit", 2, ui_state, stop),
	ui.InputField("test", 3, ui_state)
)


def main():
    common.start()

    ui_state.change_ui(main_menu, main_menu)

    try:
        while KEEP_RUNNING:
            ui_state.update()

    except KeyboardInterrupt:
        pass
    
    finally:
        common.cleanup()


def show_students():
    go_back = ui.Button("Back", 0, ui_state, lambda: ui_state.change_ui(main_menu, main_menu))

    nav = ui.Container(style, go_back)
    margin_style = ui.Style(20, ui.Alignment.CENTER, margin_left=2)
    container = ui.Container(margin_style, go_back)

    if students:
        keys = [k for k in students[0] if k != "id"]

        widths = {
            k: max(
                len(k),  # include header lengths
                *(len(str(student.get(k, ""))) for student in students)
            )
            for k in keys
        }

        header = ' | '.join(f"{k:<{widths[k]}}" for k in keys)

    
        container.add_element(ui.Label(header))

        for student in students:
            text = ' | '.join(
                f"{format_length(grades_display(student.get(k, '')) if k.startswith("grades") 
                    else str(student.get(k, '')), widths[k])}"
                for k in keys
            )

            btn = ui.Button(
                text,
                nav.element_count(),
                ui_state,
                lambda s=student: show_student(s)
            )

            container.add_element(btn)
            nav.add_element(btn)
    
    else:
        container.add_element(ui.Label("no students"))

    ui_state.change_ui(container, nav)


def edit_student(student_id: int, field: str):
    find_student(student_id)


def show_student(student: dict):
    student_display = ui.Container(ui.Style(margin_left=2))

    go_back = ui.Button("Back", 0, ui_state, show_students)
    delete = ui.Button("Delete", 1, ui_state, lambda: delete_and_quit(student.get("id", None)))

    nav = ui.Container(style, go_back, delete)

    for k, v in student.items():
        if k.startswith("grades"):
            student_display.add_element(ui.Label(f"{k}: {grades_display(v)}"))
            continue
        
        student_display.add_element(ui.Label(f"{k}: {v}"))

    student_display.add_element(go_back)
    student_display.add_element(delete)

    ui_state.change_ui(student_display, nav)


def grades_display(grades: list) -> str:
    return " ".join(color(128, 52, 65, True) + str(g) + END for g in grades)


def delete_and_quit(student_id: int | None):
    if student_id is None:
        return

    delete_student(student_id)
    show_students()

def delete_student(student_id: int):
    global students
    students = [s for s in students if s["id"] != student_id]

def find_student(student_id: int) -> dict | None:
    for s in students:
        if s.get("id", None) == student_id:
            return s
    return None

if __name__ == "__main__":
    main()