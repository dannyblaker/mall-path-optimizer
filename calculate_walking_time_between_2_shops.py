import random

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

    def get_shop_coordinates(self, shop_name):
        for shop in self.shops:
            if shop.name == shop_name:
                return shop.x, shop.y, shop.floor
        return None

    def calculate_walking_time(self, shop1_name, shop2_name):
        shop1 = self.get_shop_coordinates(shop1_name)
        shop2 = self.get_shop_coordinates(shop2_name)

        if shop1 is None or shop2 is None:
            return "Shop not found."

        if shop1[2] != shop2[2]:  # Different floors, need to take elevators
            elevator_time = 30  # Assume 30 seconds to travel between floors
            walking_time = abs(shop1[0] - shop2[0]) + abs(shop1[1] - shop2[1]) + elevator_time
        else:
            walking_time = abs(shop1[0] - shop2[0]) + abs(shop1[1] - shop2[1])

        return walking_time

# Create a 3-floor mall with 5 shops per floor
mall = Mall(3, 5)
mall.generate_mall()

# Calculate walking time between two shops
shop1_name = "Shop_1_1"
shop2_name = "Shop_2_3"
walking_time = mall.calculate_walking_time(shop1_name, shop2_name)
print(f"Walking time between {shop1_name} and {shop2_name}: {walking_time} seconds")
