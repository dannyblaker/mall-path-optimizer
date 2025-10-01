import random
import json


class Shop:
    def __init__(self, name, floor, x, y):
        self.name = name
        self.floor = floor
        self.x = x
        self.y = y


class Mall:
    def __init__(self, num_floors, num_shops_per_floor):
        self.num_floors = num_floors
        self.num_shops_per_floor = num_shops_per_floor
        self.shops = []

    def generate_mall(self):
        for floor in range(1, self.num_floors + 1):
            for shop_id in range(1, self.num_shops_per_floor + 1):
                shop_name = f'Shop_{floor}_{shop_id}'
                x = random.uniform(0, 100)
                y = random.uniform(0, 100)
                self.shops.append(Shop(shop_name, floor, x, y))

    def to_json(self):
        shop_data = [{'name': shop.name, 'floor': shop.floor,
                      'x': shop.x, 'y': shop.y} for shop in self.shops]
        return json.dumps(shop_data, indent=4)


# Create a 3-floor mall with 5 shops per floor
mall = Mall(3, 5)
mall.generate_mall()

# Convert mall data to JSON
json_data = mall.to_json()

# Save JSON data to a file
with open('mall_coordinates.json', 'w') as json_file:
    json_file.write(json_data)

print("Mall coordinates saved to mall_coordinates.json")
