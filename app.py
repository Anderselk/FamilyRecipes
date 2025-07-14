# app.py

from core.recipe import Recipe
from core.storage import load_recipes, save_recipes

DATA_FILE = "recipes/data.json"

def display_menu():
    print("\n=== Family Recipes ===")
    print("[1] Add a recipe")
    print("[2] View a recipe")
    print("[3] Edit a recipe")
    print("[4] Delete a recipe")
    print("[5] Exit")
    print("[7] Manage tags")
    print("[8] Add tags to recipe")
    print("[9] Remove tags from recipe")



def add_recipe(recipes):
    name = input("Recipe name: ").strip()

    print("Enter ingredients one at a time. Press Enter on an empty line when done:")
    ingredients = []
    while True:
        ingredient = input("> ").strip()
        if ingredient == "":
            break
        ingredients.append(ingredient)

    print("Enter the instructions (you can paste or type it all at once):")
    instructions = input("> ").strip()

    recipe = Recipe(name, ingredients, instructions)
    recipes.append(recipe)
    save_recipes(recipes, DATA_FILE)
    print(f"✅ '{name}' added successfully!")


def view_recipes(recipes):
    if not recipes:
        print("No recipes found.")
        return

    filter_keyword = input("Enter a keyword to filter recipes (or press Enter to skip): ").strip().lower()
    filter_tag = input("Enter a tag to filter recipes (or press Enter to skip): ").strip().lower()

    filtered = list(recipes)
    if filter_keyword:
        filtered = [r for r in filtered if
                    filter_keyword in r.name.lower() or
                    any(filter_keyword in ing.lower() for ing in r.ingredients) or
                    filter_keyword in r.instructions.lower()]
    if filter_tag:
        filtered = [r for r in filtered if filter_tag in [t.lower() for t in r.tags]]

    if not filtered:
        print("No recipes match your filters.")
        return

    sorted_recipes = sorted(filtered, key=lambda r: r.name.lower())

    print("\n=== Recipes ===")
    for i, r in enumerate(sorted_recipes, start=1):
        print(f"[{i}] {r.name}")

    choice = input("\nEnter a number to view a recipe, or press Enter to go back: ").strip()

    if choice == "":
        return

    if not choice.isdigit():
        print("Invalid input. Please enter a number.")
        return

    index = int(choice) - 1
    if 0 <= index < len(sorted_recipes):
        r = sorted_recipes[index]
        print(f"\n=== {r.name} ===")
        print("Ingredients:")
        for ing in r.ingredients:
            print(f" - {ing}")
        print("Instructions:")
        print(r.instructions)
    else:
        print("Invalid recipe number.")


def edit_recipe(recipes):
    if not recipes:
        print("No recipes to edit.")
        return

    sorted_recipes = sorted(recipes, key=lambda r: r.name.lower())
    for i, r in enumerate(sorted_recipes, start=1):
        print(f"[{i}] {r.name}")

    choice = input("\nEnter the number of the recipe to edit (or press Enter to cancel): ").strip()
    if choice == "":
        return
    if not choice.isdigit() or not (1 <= int(choice) <= len(sorted_recipes)):
        print("Invalid choice.")
        return

    index = int(choice) - 1
    recipe = sorted_recipes[index]

    print(f"\nEditing '{recipe.name}'")
    new_name = input(f"New name (leave blank to keep '{recipe.name}'): ").strip()
    if new_name:
        recipe.name = new_name

    print("Edit ingredients (press Enter on an empty line to finish):")
    new_ingredients = []
    while True:
        ing = input("> ")
        if ing == "":
            break
        new_ingredients.append(ing)
    if new_ingredients:
        recipe.ingredients = new_ingredients

    new_instructions = input("New instructions (leave blank to keep existing): ").strip()
    if new_instructions:
        recipe.instructions = new_instructions

    save_recipes(recipes, DATA_FILE)
    print("✅ Recipe updated.")

def delete_recipe(recipes):
    if not recipes:
        print("No recipes to delete.")
        return

    sorted_recipes = sorted(recipes, key=lambda r: r.name.lower())
    for i, r in enumerate(sorted_recipes, start=1):
        print(f"[{i}] {r.name}")

    choice = input("\nEnter the number of the recipe to delete (or press Enter to cancel): ").strip()
    if choice == "":
        return
    if not choice.isdigit() or not (1 <= int(choice) <= len(sorted_recipes)):
        print("Invalid choice.")
        return

    index = int(choice) - 1
    to_delete = sorted_recipes[index]

    confirm = input(f"Are you sure you want to delete '{to_delete.name}'? (y/n): ").strip().lower()
    if confirm == "y":
        recipes.remove(to_delete)
        save_recipes(recipes, DATA_FILE)
        print("🗑️ Recipe deleted.")
    else:
        print("Canceled.")


