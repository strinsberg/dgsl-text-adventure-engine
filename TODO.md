TODOs
=====

* Build World object
* Construct Game object /main loop
* Add simple Parser
* Add some action objects or functions
* Add GameBuilder that can read the .world json files
* Finish Container, Room, Player
* Add an inform and a move event
* Start putting together some new UML diagrams. Do them up with python in mind.
* Finish setup.py and learn about setup tools and what it can do for you
* See if you can figure out how to get CI working with gitlab
* add a target to make all to Makefile

Ideas
=====

**Don't forget to write tests and document everything as you do it not later. Event work with pylint before you are too far along to deal with those errors.**

Game loop stuff
---------------

* Get input from the user and pass it to parser
* Parser returns a dict that always has 'verb' and a list of 'subjects'
* *Later* the dict from parser can go to a menu that will ask which subject
* verb and subject will be passed to a function that deals with the action and returns the resulting string. This is so that it can be adjusted to work internally however it wants. Should be a Game method.
* *later* upgrade the code inside the above method to work with a factory and action obejcets when it gets more complex.
* The results from the action will be output to the screen
* If the player is dead the game will end


Events
------

* I wonder if in the future it would be possible to decide what in a room is affected by an action? Say the player does something that is not directly to an object, but that object wants to respond to that action anyway? Could they observe the player when they enter the room? and then unobserve when they leave again? Then the player could have events in their own events object under the games verbs and they could do nothing but be observable. I suppose that then quests and other things would be able to subscribe to the player and be activated when the player did things. It would have to be a different kind of observer pair than the events have I think. Some information might need to be passed to notify (like the verb). maybe there could even be different ones for different things, like an entity observer and a quest observer. Also perhaps even other events can subscribe to these events easily. That way they could be triggered on a specific player action.
* There could even be one that was for all player actions. Then the entity and quest notify could just send info rather than having the events observed. The entity could just be told what verb was used and execute the associated event if it has it. If the entity has many events but only one that they want to observe the player then they can just have that event registered directly. This would be more flexible.
* Another thing is how actions that would affect every entity in the room would work? Maybe they could just get the contents of the room they are in and do something to all of them. Could even use a visitor to get certain kinds of things based on the type of event it is. I imagine this would be the best way to do it. Probably even instead of useing the entity of the event the affected of the event could be used to get all things in the room.
* it might be necessary to have a way to register with the player for all actions. Or there could be a way to have a special event tag that would be run after the players action by the game. Say verbs that end with _turnend. Then before looking for input, or even before showing the results each object in the players current room could be searched for events that have the right verb and they could all be run one at a time and their affects applied to the player. I think for starters it would be esiest to have them subscribe directly to player events.
* Make kill a toggleHidden instead and it can work just like toggle active but instead work for hidden items. So that things can be hidden but revealed by player actions, or available and then hidden. Using the one time only attribute and adding a message about death could be used if someone dies. Like the player being hidden.


Equipment
---------

* I want to deal with equipment differently. I suppose that equipment should be another component and those that have it can equip things in those slots. Pehpas equipment itself could be a seperate subtree of entity and have a decorator to add certain features to it (like protection or uses). Other than the suit this is something that will come later, but even the suit is unecessary for a while and only really important to the original space game.


Environment
-----------
* environments can replace atmospheres. These can alter things about the room. They may be candidates for decorators as well, unless they can be altered. Say being able to drain water from a room, or vent radiation. The idea that an environment would also affect those in it or allow extra actions is interesting. Perhaps these could be something that was added to rooms either through decorators or subclassed room_with_environment. How, the environment would work I do not know. Perhaps it could be a persitent event that was applied after every action a player took. Ie, if your wearing your suit you could take it off and then die becauase you are no longer protected.
* The main thing is that I want to be able to make environments more interactive if possible. So that you can do differnt things with them beyond just having an atmoshpere. Though combining atmosphere with objects that represent parts of an environment might be just as good. Say dirt that could be dug up could just be labeled as a type of ground and perhaps could be somehow appended to the description rather than listed as an individual object. Then it could have events attached to it like dig and check if you have the shovel. Then if you do an event coul trigger to give you somehting or reveal a hidden item.

