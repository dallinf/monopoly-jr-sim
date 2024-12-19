from color import Color
from space import Space


class Board:
    def __init__(self):
        self._setup()
        self.spaces = [self.go_space]
        current_space = self.go_space
        while current_space.next != self.go_space:
            self.spaces.append(current_space.next)
            current_space = current_space.next

    def find_space_distance(self, current_space: Space, space_to_find: Space) -> Space:
        distance = 0
        while current_space != space_to_find:
            current_space = current_space.next
            distance += 1
        return distance

    def get_space(self, space: Space, roll: int) -> Space:
        for _ in range(roll):
            space = space.next
        return space
    
    def find_next_unowned_property(self, space: Space) -> Space:
        beginning_space = space
        current_space = space.next
        while current_space != beginning_space:
            if current_space.owner is None and current_space.cost > 0:
                return current_space
            current_space = current_space.next
        return None

    def find_max_unowned_property(self, space: Space) -> Space:
        beginning_space = space
        current_space = space.next
        max_space = None
        while current_space != beginning_space:
            if current_space.owner is None and current_space.cost > 0:
                if max_space is None or current_space.cost > max_space.cost:
                    max_space = current_space
            current_space = current_space.next
        return max_space
    
    def passed_go(self, original_space: Space, new_space: Space) -> bool:
        current_space = original_space
        while current_space != new_space:
            current_space = current_space.next
            if current_space.is_go:
                return True
        return False

    def _setup(self):
        self.go_space = Space("Go", 0, None, Color.WHITE)
        self.go_space.is_go = True

        food_truck = Space("Food Truck", 1, self.go_space, Color.BROWN)
        self.go_space.next = food_truck
        pizza_parlor = Space("Pizza Parlor", 1, food_truck, Color.BROWN)
        food_truck.next = pizza_parlor
        pizza_parlor.partner = food_truck
        food_truck.partner = pizza_parlor

        chance_1 = Space("Chance 1", 0, pizza_parlor, Color.WHITE)
        pizza_parlor.next = chance_1
        chance_1.is_chance = True
        donut_shop = Space("Donut Shop", 1, chance_1, Color.LIGHT_BLUE)
        chance_1.next = donut_shop
        ice_cream_shop = Space("Ice Cream Shop", 1, donut_shop, Color.LIGHT_BLUE)
        donut_shop.next = ice_cream_shop
        ice_cream_shop.partner = donut_shop
        donut_shop.partner = ice_cream_shop

        timeout_corner = Space("Just Visiting", 0, ice_cream_shop, Color.WHITE)
        ice_cream_shop.next = timeout_corner

        museum = Space("Museum", 2, timeout_corner, Color.PINK)
        timeout_corner.next = museum
        library = Space("Library", 2, museum, Color.PINK)
        museum.next = library
        library.partner = museum
        museum.partner = library

        chance_2 = Space("Chance 2", 0, library, Color.WHITE)
        library.next = chance_2
        chance_2.is_chance = True

        park = Space("Park", 2, chance_2, Color.ORANGE)
        chance_2.next = park
        self.beach = Space("Beach", 2, park, Color.ORANGE)
        park.next = self.beach
        self.beach.partner = park
        park.partner = self.beach

        free_parking = Space("Free Parking", 0, self.beach, Color.WHITE)
        self.beach.next = free_parking

        post_office = Space("Post Office", 3, free_parking, Color.RED)
        free_parking.next = post_office
        train_station = Space("Train Station", 3, post_office, Color.RED)
        post_office.next = train_station
        train_station.partner = post_office
        post_office.partner = train_station

        chance_3 = Space("Chance 3", 0, train_station, Color.WHITE)
        train_station.next = chance_3
        chance_3.is_chance = True

        community_garden = Space("Community Garden", 3, chance_3, Color.YELLOW)
        chance_3.next = community_garden
        pet_rescue = Space("Pet Rescue", 3, community_garden, Color.YELLOW)
        community_garden.next = pet_rescue
        pet_rescue.partner = community_garden
        community_garden.partner = pet_rescue

        self.goto_timeout = Space("Go To Timeout", 0, pet_rescue, Color.WHITE)
        self.goto_timeout.is_goto = True
        pet_rescue.next = self.goto_timeout

        aquarium = Space("Aquarium", 4, self.goto_timeout, Color.GREEN)
        self.goto_timeout.next = aquarium
        zoo = Space("Zoo", 4, aquarium, Color.GREEN)
        aquarium.next = zoo
        zoo.partner = aquarium
        aquarium.partner = zoo

        chance_4 = Space("Chance 4", 0, zoo, Color.WHITE)
        zoo.next = chance_4
        chance_4.is_chance = True

        water_park = Space("Water Park", 5, chance_4, Color.BLUE)
        chance_4.next = water_park
        self.amusement_park = Space("Amusement Park", 5, water_park, Color.BLUE)
        water_park.next = self.amusement_park
        self.amusement_park.partner = water_park
        water_park.partner = self.amusement_park
        self.amusement_park.next = self.go_space

        self.go_space.prev = self.amusement_park
