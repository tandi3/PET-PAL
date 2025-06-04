from lib.db.connection import CONN, CURSOR
from lib.db.models.owner import Owner
from lib.db.models.pet import Pet
from tabulate import tabulate

def add_owner():
    name = input("Enter owner's name: ")
    owner = Owner(name)
    owner.save()
    print(f"Owner '{name}' added with ID {owner.id}.")

def add_pet():
    name = input("Enter pet's name: ")
    pet_type = input("Enter pet type: ")
    owner_id = input("Enter owner ID: ")
    pet = Pet(name, pet_type, owner_id)
    pet.save()
    print(f"Pet '{name}' added for Owner ID {owner_id}.")

def show_pets_for_owner():
    owner_id = input("Enter Owner ID to view their pets: ")
    pets = Pet.find_by_owner_id(owner_id)
    if pets:
        for pet in pets:
            print(f"Pet ID: {pet.id}, Name: {pet.name}, Type: {pet.pet_type}")
    else:
        print("No pets found for this owner.")

def show_owners_and_pets():
    query = """
    SELECT owners.id, owners.name, pets.id, pets.name, pets.pet_type
    FROM owners
    LEFT JOIN pets ON owners.id = pets.owner_id
    ORDER BY owners.id;
    """
    CURSOR.execute(query)
    results = CURSOR.fetchall()

    if results:
        print(tabulate(results, headers=["Owner ID", "Owner Name", "Pet ID", "Pet Name", "Pet Type"], tablefmt="grid"))
    else:
        print("No owners or pets found.")

def main_menu():
    while True:
        print("\nPetPal Menu")
        print("1. Add Owner")
        print("2. Add Pet")
        print("3. Show Pets for an Owner")
        print("4. Exit")
        print("5. Show All Owners and Pets")  # new option added

        choice = input("Select an option: ")

        if choice == "1":
            add_owner()
        elif choice == "2":
            add_pet()
        elif choice == "3":
            show_pets_for_owner()
        elif choice == "4":
            show_owners_and_pets()
            break
        elif choice == "5":
            print("Exiting PetPal. Bye!")
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    main_menu()

