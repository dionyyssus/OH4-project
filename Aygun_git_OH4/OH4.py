file_name = "data.txt"


def add_person():
    id = input("ID: ").strip()

    # 1. Dosyadaki mevcut ID'leri kontrol et (Benzersizlik kontrolü)
    try:
        with open(file_name, "r") as f:
            lines = f.readlines()
            for line in lines:
                if line.strip():
                    existing_id = line.strip().split(";")[0]
                    if existing_id == id:
                        print(f"Error: Person with ID '{id}' already exists!")
                        return
    except FileNotFoundError:
        pass  # Dosya henüz oluşturulmadıysa devam et

    # 2. ID benzersizse diğer bilgileri al
    name = input("Name: ").strip()
    surname = input("Surname: ").strip()
    age = input("Age: ").strip()

    with open(file_name, "a") as f:
        f.write(f"{id};{name};{surname};{age}\n")

    print("Added successfully!")


def read_all():
    try:
        with open(file_name, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("File is empty.")
        return

    if len(lines) == 0:
        print("File is empty.")
        return

    print("\n--- ALL RECORDS ---")
    for line in lines:
        if line.strip():
            id, name, surname, age = line.strip().split(";")
            print(f"ID: {id} | {name} {surname} | Age: {age}")


def search_person():
    search_id = input("Enter ID: ").strip()
    found = False

    try:
        with open(file_name, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("File not found!")
        return

    for line in lines:
        if line.strip():
            id, name, surname, age = line.strip().split(";")
            if id == search_id:
                print(f"Found: {name} {surname}, Age: {age}")
                found = True
                break

    if not found:
        print("ID not found!")


def update_person():
    update_id = input("Enter ID to update: ").strip()

    try:
        with open(file_name, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("File not found!")
        return

    new_lines = []
    found = False

    for line in lines:
        if line.strip():
            id, name, surname, age = line.strip().split(";")

            if id == update_id:
                name = input("New name: ").strip()
                surname = input("New surname: ").strip()
                age = input("New age: ").strip()
                new_lines.append(f"{id};{name};{surname};{age}\n")
                found = True
            else:
                new_lines.append(line)

    if found:
        with open(file_name, "w") as f:
            f.writelines(new_lines)
        print("Updated successfully!")
    else:
        print("ID not found!")


def delete_person():
    delete_id = input("Enter ID to delete: ").strip()

    try:
        with open(file_name, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("File not found!")
        return

    new_lines = []
    found = False

    for line in lines:
        if line.strip():
            id, name, surname, age = line.strip().split(";")
            if id != delete_id:
                new_lines.append(line)
            else:
                found = True

    if found:
        with open(file_name, "w") as f:
            f.writelines(new_lines)
        print("Deleted successfully!")
    else:
        print("ID not found!")


def main():
    while True:
        print("\n--- MENU ---")
        print("1. Add")
        print("2. Show all")
        print("3. Search")
        print("4. Update")
        print("5. Delete")
        print("0. Exit")

        choice = input("Choice: ").strip()

        if choice == "1":
            add_person()
        elif choice == "2":
            read_all()
        elif choice == "3":
            search_person()
        elif choice == "4":
            update_person()
        elif choice == "5":
            delete_person()
        elif choice == "0":
            print("Exited!")
            break
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()