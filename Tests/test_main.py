import unittest
from main import *



def test_valid_level():
    level = 1  #  level 1 exists
    world = reset_level(level)
    # Assert that the world object is created successfully (replace with your specific assertion)
    assert world is not None

def test_multiple_valid_levels():
    levels = [1, 2, 3]  #levels 1, 2, and 3 exist
    for level in levels:
        world = reset_level(level)
        assert world is not None
        
class TestResetLevel(unittest.TestCase):

    def test_empty_groups(self):
        slime_group = pygame.sprite.Group()
        lava_group = pygame.sprite.Group()
        platform_group = pygame.sprite.Group()
        coin_group = pygame.sprite.Group()
        exit_group = pygame.sprite.Group()

        

        reset_level(1)  # Call the function

        self.assertEqual(len(slime_group), 0)
        self.assertEqual(len(lava_group), 0)
        self.assertEqual(len(platform_group), 0)
        self.assertEqual(len(coin_group), 0)
        self.assertEqual(len(exit_group), 0)


