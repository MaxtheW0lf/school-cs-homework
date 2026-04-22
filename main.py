from functions import data

import common
import text_formatting

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
	ui.Button("add student", 0, ui_state, lambda: add_student_ui()),
	ui.Button("show students", 1, ui_state, lambda: show_students()),
	ui.Button("Exit", 2, ui_state, stop),
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

def add_student_ui():
	name_field = ui.InputField("Name", 0, ui_state)
	surname_field = ui.InputField("Surname", 1, ui_state)
	date_of_birth_field = ui.DateInputField(2, ui_state)

	add_student_ui = ui.Container(
		style,
		name_field,
		surname_field,
		date_of_birth_field,
		ui.Button("add", 3, ui_state, lambda: response_to_add_student(name_field.value, surname_field.value, date_of_birth_field.value)),
		ui.Button("Back", 4, ui_state, lambda: ui_state.change_ui(main_menu, main_menu))
	)

	ui_state.change_ui(add_student_ui, add_student_ui)

def add_student(name: str, surname: str, date_of_birth: str) -> bool:
	if not name.strip() or not surname.strip() or not date_of_birth.strip():
		return False

	new_student = {
		"id": max([s["id"] for s in students], default=0) + 1,
		"name": name,
		"surname": surname,
		"date_of_birth": date_of_birth,
		"grades": {
			"mathematics": [],
			"polish": [],
			"english": []
		}
	}

	students.append(new_student)
	data.save_data(students)
	return True

def response_to_add_student(name: str, surname: str, date_of_birth: str):
	message = "Failed to add student"
	success = False
	if not name.strip() or not surname.strip() or not date_of_birth.strip():
		message = "Empty field"
	else:
		success = add_student(name, surname, date_of_birth)

	info = ui.Element()
	nav = ui.Element()

	if success:
		info = ui.Container(
			style,
			ui.Label("Student successfully added"),
			ui.Button("Ok", 0, ui_state, lambda: ui_state.change_ui(main_menu, main_menu))
		)

		nav = ui.Container(style, ui.Button("Ok", 0, ui_state, lambda: ui_state.change_ui(main_menu, main_menu)))
	else:
		info = ui.Container(
			style,
			ui.Label(message),
			ui.Button("Ok", 0, ui_state, lambda: add_student_ui())
		)
		nav = ui.Container(style, ui.Button("Ok", 0, ui_state, lambda: add_student_ui()))

	ui_state.change_ui(info, nav)

def edit_student(student: dict, name: str, surname: str, date_of_birth: str) -> bool:
	if not name.strip() or not surname.strip() or not date_of_birth.strip():
		return False

	student["name"] = name
	student["surname"] = surname
	student["date_of_birth"] = date_of_birth

	data.save_data(students)
	return True

def edit_student_ui(student: dict):
	name_field = ui.InputField("Name", 0, ui_state, default=student["name"])
	surname_field = ui.InputField("Surname", 1, ui_state, default=student["surname"])
	date_of_birth_field = ui.DateInputField(2, ui_state, default=student["date_of_birth"])

	edit_ui = ui.Container(
		style,
		name_field,
		surname_field,
		date_of_birth_field,
		ui.Button(
			"Save",
			3,
			ui_state,
			lambda: response_to_edit_student(
				student,
				name_field.value,
				surname_field.value,
				date_of_birth_field.value
			)
		),
		ui.Button("Back", 4, ui_state, lambda: ui_state.change_ui(main_menu, main_menu))
	)

	ui_state.change_ui(edit_ui, edit_ui)


def response_to_edit_student(student: dict, name: str, surname: str, date_of_birth: str):
	message = "Failed to update student"
	success = False

	if not name.strip() or not surname.strip() or not date_of_birth.strip():
		message = "Empty field"
	else:
		success = edit_student(student, name, surname, date_of_birth)

	info = ui.Element()
	nav = ui.Element()

	if success:
		info = ui.Container(
			style,
			ui.Label("Student successfully updated"),
			ui.Button("Ok", 0, ui_state, lambda: ui_state.change_ui(main_menu, main_menu))
		)

		nav = ui.Container(
			style,
			ui.Button("Ok", 0, ui_state, lambda: ui_state.change_ui(main_menu, main_menu))
		)
	else:
		info = ui.Container(
			style,
			ui.Label(message),
			ui.Button("Ok", 0, ui_state, lambda: edit_student(student, name, surname, date_of_birth))
		)

		nav = ui.Container(
			style,
			ui.Button("Ok", 0, ui_state, lambda: edit_student(student, name, surname, date_of_birth))
		)

	ui_state.change_ui(info, nav)


