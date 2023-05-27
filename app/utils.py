import random
import string
from geopy.distance import geodesic

def calculate_distance(location1, location2):
    return geodesic(location1, location2).miles


def generate_unique_number():
    number = random.randint(1000, 9999)
    letter = random.choice(string.ascii_uppercase)
    return f"{number}{letter}"