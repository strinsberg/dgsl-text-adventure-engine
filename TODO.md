TODOs
=====

Priority
--------

* hidden items are not properly hidden for some verbs or methods of collection.
* Add proper documentation to all classes and methods
* Get coverage back to 100%

General
-------

* Add some documentation on how to use the project.
* Update unit tests to use mocks so they are less coupled and cleaner
* Add the new testing world to the test folder and update continuous integration to make a proper folder and copy it if need be to run a game creation or world creation test.
* Do some UML diagrams for current design elements
* Get setup.py setup so it is possible to install and run the game.
* Figure out how to get the docs hosted on the gitlab webpage so they are viewable.
* should find a way to use a different readme on github and gitlab

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
* It would be interesting to find a way to allow more entities than the player to be affected by events.

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