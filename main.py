from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['cats_db']
collection = db['cats']

def create_cat(name, age, features):
    """
    Create a new cat document in the MongoDB collection.

    Parameters:
    name (str): The name of the cat.
    age (int): The age of the cat.
    features (list of str): A list of features/characteristics of the cat.

    Returns:
    None
    """
    try:
        # Construct the new cat document
        new_cat = {
            "name": name,
            "age": age,
            "features": features
        }
        # Insert the new cat into the collection
        result = collection.insert_one(new_cat)
        print(f"New cat created with _id: {result.inserted_id}")
    except Exception as e:
        print(f"An error occurred: {e}")

def read_all():
    """
    Retrieve and print all cat documents from the MongoDB collection.

    Parameters:
    None

    Returns:
    None
    """
    try:
        # Iterate over all documents in the collection and print them
        for cat in collection.find():
            print(cat)
    except Exception as e:
        print(f"An error occurred: {e}")

def read_by_name(name):
    """
    Retrieve and print a cat document from the MongoDB collection based on the cat's name.

    Parameters:
    name (str): The name of the cat to find.

    Returns:
    None
    """
    try:
        # Find the first document that matches the given name
        cat = collection.find_one({"name": name})
        if cat:
            print(cat)
        else:
            print("No cat found with that name.")
    except Exception as e:
        print(f"An error occurred: {e}")

def update_age(name, age):
    """
    Update the age of a cat document in the MongoDB collection based on the cat's name.

    Parameters:
    name (str): The name of the cat to update.
    age (int): The new age to set for the cat.

    Returns:
    None
    """
    try:
        # Update the age of the cat that matches the given name
        result = collection.update_one({"name": name}, {"$set": {"age": age}})
        if result.modified_count:
            print("Cat's age updated successfully.")
        else:
            print("No cat found with that name or age is the same.")
    except Exception as e:
        print(f"An error occurred: {e}")

def add_feature(name, feature):
    """
    Add a new feature to the features list of a cat document in the MongoDB collection based on the cat's name.

    Parameters:
    name (str): The name of the cat to update.
    feature (str): The new feature to add to the cat's features list.

    Returns:
    None
    """
    try:
        # Add a new feature to the cat's features list
        result = collection.update_one({"name": name}, {"$addToSet": {"features": feature}})
        if result.modified_count:
            print("Feature added successfully.")
        else:
            print("No cat found with that name or feature already exists.")
    except Exception as e:
        print(f"An error occurred: {e}")

def delete_by_name(name):
    """
    Delete a cat document from the MongoDB collection based on the cat's name.

    Parameters:
    name (str): The name of the cat to delete.

    Returns:
    None
    """
    try:
        # Delete the cat that matches the given name
        result = collection.delete_one({"name": name})
        if result.deleted_count:
            print("Cat deleted successfully.")
        else:
            print("No cat found with that name.")
    except Exception as e:
        print(f"An error occurred: {e}")

def delete_all():
    """
    Delete all cat documents from the MongoDB collection.

    Parameters:
    None

    Returns:
    None
    """
    try:
        # Delete all documents in the collection
        result = collection.delete_many({})
        print(f"All cats deleted. Count: {result.deleted_count}")
    except Exception as e:
        print(f"An error occurred: {e}")


print("MongoDB CRUD operations:")
print("Creating cats...")
create_cat('barsik', 3, ["ходить в капці", "дає себе гладити", "рудий"])
create_cat('murchik', 3, ["багато їсть", "багато спить", "сірий"])
print("Reading all cats...")
read_all()
print("Reading cat by name...")
read_by_name('barsik')
print("Updating cat's age...")
update_age('barsik', 4)
print("Adding feature to cat...")
add_feature('barsik', 'любить іграшки')
print("Deleting cat by name...")
delete_by_name('barsik')
print("Deleting all cats...")
delete_all()