def show_students():
	go_back = ui.Button(
		"Back", 0, ui_state,
		lambda: ui_state.change_ui(main_menu, main_menu)
	)

	margin_style = ui.Style(20, ui.Alignment.CENTER)

	nav = ui.Container(margin_style, go_back)
	container = ui.Container(margin_style, go_back)

	if students:
		# Define columns explicitly (new schema)
		keys = ["id", "name", "surname", "date_of_birth"]

		widths = {}

		for k in keys:
			# start with header size
			max_len = len(k)

			for student in students:
				if k in ["id", "name", "surname", "date_of_birth"]:
					value = str(student.get(k, ""))
				else:
					value = str(student.get("grades", {}).get(k, ""))

				max_len = max(max_len, len(value))

			widths[k] = max_len
				
		header = " | ".join(f"{k:<{widths[k]}}" for k in keys)
		separator = "-+-".join("-" * widths[k] for k in keys)
		
		container.add_element(ui.Label(header))
		container.add_element(ui.Label(separator))

		for student in students:
			row = " | ".join(
				f"{(
					str(student.get(k, "")) if k in ["id", "name", "surname", "date_of_birth"]
					else str(student.get("grades", {}).get(k, ""))
				):<{widths[k]}}"
				for k in keys
			)

			btn = ui.Button(
				row,
				nav.element_count(),
				ui_state,
				lambda s=student: show_student(s)
			)

			container.add_element(btn)

			container.style.width = len(header)

			nav.add_element(btn)

	else:
		container.add_element(ui.Label("no students"))

	ui_state.change_ui(container, nav)

def return_list_of_floats(_list: list[str]) -> list[float]:
	new_list: list[float] = []
	for i in _list:
		try:
			new_list.append(float(i))
		except ValueError:
			pass
	return new_list

def average(l: list) -> float:
	nl = return_list_of_floats(l)
	if len(nl) == 0:
		return 0.0
	return sum(nl) / len(nl)


def show_student(student: dict):
	student_display = ui.Container(ui.Style(margin_left=2))

	nav = ui.Container(style)
	idx = 0
	grade_inputs: list[ui.InputField] = []

	for k, v in student.items():
		if k == "grades":
			avg = average([g for grades in v.values() for g in grades])
			
			student_display.add_element(ui.Label(f"{k}: (average: {avg:.2f})"))

			for name, grades_of_one_subject in v.items():
				input_field = ui.InputField("", idx, ui_state)
				input_field.value = " ".join(grades_of_one_subject)
				grade_inputs.append(input_field)

				h_sec = ui.HorizontalSection(ui.Style(), ui.Label(f"  {name}: "),  input_field, ui.Label(f" (average: {average(grades_of_one_subject):.2f})"))

				student_display.add_element(h_sec)
				nav.add_element(input_field)

				idx += 1

			continue
			
		student_display.add_element(ui.Label(f"{k}: {v}"))

	save_grades = ui.Button(
		"Save Grades",
		idx,
		ui_state,
		lambda: save_and_refresh(student, grade_inputs)
	)
	
	go_back = ui.Button("Back", idx+1, ui_state, show_students)

	edit_student = ui.Button("Edit Student", idx +2, ui_state, lambda: edit_student_ui(student))
	delete_student = ui.Button("Delete Student", idx +3, ui_state, lambda: delete_and_quit(student.get("id", None)))

	student_display.add_element(save_grades)

	student_display.add_element(go_back)

	student_display.add_element(edit_student)
	student_display.add_element(delete_student)

	nav.add_element(save_grades)

	nav.add_element(go_back)

	nav.add_element(edit_student)
	nav.add_element(delete_student)

	ui_state.change_ui(student_display, nav)

def save_and_refresh(student: dict, grade_inputs: list):
    values = [i.value for i in grade_inputs]
    update_grades(student, values)

    data.save_data(students)
    show_student(student)
	
def update_grades(student: dict, list_of_grades_of_subjects: list[str]) -> None:
	keys = list(student["grades"].keys())

	for key, grades in zip(keys, list_of_grades_of_subjects):
		student["grades"][key] = grades.split()


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