import unittest
from func import Elevator, Computer
from time import time, sleep
from threading import Thread

class TestElv(unittest.TestCase):
    def setUp(self) -> None:
        self.elv = Elevator(name='test_elv', floor=4)

    def tearDown(self) -> None:
        self.elv.running = False

    def test_move(self):
        st = time()
        self.elv.move(self.elv.display_floor(), 9)
        et = time()
        self.assertEqual(self.elv.display_floor(), 9, f'elv @ {self.elv.display_floor()} but expect 9')
        self.assertGreaterEqual(et-st, 5, f'spent {et-st}s but expect more than 5s')
        st = time()
        self.elv.move(self.elv.display_floor(), 7)
        et = time()
        self.assertEqual(self.elv.display_floor(), 7, f'elv @ {self.elv.display_floor()} but expect 7')
        self.assertGreaterEqual(et-st, 2, f'spent {et-st}s but expect more than 2s')
        st = time()
        self.elv.move(self.elv.display_floor(), 8)
        et = time()
        self.assertEqual(self.elv.display_floor(), 8, f'elv @ {self.elv.display_floor()} but expect 8')
        self.assertGreaterEqual(et-st, 1, f'spent {et-st}s but expect more than 1s')

class TestCom(unittest.TestCase):
    def setUp(self) -> None:
        self.com = Computer()
        self.com_thread = Thread(target=self.com.get_tasks)
        self.com_thread.start()
    
    def tearDown(self) -> None:
        self.com.running = False
        self.com_thread.join()
    
    def test1(self):
        self.com.tasks.put((0, 1, 5))
        sleep(0.1)
        self.com.tasks.put((1, 2, 4))
        sleep(4)
        self.assertTrue((self.com.elevator1.display_floor() == 5 and self.com.elevator2.display_floor() == 1)
                        or (self.com.elevator1.display_floor() == 1 and self.com.elevator2.display_floor() == 5),
                        f'elv1 @ {self.com.elevator1.display_floor()}, elv2 @ {self.com.elevator2.display_floor()}')

    def test2(self):
        self.com.tasks.put((0, 1, 5))
        sleep(0.1)
        self.com.tasks.put((1, 4, 2))
        sleep(5)
        self.assertTrue((self.com.elevator1.display_floor() == 5 and self.com.elevator2.display_floor() == 2)
                        or (self.com.elevator1.display_floor() == 2 and self.com.elevator2.display_floor() == 5),
                        f'elv1 @ {self.com.elevator1.display_floor()}, elv2 @ {self.com.elevator2.display_floor()}')
    
    def test3(self):
        self.com.tasks.put((0, 1, 10))
        sleep(0.1)
        self.com.tasks.put((1, 7, 5))
        sleep(9)
        self.assertTrue((self.com.elevator1.display_floor() == 5 and self.com.elevator2.display_floor() == 10)
                        or (self.com.elevator1.display_floor() == 10 and self.com.elevator2.display_floor() == 5),
                        f'elv1 @ {self.com.elevator1.display_floor()}, elv2 @ {self.com.elevator2.display_floor()}')
        self.com.tasks.put((2, 6, 4))
        sleep(3)
        self.assertTrue((self.com.elevator1.display_floor() == 4 and self.com.elevator2.display_floor() == 10)
                        or (self.com.elevator1.display_floor() == 10 and self.com.elevator2.display_floor() == 4),
                        f'elv1 @ {self.com.elevator1.display_floor()}, elv2 @ {self.com.elevator2.display_floor()}')

if __name__ == '__main__':
   unittest.main()