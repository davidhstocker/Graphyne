
When visualizing graphs, or subgraphs (known as clusters), it is handy to have a standard visualization language to make reading these visualizations easier.  

The symbols below are for both memes and entities.  And given graph visualization will be either entities or memes.  Hence, the generic term *node* will be used in the legend table.

|  Symbol  |  Explanation  |
|  ---  |  --- |
|  ![][image-1]  |  **Node** - This symbol is used for all non-singleton nodes.  It is a circle with a light gray/blue background  (html color code **BDD0E9**) and no border.  Optionally, the name of the meme can be displayed as text, though it is better to use callouts.  |
|  ![][image-2]  |  **Singleton Node** - Singletons are differentiated from other nodes by having a black border |
|  x  |  **Link (Atomic) **- Links between two entities are drawn with an arrow, from the origin to the destination entity.  Atomic links are drawn in *black*.  |
|    |  **Invalid Meme** - If the visualization is displaying memes, meme validity can be optionally displayed via color code.  Valid memes are left untouched.  Invalid memes are red.  |
|    |  **Inherited invalidity** - If a meme has inherited invalidity, it is invalid because there is an invalid meme somewhere among its members.  Memes with a member that has inherited invalidity inherit invalidity themselves.  Memes that are themselves valid, but inherit invalidity are displayed with transparent red.  |


[image-1]:	https://raw.githubusercontent.com/davidhstocker/Graphyne/master/Docs/Images/GetCluster_Legend_Node.png
[image-2]:	https://raw.githubusercontent.com/davidhstocker/Graphyne/master/Docs/Images/GetCluster_Legend_Singleton.png