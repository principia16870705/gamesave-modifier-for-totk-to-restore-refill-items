## The Description  
A small app that allows a player to modify their Zelda TOTK gamesaves directly in their 
emulator's gamesave directory. When the TOTK game auto-saves or manual-saves, a player 
can refresh this app, click its options, and then reload their game from the TOTK pause 
menu. The process is designed to be quick and simple.

When the game reloads from the modified gamesave data, the player can have full durability 
of their swords, bows, and shields. This app can also refill hearts, arrows, rupees, and 
material quantities. This app is meant to maintain the fun of finding new types of items, 
so it does not give the player new items, but simply restores or refills the player's current items.

## The Lore
I was thinking, instead of using duplication glitches, it would be nice if my character 
could take a rest while a Santa Claus-like being repaired my weapons and maybe filled my 
stockings with a few rupees and item refills.

So that's the basic idea, but instead of Saint Nick we have a troupe of magic frogs whose 
origin is clouded in mystery. Perhaps they operate secretly while our character is sleeping. 
Perhaps they hold the weapons gently and whisper healing incantations. Or, perhaps they 
heat the weapons in a portable froggish forge and pound them into shape while drinking
froggish beverages and singing rowdy froggish melodies. Perhaps they are the size of spring 
peepers, or perhaps they are more like dwarves, or perhaps their size would dwarf a human. 
I leave it to the user to decide.

![app preview](doc/app_preview.png)

## Another Angle
I wanted to spend more time enjoying my favorite weapons and items, more time exploring, and 
less time replacing broken weapons. I also didn't want to ruin the fun of finding new types 
of items, so this app was developed with the goal of simply restoring or refilling current items.

Before I developed this app, I was getting a similar game-play experience by using item and 
weapon duplication glitches to prolong the durability of weapons, but weapon duplication 
glitches need you to leave some weapons untouched which is tedious, and performing any glitch 
is a bit tedious anyway. This app replaces the duplication glitches that I had been using.

## Download this App as an Executable File  
You can download this app built as an exe for Windows or a bin for Linux.  
[Download](https://github.com/principia16870705/gamesave-modifier-for-totk-to-restore-refill-items/releases/tag/v1.0.0)

## Test the App with Test Data  
You can use this app directly on your TOTK gamesaves, but you can also make use of the test 
data in this repo. Test this app's ability to work on the TOTK gamesave directory structure by 
downloading and unzipping for_testing_only_parent_directory.zip. Test this app's ability 
to work on a single TOTK gamesave file by downloading for_testing_only_progress.sav.

## Running and Building on Windows  

### Dependencies  
This project uses Python, Pillow, pyinstaller, and tkinter.  
(in our case, tkinter was included with Python automatically)  
For Windows, we used these versions.

Python 3.11.4  
Pillow 10.0.0  
pyinstaller 5.12.0  

### Run Command  
If your dependencies are in place, and you cloned or downloaded this repo, you can run the 
app directly with python.  
`python main.py`

### Build Command  
If your dependencies are in place, and you cloned or downloaded this repo, you can build 
the project to a single executable file.  
`pyinstaller --onefile --windowed --add-data images/*;images main.py`

## Running and Building on Linux  

### Dependencies  
This project uses Python, Pillow, pyinstaller, and tkinter.  
For Linux, we used these versions.

Python 3.9.2  
Pillow 10.0.0  
pyinstaller 5.13.0  
tkinter 3.9.2-1  

### Run Command  
If your dependencies are in place, and you cloned or downloaded this repo, you can run the 
app directly with python.  
`python3 main.py`

### Build Command  
If your dependencies are in place, and you cloned or downloaded this repo, you can build 
the project to a single executable file.  
`pyinstaller --onefile --windowed --add-data images/*:images --hidden-import PIL._tkinter_finder main.py`
