
Graphyne is a smart graph, written in Python.  A smart graph is a property graph that can react to changes and incorporate decision making logic, not just passively hold data.

## Easy to Integrate into Python Projects
Being pure python code, Graphyne can be used simply by importing it and initializing the graph.  There are no REST services or external graph servers to worry about.  You can choose to use SQLite persistence, an external SQL based database or forgo persistence entirely if you don’t need it and gain a performance bump.  It is designed to be easy to integrate into your Python projects, simple to use and very powerful.  It uses [Memetic][1] as its graph definition and query language.

## Simple to Use
Within 5 statements, you can import the Graphyne library, initialize the graph, and create a hello world graph by creating a pair of entities and linking them.  This allows you to get started with using Graphyne quickly in your projects.

## Powerful
Graphyne is powerful and includes some features that set it apart from other property graphs.  It can:
- Make full use of [Memetic’s schema definitions][2] 
- Use Memetic’s powerful query [traverse language][3]
- Create schema-less (aka Generic) entities, or entities and networks of entities with a single command.
- Create unidirectional or bidirectional links between entities.
- Has support for singleton entities.
- Entities and links can carry attributes.
- The ability to create private subgraphs of entities, which appear as a single entity to the rest of the graph.
- Entities are scriptable.
- Graphyne includes an eventing mechanism, allowing entity scripts to be triggered based on events.


[An overview of the diagram conventions for Graphyne graphs][4]

[The graph API reference][5]


# Getting Started

## Installing

To install Graphyne, use pip.
```
pip install graphyne
```

Graphyne has dependencies on [Memetic][6] and [Pyodbc][7].  The main use of Memetic is to provide the Memetic’s standard schema.  It is possible to run Graphyne graphs without the standard schema however.


## The Hello World Graph
In order to use the graph in your projects, you will have to import and initialize it.  There are several modules within the Graphyne package, but the one of real interest is Graph.

```python
import Graphyne.Graph
```

Or if you prefer to use a shorthand alias,
```python
import Graphyne.Graph as Graph
```

You can start the graph, but entering the following command (example uses the alias, Graph):
```python
Graph.startDB()
```

To start the graph using SQLite and a file named ‘MyDatabase.sqlite’ as the persistence, start the graph with the following setup:
```python
Graph.startDB([], ’sqlite’, ‘MyDatabase.sqlite’)
```

## Your First Graph

Now that the graph is running, let’s create a simple graph.  It will have two entities and they will be linked.

Create entities and Link them:
```python
node1 = Graph.api.createEntity()
node2 = Graph.api.createEntity()
Graph.api.addEntityLink(node1, node2)
```

The entities node1 and node2 have been created and are linked.  The return value of createEntity is a UUID, which is all we need to refer to a particular entity.  We can verify that they are linked by traversing from node1 to node2, using the getLinkCounterparts() method.
```python
counterpartList = Graph.api.getLinkCounterparts()
```

counterpartList will contain a list of stings, with the UUIDs of node1’s nearest neighbors.  That list will have a single entry, the UUID of node2. 




# Using Graphyne

## startDB() Options
If the startDB() method is executed without parameters, then it is started without any schema repositories and no persistence.  The graph will be contained in dictionaries, in memory and lost when the graph’s process is ended.  startDB has a number of location based parameters, which can change the nature of how the graph behaves.  They are (in order)

#### repoLocations
**(default =  []) **- A list of all of the filesystem locations that that compose the memetic repositories used by Graphyne.  If you are using Memetic schemas, then you would enter the folder or folders  as strings into this list.  

#### flaggedPersistenceType
**(default = None)** - The type of database used by the persistence engine.  In principle, Graphyne can use any sort of persistence, as long as an adapter (called a driver) is written for that persistence type.  As of now, only two basic types of persistence are implemented; a dictionary based “persistence” (which is not actually persistent) and an relational database approach.  Currently, a couple of different SQL database flavors are implemented.  The parameter value could be None.  If it is one of the SQL database types, it is also used to determine which flavor of SQL syntax to use.  If you are using a Memetic schema that includes implicit memes, then you will need to use one 
Enumeration of Possible values:
- *None* (default) - no persistence
- "*sqlite*" - Sqlite3
- "*mssql*" - Miscrosoft SQL Server
- "*hana*" - SAP Hana

