This simple rest website can return the deviation for a given long/lat and date. However it is severely rate limited even with a 2 second sleep so a temporary database is created so that restarts do not lose any data and do not repeat the same request for the same map.

After all the data has been obtained then a cursor can update the squaremap index.

Run the script. If required delete the mag.sqlite database for a new set of maps or dates.

Note that the deviation is from True North, not Grid North
