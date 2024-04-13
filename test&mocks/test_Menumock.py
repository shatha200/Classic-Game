import unittest
from unittest.mock import MagicMock
from Menu import*


 # Mocking pygame module
pygame = MagicMock()

# Mocking pygame.mouse module
pygame.mouse = MagicMock()

# Mocking pygame.mouse.get_pos function
pygame.mouse.get_pos = MagicMock(return_value=(0, 0))

# Mocking pygame.mouse.get_pressed function
pygame.mouse.get_pressed = MagicMock(return_value=(0, 0, 0))



class TestChar(unittest.TestCase):
    def test_char_creation(self):
        x, y = 0, 0
        image = MagicMock()
        char = Char(x, y, image)
        self.assertEqual(char.rect.x, x)
        self.assertEqual(char.rect.y, y)
        self.assertFalse(char.clicked)

    

class TestButton(unittest.TestCase):
    def test_button_creation(self):
        x, y = 0, 0
        image = MagicMock()
        button = Button(x, y, image)
        self.assertEqual(button.rect.x, x)
        self.assertEqual(button.rect.y, y)
        self.assertFalse(button.clicked)


if __name__ == '__main__':
    unittest.main()
