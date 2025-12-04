"""graphical combat
all background, sfx, and sprites from opengameart.org
"""

import random, pygame, simpleGE

from tbc import Character, fight 

warrior = Character(name="Warrior", hitPoints=60, hitChance=65, maxDamage=13, armor=5)
tank = Character(name="Tank", hitPoints=90, hitChance=50, maxDamage=8, armor=10)
assassin = Character(name="Assassin", hitPoints=45, hitChance=90, maxDamage=22, armor=3)

class Sprite(simpleGE.Sprite):
    def __init__(self, scene, filename, size=(75,75), center=(320, 400)):
        super().__init__(scene)
        self.setImage(filename)
        self.setSize(*size)
        self.center = center
        self.hide()
        self.filename=filename
     
    '''def show(self):
        super().show()
        self.center = self.center 

'''
def Enemy():
    enemyImage = [
        ("RedKnight.png", (100, 100)),
        ("fenrir_wolf.png", (100, 100)), 
        ("troll_1.png", (150,150)),
    ]
    filename, size=random.choice(enemyImage)
    
    hitPoints = random.randint(30, 95)
    hitChance = random.randint(35, 87)
    maxDamage = random.randint(7, 25)
    armor = random.randint(0, 7)

    enemyCharacter = Character(name="Enemy", hitPoints=hitPoints,
                          hitChance=hitChance, maxDamage=maxDamage, armor=armor)

    return enemyCharacter, filename, size

    
class Game(simpleGE.Scene):
    def __init__(self, playerCharacter):
        super().__init__()
        self.setImage("bg.png")
        self.setCaption("Combat")
        self.playerCharacter=playerCharacter
        
        if playerCharacter == warrior:
            self.playerSprite = Sprite(self, "knight3.png", center=(300, 320), size=(100, 100))
        elif playerCharacter == tank:
            self.playerSprite = Sprite(self, "tank.png", center=(300, 320), size=(150, 150))
        elif playerCharacter == assassin:
            self.playerSprite = Sprite(self, "ninja.png", center=(300, 320), size=(75, 75))
        self.playerSprite.show()

        self.enemyCharacter, filename, size = Enemy()
        self.enemySprite = Sprite(self, filename, size=size, center=(490, 320))
        self.enemySprite.show()
        
        self.enemyStats = simpleGE.MultiLabel()
        self.enemyStats.center = (530, 75)
        self.enemyStats.size = (200, 140)
        self.enemyStats.font = pygame.font.SysFont(None, 16)
        self.enemyStats.textLines = [
            "Enemy",
            f"HitPoints: {self.enemyCharacter.hitPoints}",
            f"Hit Chance: {self.enemyCharacter.hitChance}%",
            f"Max Damage: {self.enemyCharacter.maxDamage}",
            f"Armor: {self.enemyCharacter.armor}"
        ]
        
        self.playerStats = simpleGE.MultiLabel()
        self.playerStats.center = (110, 75)   
        self.playerStats.size = (200, 140)
        self.playerStats.font = pygame.font.SysFont(None, 16)
        self.playerStats.textLines = [
            "Your Character",
            f"Health: {self.playerCharacter.hitPoints}",
            f"Hit Chance: {self.playerCharacter.hitChance}%",
            f"Max Damage: {self.playerCharacter.maxDamage}",
            f"Armor: {self.playerCharacter.armor}"
        ]

        self.fightLog = simpleGE.MultiLabel()
        self.fightLog.center = (320, 250)   
        self.fightLog.size = (400, 150)     
        self.fightLog.textLines = ["Choose to Attack or Run"]

        pygame.mixer.music.load("fight.wav")
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)
        
        self.btnAttack=simpleGE.Button()
        self.btnAttack.text="Attack"
        self.btnAttack.center=(100,420)
        
        self.btnRun=simpleGE.Button()
        self.btnRun.text="Run"
        self.btnRun.center=(520,420)
        
        self.btnQuit = simpleGE.Button()
        self.btnQuit.text = "Quit Game"
        self.btnQuit.center = (320, 20)
        
        self.sndHit=simpleGE.Sound("hit.flac")
        
        self.sprites= [
            self.btnAttack,
            self.btnRun,
            self.btnQuit,
            self.playerSprite,
            self.enemySprite,
            self.enemyStats,
            self.playerStats,
            self.fightLog
            ]
        
    def process(self):
         if self.btnAttack.clicked:
            self.sndHit.play()
            results = fight(self.playerCharacter, self.enemyCharacter)
            self.fightLog.textLines = results + [
                f"{self.playerCharacter.name} HP: {self.playerCharacter.hitPoints}",
                f"{self.enemyCharacter.name} HP: {self.enemyCharacter.hitPoints}"
            ]
                
            if self.enemyCharacter.hitPoints <= 0:
                self.response = "Win"
                self.stop()
            elif self.playerCharacter.hitPoints <= 0:
                self.response = "Lose"
                self.stop()

         if self.btnQuit.clicked:
            self.response = "Quit"
            self.stop()
        
         if self.btnRun.clicked:
            self.response = "Run"
            self.stop()
            