from core.storage import load_tags, save_tags

def manage_tags():
    tags = load_tags()

    while True:
        print("\n=== Manage Tags ===")
        print("Current tags:", ", ".join(tags) if tags else "No tags yet.")
        print("[1] Add a tag")
        print("[2] Delete a tag")
        print("[3] Return to main menu")
        choice = input("Select: ").strip()

        if choice == "1":
            new_tag = input("New tag name: ").strip()
            if new_tag and new_tag not in tags:
                tags.append(new_tag)
                save_tags(tags)
                print(f"Tag '{new_tag}' added.")
            else:
                print("Tag already exists or invalid input.")

        elif choice == "2":
            if not tags:
                print("No tags to delete.")
                continue
            for i, t in enumerate(tags, 1):
                print(f"[{i}] {t}")
            to_del = input("Enter number of tag to delete (or Enter to cancel): ").strip()
            if to_del.isdigit() and 1 <= int(to_del) <= len(tags):
                removed = tags.pop(int(to_del) - 1)
                save_tags(tags)
                print(f"Tag '{removed}' deleted.")
            else:
                print("Canceled or invalid input.")

        elif choice == "3":
            break
        else:
            print("Invalid choice.")

def add_tags_to_recipe(recipes):
    tags = load_tags()
    if not tags:
        print("No tags defined. Please add tags first in Manage Tags.")
        return

    if not recipes:
        print("No recipes available.")
        return

    # Pick a recipe
    sorted_recipes = sorted(recipes, key=lambda r: r.name.lower())
    for i, r in enumerate(sorted_recipes, 1):
        print(f"[{i}] {r.name}")
    choice = input("Select recipe to add tags (or Enter to cancel): ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(sorted_recipes)):
        print("Canceled or invalid input.")
        return
    recipe = sorted_recipes[int(choice) - 1]

    # Show current tags
    print(f"Current tags on '{recipe.name}': {', '.join(recipe.tags) if recipe.tags else 'None'}")

    # Select tags to add
    print("Available tags:")
    for i, t in enumerate(tags, 1):
        print(f"[{i}] {t}")
    tag_choices = input("Enter tag numbers to add, separated by commas: ").strip()
    if not tag_choices:
        print("No tags added.")
        return

    indices = [int(x) for x in tag_choices.split(",") if x.strip().isdigit()]
    for idx in indices:
        if 1 <= idx <= len(tags):
            tag = tags[idx - 1]
            if tag not in recipe.tags:
                recipe.tags.append(tag)

    save_recipes(recipes, DATA_FILE)
    print(f"Tags updated for '{recipe.name}'.")


def remove_tags_from_recipe(recipes):
    if not recipes:
        print("No recipes available.")
        return

    # Pick a recipe
    sorted_recipes = sorted(recipes, key=lambda r: r.name.lower())
    for i, r in enumerate(sorted_recipes, 1):
        print(f"[{i}] {r.name}")
    choice = input("Select recipe to remove tags from (or Enter to cancel): ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(sorted_recipes)):
        print("Canceled or invalid input.")
        return
    recipe = sorted_recipes[int(choice) - 1]

    if not recipe.tags:
        print(f"'{recipe.name}' has no tags.")
        return

    # Show current tags
    print(f"Current tags on '{recipe.name}':")
    for i, t in enumerate(recipe.tags, 1):
        print(f"[{i}] {t}")

    tag_choices = input("Enter tag numbers to remove, separated by commas: ").strip()
    if not tag_choices:
        print("No tags removed.")
        return

    indices = [int(x) for x in tag_choices.split(",") if x.strip().isdigit()]
    removed_any = False
    for idx in sorted(indices, reverse=True):  # remove from end to avoid index shift
        if 1 <= idx <= len(recipe.tags):
            removed_tag = recipe.tags.pop(idx - 1)
            removed_any = True
            print(f"Removed tag '{removed_tag}'")

    if removed_any:
        save_recipes(recipes, DATA_FILE)
    else:
        print("No valid tags removed.")


def main():
    recipes = load_recipes(DATA_FILE)

    while True:
        display_menu()
        choice = input("Select an option: ").strip()

        if choice == "1":
            add_recipe(recipes)
        elif choice == "2":
            view_recipes(recipes)
        elif choice == "3":
            edit_recipe(recipes)
        elif choice == "4":
            delete_recipe(recipes)
        elif choice == "5":
            print("Goodbye!")
            break
        elif choice == "7":
            manage_tags()
        elif choice == "8":
            add_tags_to_recipe(recipes)
        elif choice == "9":
            # You still need to implement remove_tags_from_recipe()
            remove_tags_from_recipe(recipes)  # You can add this next
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()

