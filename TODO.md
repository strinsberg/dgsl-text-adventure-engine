TODOs
=====

Priority
--------

* hidden items are not properly hidden for some verbs or methods of collection.

General
-------

* **Fix unit tests**. They need to be updated to work with the changes and bug fixes. Also try to make them cleaner and use proper testing structures so they are not so coupled to other modules.
* Add the new testing world to the test folder and update continuous integration to make a proper folder and copy it if need be to run a game creation or world creation test.
* Work on the documentation for both the code and using the engine.
* Do some UML diagrams for current design elements
* consider this a beta release 0.1 and start using changelog and branches when making changes.
* Get setup.py setup so it is possible to install and run the game.
* Figure out how to get the docs hosted on the gitlab webpage so they are viewable once it is public. This might need to wait until it is public.

Features and Fixes
------------------

* Adjust the way that the parser splits up text and how it collects the objects that might be what the player asked for. think about only matching whole words rather than parts of words. While it can be convenient to abbreviate the word selection would eliminate some bad matches.
* Adjust the parser to be able to handle commands with 2 objects like give x to y
* Along with these consider having the parser remove articles and stuff that does not really determine the identity of the object
* Add verbs for Give, Put, and custom verbs
* When describing things list objects with the same name in a container only once with a number. ie) there are 4 gold coins. Also, see if you can get the parser to accept asking to get 4 gold coins if there are 4. Perhaps even a get all.
* See if you can set it up to allow an event to be triggered by more than one verb, without using observers.
* consider what ways observers might want to be notified. To execute, to set is_done, etc. Also, put the code for this in it's own methods so that each event can call it at the appropriate moment.
* Custom messages for inactive or unobtainable items
* A simple structure for a 2 way door
* Add filter methods to the actions that need them. Drop should only show you things you have in your inventory and possibly your equipment.

Ideas
=====

Events
------
* I wonder if in the future it would be possible to decide what in a room is affected by an action? Say the player does something that is not directly to an object, but that object wants to respond to that action anyway? Could they observe the player when they enter the room? and then un-observe when they leave again? Then the player could have events in their own events object under the games verbs and they could do nothing but be observable. I suppose that then quests and other things would be able to subscribe to the player and be activated when the player did things. It would have to be a different kind of observer pair than the events have I think. Some information might need to be passed to notify (like the verb). maybe there could even be different ones for different things, like an entity observer and a quest observer. Also perhaps even other events can subscribe to these events easily. That way they could be triggered on a specific player action.
* There could even be one that was for all player actions. Then the entity and quest notify could just send info rather than having the events observed. The entity could just be told what verb was used and execute the associated event if it has it. If the entity has many events but only one that they want to observe the player then they can just have that event registered directly. This would be more flexible.
* Another thing is how actions that would affect every entity in the room would work? Maybe they could just get the contents of the room they are in and do something to all of them. Could even use a visitor to get certain kinds of things based on the type of event it is. I imagine this would be the best way to do it. Probably even instead of using the entity of the event the affected of the event could be used to get all things in the room.
* it might be necessary to have a way to register with the player for all actions. Or there could be a way to have a special event tag that would be run after the players action by the game. Say hidden verbs that end with _turnend. Then before looking for input, or even before showing the results each object in the players current room could be searched for events that have the right verb and they could all be run one at a time and their affects applied to the player. I think for starters it would be esiest to have them subscribe directly to player events.


Environment
-----------
* It would be cool to have environments that could be added to a room. This could then allow some different actions in the room or something like that. Though I am not sure how it could be made easily customizable.
* Really to have a deadly environment or conditions when the player enters the protection condition is all that is needed along with a conditional event. Simple make an enter event that checks if the player is protected and reacts accordingly, killing the player or something else.

Conditions
----------
* Should all accept more than one answer if desired. So a question can have multiple right answers or has_item can check for having more than one item (like all peices of a key). Some environments could require protection from more than one thing. It will just allow for more flexibility.

Custom verbs
------------
* Custom verbs can just be events attached to an entity. Then any verb will be allowed and if an object has an event it will be run, otherwise you will be told you can't act that way on an entity.
* If the parser was to work with a list of verbs then it might be possible to parse the json and take all the custom verbs and add them to the parser so that if a person uses a verb that is in the game somewhere they will get a message that is different than if they use one that will never be allowed.

Parsing
-------
* Should spend some time trying to work with the parser to make it possible to give commands in a slightly more natural way. This is not all that hard, but some kind of grammar would have to be created if a recursive decent parser was to be created. Also, the way I allow items to be collected with only parts of their text might make this more difficult.