#### persistenceArg
 **(default = None)**  - The Module/class supplied to host the entityRepository and LinkRepository.  If default, then use the Graphyne.DatabaseDrivers.NonPersistent module.

Enumeration of possible values:
*None* - May only be used in conjunction with "sqlite" or None as persistenceType and will throw an InconsistentPersistenceArchitecture otherwise.  If SQLite is being used as the persistence type, then it will use SQLite in in-memory mode (connection = ":memory:")
"*none*" (written and lowercase string text) - no persistence.  This is an alternative way of declaring *None*.
"*memory*" - Use SQLite in in-memory mode (connection = ":memory:")
"*\<existing file path with .sqlite as file extension\>*" - Use SQLite, with that file as the database.
"*\<file path with .sqlite as extension, but no file\>*" - Use SQLite and create that file to use as the DB file.
"*\<anything else\>*" - (currently, as no no-sql backend adapters have been written) Presume that it is a **pyodbc** connection string and throw a InconsistentPersistenceArchitecture exception if the dbtype is "sqlite".

#### useDefaultSchema
**(default =  False)  ** - If True, then load the 'default schema' of Graphyne.

#### resetDatabase -
**(default =  False)  **  - If it is set to True and a database already exists (e.g. when using sqlite with a file, or any other kind of relational database
with preexisting data, then the DB tables will be cleared.
createTestDatabase = a flag for creating regression test data.  This is a very dangerous flag, as it essentially re-initializes the databse.   It is used for regression testing the graph or resetting a graph to the bare schema.




# Persistence

Persistence is an optional feature in Graphyne.  In principle, nosql databases can also be used for persistence, but as of this time, only relational persistence is supported.   Graphyne uses an adapter pattern to connect to and consume relational backend content.  When the graph is bootstrapped, one of the modules from the Graphyne.DatabaseDrivers package is used and handles the entity repository (where currently active entities are cataloged) at runtime.  

The driver module is responsible for managing the entity repository and links.  API commands are directed to the driver.

## No Persistence

No Persistence is the default option for the Graphyne graph.  It uses python dictionaries for cataloging entities and link relationships.  It is simple to use and very fast, but obviously can’t persist a graph beyond its current process.  Use this persistence type when no long term persistence is needed and no implicit memes are being used.


## Relational Persistence

This module uses an SQL database to manage the entity repository and links between entities.  It is ACID and persistent, but comes at a price in performance and landscape complexity.  The second and third parameters in Graph.startDB() determine how this module functions.  The flaggedPersistenceType parameter determines which SQL syntax to select from  SQLDictionary.py.  The persistenceArg parameter is the connection string.  If you wish to use SQLite with :memory: persistence, then this perimeter can be left blank.  Before you use this combination however, keep in mind that this is slower than the NonPersistent option.

If the the tables that Graphyne uses for persistence don’t already exist in the database, then they will be created on startup.  Here is the SQLlite flavored DB schema:

```
"CREATE TABLE Entity(entityID NVARCHAR(38) NOT NULL, depricated INT NOT NULL, memePath NVARCHAR(100) NOT NULL, metaMeme NVARCHAR(100) NOT NULL, masterEntityID NVARCHAR(38) NOT NULL, PRIMARY KEY (entityID))"
"CREATE TABLE EntityTags(entityID NVARCHAR(38) NOT NULL, tag NVARCHAR(100) NOT NULL, FOREIGN KEY(entityID) REFERENCES Entity(entityID))"
"CREATE TABLE EntityPropertyLists(entityID NVARCHAR(38) NOT NULL, propName NVARCHAR(100) NOT NULL, propVal NVARCHAR(1000) NOT NULL, memePath NVARCHAR(100), FOREIGN KEY(entityID) REFERENCES Entity(entityID))"
"CREATE TABLE EntityPropertyBooleans(entityID NVARCHAR(38) NOT NULL, propName NVARCHAR(100) NOT NULL, propVal INT NOT NULL, memePath NVARCHAR(100), FOREIGN KEY(entityID) REFERENCES Entity(entityID))"
"CREATE TABLE EntityPropertyStrings(entityID NVARCHAR(38) NOT NULL, propName NVARCHAR(100) NOT NULL, propVal NVARCHAR(100) NOT NULL, restList NVARCHAR(100), memePath NVARCHAR(100), FOREIGN KEY(entityID) REFERENCES Entity(entityID))"
"CREATE TABLE EntityPropertyTexts(entityID NVARCHAR(38) NOT NULL, propName NVARCHAR(100) NOT NULL, propVal NVARCHAR(1000) NOT NULL, memePath NVARCHAR(100), FOREIGN KEY(entityID) REFERENCES Entity(entityID))"
"CREATE TABLE EntityPropertyDecimals(entityID NVARCHAR(38) NOT NULL, propName NVARCHAR(100) NOT NULL, propVal DECIMAL(15,5) NOT NULL, restMin DECIMAL(15,5), restMax DECIMAL(15,5), restList NVARCHAR(100), memePath NVARCHAR(100), FOREIGN KEY(entityID) REFERENCES Entity(entityID))"
"CREATE TABLE EntityPropertyIntegers(entityID NVARCHAR(38) NOT NULL, propName NVARCHAR(100) NOT NULL, propVal INT NOT NULL, restMin INT, restMax INT, restList NVARCHAR(100), memePath NVARCHAR(100),  FOREIGN KEY(entityID) REFERENCES Entity(entityID))"

"CREATE TABLE EntityLink (entityLinkID NVARCHAR(39) NOT NULL, memberID1 NVARCHAR(38) NOT NULL, memberID2 NVARCHAR(38) NOT NULL, membershipType INT NOT NULL, masterEntity NVARCHAR(38), PRIMARY KEY (EntityLinkID), FOREIGN KEY(memberID1) REFERENCES Entity(entityID), FOREIGN KEY(memberID2) REFERENCES Entity(entityID), FOREIGN KEY(masterEntity) REFERENCES Entity(entityID))"
"CREATE TABLE EntityLinkPropertyBooleans(entityLinkID NVARCHAR(39) NOT NULL, propName NVARCHAR(100) NOT NULL, propVal INT NOT NULL, FOREIGN KEY(entityLinkID) REFERENCES EntityLink(entityLinkID))"
"CREATE TABLE EntityLinkPropertyStrings(entityLinkID NVARCHAR(39) NOT NULL, propName NVARCHAR(100) NOT NULL, propVal NVARCHAR(1000) NOT NULL, FOREIGN KEY(entityLinkID) REFERENCES EntityLink(entityLinkID))"
"CREATE TABLE EntityLinkPropertyDecimals(entityLinkID NVARCHAR(39) NOT NULL, propName NVARCHAR(100) NOT NULL, propVal DECIMAL(15,5) NOT NULL, FOREIGN KEY(entityLinkID) REFERENCES EntityLink(entityLinkID))"
"CREATE TABLE EntityLinkPropertyIntegers(entityLinkID NVARCHAR(39) NOT NULL, propName NVARCHAR(100) NOT NULL, propVal INT NOT NULL,  FOREIGN KEY(entityLinkID) REFERENCES EntityLink(entityLinkID))"

```

# Memetic in Graphyne

Graphyne was built around Memetic and this section discusses the details of how certain Memetic features are implemented in Graphyne and how you can use them.

### Short note on nomenclature

For our examples, we’ll import Graphyne.Graph as Graph.  
```python
import Graphyne.Graph as Graph
```
This module has an attribute called api, which we can use to access the graph’s methods.  Using **Graph.api **is less verbose that always writing **Graphyne.Graph.api**.


## Creating Entities

There are two ways of creating entities in Graphyne.  The first method creates a generic entity, which does not require any schema,.  You have already been exposed to this api method, the createEntity().  This creates an entity of meme type *Graphyne.Generic,* which is just an empty entity with no properties.  You can use this method to create entities whenever you don’t want to bother with creating a schema, or just need a spontaneous, ad hoc entity.  This method creates the entity, indexes it in the entity repository and returns the UUID of the entity, with which it can be referenced later in other api methods.  This uuid is returned in string form, rather than as a standard python library uuid object.  

```python
entityUUID = Graph.api.createEntity()
```

The second method for creating entities is createEntityFromMeme().  With this method, you are creating an entity from a specific meme from the catalog of available memes in your schema.  E.g. we can create a *Graphyne.Generic* entity using createEntityFromMeme(), which will create exactly the same kind of meme as createEntity().

```python
entityUUID = Graph.api.createEntityFromMeme(‘Graphyne.Generic’)
```

There are a couple things to note when creating entities with createEntityFromMeme().  Firstly, if the meme in question has child memes in its definition, then entities for those memes will be created.  In the picture below, we have a meme (in dark blue), which we want to create.  That meme has three child memes in its definition and one of those three in turn has child memes.  Not only would an entity be created from our dark blue meme, but also child and grandchild entities would be created from their respective memes and all the entities would be linked in order (links originating with “parent” entities and ending at “child” entities)

![][image-1]


## Singletons

Memes flagged as singletons will always have a single entity of this type present in the graph.  It will be created on startup.  If you try to create an entity from a meme that is a singleton, the entity already exists and its UUID will be returned, as if a new entity had been created.  In the example below, meme **a** has been created twice, using getEntityFromMeme(‘a’).  **d** is among the  children of a and is created when **a** is created.  **x** (highlighted in dark) in turn is a child of **d**, but **x** is a singleton.  As you can see, it is possible to traverse between the two **a** entities, via the singleton, **x**.

![][image-2]

Singletons can be used a highly connected **hyper-nodes**.  When a singleton acts as the sole connecting point between different parts of a graph, this constellation is known as a *singleton bridge*.  x, above, is an example of a singleton bridge.


## Links

There is an API method for creating a link between two entities and one for destroying an existing link.  The method for creating a link between two entities is addEntityLink() and the method for removing a link is removeEntityLink().   You can define the link type value of 0 (atomic) or 1 (subatomic) when creating links.  The default value is 0.  Links created between entities that are based on meme and child meme relationships can have their link type defined in the memes and the cluster will be created using whatever link types are chosen by the designer.

When designing memes, links defined in memes/child relationships can also be atomic or subatomic.  If the designer wishes to make use of this option, she can add a linktype attribute to the MemberMeme element, with a value of “atomic” or “subatomic”.  The example below shows this attribute in usage.  

When a ParentMeme meme and its children are instantiated, the link between the *ParentMeme* entity and the *ChildMeme1* will be subatomic, while the link between *ParentMeme* entity and the *ChildMeme2* will be subatomic.  Note that there is no explicit **linktype="atomic"** attribute.  This is because the default value for link types is atomic, just as when dynamically creating links at runtime and a missing linktype attribute is treated as atomic.

```
<Meme id="ParentMeme" metameme="ParentMM">
	<MemberMeme occurrence="1" memberID="ChildMeme1" linktype="subatomic"/>
	<MemberMeme occurrence="1" memberID="ChildMeme2"/>
</Meme>

<Meme id="ChildMeme1" metameme="ChildMM">
</Meme>

<Meme id="ChildMeme2" metameme="ChildMM">
</Meme>
```


## Traversing a Graph

In Graphyne, there are three commands for traversing a graph.  You already met the first, getLinkCounterparts(), in the intro section above.  This method provides a simple and convenient way of getting the nearest neighbors.  It returns the UUIDS of all entities that are one hop away.  If you need more power and need to traverse along a specific search path, then there are two other methods that you can use.  Both use [Memetics’ path traverse syntax][8].  They are getLinkCounterpartsByType(), which traverses along the graph, using the entities memes to find its way.  getLinkCounterpartsByMetaMemeType() is similar, but uses the metamemes of the entities in the graph.

Traverse paths for memes and metamemes are similar.  Both following similar parsing and searching algorithms, but so so in different search spaces; the memePath attribute and the metameme attribute of the entities, respectively.  

E.g in the graph below, to traverse from entity **a** to entity **e**, we’d could use the traverse path “d::e”, while “d::a” would take us back from **e** to **a**.

![][image-3]

### No Backtracking

When traversing graphs, the path can only cross a particular entity once.  If you look at the graph pictured above, it is not possible to reach **e** from **a** with the following path, “b::c::b::a::d::e”, because it would require us to backtrack across both **b** and **a**, where the traverse path originates from.


## Singleton Bridges

Because singleton entities have the potential to be highly connected **hyper-nodes**, traversing methods such as getLinkCounterparts() and getCluster() do not cross singleton bridges by default.  There is an optional flag for crossing a singlton bridge.  The user must actively choose to cross the singleton bridge and is presumably aware of the potential result set size and performance penalty,  In the graph below, entity d represents a singleton.  A getLinkCounterparts() on **c** with the default singleton bridge parameter would not see **e** and vice versa.

![][image-4]


## Subgraphs and Clusters

Memetic has provision for a “graph within a graph” - or graph fragment if you prefer - concept.  In Graphyne, there are two types of partial graphs; the cluster and subgraph.  

**Cluster** - A portion of a graph (or even an entire graph) that has *natural* boundaries.  Natural boundaries can be:
- End effectors (entities with no links leading out of them)
- Entities where the outbound links are filtered by traverse parameters
- Entities where the outbound links change type from atomic to subatomic, or vice versa.  
- Singletons act as end effectors for clusters.

A cluster can have atomic or subatomic links but only one type.

**Subgraph** - A cluster where all links are subatomic.  Generally speaking, a subgraph is built from a meme that has subatomic child memes.  This means that there is a root node entity that acts as a the public facing member of the subgraph and the other entities in the subgraph are private.  

Subgraphs allow complex structures that have a single, public face.  E.g. we have a subgraph where each entity has a property, *Foo*.  The parent (public facing) entity might have an evaluation script that sums up the total *Foo* values of the subgraph and returns an aggregate *Foo* value.  This functions akin to [OLAP aggregation][9].

In the graph shown in the figure below, there are three clusters; one of which is a subgraph.

![][image-5]

The first cluster contains the entities **a**, **b**, **c** and **d**.  They share atomic links and **d** is a singleton.

![][image-6]

The second cluster contains the entities **d** and **e**.

![][image-7]

The third cluster is the subgraph with **c** and **f**.

![][image-8]



## Subgraphs and Link Type

When linking entities via the Graph.api.addEntityLink() method, the developer can decide whether the link will be a public one or private and visible only within a subgraph.

Consider the graph below.  The subdued part of the graph shows entities connected via atomic links.  The darker portion indicates entities that share a subgraph and are connected to each other via subatomic links.  The Orange entity is the entity sharing both subatomic links with the subgraph and atomic links outside of it.

![][image-9]

The third parameter of getLinkCounterpartsByType() - and the only optional one - is the link type restriction.  This value can be 0 (atomic), 1 (subatomic) or *None*.  If there is no link type restriction (and this is the default), then we can happily traverse both atomic and subatomic links.  Then we’d have access to the whole graph, above.  We may want to exclude certain type of links, either for performance or application logic reasons.  E.g. we might be aggregating property values from the subgraph in a single node.  In this case, if we were traversing the graph from outside of the subgraph, we would want to traverse atomic links.  Then the graph would look like the one below.

![][image-10]

If we were traversing from one of the entities participating in the subgraph and limited our link types to subatomic, then we’d only see the subgraph, as shown below.

![][image-11]


## Repositories

Graphyne calls the folders where [Memetic Schemas][10] are stored Repositories.  When the Graph.startdb() method is started, it can be called with a non empty first parameter.  This parameter, repoLocations, is a list of strings, each pointing to a folder on the local filesystem.  

If a Graphyne repo is also a python package (and contains python scripts), it needs a \_\_init\_\_\(\) file.  Memetic repositories need not be in the python path, as they will be added dynamically when Graph.startDB() is started.

Strictly speaking, Memetic allows nested repository folders, creating a hierarchy of template paths.  [The top level is the Package and the child folders contain sub-packages][11].  E.g. you could have a Bar subfolder inside a Foo repository folder and import only the Foo folder.  A meme from another repo would access meme XXX inside of Boo via “Foo.Bar.XXX”.  Right now, Graphyne supports this for templates (memes, metamemes and restrictions), but not for script files.  If a folder contains .py files, it must be at the top of a package tree.  This has been logged as [Issue #15][12].

#### The Default Repository
Graphyne can use the Memetic package as its default repository.  Memetic has a pip installer and Graphyne has a dependency on it, so it should be installed if you used pip and its repo is stored in the python libraries folder.  If you want to use it, then you don’t need to manually track down this folder.  You can simply set useDefaultSchema (the fourth parameter) to **True** when you call Graph.startDB(); in which case Graphyne will find this folder and add it to the repository list automatically.  


## Implicit Memes

If you are using [implicit memes][13], there are a couple of things that need to be done in order for this to work.  Firstly, there needs to be an SQL table for each meme and secondly, the graph has to be directed to use that database as its persistence.  


## Graph Bootstrap Process

When Graph.startDB() is executed, this is the bootstrap order:
1. All repositories are walked, python paths are updated and templates are indexed.
2. Restrictions are cataloged, in no particular order.
3. Metamemes are cataloged, again in no particular order.
4. Metameme enhancements are merged.  This is the phase where metamemes that extend other metamemes have their ancestor properties added.  
5. Memes are loaded from XML and the database (if used) into a temporary list.
6. Implicit memes are fully built up at this point and references defined by database fields are turned into proper subgraphs of meme child references.  E.g. a [back reference][14] from child B to parent A in the metameme declaration and SQL table contents becomes a member meme reference from A to B in the catalog.
7. Memes are now validated against their metamemes.  The results are published in //\<userhomedir\>/Graphyne/GraphyneValidationStatus.html.  If the Memetic content is buggy, this is a good place to start working the problem.
8. Any entities stored in database persistence are now re-instated into the catalog.
9. Any singleton memes are instantiated, if they were not already re-instantiated from persistence.


## Entity Bootstrap Process

Whenever a new entity is created, there is a five step process that it undergoes, before it is live in the graph.  
1. A "stub" version of the entity is created from the meme, containing only the meme and metameme related metadata and the new entity's ID.
2. If the meme has child memes, then those entities will also be ordered created now.
3. Any entities created in step two are now linked.
4. Any properties defined in the meme are now added to the entity.
5. The initialize SES event script - if there is any - is now executed.



# Memetic Scripting

This section deals specifically with how Graphyne handles scripting in Entities derived from the Graphyne.DNA.StateEventScript and Graphyne.DNA.Script metamemes.

## Graphyne.DNA.Script Memes

Graphyne supports a special Memetic metameme for scripts.  The Graphyne.DNA.Script metameme (that is a metameme named Script, in the DNA module of the Memetic package).  If a meme is derived from this metameme or one that extends it, then the script code inside the file referred to in the Script element is read and placed into an attribute called **execute**.  When Graph.api..evaluateEntity() is called, execute is in turn called.  With this, entities can become executable.

Below is the Script metameme.  Note that currently, only Python (3) is supported as a language.  The Script metameme is designed to be language agnostic, to potentially allow other scripting languages to be used if implemented.

```
<MetaMeme id="Script" singleton="true">
<MetaMemeProperty name="Script" type="string"/>
<MetaMemeProperty name="Language" 
type="string" 
constrained="true" 
restriction="ScriptLanguage"/>
</MetaMeme>
```

If the entity is not an instance of Graphyne.DNA.Script, or if it does not have a valid script element that points to a valid python file, then Graph.evaluateEntity() will raise an Exceptions.ScriptError exception.  


## Graphyne.DNA.StateEventScript Memes

Graphyne supports a mechanism for tying scripts to entity life cycle events.  These are defined as restrictions in the Memetic standard schema.  The restriction is *Memetic.StateEventType* and the current list of supported events are:
**initialize** - triggered when an entity is created.
**execute** - triggered explicitly, via the [evaluateEntity() method][15].
**terminate** - triggered when an entity is deprecated or deleted.
**linkAdd** - triggered when an entity is on either end of a new link.
**linkRemove** - triggered when a link that joins the entity is removed.
**propertyChanged** - triggered whenever the properties of an entity are changed.

If we want to add event to an entity, we have to consider three things.  Firstly, we need to be able to declare which language the script is written in.  Secondly, we need to declare which event it is and lastly, we need the location of the file containing the script.

### How Graphyne handles state event script memes

When a schema designer wants to add a state event script to a meme, she does so by creating a chain of entities as diagramed in the picture, below.  Firstly, there is a parent meme.  It is the entities of this meme which will eventually be “executable”.  Secondly, there are 0..n child memes that extend *Graphyne.DNA.StateEventScript*.  Each of these has a *State* property, with restriction type *Memetic.StateEventType*.  Each *Graphyne.DNA.StateEventScript* derived meme has a *Graphyne.DNA.Script* derived child meme.  This meme in turn has a *Script* property, which points to a filesystem location.  If the event type is execute, then it can be called at any time, with the **evaluateEntity()** api method.  The others are internal events, tied to the life cycle of an entity.

![][image-12]

You can see an example of this in action in Graphyne’s test framework.  In the test repository, there is a module called *TestCaseAppendix*.  It follows this chain of memes pattern.

```
<Meme id="ConditionTrueOrFalse_CScr" metameme="Memetic.Condition.ConditionScript"\>
<MemberMeme occurrence="1" memberID="Memetic.Condition.ConditionInitSES"/\>
<MemberMeme occurrence="1" memberID="TrueOrFalseSES"/\>
</Meme\>
<Meme id="TrueOrFalseScript" metameme="Graphyne.DNA.Script"\>
<MemeProperty name="Script" value="TestCaseAppendix.ConditionTrueOrFalse"/\>
<MemeProperty name="Language" value="python"/\>
</Meme\>
<Meme id="TrueOrFalseSES" metameme="Graphyne.DNA.StateEventScript"\>
<MemeProperty name="State" value="execute"/\>
<MemberMeme occurrence="1" memberID="TrueOrFalseScript" /\>
</Meme\>
```

You can see that ConditionTrueOrFalseCScr has TrueOrFalseSES as a child meme, which in turn has TrueOrFalseScript as a child meme.  We see that the State is “execute”, so we’ll be able to call it with the  **evaluateEntity()** api method.  We also see that the value of *TrueOrFalseSES’s* *Script* property is **TestCaseAppendix.ConditionTrueOrFalse**.  The part before the period separator is the file (within the same repository package) and the trailing part is the class name.  

In the next picture, we can see how the scripts are assembled when the memes are instantiated into entities.  

![][image-13]

If a meme has a *Graphyne.DNA.StateEventScript* derived child meme, then the graph engine recognizes that the parent has a state event script.  Suppose a meme **A** has a *Graphyne.DNA.StateEventScript* derived child meme.  When entity **A’ **is created from **A**, the graph engine:
Extracts the *State* property value to determine which even it is attached
It looks for a *Graphyne.DNA.Script* derived child meme of the *Graphyne.DNA.StateEventScript* meme.  
The Script property is parsed and a new python object of the class being referenced is created.  (if it has an init event, that is run)
The new object is then added to **A’** as the appropriate *xxxScript*.  It is a callable object and its *execute() *method is callable.
The StateEventScript and Script memes are instantiated as entities in the graph,  but they are mostly present for metadata purposes.  The callable objects are installed directly onto the parent meme.

![][image-14]

###State Event Script Python code

The actual state event "scripts" themselves are python classes that have an execute() method.  When the entity is bootstrapped,  this class is instantiated and added as a callable object on the entity, which is then manually called via the graph api (as in the case of the execute event) or triggered automatically in the case of the other events.

Writing SES script python code is easy.  If you want to write a state event script class, you will need the following:    
- import Graphyne.Scripting in the module containing your class.
- import Graph.api, if you plan on accessing the graph api.
- Your class should extend **StateEventScript** (from Graphyne.Scripting).  
- **Do not** override the __init__() method.  That is triggered behind the scenes during bootstrapping of the entity.
- Override the execute() method.  This is where your scripting goes.  This method will always be called with two positional parameters at runtime; UUID (as a string) of the entity at position 0 and a dictionary at position 1.
- The dictionary object at position 1 has content that may be useful in handling the event script.  It has [event specific keys][16].
- There are no restrictions on what the execute() method returns.
  

Below is an example for such a script class.

```python
import Graphyne.Scripting
import Graphyne.Graph

class SomeClassName(Graphyne.Scripting.StateEventScript): 

def execute(self, entityID, params):
    return None
```

If the SES script raises an exception, it will be caught by Graphyne and raised as a **Exceptions.EventScriptFailure** exception, along with Python 3 raise… from… nesting information about the inner exception.  Note that if an exception is called during a Graph.api call, the nested exception will probably be of type **Exceptions.ScriptError**.
  
The **params** dictionary object has event specific keys.  These are documented in detail in the [Graph Event Scripting Parameter Reference][16].

# Conditions

Conditions are a significant new feature, introduced in 1.2.  They have [their own documentation page][17].





[1]:	https://github.com/davidhstocker/Memetic
[2]:	https://github.com/davidhstocker/Memetic/blob/master/README.md#schemas
[3]:	https://github.com/davidhstocker/Memetic/blob/master/README.md#traverse-path-syntax
[4]:	https://github.com/davidhstocker/Graphyne/blob/master/Docs/Cluster%20Visualization.md
[5]:	https://github.com/davidhstocker/Graphyne/blob/master/Docs/Graph%20API%20Methods.md
[6]:	https://github.com/davidhstocker/Memetic
[7]:	https://pypi.python.org/pypi/pyodbc
[8]:	https://github.com/davidhstocker/Memetic/blob/master/README.md#traverse-path-syntax
[9]:	https://en.wikipedia.org/wiki/Aggregate_(data_warehouse)
[10]:	https://github.com/davidhstocker/Memetic/blob/master/README.md#schemas
[11]:	https://github.com/davidhstocker/Memetic/blob/master/README.md#entity
[12]:	https://github.com/davidhstocker/Graphyne/issues/15
[13]:	https://github.com/davidhstocker/Memetic/blob/master/README.md#implicit-memes
[14]:	https://github.com/davidhstocker/Memetic/blob/master/README.md#back-references
[15]:	https://github.com/davidhstocker/Graphyne/blob/master/Docs/Graph%20API%20Methods.md#evaluateEntity
[16]:	https://github.com/davidhstocker/Graphyne/blob/master/Docs/GraphEventScriptingParameterReference.md
[17]:	https://github.com/davidhstocker/Graphyne/blob/master/Docs/Conditions.md



[image-1]:	https://raw.githubusercontent.com/davidhstocker/Graphyne/master/Docs/Images/ChildMemes.png
[image-2]:	https://raw.githubusercontent.com/davidhstocker/Graphyne/master/Docs/Images/SingletonBridge.png
[image-3]:	https://raw.githubusercontent.com/davidhstocker/Graphyne/master/Docs/Images/Cluster.png
[image-4]:	https://raw.githubusercontent.com/davidhstocker/Graphyne/master/Docs/Images/GetCluster_Whole.png
[image-5]:	https://raw.githubusercontent.com/davidhstocker/Graphyne/master/Docs/Images/GetCluster_Whole.png
[image-6]:	https://raw.githubusercontent.com/davidhstocker/Graphyne/master/Docs/Images/GetCluster_CAtomic.png
[image-7]:	https://raw.githubusercontent.com/davidhstocker/Graphyne/master/Docs/Images/GetCluster_EAtomic.png
[image-8]:	https://raw.githubusercontent.com/davidhstocker/Graphyne/master/Docs/Images/GetCluster_CSubAtomic.png
[image-9]:	https://raw.githubusercontent.com/davidhstocker/Graphyne/master/Docs/Images/SubGraphAll.png
[image-10]:	https://raw.githubusercontent.com/davidhstocker/Graphyne/master/Docs/Images/SubGraphAtomic.png
[image-11]:	https://raw.githubusercontent.com/davidhstocker/Graphyne/master/Docs/Images/SubGraphSubAtomic.png
[image-12]:	https://raw.githubusercontent.com/davidhstocker/Graphyne/master/Docs/Images/ExecScript_Schema.png
[image-13]:	https://raw.githubusercontent.com/davidhstocker/Graphyne/master/Docs/Images/ExecScript_Bootstrap.png
[image-14]:	https://raw.githubusercontent.com/davidhstocker/Graphyne/master/Docs/Images/ExecScript_SESLive.png