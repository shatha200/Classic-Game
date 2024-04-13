import unittest
from unittest.mock import MagicMock
from World import*


# Mocking pygame module
pygame = MagicMock()

# Mocking pygame.sprite.Sprite class
class SpriteMock(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = MagicMock()
        self.rect = MagicMock()

# Mocking pygame.image.load function
pygame.image.load = MagicMock()

class TestWorld(unittest.TestCase):
    def test_world_creation(self):
        # Mocking return value for pygame.image.load
        pygame.image.load.return_value = MagicMock()
        
        data = [
            [1, 2]
        ]
        world = World(data)
        self.assertEqual(len(world.tile_list), 2) 

if __name__ == '__main__':
    unittest.main()

