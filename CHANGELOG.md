# [0.0.2] - 2019-08-30
## Added
- *Disaster on the Good Ship Lethbridge* test world
- Added usage instructions to the README
- Updated unit tests and started using mocking where appropriate
- HasItem condition can now check containers other than the player
- HasItem checks in sub containers
- Input case is ignored
- Install now creates a game directory with install
- Actions can filter entities when considering more than one
- End game event
- Collector to find items by id
- Condition to check if an entity is active

## Removed
- Old start up scripts


# [0.0.1] - 2019-07-20
## Added
- Initial Release
- Basic working version that allows loading worlds from properly formated json files.
- Test coverage at 97%. Some test suites need updating.
- Verbs: Get, Drop, Look, Talk, Use, Inventory, Equip, Remove, Go
- Continuous integration setup on GitLab repo
- Partial code documentation using sphinx
- Pylint setup