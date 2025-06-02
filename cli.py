from lib.db.connection import CONN, CURSOR
from lib.db.models.owner import Owner
from lib.db.models.pet import Pet
from tabulate import tabulate


Owner.CONN = CONN
Owner.CURSOR = CURSOR
Pet.CONN = CONN
Pet.CURSOR = CURSOR

def add_owner():
    name = input("Enter owner's name: ")
    owner = Owner(name)
    owner.save()
    print(f"Owner '{name}' added with ID {owner.id}.")

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
    print(f"Pet '{name}' added for owner '{owner.name}'.")

def show_pets_for_owner():
    owner_id = input("Enter Owner ID to view their pets: ")

    try:
        owner = Owner.find_by_id(int(owner_id))
    except ValueError:
        print("Invalid ID format.")
        return

    if not owner:
        print("Owner not found.")
        return

    pets = Pet.find_by_owner_id(owner.id)

    if pets:
        data = [(pet.id, pet.name, pet.pet_type) for pet in pets]
        print(tabulate(data, headers=["Pet ID", "Name", "Type"], tablefmt="fancy_grid"))
    else:
        print(f"{owner.name} has no pets yet.")

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
        print(tabulate(
            results,
            headers=["Owner ID", "Owner Name", "Pet ID", "Pet Name", "Pet Type"],
            tablefmt="grid"
        ))
    else:
        print("No owners or pets found.")

def run():
    while True:
        print("\nPetPal Menu")
        print("1. Add Owner")
        print("2. Add Pet")
        print("3. Show Pets for an Owner")
        print("4. Show All Owners and Pets")
        print("5. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            add_owner()
        elif choice == "2":
            add_pet()
        elif choice == "3":
            show_pets_for_owner()
        elif choice == "4":
            show_owners_and_pets()
        elif choice == "5":
            print("Exiting PetPal. Bye!")
            break
        else:
            print("Invalid option. Please try again.")

    CONN.close()

if __name__ == "__main__":
    run()
