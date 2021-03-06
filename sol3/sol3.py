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
    def __init__(self, Class = 0, A_monster = Monster()):
        self.Class = Class
        self.A_monster = A_monster

class Game_status:
    def __init__(self, maze = [], Monsters = [], Hero = Hero()):
        self.maze = maze
        self.Monsters = Monsters
        self.Hero = Hero

    def Move_left(self):
        if self.Hero.pos_y == 0:
            return False
        for i in reversed(range(self.Hero.pos_y)):
            if self.maze[self.Hero.pos_x][i].Class != 0:
                self.Hero.pos_y = i
                self.maze[self.Hero.pos_x][self.Hero.pos_y].Class -= 1
                return True

    def Move_right(self):
        if self.Hero.pos_y == len(self.maze[0]) - 1:
            return False
        for i in range(self.Hero.pos_y + 1, len(self.maze[0])):
            if self.maze[self.Hero.pos_x][i].Class != 0:
                self.Hero.pos_y = i
                self.maze[self.Hero.pos_x][self.Hero.pos_y].Class -= 1
                return True

    def Move_up(self):
        if self.Hero.pos_x == 0:
            return False
        for j in reversed(range(self.Hero.pos_x)):
            if self.maze[j][self.Hero.pos_y].Class != 0:
                self.Hero.pos_y = j
                self.maze[self.Hero.pos_x][self.Hero.pos_y].Class -= 1
                return True

    def Move_down(self):
        if self.Hero.pos_x == len(self.maze) - 1:
            return False
        for j in range(self.Hero.pos_x + 1, len(self.maze)):
            if self.maze[j][self.Hero.pos_y].Class != 0:
                self.Hero.pos_y = j
                self.maze[self.Hero.pos_x][self.Hero.pos_y].Class -= 1
                return True
    
    def Dead_end(self):
        min_AP = self.Monsters[0].AP
        min_HP = self.Monsters[0].HP
        sp_mon_num = 0
        for m in self.Monsters[1:]:
            if min_AP < m.AP:
                min_AP = m.AP
            if min_HP < m.HP:
                min_HP = m.HP
            if m.hasBuff:
                sp_mon_num += 1

        if (len(self.Monsters) * min_HP / self.Hero.AP) > (self.Hero.BUFF + sp_mon_num * 5 + self.Hero.HP / min_AP):
            return True
        return False

    def distance_remain(self):
        dis = 0
        for m in self.Monsters:
            dis += block_distance(self.Hero, m)
        return dis
class Search_tree:
    def __init__(self, child = [], status = Game_status(), turns = 0, remained_distance = 500):
        self.child = child
        self.status = status
        self.turns = turns
        self.remained_distance = remained_distance

def block_distance(The_Hero, A_Monster):
    return abs(The_Hero.pos_x + The_Hero.pos_y - A_Monster.pos_x - A_Monster.pos_y)

