import unittest
from  EnemyClasses import *
class TestEnemy(unittest.TestCase):

    def test_enemy_movement(self):
        enemy = Enemy(100, 200)

        # Call update multiple times (simulate movement)
        for _ in range(100):
            enemy.update()

        # Assert enemy moved to the right
        self.assertGreater(enemy.rect.x, 100)

        # Call update more times (direction change)
        for _ in range(100):
            enemy.update()

        # Assert enemy moved to the left
        self.assertLess(enemy.rect.x, 100)