class Result(simpleGE.Scene):
    def __init__(self, result, playerSprite):
        super().__init__()
        self.setImage("bg.png")
        self.setCaption("Fight Result")
        
        pygame.mixer.music.load("load.wav")
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)
        
        self.btnQuit = simpleGE.Button()
        self.btnQuit.text = "No"
        self.btnQuit.center = (540, 440)
        
        self.result=simpleGE.MultiLabel()
        self.result.center=(320,75)
        self.result.size=(200,100)
                          
        self.btnNext=simpleGE.Button()
        self.btnNext.text="Yes"
        self.btnNext.center=(100, 440)
        
        
        self.playerSprite = Sprite(
            self,
            playerSprite.filename,  
            center=(320, 250),
            size=(150,150)
        )
        self.playerSprite.show()

        if result == "Win":
            self.result.textLines = ["You won!",
                                    "Fight Again?"]
        elif result == "Lose":
            self.result.textLines = ["You lost..."
                                    "Fight Again?"]
        
        self.sprites=[
            self.btnQuit,
            self.btnNext,
            self.result,
            self.playerSprite
            ]
                
    def process(self):
        if self.btnQuit.clicked:
            self.response = "Quit"
            self.stop()
        
        if self.btnNext.clicked:
            self.response="Next Fight"
            self.stop()
        
class Intro(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.setCaption("Combat Game")
        self.setImage("RockBG.png")

        pygame.mixer.music.load("load.wav")
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)
        self.sndClick=simpleGE.Sound("click3.wav")

        self.btnStart = simpleGE.Button()
        self.btnStart.text = "Start Game"
        self.btnStart.center = (100, 420)

        self.btnQuit = simpleGE.Button()
        self.btnQuit.text = "Quit"
        self.btnQuit.center = (520, 420)

        self.btnWarrior = simpleGE.Button()
        self.btnWarrior.text = "Warrior"
        self.btnWarrior.center = (100, 135)

        self.btnTank = simpleGE.Button()
        self.btnTank.text = "Tank"
        self.btnTank.center = (100, 90)

        self.btnAssassin = simpleGE.Button()
        self.btnAssassin.text = "Assassin"
        self.btnAssassin.center = (100, 45)

        self.stats = simpleGE.MultiLabel()
        self.stats.center = (500,120)
        self.stats.size = (220, 190)
        self.stats.font = pygame.font.SysFont(None, 24)
        self.stats.textLines = ["View Character Stats"]
        
        self.warriorSprite = Sprite(self, "knight3.png", center=(320,440), size=(100, 100))
        self.tankSprite = Sprite(self, "tank.png",   center=(320,440), size=(150, 150))
        self.assassinSprite= Sprite(self, "ninja.png",  center=(320,440), size=(75, 75))

        self.sprites = [
            self.btnStart,
            self.btnQuit,
            self.btnWarrior,
            self.btnTank,
            self.btnAssassin,
            self.stats,
            self.warriorSprite,
            self.tankSprite,
            self.assassinSprite
        ]

    def updateStats(self, character):
        self.stats.textLines = [
            f"Class: {character.name}",
            f"Health: {character.hitPoints}",
            f"Hit Chance: {character.hitChance}%",   
            f"Max Damage: {character.maxDamage}",
            f"Armor: {character.armor}"
        ]
    
    def process(self):
        if self.btnWarrior.clicked:
            self.userCharacter = warrior
            self.updateStats(warrior)
            self.warriorSprite.show()
            self.tankSprite.hide()
            self.assassinSprite.hide()
            self.sndClick.play()

        if self.btnTank.clicked:
            self.userCharacter = tank
            self.updateStats(tank)
            self.tankSprite.show()
            self.warriorSprite.hide()
            self.assassinSprite.hide()
            self.sndClick.play()

        if self.btnAssassin.clicked:
            self.userCharacter = assassin
            self.updateStats(assassin)
            self.assassinSprite.show()
            self.warriorSprite.hide()
            self.tankSprite.hide()
            self.sndClick.play()

        if self.btnStart.clicked:
            if not hasattr(self, "userCharacter"):
                self.stats.textLines = ["Select a character",
                                        "before starting"]
            else:
                self.response = "Play"
                self.stop()

        if self.btnQuit.clicked:
            self.response = "Quit"
            self.stop()

def main():
    keepGoing = True
    while keepGoing:
        intro = Intro()
        intro.start()

        if intro.response == "Play":
            fightLoop = True
            while fightLoop:
                game = Game(intro.userCharacter)
                game.start()

                if game.response == "Run":
                    fightLoop = False

                elif game.response in ["Win", "Lose"]:
                    result = Result(game.response, game.playerSprite)
                    result.start()

                    if result.response == "NextFight":
                        continue
                    elif result.response == "Quit":
                        keepGoing = False
                        fightLoop = False
                    else:
                        fightLoop = False
        else:
            keepGoing = False

if __name__ == "__main__":
    main()