def search(search_tree):
    global turn_counter_min
    if search_tree.status.Dead_end():
        return
    elif search_tree.status.Monsters == []:
        if turn_counter_min < 0 or turn_counter_min > search_tree.turns:
            turn_counter_min = search_tree.turns
        return
    
    if search_tree.turns >= turn_counter_min and turn_counter_min > 0: #no need to continue
        return
    
    temp_status_l = Game_status(search_tree.status.maze, search_tree.status.Monsters, search_tree.status.Hero)
    temp_status_r = Game_status(search_tree.status.maze, search_tree.status.Monsters, search_tree.status.Hero)
    temp_status_u = Game_status(search_tree.status.maze, search_tree.status.Monsters, search_tree.status.Hero)
    temp_status_d = Game_status(search_tree.status.maze, search_tree.status.Monsters, search_tree.status.Hero)

    if temp_status_l.Move_left():
        passed_turns = int(temp_status_l.maze[temp_status_l.Hero.pos_x][temp_status_l.Hero.pos_y].A_monster.HP/temp_status_l.Hero.AP)
        if passed_turns < temp_status_l.maze[temp_status_l.Hero.pos_x][temp_status_l.Hero.pos_y].A_monster.HP/temp_status_l.Hero.AP:
            passed_turns += 1
        if temp_status_l.maze[temp_status_l.Hero.pos_x][temp_status_l.Hero.pos_y].Class != 0:
            if passed_turns - temp_status_l.Hero.BUFF > 0:
                temp_status_l.Hero.HP -= (passed_turns - temp_status_l.Hero.BUFF) * temp_status_l.maze[temp_status_l.Hero.pos_x][temp_status_l.Hero.pos_y].A_monster.AP
                temp_status_l.Hero.BUFF = 0
            else:
                temp_status_l.Hero.BUFF -= passed_turns
            if temp_status_l.Hero.HP <= 0 or temp_status_l.distance_remain() > search_tree.remained_distance:
                return
            if temp_status_l.maze[temp_status_l.Hero.pos_x][temp_status_l.Hero.pos_y].A_monster.hasBuff:
                temp_status_l.Hero.BUFF = 5
            temp_status_l.maze[temp_status_l.Hero.pos_x][temp_status_l.Hero.pos_y].Class -= 1
            temp_status_l.Monsters.remove(temp_status_l.maze[temp_status_l.Hero.pos_x][temp_status_l.Hero.pos_y].A_monster)
            temp_status_l.maze[temp_status_l.Hero.pos_x][temp_status_l.Hero.pos_y].A_monster = Monster()
        
        search_tree.child.append(Search_tree(status = temp_status_l, turns = search_tree.turns + passed_turns, remained_distance = temp_status_l.distance_remain()))

    if temp_status_r.Move_right():
        passed_turns = int(temp_status_r.maze[temp_status_r.Hero.pos_x][temp_status_r.Hero.pos_y].A_monster.HP/temp_status_r.Hero.AP)
        if passed_turns < temp_status_r.maze[temp_status_r.Hero.pos_x][temp_status_r.Hero.pos_y].A_monster.HP/temp_status_r.Hero.AP:
            passed_turns += 1
        if temp_status_r.maze[temp_status_r.Hero.pos_x][temp_status_r.Hero.pos_y].Class != 0:
            if passed_turns - temp_status_r.Hero.BUFF > 0:
                temp_status_r.Hero.HP -= (passed_turns - temp_status_r.Hero.BUFF) * temp_status_r.maze[temp_status_r.Hero.pos_x][temp_status_r.Hero.pos_y].A_monster.AP
                temp_status_r.Hero.BUFF = 0
            else:
                temp_status_r.Hero.BUFF -= passed_turns
            if temp_status_r.Hero.HP <= 0 or temp_status_r.distance_remain() > search_tree.remained_distance:
                return
            temp_status_r.maze[temp_status_r.Hero.pos_x][temp_status_r.Hero.pos_y].Class -= 1
            temp_status_r.Monsters.remove(temp_status_r.maze[temp_status_r.Hero.pos_x][temp_status_r.Hero.pos_y].A_monster)
            temp_status_r.maze[temp_status_r.Hero.pos_x][temp_status_r.Hero.pos_y].A_monster = Monster()
        
        search_tree.child.append(Search_tree(status = temp_status_r, turns = search_tree.turns + passed_turns, remained_distance = temp_status_r.distance_remain()))

    if temp_status_u.Move_up():
        passed_turns = int(temp_status_u.maze[temp_status_u.Hero.pos_x][temp_status_u.Hero.pos_y].A_monster.HP/temp_status_u.Hero.AP)
        if passed_turns < temp_status_u.maze[temp_status_u.Hero.pos_x][temp_status_u.Hero.pos_y].A_monster.HP/temp_status_u.Hero.AP:
            passed_turns += 1
        if temp_status_u.maze[temp_status_u.Hero.pos_x][temp_status_u.Hero.pos_y].Class != 0:
            if passed_turns - temp_status_u.Hero.BUFF > 0:
                temp_status_u.Hero.HP -= (passed_turns - temp_status_u.Hero.BUFF) * temp_status_u.maze[temp_status_u.Hero.pos_x][temp_status_u.Hero.pos_y].A_monster.AP
                temp_status_u.Hero.BUFF = 0
            else:
                temp_status_u.Hero.BUFF -= passed_turns
            if temp_status_u.Hero.HP <= 0 or temp_status_u.distance_remain() > search_tree.remained_distance:
                return
            temp_status_u.maze[temp_status_u.Hero.pos_x][temp_status_u.Hero.pos_y].Class -= 1
            temp_status_u.Monsters.remove(temp_status_u.maze[temp_status_u.Hero.pos_x][temp_status_u.Hero.pos_y].A_monster)
            temp_status_u.maze[temp_status_u.Hero.pos_x][temp_status_u.Hero.pos_y].A_monster = Monster()
        
        search_tree.child.append(Search_tree(status = temp_status_u, turns = search_tree.turns + passed_turns, remained_distance = temp_status_u.distance_remain()))

    if temp_status_d.Move_down():
        passed_turns = int(temp_status_d.maze[temp_status_d.Hero.pos_x][temp_status_d.Hero.pos_y].A_monster.HP/temp_status_d.Hero.AP)
        if passed_turns < temp_status_d.maze[temp_status_d.Hero.pos_x][temp_status_d.Hero.pos_y].A_monster.HP/temp_status_d.Hero.AP:
            passed_turns += 1
        if temp_status_d.maze[temp_status_d.Hero.pos_x][temp_status_d.Hero.pos_y].Class != 0:
            if passed_turns - temp_status_d.Hero.BUFF > 0:
                temp_status_d.Hero.HP -= (passed_turns - temp_status_d.Hero.BUFF) * temp_status_d.maze[temp_status_d.Hero.pos_x][temp_status_d.Hero.pos_y].A_monster.AP
                temp_status_d.Hero.BUFF = 0
            else:
                temp_status_d.Hero.BUFF -= passed_turns
            if temp_status_d.Hero.HP <= 0 or temp_status_d.distance_remain() > search_tree.remained_distance:
                return
            temp_status_d.maze[temp_status_d.Hero.pos_x][temp_status_d.Hero.pos_y].Class -= 1
            temp_status_d.Monsters.remove(temp_status_d.maze[temp_status_d.Hero.pos_x][temp_status_d.Hero.pos_y].A_monster)
            temp_status_d.maze[temp_status_d.Hero.pos_x][temp_status_d.Hero.pos_y].A_monster = Monster()
        
        search_tree.child.append(Search_tree(status = temp_status_d, turns = search_tree.turns + passed_turns, remained_distance = temp_status_d.distance_remain()))

    for c in search_tree.child:
        search(c)


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
            line.append(cell(2, Monster_list[-1]))
        elif input_line[j] == "M":
            Monster_list.append(Monster(hasBuff = False, pos_x = i, pos_y = j))
            line.append(cell(2, Monster_list[-1]))
        elif input_line[j] == "D":
            line.append(cell())
            Little_HI = Hero(BUFF = 5, pos_x = i, pos_y = j)
        else:
            line.append(cell(Class = 1))
    Maze.append(line)
    line = []
for monster in Monster_list:
    attrs = input().split(" ")
    monster.HP = int(attrs[0])
    monster.AP = int(attrs[1])

hero_attrs = input().split(" ")
Little_HI.HP = int(hero_attrs[0])
Little_HI.AP = int(hero_attrs[1])
Initial_game = Game_status(Maze, Monster_list, Little_HI)
Search_root = Search_tree([], Initial_game, 0)
turn_counter_min = -1
search(Search_root)
print (turn_counter_min)