import random
import math
import numpy as np



class World:

    def __init__(self, size=8):
        self.size = size
        self.game_over = False
        self.score = 0
        self.obs = np.zeros((self.size, self.size), dtype=int)
        middle = [math.floor((self.size + 1) / 2) - 1, math.ceil((self.size + 1) / 2) - 1]
        y = random.randint(*middle)
        x = random.randint(*middle)
        self.obs[y, x] = 1  # head
        self.obs[y + 1, x] = 2  # body
        self.generate_apple()

    def generate_apple(self):
        y = random.randint(0, self.size - 1)
        x = random.randint(0, self.size - 1)
        while self.obs[y, x] != 0:
            y = random.randint(0, self.size - 1)
            x = random.randint(0, self.size - 1)
        self.obs[y, x] = -1

    def step(self, action):
        if self.game_over:
            return
        apple_collected = False
        tail_value = 0
        for y in range(self.size):
            for x in range(self.size):
                if self.obs[y, x] == 1:
                    head = [y, x]
                    self.obs[y, x] += 1
                elif self.obs[y, x] == 2:
                    neck = [y, x]
                    self.obs[y, x] += 1
                elif self.obs[y, x] > 2:
                    body = [y, x]
                    self.obs[y, x] += 1
                if self.obs[y, x] > tail_value:
                    tail = [y, x]
                    tail_value = self.obs[y, x]

        y = head[0] - neck[0]
        x = head[1] - neck[1]
        look_dir = [y, x]

        look_dirs = [[0, -1], [-1, 0], [0, 1], [1, 0]]
        look_dir_index = look_dirs.index(look_dir)
        head_movement = None

        if action == -1:  # left
            head_movement = look_dirs[look_dir_index - 1]
        elif action == 0:  # straight
            head_movement = look_dirs[look_dir_index]
        elif action == 1:  # right
            if look_dir_index == 3:
                head_movement = look_dirs[0]
            else:
                head_movement = look_dirs[look_dir_index + 1]

        new_head_y = head[0] + head_movement[0]
        new_head_x = head[1] + head_movement[1]

        if (new_head_x > self.size - 1) or (new_head_y > self.size - 1) or (new_head_x < 0) or (new_head_y < 0) or (
                self.obs[new_head_y, new_head_x] > 1):
            self.game_over = True
            self.obs[tail[0], tail[1]] = 0
        else:
            if self.obs[new_head_y, new_head_x] == -1:
                self.generate_apple()
                self.score += 1
            else:
                self.obs[tail[0], tail[1]] = 0
            self.obs[new_head_y, new_head_x] = 1

    def snake_view_1(self):
        tail_value = 0
        for y in range(self.size):
            for x in range(self.size):
                #if self.obs[y, x] == 1:
                #    head = [y, x]
                elif self.obs[y, x] == 2:
                    neck = [y, x]
                elif self.obs[y, x] > 2:
                    body = [y, x]
                if self.obs[y, x] > tail_value:
                    tail = [y, x]
                    tail_value = self.obs[y, x]

        y = head[0] - neck[0]
        x = head[1] - neck[1]
        look_dir = [y, x]

        look_dirs = [[0, -1], [-1, 0], [0, 1], [1, 0]]
        look_dir_index = look_dirs.index(look_dir)
        info_left = []
        indices_left = []
        info_straight = []
        indices_straight = []
        info_right = []
        indices_right = []

        for ii in range(1, 4):
            shift_left = look_dirs[look_dir_index - 1]
            pixel_left_y = head[0] + ii * (shift_left[0])
            pixel_left_x = head[1] + ii * (shift_left[1])
            if (pixel_left_x > self.size - 1) or (pixel_left_y > self.size - 1) or (pixel_left_x < 0) or (
                    pixel_left_y < 0):  # if we can still move
                info_left.append(-2)
                indices_left.append(ii)
                break
            if self.obs[pixel_left_y, pixel_left_x] != 0:
                info_left.append(self.obs[pixel_left_y, pixel_left_x])
                indices_left.append(ii)

        for ii in range(1, 4):
            shift_straight = look_dirs[look_dir_index]
            pixel_straight_y = head[0] + ii * (shift_straight[0])
            pixel_straight_x = head[1] + ii * (shift_straight[1])
            if (pixel_straight_x > self.size - 1) or (pixel_straight_y > self.size - 1) or (pixel_straight_x < 0) or (
                    pixel_straight_y < 0):  # if we can still move
                info_straight.append(-2)
                indices_straight.append(ii)
                break
            if self.obs[pixel_straight_y, pixel_straight_x] != 0:
                info_straight.append(self.obs[pixel_straight_y, pixel_straight_x])
                indices_straight.append(ii)

        for ii in range(1, 4):
            if look_dir_index == 3:
                shift_right = look_dirs[0]
            else:
                shift_right = look_dirs[look_dir_index + 1]
            pixel_right_y = head[0] + ii * (shift_right[0])
            pixel_right_x = head[1] + ii * (shift_right[1])
            if (pixel_right_x > self.size - 1) or (pixel_right_y > self.size - 1) or (pixel_right_x < 0) or (
                    pixel_right_y < 0):  # if we can still move
                info_right.append(-2)
                indices_right.append(ii)
                break
            if self.obs[pixel_right_y, pixel_right_x] != 0:
                info_right.append(self.obs[pixel_right_y, pixel_right_x])
                indices_right.append(ii)
        return info_left, indices_left, info_straight, indices_straight, info_right, indices_right

    def __repr__(self):
        lll = []
        for y in range(self.obs.shape[0]):
            ll = []
            for x in range(self.obs.shape[1]):
                if self.obs[y, x] == 0:


                    ll.append('  ')
                elif self.obs[y, x] > 1:
                    ll.append('░░')
                elif self.obs[y, x] == 1:
                    ll.append('██')
                else:
                    ll.append('◯◯')
            lll.append(''.join(ll))
        world = '|\n'.join(lll)
        gameover = ' Game Over' if self.game_over else ''
        return f"{world}| score={self.score} {self.snake_view_1()}{gameover}"


