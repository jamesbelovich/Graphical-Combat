"""tbc.py
tbc module
"""

import random

class Character:
    def __init__(self, name="Unnamed", hitPoints=10, hitChance=50, maxDamage=5, armor=0):
        self._name = str(name) if name is not None else "Unnamed"
        self._hitPoints = hitPoints
        self._hitChance = self.testInt(hitChance, 0, 100, 50)
        self._maxDamage = self.testInt(maxDamage, 1, 100, 5)
        self._armor = self.testInt(armor, 0, 100, 0)

    def testInt(self, value, min=0, max=100, default=0):
        out = default
        if isinstance(value, int):
            if min <= value <= max:
                out = value
            elif value > max:
                print("Too large")
            else:
                print("Too small")
        else:
            print("Must be an int")
        return out

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self._name = str(value)

    @property
    def hitPoints(self):
        return self._hitPoints
    @hitPoints.setter
    def hitPoints(self, value):
        self._hitPoints = value

    @property
    def hitChance(self):
        return self._hitChance
    @hitChance.setter
    def hitChance(self, value):
        self._hitChance = self.testInt(value, 0, 100, 50)

    @property
    def maxDamage(self):
        return self._maxDamage
    @maxDamage.setter
    def maxDamage(self, value):
        self._maxDamage = self.testInt(value, 1, 100, 5)

    @property
    def armor(self):
        return self._armor
    @armor.setter
    def armor(self, value):
        self._armor = self.testInt(value, 0, 100, 0)

    
    def printStats(self):
        print(f"{self.name}")
        print("=" * 15)
        print(f"Hit points: {self.hitPoints}")
        print(f"Hit chance: {self.hitChance}")
        print(f"Max damage: {self.maxDamage}")
        print(f"Armor:      {self.armor}\n")

    def hit(self, opponent):
        roll = random.randint(1, 100)
        if roll <= self.hitChance:
            damage = random.randint(1, self.maxDamage)
            absorbed = min(damage, opponent.armor)
            totalDamage = max(damage - absorbed, 0)

            print(f"{self.name} hits {opponent.name}...")
            print(f"  for {damage} points of damage")
            print(f"  {opponent.name}'s armor absorbs {absorbed} points")

            opponent.hitPoints -= totalDamage
        else:
            print(f"{self.name} misses {opponent.name}!")

'''def fight(hero, villian):
    round_num = 1
    keepGoing = True

    while keepGoing:
        print(f"\nRound {round_num}\n")
        
        hero.hit(villian)
        print(f"{hero.name}: {hero.hitPoints} HP")
        print(f"{villian.name}: {villian.hitPoints} HP")

        if villian.hitPoints <= 0:
            print(f"{hero.name} wins!")
            keepGoing = False
        else:
            villian.hit(hero)
            print(f"{hero.name}: {hero.hitPoints} HP")
            print(f"{villian.name}: {villian.hitPoints} HP")

            if hero.hitPoints <= 0:
                print(f"{villian.name} wins!")
                keepGoing = False

        round_num += 1

        if keepGoing:
            input("Press <ENTER> for another round")
            
        '''

def fight(hero, villain):
    log = []

    # Hero attacks first
    roll = random.randint(1, 100)
    if roll <= hero.hitChance:
        damage = random.randint(1, hero.maxDamage)
        damage = max(0, damage - villain.armor)
        villain.hitPoints -= damage
        log.append(f"{hero.name} hits {villain.name} for {damage} damage!")
    else:
        log.append(f"{hero.name} misses {villain.name}!")

    # Check if villain is defeated
    if villain.hitPoints <= 0:
        log.append(f"{hero.name} wins!")
        return log

    # Villain counter‑attacks
    roll = random.randint(1, 100)
    if roll <= villain.hitChance:
        damage = random.randint(1, villain.maxDamage)
        damage = max(0, damage - hero.armor)
        hero.hitPoints -= damage
        log.append(f"{villain.name} hits {hero.name} for {damage} damage!")
    else:
        log.append(f"{villain.name} misses {hero.name}!")

    # Check if hero is defeated
    if hero.hitPoints <= 0:
        log.append(f"{villain.name} wins!")

    return log


if __name__ == "__main__":
    hero = Character("Hero", 10, 50, 5, 2)
    villian = Character("Villian", 20, 30, 5, 0)
    hero.printStats()
    villian.printStats()
    fight(hero, villian)