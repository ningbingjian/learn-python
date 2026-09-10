items = []
next_id = 1
while True:
    command = input("Command (add/list/pack/quit): ").strip().lower()
    match command:
        case "add":
            name = input("Name: ").strip()
            if not name:
                print("Error: name cannot be empty.")
                continue
            items.append({"id": next_id, "name": name, "packed": False})
            print(f"Added #{next_id}.")
            next_id += 1
        case "list":
            if not items:
                print("Empty.")
            for item in items:
                marker = "x" if item["packed"] else " "
                print(f"#{item['id']} [{marker}] {item['name']}")
        case "pack":
            try:
                target = int(input("Item id: "))
            except ValueError:
                print("Error: id must be an integer.")
                continue
            for item in items:
                if item["id"] == target:
                    if item["packed"]:
                        print("Already packed.")
                    else:
                        item["packed"] = True
                        print(f"Packed #{target}.")
                    break
            else:
                print(f"Error: item #{target} does not exist.")
        case "quit":
            print("Bye.")
            break
        case "":
            print("Enter a command.")
        case _:
            print(f"Unknown command: {command}")
