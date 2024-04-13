import unittest
from World import*

class TestWorld(unittest.TestCase):

    def test_initialization(self):
        # Simplified world map data
        map_data = [
            [1, 2, 3],
            [4, 5, 6],
        ]

        world = World(map_data)
    def test_draw_basic(self):
        pygame.init()
        win = pygame.Surface((1, 1))  
        map_data = [[0]]  
        world = World(map_data)
        pygame.quit()
