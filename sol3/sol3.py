class Hero:
    def __init__(self, HP = 0, AP = 0, BUFF = 0, pos_x = 0, pos_y = 0):
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
    def __init__(self, Class = 0, A_monster = Monster(), hasMonster = False):
        self.Class = Class
        self.A_monster = A_monster
        self.hasMonster = hasMonster

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
            line.append(cell(1,Monster_list[-1],True))
        elif input_line[j] == "M":
            Monster_list.append(Monster(hasBuff = False, pos_x = i, pos_y = j))
            line.append(cell(2,Monster_list[-1],True))
        elif input_line[j] == "D":
            line.append(cell())
            Little_HI = Hero(BUFF = 5, pos_x = i, pos_y = j)
        else:
            line.append(cell())
    Maze.append(line)
    line = []
for monster in Monster_list:
    attrs = input().split(" ")
    monster.HP = attrs[0]
    monster.AP = attrs[1]
hero_attrs = input().split(" ")
Little_HI.HP = hero_attrs[0]
Little_HI.AP = hero_attrs[1]