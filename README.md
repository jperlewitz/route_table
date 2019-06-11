# route_table
Create a route table and pull longest matches
Run with arg -a x.x.x.x/xx to add new prefix to route table
Run with arg -c to check is a route is in the table
======
Uses a binary tree to store all routes
It serilaizes the routetable obj to a local drive to save the routing state
Every time you run the program is pulls the serialized obj to pull the last saved state
