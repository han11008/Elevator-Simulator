from time import sleep
from enum import Enum
from queue import Empty, Queue
from random import choice
from threading import Thread

class PassengerState(Enum):
    WAITING = 0
    SCHEDULED = 1
    TAKING = 2
    ARRIVED = 3

class ElevatorState(Enum):
    UP = False
    DOWN = True
    STOP = None

class Elevator(object):
    def __init__(self, name: str, floor: int = 1):
        self.current_floor = floor
        self.target_floor = None
        self.moving_queue = Queue()
        self.running = True
        self.moving = False
        self.name = name
        self.state = ElevatorState.STOP

    def display_floor(self) -> int:
        return self.current_floor
    
    def move(self, current: int, floor: int):
        if floor > 10 or floor < 1:
            return
        self.moving = True
        self.state = floor < self.current_floor
        while self.current_floor != floor:
            self.current_floor += -1 if self.state else 1
            # print(f'{self.name} @ {self.display_floor()}')
            sleep(1)
        self.moving = False

class Computer(object):
    def __init__(self):
        self.elevator1 = Elevator(name='e1')
        self.elevator2 = Elevator(name='e2')
        self.tasks = Queue()
        self.waiting_queue = Queue()
        self.task_state: dict[int, tuple[int, Elevator, int, int]] = {} # tid: (PassengerState, Elevator, from, to)
        self.running = True

        self.elv1_thread = Thread(target=self.elevator_move, args=[self.elevator1])
        self.elv2_thread = Thread(target=self.elevator_move, args=[self.elevator2])
        self.elv1_thread.start()
        self.elv2_thread.start()

    def check_waiting(self):
        if not self.waiting_queue.empty():
            if (
                self.elevator1.target_floor is None and self.elevator1.running and
                self.elevator2.target_floor is None and self.elevator2.running
            ):
                tid, psg_flr, tar = self.waiting_queue.get()
                dist1 = abs(self.elevator1.display_floor() - psg_flr)
                dist2 = abs(self.elevator2.display_floor() - psg_flr)
                if dist1 > dist2:
                    pick = self.elevator2
                elif dist1 < dist2:
                    pick = self.elevator1
                else:
                    pick = choice([self.elevator1, self.elevator2])
            elif self.elevator1.target_floor is None and self.elevator1.running:
                pick = self.elevator1
                tid, psg_flr, tar = self.waiting_queue.get()
            elif self.elevator2.target_floor is None and self.elevator2.running:
                pick = self.elevator2
                tid, psg_flr, tar = self.waiting_queue.get()
            else:
                return
            self.task_state[tid] = (PassengerState.SCHEDULED, pick, psg_flr, tar)
            pick.target_floor = tar
            pick.moving_queue.put((pick.display_floor(), psg_flr))
            pick.moving_queue.put((psg_flr, tar)) 

    def new_task(self):
        try:
            tid, psg_flr, tar = self.tasks.get(block=False)
            # print(f'get task: ({tid}, {psg_flr}, {tar})')
            self.task_state[tid] = (PassengerState.WAITING, None, psg_flr, tar)
            # Check if the passenger can take a moving elevator
            psg_dir = tar < psg_flr # True for going down while False for going up
            elv1_ava = elv2_ava = False
            if self.elevator1.target_floor is not None:
                if psg_dir == self.elevator1.state:
                    if (
                        (psg_dir and self.elevator1.target_floor <= psg_flr <= self.elevator1.display_floor()) or
                        (not psg_dir and self.elevator1.display_floor() <= psg_flr <= self.elevator1.target_floor)
                    ):
                        elv1_ava = True
            if self.elevator2.target_floor is not None:
                if psg_dir == self.elevator2.state:
                    if (
                        (psg_dir and self.elevator2.target_floor <= psg_flr <= self.elevator2.display_floor()) or
                        (not psg_dir and self.elevator2.display_floor() <= psg_flr <= self.elevator2.target_floor)
                    ):
                        elv2_ava = True
            if elv1_ava or elv2_ava:
                if elv1_ava and elv2_ava:
                    dist1 = abs(self.elevator1.display_floor() - psg_flr)
                    dist2 = abs(self.elevator2.display_floor() - psg_flr)
                    if dist1 > dist2:
                        pick = self.elevator2
                    elif dist1 < dist2:
                        pick = self.elevator1
                    else:
                        pick = choice([self.elevator1, self.elevator2])
                elif elv1_ava:
                    pick = self.elevator1
                elif elv2_ava:
                    pick = self.elevator2
                self.task_state[tid] = (PassengerState.SCHEDULED, pick, psg_flr, tar)
                if (
                    (psg_dir and pick.target_floor > tar) or
                    (not psg_dir and pick.target_floor < tar)
                ):
                    pick.moving_queue.put((pick.target_floor, tar))
                    pick.target_floor = tar
            # Schedule the passenger to an idle elevator or wait
            else:
                if (self.elevator1.target_floor is None and self.elevator1.running and
                    self.elevator2.target_floor is None and self.elevator2.running
                ):
                    dist1 = abs(self.elevator1.display_floor() - psg_flr)
                    dist2 = abs(self.elevator2.display_floor() - psg_flr)
                    if dist1 > dist2:
                        pick = self.elevator2
                    elif dist1 < dist2:
                        pick = self.elevator1
                    else:
                        pick = choice([self.elevator1, self.elevator2])
                elif self.elevator1.target_floor is None and self.elevator1.running:
                    pick = self.elevator1
                elif self.elevator2.target_floor is None and self.elevator2.running:
                    pick = self.elevator2
                else:
                    self.waiting_queue.put((tid, psg_flr, tar))
                    return
                self.task_state[tid] = (PassengerState.SCHEDULED, pick, psg_flr, tar)
                pick.moving_queue.put((pick.display_floor(), psg_flr))
                pick.moving_queue.put((psg_flr, tar))
                pick.target_floor = tar
        except Empty:
            pass

    def update_task_state(self):
        for tid, state in self.task_state.items():
            if state[0] == PassengerState.SCHEDULED and state[1].display_floor() == state[2]:
                self.task_state[tid] = (PassengerState.TAKING, state[1], state[2], state[3])
            elif state[0] == PassengerState.TAKING and state[1].display_floor() == state[3]:
                self.task_state[tid] = (PassengerState.ARRIVED, None, None, None)
                # print(f'task {tid} arrived')
    
    def elv_to_maintain(self, n):
        if n == 1:
            self.elevator1.running = False
            self.elevator1.target_floor = None
            self.elv1_thread.join()
        elif n == 2:
            self.elevator2.running = False
            self.elevator2.target_floor = None
            self.elv2_thread.join()
    
    def elv_restart(self, n):
        if n == 1:
            self.elevator1.running = True
            self.elv1_thread = Thread(target=self.elevator_move, args=[self.elevator1])
            self.elv1_thread.start()
        elif n == 2:
            self.elevator2.running = True
            self.elv2_thread = Thread(target=self.elevator_move, args=[self.elevator1])
            self.elv2_thread.start()
        
    def clean_task_state(self):
        rm_keys = []
        for tid, state in self.task_state.items():
            if state[0] == PassengerState.ARRIVED:
                rm_keys.append(tid)
        for key in rm_keys:
            self.task_state.pop(key)

    def get_tasks(self):
        while self.running:
            self.check_waiting()
            self.new_task()
            self.update_task_state()
            if len(self.task_state) > 10:
                # print('clean!')
                self.clean_task_state()
        self.stop()

    def stop(self):
        self.elevator1.running = False
        self.elevator2.running = False
        self.elv1_thread.join()
        self.elv2_thread.join()

    def elevator_move(self, elv: Elevator):
        while elv.running:
            try:
                cur, tar  = elv.moving_queue.get(block=False)
                # print(f'{elv.name} is going to move from {cur} to {tar}')
                elv.move(cur, tar)
                if elv.display_floor() == elv.target_floor:
                    elv.target_floor = None
                    # print(f'{elv.name} stops')
            except Empty:
                pass
    