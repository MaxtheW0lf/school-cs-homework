import json

def save_data(data):
    with open("data.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

def read_data():
    with open("data.json", "r", encoding="utf-8") as file:
        return json.load(file)



def print_data(data:list[dict]):
    for el in data:
        print("==="*20)
        for k,v in el.items():
            print(f"{k} ----- {v}")
