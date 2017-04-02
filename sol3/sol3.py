class Hero:
    def __init__(self, HP = 0, AP = 0, BUFF = 0, pos_x = 0, pos_y = 0):#pos_x 为行数，pos_y 为列数（just a reminder
        self.HP = HP
        self.AP = AP
        self.BUFF = BUFF
        self.pos_x = pos_x
        self.pos_y = pos_y

class Monster:
    def __init__(self, HP = 0, AP = 0, hasBuff = False, pos_x = 0, pos_y = 0):
        self.HP = HP
        self.AP = AP
        self.hasBuff = hasBuff
        self.pos_x = pos_x
        self.pos_y = pos_y

class cell:
    def __init__(self, Class = 0, A_monster = Monster(), hasMonster = False, Monster_num = 20):
        self.Class = Class
        self.A_monster = A_monster
        self.hasMonster = hasMonster
        self.Monster_num = Monster_num

class Game:
    def __init__(self, maze = [], Monsters = [], Hero = Hero()):
        self.maze = maze
        self.Monsters = Monsters
        self.Hero = Hero

    def Move_left(self):
        for i in reversed(range(self.Hero.pos_y)):
            if self.maze[self.Hero.pos_x][i].Class != 0:
                self.Hero.pos_y = i
            return

    def Move_right(self):
        for i in range(self.Hero.pos_y + 1, len(self.maze[0])):
            if self.maze[self.Hero.pos_x][i].Class != 0:
                self.Hero.pos_y = i
            return

    def Move_up(self):
        for j in reversed(range(self.Hero.pos_x)):
            if self.maze[j][self.Hero.pos_y].Class != 0:
                self.Hero.pos_y = i
            return

    def Move_down(self):
        for j in range(self.Hero.pos_x + 1, len(self.maze)):
            if self.maze[j][self.Hero.pos_y].Class != 0:
                self.Hero.pos_y = i
            return

class Search_tree:
    def __init__(self, child = [], status = Game()):
        self.child = child
        self.status = status
def block_distance(The_Hero, A_Monster):
    return abs(The_Hero.pos_x + The_Hero.pos_y - A_Monster.pos_x - A_Monster.pos_y)

size = input().split(" ")
N = int(size[0])
M = int(size[1])
Maze = []
line = []
Monster_list = []
for i in range(N):
    input_line = input()
    for j in range(M):
        if input_line[j] == "S":
            Monster_list.append(Monster(hasBuff = True, pos_x = i, pos_y = j))
            line.append(cell(2, Monster_list[-1], True, len(Monster_list) - 1))
        elif input_line[j] == "M":
            Monster_list.append(Monster(hasBuff = False, pos_x = i, pos_y = j))
            line.append(cell(2, Monster_list[-1], True, len(Monster_list) - 1))
        elif input_line[j] == "D":
            line.append(cell())
            Little_HI = Hero(BUFF = 5, pos_x = i, pos_y = j)
        else:
            line.append(cell(Class = 1))
    Maze.append(line)
    line = []
for monster in Monster_list:
    attrs = input().split(" ")
    monster.HP = attrs[0]
    monster.AP = attrs[1]
hero_attrs = input().split(" ")
Little_HI.HP = hero_attrs[0]
Little_HI.AP = hero_attrs[1]
Initial_game = Game(Maze, Monster_list, Little_HI)