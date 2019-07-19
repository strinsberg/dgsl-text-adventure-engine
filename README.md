DGSL Text Adventure Engine
==========================

[![pipeline status](https://gitlab.com/strinsberg/dgsl-text-adventure-engine/badges/master/pipeline.svg)](https://gitlab.com/strinsberg/dgsl-text-adventure-engine/commits/master)
[![coverage report](https://gitlab.com/strinsberg/dgsl-text-adventure-engine/badges/master/coverage.svg)](https://gitlab.com/strinsberg/dgsl-text-adventure-engine/commits/master)

The DGSL Text Adventure Engine is a program for running custom text based adventure games.

Game worlds can be created using the DGSL World Editor (add link). ***No Coding Required**. These worlds can then be loaded by the engine and played. You can then share them with your friends that also have a copy of the DGSL engine.

**Note** This project is still a work in progress. With the world editor and game engine it is possible to create worlds and play them, but both programs may be subject to changes that break compatibility with older versions.

The engine comes with 2 Test worlds. The first 'Disaster on the Good Ship Lethbridge' was part of a school group project by myself and Max Niu. This project was also the inspiration for the game engine, hence the DGSL in the title. The second world 'Mystery of Stumplewood' is designed to showcase some of the capability of the engine and world editor. As a story it may be lacking a little bit, but it should be a good example of the complex behavior that can added to the games.

This project is designed to allow people to make and share their own text based adventure games with each other without needing to know how to computer program. The style of games intended to be made with it is more like the old school text adventure games where the player explores a world and interacts with items and other characters.

This project is not designed to create interactive novels where text is given and a player picks an option and then more text is given. It may be possible to do this with the engine, but it would likely be unpleasant. There are many other tools that can be used for doing this.

Another thing that may be conspicuously lacking is any kind of combat system and stats. There are some features that allow a player to where equipment that can protect them and eventually it will be possible to use tools or weapons that could affect other items or characters. However, these will all be one time actions that will have the desired effect or fail. eg) hitting a person with a sword will just kill them if they are not protected from it. It will not do x damage and then give them the opportunity to retaliate. There is no health and mana etc. This is not because these things might not be fun, but they add a lot of complexity and there are many other game types that do this kind of thing better.

Installation
============

There is no way as yet to install.

To give it a try
1. clone the repo and cd into it
2. run the quick start script

```
$ python3 dgsl-quickstart
```

3. run the program

```
$ python3 dgsl.py
```

How To Play a World
===================

The DGSL World Editor will have instructions for making worlds.

If you have a .world file place it in .dgsl/worlds directory that should be located in your home directory if you ran the quick start.

When you start the engine select the option to load a world (saved games are not possible yet). Enter the name of your world and the game should start.

Type help to get information on how to enter commands and what commands are available.

TODO: Create a more detailed user manual.
