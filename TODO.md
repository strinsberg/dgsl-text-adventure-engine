TODOs
=====

Priority
--------

* Finish a sample world
* Finish code documentation
* Update and finish unit testing
* Add a condition to check active
* Fix condition to be able to test an entity other than player
* Fix ordered events to work properly with conditionals
* Write another world and try to get a feel for features that are missing or poorly designed

General
-------

* Update unit tests to use mocks so they are less coupled and cleaner
* Add the new testing world to the test folder and update continuous integration to make a proper folder and copy it if need be to run a game creation or world creation test.
* Do some UML diagrams for current design elements
* Add save and load commands
* Set up the choose world menu to give a selection of worlds to load, or make it possible to specify only part of a world name and give a menu if there is more than one of the same name.
* Update display
* Update Parser
* Add additional events
* Add new verbs and custom verbs


Bugs
----

* Conditions are currently not working for any target except the player. This needs to be fixed because it seriously limits their usefulness.
* Ordered events are not treating conditionals as unfinished if they have their failure events run instead of success.


Ideas
=====

* Adjust how display works for listing a rooms contents. Would be nice to have the room description and then a section of doors, but all in a nice sentence. Then a list of things in the room. Possibly also changing the way an item should be named as well.
* Custom messages for inactive items could be a neat thing to add. It might change the way the world editor deals with states, but it would make the game more expressive.
* When describing things list objects with the same name in a container only once with a number. ie) there are 4 gold coins. Also, see if you can get the parser to accept asking to get 4 gold coins if there are 4. Perhaps even a get all.
* Maybe add an ordered option for interactions. It is possible to adjust the events with an ordered event, but it is not possible to change the option text. And it might be possible with conditions or observers to make options appear and disappear as other events happen, but it could get complicated.


Items
-----

* A structure for a 2 way door. I like the idea of being able to create an item that leads you somewhere, but many doors just lead to a room and then another door has to be created to lead back. Having a predefined structure that can make both in one object would be handy for most generic doors. At the very least by having something in the world editor that makes them both for you.
* 2 way doors could just be implemented with a move event that is tied to an object instead of a room. It could lead you to the other object. This could also be cool for things like teleporters or portals that you could move around with you. It could also be part of a dynamic move event that creates a hidden object when you use the dynamic move object. The next time you use it it can take you back to the hidden object and remove it.

Quests
------

* implicit quests are fine, but it would be cool to have some kind of simple quest system with a quest log to keep track of things you are asked to do. Puzzles can still force the player to find and do things without being told, but having quests can give the player an idea of what to work on next and add story elements.
* Quest log would be a component added to the player that could be accessed with it's own command. Once open it could be it's own sub-process with it's own commands and output.
* There could be events for adding and removing quests from a players quest log. So you could talk to someone and they would give you a quest, or you could get an object and it would start a quest.
* There could also be conditions to check to see if a player had a particular quest or had finished a quest.
* quests could be their own type and work similar to events and conditions. They could have information that would be displayed in the quest log. They could have a condition attached to them and be setup to check those conditions at certain times or when certain actions were performed. They could also have a completion event and a field that would record if they were complete. Some might need to check periodically to make sure they were still completed, like events that require you to collect an item. If it was dropped the quest would have to be notified.
* They don't have to be overly complicated to add some a nice extra depth to the games that could be constructed for the engine.

Events
------
* It would be interesting to find a way to allow more entities than the player to be affected by events.
* It should be possible to associate more than one verb with an event. Possibly have the main verb as the key in the events table and then extra verbs in an event object as the value. If a verb isn't found it can check the extra verbs in each event and see if its there before saying false. Or events can be stored in a tuple with a list of verbs and the event object. Since there will never be enough events to make searching for one this way time consuming it is probably simplest. Then each events verb list can be checked to run the appropriate event.
* When implementing observers and notify it may be necessary to add some more flexibility to it. Sending the verb that was used might be a start. Also, instead of just executing events there might be a way to execute them differently based on the notify, like not printing a message if notified. Also, call order with notify might be difficult.
* A dynamic move event that somehow remembers where you moved from so it can take you back. Say for carrying an item that moves you to a location that is not accessible by any other means. You would want to go back to where you left from or at least a convenient location close by.
* Change description event, or an event that is triggered in addition to the description so you can put all the stuff that might change in the event and it can update when it needs to.
* Different ways to subscribe to an observer so that the event that subscribed can behave in an appropriate way. As in you can pass the message that you want notify to pass back to you and determine what to do with it. Or even pass a function or object that will do the right thing when called so that there do not have to be if-then-else in notify. though there will likely not be too many different notify situations for an event. Plus this kid of thing will have to be added to the editor so it needs to remain simple.
* An event to check if something is active is needed. Possibly even one for hidden.


Environment
-----------
* It would be cool to have environments that could be added to a room. This could then allow some different actions in the room or something like that. Though I am not sure how it could be made easily customizable.
* Really to have a deadly environment or conditions when the player enters the protection condition is all that is needed along with a conditional event. Simple make an enter event that checks if the player is protected and reacts accordingly, killing the player or something else.

Conditions
----------
* Should all accept more than one answer if desired. So a question can have multiple right answers or has_item can check for having more than one item (like all peices of a key). Some environments could require protection from more than one thing. It will just allow for more flexibility.

Verbs and Commands
------------------
* Add verbs for Give, Put, and custom verbs
* Custom verbs can just be events attached to an entity. Then any verb will be allowed and if an object has an event it will be run, otherwise you will be told you can't act that way on an entity.
* If the parser was to work with a list of verbs then it might be possible to parse the json and take all the custom verbs and add them to the parser so that if a person uses a verb that is in the game somewhere they will get a message that is different than if they use one that will never be allowed.


Parsing
-------
* Adjust the way that the parser splits up text and how it collects the objects that might be what the player asked for. think about only matching whole words rather than parts of words. While it can be convenient to abbreviate the word selection would eliminate some bad matches.
* Adjust the parser to be able to handle commands with 2 objects like give x to y
* Along with these consider having the parser remove articles and stuff that does not really determine the identity of the object
* Should spend some time trying to work with the parser to make it possible to give commands in a slightly more natural way. This is not all that hard, but some kind of grammar would have to be created if a recursive decent parser was to be created. Also, the way I allow items to be collected with only parts of their text might make this more difficult.
* If parser needs to know what words are verbs ahead of time custom verbs etc. can be retrieved by walking all items and looking for the verbs in their events dicts.