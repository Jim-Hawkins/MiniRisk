class Region:
    def __init__(self, name, gov = None, num_troops = 0):
        self.name = name
        self.gov = gov
        self.num_troops = num_troops
        self.fuerza = num_troops * 2
        
        if self.gov is None:
            self.color = 0
        else:
            self.color = self.gov.color
            
    def is_free(self):
        return self.gov is None
        
    def __str__(self):
        if self.gov is not None:
            government = self.gov.name
        else:
            government = None
        return ("name: " + self.name + ", gov: " + str(government) + ", troops: " + \
                str(self.num_troops) + ", color: " + str(self.color))
        
        
class Player:
    def __init__(self, name, color, num_troops, num_regs = 1):
        self.name = name
        self.color = color
        self.num_troops = num_troops
        self.num_regs = num_regs
        self.points = 1
        
    def attack(self, map, my_reg, enemy, troops):
            
        if map.adyacent(my_reg, enemy):
            if map.attack(my_reg, enemy, troops):
                return ("Success! You conquered " + enemy)
            else:
                return ("Failure! " + enemy + " troops won yours")
        else:
            return (my_reg + " and " + enemy + " are not bordering regions")
            
            
class Map:
    def __init__(self, player_list):
        self.graph = {"A Coruña":   ["Lugo", "Pontevedra", "Ourense"],
                      "Lugo":       ["A Coruña", "Ourense"],
                      "Pontevedra": ["A Coruña", "Ourense"],
                      "Ourense":    ["Lugo", "Pontevedra", "Ourense"]}
        
        self.regions = {"A Coruña":   Region("A Coruña"),
                        "Lugo":       Region("Lugo", player_list[0], player_list[0].num_troops),
                        "Pontevedra": Region("Pontevedra", player_list[1], player_list[1].num_troops),
                        "Ourense":    Region("Ourense")}
                   
    def adyacent(self, region_1, region_2):
        return region_1 in self.graph.keys() and region_2 in self.graph[region_1]
        
    def attack(self, attacker, defensor, troops):
        if self.regions[attacker].num_troops == 0 or\
           self.regions[attacker].num_troops < troops:
            print("Not enoug troops!")
            return 0
        else:
            self.regions[attacker].num_troops -= troops 
            
        if self.regions[defensor].gov is None:
            self.regions[attacker].gov.points += 1
            self.regions[attacker].gov.num_regs += 1
            
            self.regions[defensor].num_troops = troops
            self.regions[defensor].color = self.regions[attacker].color
            self.regions[defensor].gov = self.regions[attacker].gov
            return 1
            
            
        if troops <= self.regions[defensor].num_troops:
            self.regions[defensor].num_troops -= troops
            return 0
        else:
            self.regions[defensor].gov.points -= 1
            self.regions[defensor].gov.num_regs -= 1
            self.regions[attacker].gov.points += 1
            self.regions[attacker].gov.num_regs += 1
            
            self.regions[defensor].num_troops = troops - self.regions[defensor].num_troops
            self.regions[defensor].color = self.regions[attacker].color
            self.regions[defensor].gov = self.regions[attacker].gov
            return 1
            
    def show(self):
        print("A Coruña", self.regions["A Coruña"])
        print("Lugo", self.regions["Lugo"])
        print("Ourense", self.regions["Ourense"])
        print("Pontevedra", self.regions["Pontevedra"])
            
            
players = [Player("pepe", 1, 50), Player("paco", 2, 35)]
map = Map(players)
done = False
turn = 0

while not done:
    order = input("Action for player {}: ".format(players[turn].name))
    
    if order.lower() == "q":
        done = True
        
    if order == "a":
        attacker = input("attacker region? ").trim()
        defensor = input("where do you want to attack? ").trim()
        troops = int(input("how many troops? "))
        print(players[turn].attack(map, attacker, defensor, troops))
        
        turn = (turn + 1)%len(players)
        
    if order == "s":
        map.show()
        
"""
cuando solo quede un jugador, darlo por ganador
mejorar comando s (posiblemente añadiendo mapa)
añadir comando h
mejorar la aparición de mensajes de error con algo parecido a switch case y códigos de error
"""