import argparse
import json
import sys

from .api import get_fruit, FruitNotFoundError


def main():
    parser = argparse.ArgumentParser(
        description="Looks up fruit info from FruityVice"
    )

    parser.add_argument(
        "fruit", 
        nargs="+", 
        help="name of the fruit (eg. strawberry)"
    )
    
    parser.add_argument(
        "--format",
        choices=["human", "json"],
        default="human",
        help="output format options: human (default) or json")

    args = parser.parse_args()

    try:
        fruit = get_fruit(" ".join(args.fruit))
    except FruitNotFoundError as error:
        print(f"Error: {error}")
        sys.exit(1)
    except Exception as error:
        print(f"Error: {error}")
        sys.exit(1)

    if args.format == "json":
        print(json.dumps(fruit.to_dict(), indent=2))
    elif args.format == "human":
        print(f"Name: {fruit.name}")
        print(f"ID: {fruit.id}")
        print(f"Family: {fruit.family}")
        print(f"Sugar: {fruit.sugar}g")
        print(f"Carbohydrates: {fruit.carbs}g")


if __name__ == "__main__":
    main()
