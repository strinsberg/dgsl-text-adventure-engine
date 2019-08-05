DGSL Text Adventure Engine
==========================

A program for playing custom text based adventure game worlds made with the DGSL World Editor.

[![pipeline status](https://gitlab.com/strinsberg/dgsl-text-adventure-engine/badges/master/pipeline.svg)](https://gitlab.com/strinsberg/dgsl-text-adventure-engine)
[![coverage report](https://gitlab.com/strinsberg/dgsl-text-adventure-engine/badges/master/coverage.svg)](https://gitlab.com/strinsberg/dgsl-text-adventure-engine)

The goal of this project, along with the DGSL World Editor, is to allow people to create, share, and run their own text adventure games. All without writing any code. The World Editor provides a graphical interface to creates world files that can then be loaded by the Adventure Engine.

This program is an extension of a C++ text adventure game that myself and Max Niu created in the spring of 2019 at the University of Lethbridge. I have taken parts of the design and ported them to Python 3 and made it possible to load game information from json files. I then wrote the companion world editor to facilitate world construction and editing.

## Status
Both programs are still in the early stages of development. If you install the Engine it comes with a sample world 'Disaster on the Good Ship Lethbridge' to show a little of what is possible. Though in the future there will likely be significant changes that I hope will greatly expand the options for making games. I will be very busy in the coming months, so updates will likely be slow for now.

The World Editor is functional, but lacks the necessary documentation to be useful at this time.


Installation
============

First clone or download the project.

Open a terminal and navigate to the downloaded directory.

Run
```
$ pip3 install --user .
```

Once installed the program can be started from the command line.
```
$ dgsl
```

Loading a World
===================

When you run dgsl in the terminal you will first be given some options.

```
$ dgsl
Welcome to the DGSL Text Adventure Engine
0.2.0

1. Load a world
2. Load a saved game (not implemented)
3. Cancel
Choice: 
```

To play the sample world select 1 and type the worlds name in lower case.

```
Choice: 1

What world would you like to load? disaster on the good ship lethbridge
```

This will start the game from the beginning.
```
----------------------------------------------------
You are in the best room on the ship. It has nice furnishings and is a lot larger than the other crew members' quaters. It is your sanctuary from the demands of your position.
There is a door to the common area
There is a viewport
There is a computer terminal
There is a bed
There is a medkit

> 
```

From here you explore the world and try to save the galaxy!

How To Play
===========

### Game input

All input takes one of the following forms:
```
> <verb> <noun>
> <verb>
```

A noun can be more than one word. All words will be used to find the noun. You do not have to type the full name of an item to interact with it. The words must be in the same order as they are in the item name though.

If there were 'a door to the common area'. The following would work.
```
> use door
> use door to common
> use common
```

But not
```
> use common area door
> use to common
```

If there are more than one items that match the noun they will be listed in a menu for you to pick.
```
> use door

----------------------------------------------------
1. a door to the captain's room
2. a door to the engineer's room
3. a door to the main hall
4. a keypad lock for engineer's door
5. Cancel
Choice:
```

Input is not case sensitive. The following should both work the same.
```
> GET BOX
> get box
```

I hope to make the parser a little more flexible eventually. As well as actions that take two nouns like 'give gold to guard' or 'use medkit on barbara'.

### List of Actions

1.  Get    
Moves an item from the room you are in into your inventory. The item can be in the room or nested inside a container in the room and you will be able to take it.
```
> get box

---------------------------------------------------
You take the box
```

Or if the box is not something you can take
```
> get box

---------------------------------------------------
You can't take that
```

2.  Drop  
Removes an item from your inventory and places it in the room.  
```
> drop box

---------------------------------------------------
You drop the box
```

Or if you don't have the box
```
> drop box

---------------------------------------------------
You don't have that
```

3. Use   
Attempts to use an object in the world. If an object is usable you will interact it.
```
> use door to the common area

----------------------------------------------------
You are in a room where the crew relax and socialize after a long day in space
There is a door to the captain's room
etc...
```

Or if you can't use something
```
> use medkit

---------------------------------------------------
You can't use that
```

Or if something is useable, but is currently inactive.
```
> use door to the engineer's room

---------------------------------------------------
For some reason you can't
```

4. Talk
Interacts with an NPC. It may start an interaction or They may just respond. Sometimes talking to them more than once will give you different results. It is also possible that the options available in the interactions will differ for various reasons. For example you have, or don't have, an item.
```
> talk barbara

-----------------------------------------------------
"Oh I don't feel so good...

1. What's happening?
2. Heal her                       -- Only if you have the medkit
Choice: 
```

Or
```
> talk whinny

---------------------------------------------------
"You need to get to the bridge quickly"

> talk whinny

---------------------------------------------------
"What are you still doing here!"
```

5. Look  
If you type only look it will give information about the room you are in.
```
> look

----------------------------------------------------
You are in a room where the crew relax and socialize after a long day in space
There is a door to the captain's room
etc...
```

Or if you specify an object in the room or your inventory.
```
> look medkit

----------------------------------------------------
You see a first aid kit that could save someones life.
```

6. Equip
Allows you to equip different kinds of equipment. For the sample game there are only suits. If you are wearing a similar piece of equipment it will be removed and placed in your inventory.
```
> equip space suit

-----------------------------------------------------
You equip it
```


7. Remove
Removes a piece of equipment that you are wearing.
```
> remove space suit

-----------------------------------------------------
You remove it
```

7. Inventory  
Lists the items in your inventory and any equipment you are wearing.
```
> inventory

----------------------------------------------------
You are carrying ...
A medkit

You are wearing ...
A space suit
```

If you specify an item you will be told if you have it or not.
```
> inventory medkit

----------------------------------------------------
You have that

> inventory viewport

----------------------------------------------------
You don't have that
```

### Game Commands

There is only one game command right now. Others like Help, Save, and Load will be added eventually.

* Exit
Quits the game. Because there is no saving your progress will be lost.
```
> exit

----------------------------------------------------
Quitting ...

Thanks for playing
```

### Common action responses
* The item you are looking for could not be found
```
There is no <noun>
```

* Unavailable Action
```
You don't know how to <verb>
```

* Inactive item
```
For some reason you can't
```

* You need a specific item in your inventory to take the action
```
You don't have what you need
```
  
# Tips
1. Items can be active or inactive. Look for ways to activate them. They may not always let you know when you have done the right thing.

2. Some items are not obtainable. If you are told you can't get something that means you can't ever get it. You don't need to keep trying.

3. Interaction with NPC is not always the same. Try different things. You never know if an NPC might have more to say or be more responsive if you have something they want in your inventory.

4. There is no limit to how much you can carry. 
