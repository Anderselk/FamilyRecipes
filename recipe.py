class Recipe:
    def __init__(self, name, ingredients, instructions, tags=None):
        self.name = name
        self.ingredients = ingredients
        self.instructions = instructions
        self.tags = tags if tags else []  # list of strings

    def to_dict(self):
        return {
            "name": self.name,
            "ingredients": self.ingredients,
            "instructions": self.instructions,
            "tags": self.tags
        }

    @staticmethod
    def from_dict(data):
        return Recipe(
            data["name"],
            data["ingredients"],
            data["instructions"],
            data.get("tags", [])
        )
