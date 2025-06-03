from lib.db.connection import CONN, CURSOR
from lib.db.models.owner import Owner
from lib.db.models.pet import Pet

def menu():
    print("\nPetPal Menu")
    print("1. Add Owner")
    print("2. Add Pet")
    print("3. Show Pets for an Owner")
    print("4. Exit")

def add_owner():
    name = input("Enter owner's name: ")
    owner = Owner(name)
    owner.save()
    print(f"Owner '{owner.name}' added with ID {owner.id}.")

def add_pet():
    name = input("Enter pet's name: ")
    pet_type = input("Enter pet type: ")
    owner_id = input("Enter owner ID: ")

    try:
        owner = Owner.find_by_id(int(owner_id))
    except ValueError:
        print("Invalid ID format.")
        return

    if not owner:
        print("Owner not found.")
        return

    pet = Pet(name=name, pet_type=pet_type, owner_id=owner.id)
    pet.save()
    print(f"Pet '{pet.name}' added for Owner '{owner.name}'.")

def show_pets_for_owner():
    owner_id = input("Enter owner ID: ")
    try:
        owner = Owner.find_by_id(int(owner_id))
    except ValueError:
        print("Invalid ID format.")
        return

    if not owner:
        print("Owner not found.")
        return

    pets = Pet.find_by_owner_id(owner.id)
    if not pets:
        print(f"No pets found for Owner '{owner.name}'.")
    else:
        print(f"Pets for Owner '{owner.name}':")
        for pet in pets:
            print(f"- {pet.name} ({pet.pet_type})")

if __name__ == "__main__":
    while True:
        menu()
        choice = input("Select an option: ")
        if choice == "1":
            add_owner()
        elif choice == "2":
            add_pet()
        elif choice == "3":
            show_pets_for_owner()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")
