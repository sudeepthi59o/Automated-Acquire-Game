
## Updates in Class Definitions

### Player 
		- Added variables to store name, cash and shares
		- Removed hotels array, storing it in the "Game" class instead
		- Added utility functions to update the above mentioned variables
### Share 
		- Added variables to store name and count
		- Added utility function to get the share's details as an object
### Hotel 
		- Added an array - `validnames` to store valid hotel labels
		- Storing the elements in the tiles array as an array of Tile class objects
		- Added overriding functions for internal computing
		- Added utility function to get the hotel's details as an object
		- ShareDict is now stored as a separate module
### Game
There have been several changes made in this class <br>
	    - The AI player definition has been eliminated
	    - A dict - `numShares` is stored to keep track of available number of shares for each hotel group
	

The following are the list of new functions implemented in this class  

   `pickRandomTile()`
	Returns a random unoccupied tile from the current state of the board
	
   `getStateObj()`
    Returns the State Object - the required response for a request

   `setup()`
    Handles the initial setup of the board, players, random allottment of tiles

   `getShareObj()`
    Returns an object of a particular share's details

   `getTileObj()`
    Returns an object of a particular Tile's details

   `getPlayerObj()`
    Returns an object of a particular Player's details

   `place()`
    Handles placing a tile on the board and taking the appropriate move

   `buyShare()`
    Handles buying a share on behalf of a given player, hotel and count

   `buy()`
    Reads the request object and calls `buyShare()` with the data received

   `done()`
    Handles the "done" request type

   `handleRequest()`
    Intercepts all requests and calls the respective game function to handle it