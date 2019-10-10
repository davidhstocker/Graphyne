# Graph API Methods

This is an overview of the api methods for interrogating and manipulating graphs in Graphyne.


---- 


## addEntityBooleanProperty
Adds/Updates a boolean True/False value to an entity.  If the property does not yet exist on the entity, then it will be created, with the new value.  If the property already exists, it will be updated.

#### Parameters

This method has three positional parameters.

- **entityUUID** (mandatory) - The UUID (as a string) of the graph entity that you want to add the new property to. 
- **name** (mandatory) - The name of the property.
- **value** (mandatory) - The boolean value, True or False.

#### Example
Suppose you want to add a new boolean property to an entity.  
- The uuid (in string form) is 'a38f34bc-769f-4bff-9815-1c28222da555'.
- The name of the new property will be 'myNewProperty'.
- The value will be True

```python
Graph.api.addEntityBooleanProperty('a38f34bc-769f-4bff-9815-1c28222da555', 'myNewProperty', True)
```


---- 


## addEntityDecimalProperty

Adds/Updates a Decimal value to an entity.  If the property does not yet exist on the entity, then it will be created, with the new value.  If the property already exists, it will be updated.  The value will be cast to a Decimal when added.

#### Parameters

This method has three positional parameters.

**entityUUID** - The UUID (as a string) of the graph entity that you want to add the new property to. 
**name** - The name of the property.
**value** - The Decimal value, 88.8.  It can also be a string, or float.  It will be cast to a Decimal, if it is not already.

#### Examples

Suppose you want to add a new Decimal property to an entity.  
The uuid (in string form) is 'a38f34bc-769f-4bff-9815-1c28222da555'.
The name of the new property will be 'myNewProperty'.
The value will be 88.8
```python
Graph.api.addEntityDecimalProperty('a38f34bc-769f-4bff-9815-1c28222da555', 'myNewProperty', '88.8')
```
or
```python
Graph.api.addEntityDecimalProperty('a38f34bc-769f-4bff-9815-1c28222da555', 'myNewProperty', 88.8)
```


---- 


## addEntityIntegerProperty

Adds/Updates a Integer value to an entity.  If the property does not yet exist on the entity, then it will be created, with the new value.  If the property already exists, it will be updated.  The value will be cast to a Integer when added.

#### Parameters

This method has three positional parameters.

**entityUUID** - The UUID (as a string) of the graph entity that you want to add the new property to. 
**name** - The name of the property.
**value** - The Integer value, 88.  It can also be a string or float, as it will be cast to int.

#### Examples

Suppose you want to add a new Integer property to an entity.  
The uuid (in string form) is 'a38f34bc-769f-4bff-9815-1c28222da555'.
The name of the new property will be 'myNewProperty'.
The value will be 88
```python
Graph.api.addEntityIntegerProperty('a38f34bc-769f-4bff-9815-1c28222da555', 'myNewProperty', '88')
```
or 
```python
Graph.api.addEntityIntegerProperty('a38f34bc-769f-4bff-9815-1c28222da555', 'myNewProperty', 88)
```


---- 


## addEntityLink

Adds/Updates a String value to an entity.  If the property does not yet exist on the entity, then it will be created, with the new value.  If the property already exists, it will be updated.  The value will be cast to a String when added.  All links are directional and have a source + target entity combination.  Traverse queries can choose to ignore directionality.

#### Parameters

This method has four positional parameters.

1. **entityUUID1** - The entity that the link originates from.
2. **entityUUID2** - The target entity.
3. **linkAttributes** (default = {} ) - A python dictionary, containing the values to be added to the link.  The keys will become the attribute names and the values will be the attribute values.  They are all handled as strings.
4. **linkType** (default = 0) - The type of link to be created.  There are two possible codes for these link types; 0 (atomic) and 1 (subatomic).  Subatomic links can only be traversed from within the same cluster.


#### Examples

Suppose you want to add a link between two entities.  
- The uuid (in string form) of the source entity (where the link is originating from) is 'a38f34bc-769f-4bff-9815-1c28222da555'.
- The uuid (in string form) of the target entity (where the link is originating from) is 'b49f34bc-769f-4bff-9815-1c28222da555'.
- There are no link attributes.
- The link type is atomic.

```python
Graph.api.addEntityLink('a38f34bc-769f-4bff-9815-1c28222da555', 'b49f34bc-769f-4bff-9815-1c28222da555')
```

In the second example, we'll add link attributes.
- The uuid (in string form) of the source entity (where the link is originating from) is 'a38f34bc-769f-4bff-9815-1c28222da555'.
- The uuid (in string form) of the target entity (where the link is originating from) is 'b49f34bc-769f-4bff-9815-1c28222da555'.
- There are two link attributes.  "textValue" = "Hello World" and "attribCount" = 2
- The link type is still atomic.
```python
Graph.api.addEntityLink('a38f34bc-769f-4bff-9815-1c28222da555', 'b49f34bc-769f-4bff-9815-1c28222da555', {"textValue" : "Hello World", "attribCount" : 2})
```

In the third example, we'll add make the link subatomic.
- The uuid (in string form) of the source entity (where the link is originating from) is 'a38f34bc-769f-4bff-9815-1c28222da555'.
- The uuid (in string form) of the target entity (where the link is originating from) is 'b49f34bc-769f-4bff-9815-1c28222da555'.
- There are two link attributes.  "textValue" = "Hello World" and "attribCount" = 2
- The link type is subatomic.
```python
Graph.api.addEntityLink('a38f34bc-769f-4bff-9815-1c28222da555', 'b49f34bc-769f-4bff-9815-1c28222da555', {"textValue" : "Hello World", "attribCount" : 2}, 1)
```
 


---- 


## addEntityStringProperty

Adds/Updates a String value to an entity.  If the property does not yet exist on the entity, then it will be created, with the new value.  If the property already exists, it will be updated.  The value will be cast to a String when added.

#### Parameters

This method has three positional parameters.

**entityUUID** - The UUID (as a string) of the graph entity that you want to add the new property to. 
**name** - The name of the property.
**value** - The String value, 88.  It can also be a string or float, as it will be cast to int.

#### Example

Suppose you want to add a new String property to an entity.  
The uuid (in string form) is 'a38f34bc-769f-4bff-9815-1c28222da555'.
The name of the new property will be 'myNewProperty'.
The value will be 'Hello World'
```python
Graph.api.addEntityStringProperty('a38f34bc-769f-4bff-9815-1c28222da555', 'myNewProperty', 'Hello World')
```



---- 



## createEntity

Creates a new, blank entity of type Graphyne.Generic.

#### Parameters
none

#### Returns
The uuid (as string) of the newly created entity.

#### Example

```python
Graph.api.createEntity()
```



---- 



## createEntityFromMeme

Creates a new, blank entity of type Graphyne.Generic and returns the UUID of the newly created entity.

#### Parameters
none

#### Returns
The uuid (as string) of the newly created entity.


#### Example

If you wanted to create an Entity of type Graphyne.Generic (the type of Entity created by createEntity()), but explicitly declare the meme.

```python
Graph.api.createEntityFromMeme("Graphyne.Generic")
```



---- 



## evaluateEntity

Executes the *execute* state event script for a particular entity, if it has one.  See the [documentation on state event scripts][1] for more information on how they are defined in a schema.

#### Parameters

This method has two positional parameters.

**entityUUID** - The UUID of the entity whose execute state event script callable object’s (self.execScript) execute method is to be fired.  
**runtimeVariables** - A dictionary, containing any information that needs to be passed to the execute method of the callable object.  

#### Returns
State event script execute() methods are expected to return something, or they will throw a Exceptions.ScriptError exception.

#### Example

If you had an entity, **X**, that had an execute state event script and you wanted to execute it and had no parameters.
```python
evalResults = Graph.api.evaluateEntity(X)
```


If you had an entity, **X**, that had an execute state event script and you wanted to execute it and had parameters contained in a dictionary, called **rtParams**.
```python
evalResults = Graph.api.evaluateEntity(X, rtParams)
```

If you had an entity, **X**, that had **no** execute state event script and you tried to execute it, a Graphyne Exceptions.ScriptError exception would be raised, with a nested AttributeError exception.



---- 


## getCluster

Initiates a generic (non-directed) traverse from a given entity  and returns a subgraph.  This subgraph can be limited to specific link types (atomic or subatomic) and to specific traverse parameters.   Because of this traverse parameter filtering, these subgraph fragments are referred to as clusters.  It returns dictionary with two keys; “links” and “nodes”.  “nodes” has a list of all of the entities in the cluster, their ID, meme and metameme.  “links” has a list of links pairs, from UUID and to UUID.  This method differs from [getTraverseReport][8] in that this method does not follow a specific traverse path and follows all branching links in all directions, while **getTraverseReport** traverses a specific path and returns only the entities along this path and their nearest neighbors.

#### Parameters

This method has four positional parameters.

**entityUUID** - The UUID (as a string) of the graph entity that you want use as the root node for finding the cluster. 
**linkTypes** - Either 0 (atomic) or 1 (subatomic).  Default is 0.
**linkAttributes** (default = {} ) - A python dictionary, containing the link attributes to be filtered for.  The keys will become the attribute names and the values will be the attribute values. 
**crossSingletons** (default = False) - Whether or not singletons are to be treated as end effectors.  The default is false.  Crossing singleton bridges is considered an option, as there may be times when you want to do this, but it should be done with care as the result sets may be monumentally large.

#### Returns

It returns dictionary with two keys; “links” and “nodes”.  “nodes” has a list of all of the entities in the subgraph.  Each entity is represented by a dictionary; with, meme, metameme and position.  “links” has a list of links pairs, from UUID and to UUID.

{
	'nodes': [
		{
			'id': <entity UUID>, 
			'meme': <entity Meme>, 
			'metaMeme': '<entity Metameme>, 
			'position': XXX
		}, 
		...										
	],
	'links' : [
		{
			'source': <source entity UUID>, 
			'target': <target entity UUID>, 
			'value': 1
		}, 
		...
	]
}

The return value of **getCluster()** differs from the one from **getTraverseReport()** by its use of the **position** attribute in the entity dictionaries.  In this method, there is no traverse path to convey, so position tells us about the state of the entity.  If it is the entity that we are marshalling the subgraph from, then the value of the position attribute is **0**.  If it is a singleton (even if it is the origin entity), then the value of the position attribute is **2**.  In all other cases, it is **1**. 



#### Example

This method in action can be best displayed by looking at the testGetCluster() method of Graphyne’s regression test utility, smoketest.py.  To set up te test, five Graphyne.Generic generic entities are created - which we will label **a**, **b**, **c**, **e** and **f** - and the createEntitiyFromMeme method is used on Examples.MemeA4, which is a singleton and will be labeled **d**.  We then chain them together with addEntityLink() to create the image below, which follows the [Graphyne graph diagraming conventions][2].  Note that the link from c to f is subatomic.
![][image-1]

The first test collects the atomic cluster rooted on **c**.  We use no link attribute filters.
```python
api.getClusterMembers(c)
```
![][image-2]

Next, we repeat the last exercise, but allow the cluster to cross singleton bridges.
```python
api.getClusterMembers(c)
```
![][image-3]

Next, we collect the subatomic cluster rooted on **c**.  We use no link attribute filters.
```python
api.getClusterMembers(c, 1)
```
![][image-4]

The atomic cluster rooted on **e**.  We use no link attribute filters.
```python
api.getClusterMembers(e)
```
![][image-5]

The subatomic cluster rooted on **e**.  We use no link attribute filters.
```python
api.getClusterMembers(e, 1)
```
![][image-6]



---- 


## getClusterJSON

An alternate to [getCluster][3], which returns the cluster in a [D3][4] friendly JSON format.


---- 


## getClusterMembers


Another [getCluster][5] variant.  This one returns only a list of the entity UUIDs in the cluster, without any node or relationship metadata.


---- 


## getEntity

Gets the actual Graph.Entity object that the graph engine is using.  It is not normally recommended to work directly with the entity object itself - mainly due to thread safety and the fact that the persistence may be tracking entity state separately and direct access could put it out of sync.  This method is available if you need it however.

#### Parameters

This method has one positional parameter.

**entityUUID** - The UUID (as a string) of the entity object to be returned.

#### Returns
The *Graph.Entity* object whose *id* property matches the *entityUUID* parameter.


#### Example

If you wanted to create an Entity of type Graphyne.Generic (the type of Entity created by createEntity()), but explicitly declare the meme.
```python
myEntity = Graph.api.getEntity(entityUUID)
```



---- 


## getEntity

Gets the actual Graph.Entity object that the graph engine is using.  It is not normally recommended to work directly with the entity object itself - mainly due to thread safety and the fact that the persistence may be tracking entity state separately and direct access could put it out of sync.  This method is available if you need it however.

#### Parameters

This method has one positional parameter.

**entityUUID** - The UUID (as a string) of the entity object to be returned.

#### Returns
The *Graph.Entity* object whose *id* property matches the *entityUUID* parameter.


#### Example

If you wanted to create an Entity of type Graphyne.Generic (the type of Entity created by createEntity()), but explicitly declare the meme.
```python
myEntity = Graph.api.getEntity(entityUUID)
```




---- 


## getEntityHasProperty

Tests whether an entity has a given property assigned.

#### Parameters

This method has two positional parameters.

**entityUUID** - The UUID (as a string) of the entity to be tested.
**propertyName** - The name of the property.

#### Returns
*True* or *False*.


#### Example

The following tests whether the property *foo* is in entity **x**.
```python
myEntity = Graph.api.getEntityHasProperty(x, “foo”)
```



---- 


## getEntityMemeType

Gets the entity’s meme path.

#### Parameters

This method has two positional parameters.

**entityUUID** - The UUID (as a string) of the entity to be tested.


#### Returns

The full template path of the meme, as a string.


#### Example

The following gets the meme path of entity **x**.
```python
myEntity = Graph.api.getEntityMemeType(x)
```



---- 


## getEntityPropertyType

Gets the property type of a given entity property.

#### Parameters

This method has two positional parameters.

**entityUUID** - The UUID (as a string) of the entity to be tested.
**propertyName** - The name of the property, as a string.


#### Returns
If the property is present, this method returns one of the following string values:
- String
- Integer
- Decimal
- Boolean
- List

If the property is not present, an empty string is returned.  If the entity is not present, an *ScriptError* exception is returned.

#### Example

Presuming that we have a property “a” on entity x, the following returns its type.
```python
thePropertyType = Graph.api.getEntityPropertyType(x, “a”)
```



---- 


## getEntityPropertyValue

Gets the value of a given entity property.

#### Parameters

This method has two positional parameters.

**entityUUID** - The UUID (as a string) of the entity to be tested.
**propertyName** - The name of the property, as a string.


#### Returns
If the property is present, this method returns its value.  The value will be of the type of the property, so an integer property will return an integer,  a Decimal property will return a Decimal value, etc.

If the property is not present, an *None* is returned.  If the entity is not present, an *ScriptError* exception is returned.

#### Example

Presuming that we have a property “a” on entity x, the following returns its value.
```python
thePropertyValue = Graph.api.getEntityPropertyValue(x, “a”)
```



---- 


## getIsEntitySingleton

Gets whether or not a given entity is a singleton.

#### Parameters

This method has one positional parameter.

**entityUUID** - The UUID (as a string) of the entity to be tested.


#### Returns
**True** or **False**.

If the entity is not present, an *ScriptError* exception is returned.


#### Example

Determines whether or not entity **x** is a singleton..
```python
isSingleton = Graph.api.getIsEntitySingleton(x)
```



---- 


## getIsMemeSingleton

Gets whether or not a given meme is a singleton.  

#### Parameters

This method has one positional parameter.

**memePath** - The full template path (as a string) of the meme to be tested.

#### Returns
**True** or **False**.

If the meme is not present, an *ScriptError* exception is returned.


#### Example

Determines whether or not meme **”SomeMeme”** is a singleton.
```python
isSingleton = Graph.api.getIsMemeSingleton(“SomeMeme”)
```



---- 


## getLinkCounterparts

Gets all of the target entity’s nearest neighbors (exactly one hop away) of the given link type.  

#### Parameters
This method has two positional parameters.

**entityID** - The entity uuid.
**linkType (default = None)** - *0* to restrict the search to atomic links, *1* to restrict it to a subgraph (subatomic links only) and None to traverse both link types with no restrictions.

#### Returns
A list of entity uuids at the traverse terminus.  If nothing is there, or if it is not possible to complete the traverse, then an empty list, [] is returned.

#### Examples

Gets all of the nearest neighbors of entity x (using its uuid), regardless of link type.
```python
entityUUIDList = Graph.api.getLinkCounterparts(x)
```

Gets all of the nearest neighbors of entity x (using its uuid) with atomic links.
```python
entityUUIDList = Graph.api.sgetLinkCounterparts(x, 0)
```

Gets all of the nearest neighbors of entity x (using its uuid) in the same subgraph (with subatomic links).
```python
entityUUIDList = Graph.api.getLinkCounterparts(x, 1)
```


---- 


## getLinkCounterpartsByType

Traverses from a specific entity in the graph and retrieves any entities found at the end of the specified traverse path.  This is a workhorse method from getting from one point in a graph to another and finding entities based on their relationship to another.  These traverses are not limited to entities within the same cluster.  

#### Parameters

This method has four positional parameters.

**entityID** - The entity uuid.
**memePath** - The traverse path, including filters.
**linkType (default = None)** - *0* to restrict the search to atomic links, *1* to restrict it to a subgraph (subatomic links only) and None to traverse both link types with no restrictions.
**fastSearch (default = False)** - When this option is used, the traverse will never cross the same entity twice.  The fast search option can significantly speed up traverses of dense clusters, but also changes the nature of the traverse.  

As an example, consider the following graph.  

![][image-7]

If we wanted to traverse via *a\>\>b\>\>c\>\>d\>\>b\>\>e*; where we did not want to traverse the shortest path to e, but rather wanted to be certain that c and d were also within the cluster, we’d need to do so without the fast search option enabled.  Each time we reach entity b, there are three outbound links and all need to be evaluated.  

![][image-8]

By turning this option on, our *a\>\>b\>\>c\>\>d\>\>b\>\>e* traverse would fail and return an empty result, as we’d not cross b the second time.  

![][image-9]

It should be noted that double wildcard options within traverse strings always have an implicit **fastSearch**.  So if our traverse was a\>\>\*\*\>\>e, the graph would begin searching down both outbound links at b (the link from d to b is inbound, from b’s perspective).  Once the c to d branch reached b again, it would terminate and the hop directly from b to e would be the only one left to traverse.


#### Returns
A list of entity uuids at the traverse terminus.  If nothing is there, or if it is not possible to complete the traverse, then an empty list, [] is returned.

#### Examples

The following examples all use the example a-b-c-d-e graph shown above and start from **a** (and using its uuid.  b through e are known only by their memes).
![][image-10]

The following returns a list containing b’s uuid, regardless of link type (atomic or subatomic)
```python
entityUUIDList = Graph.api.getLinkCounterpartsByType(a, “b”)
```

The following returns a list containing b’s uuid, regardless of link type (atomic or subatomic), because a single asterisk wildcard  (“\*”) always selects nearest neighbors, one hop away.  In fact, getLinkCounterparts() wraps getLinkCounterpartsByType() and executes it with a single wildcard traverse string.
```python
entityUUIDList = Graph.api.getLinkCounterpartsByType(a, “\*”)
```

The following returns an empty list, because there is no x in the graph.
```python
entityUUIDList = Graph.api.getLinkCounterpartsByType(a, “b”)
```


The following returns a list containing b’s uuid, because it has an atomic link.
```python
entityUUIDList = Graph.api.getLinkCounterpartsByType(a, “b”, 0)
```

The following returns an empty list, because it has an atomic link, but we are restricting our search to a subgraph.
```python
entityUUIDList = Graph.api.getLinkCounterpartsByType(a, “b”, 1)
```

The following returns a list containing b’s uuid, regardless of link type (atomic or subatomic), because the link runs from a to b.
```python
entityUUIDList = Graph.api.getLinkCounterpartsByType(a, “\>\>b”)
```

The following returns an empty list, because the link runs from a to b and we are searching for a link from b to a.
```python
entityUUIDList = Graph.api.getLinkCounterpartsByType(a, “\<\<b”)
```

The following returns a list containing e’s uuid, regardless of link type (atomic or subatomic), and regardless of direction.
```python
isSingleton = Graph.api.getLinkCounterpartsByType(a, “b::e”)
```

The following returns a list containing e’s uuid, regardless of link type (atomic or subatomic), because the link runs from b to e.
```python
isSingleton = Graph.api.getLinkCounterpartsByType(a, “b\>\>e”)
```

The following returns an empty list, regardless of link type (atomic or subatomic), because the link runs from b to e.
```python
isSingleton = Graph.api.getLinkCounterpartsByType(a, “b\<\<e”)
```

The following returns a list containing e’s uuid, regardless of link type (atomic or subatomic), because we follow the path in the picture.
![][image-11]
```python
isSingleton = Graph.api.getLinkCounterpartsByType(a, “b\>\>c\>\>d\>\>b\>\>e”)
```

The following returns an empty list, because although we are traversing all atomic links and the links are in the correct direction we have a fastSearch termination the second time we try to cross b.
![][image-12]
```python
isSingleton = Graph.api.getLinkCounterpartsByType(a, “b\>\>c\>\>d\>\>b\>\>e”, 0, True)
```

The following returns a list containing e, because we have a single wildcard
```python
isSingleton = Graph.api.getLinkCounterpartsByType(a, “\*\>\>e”)
```

The following returns a list containing e, because we have a double wildcard
```python
isSingleton = Graph.api.getLinkCounterpartsByType(a, “\*\*\>\>e”)
```


---- 


## getTraverseReport

Initiates a traverse from a given entity  and returns a subgraph with the same format as [getCluster][3].  It returns dictionary with two keys; “links” and “nodes”.  “nodes” contaoins all of the entities in the subgraph and their metadata.  “links” has a list of links pairs, from UUID and to UUID.  

#### Parameters

This method has three positional parameters.

**entityUUID** - The UUID (as a string) of the graph entity that you want use as the root node for finding the cluster. 
**traversePath** - The traverse path, including filters.
**isMeme** (default = True ) - Whether the traverse path follows the entity memes or not.  If False, it will follow the entity metamemes. 

#### Returns

It returns dictionary with two keys; “links” and “nodes”.  “nodes” has a list of all of the entities in the subgraph.  Each entity is represented by a dictionary; with, meme, metameme and position.  “links” has a list of links pairs, from UUID and to UUID.

{
	'nodes': [
		{
			'id': <entity UUID>, 
			'meme': <entity Meme>, 
			'metaMeme': '<entity Metameme>, 
			'position': XXX
		}, 
		...										
	],
	'links' : [
		{
			'source': <source entity UUID>, 
			'target': <target entity UUID>, 
			'value': 1
		}, 
		...
	]
}

The return value of **getTraverseReport()** differs from the one from **getCluster()** by its use of the **position** attribute in the entity dictionaries.  In this method, it conveys the position of each particular entity in the cluster.  The entities along the traverse path have positive values, with the starting entity having the lowest value and the value increasing with further distance along the traverse and the end effector having trhe highest value.  The subgraph also includes the nearest neighbor entities,  linked to the entities along the traverse path (one hop only), but not directly in the path themselves.  These entities are all given a **position** attribute value of -1.  The intent of this attribute is to give tools displaying thse subgraphs to convey spatial position withon the subgraph, relative to the start entity. 


---- 


## getTraverseReportJSON

An alternate to [getTraverseReport][8], which returns the subgraph in a [D3][4] friendly JSON format.


---- 


## removeAllCustomPropertiesFromEntity

Removes all properties on an entity that were not defined in its meme.  This is not a full reset, as properties that were defined in the meme are left untouched, even if they were changed.  To reset the properties to their meme defined values, you need to use [revertEntityPropertyValues()][6].  

#### Parameters

This method has one positional parameter.

**entityID** - The entity uuid.

#### Returns

nothing is returned from this method.


#### Example

Given an entity with uuid x, the following removes all properties not defined in the meme.
```python
Graph.api.removeAllCustomPropertiesFromEntity(x)
```



---- 


## removeEntityLink

Removes links going from a particular entity to another particular entity..  

#### Parameters

This method has two positional parameters.

**entityID** - The entity uuid where the link(s) originate from.
**memberUUID** - The entity uuid where the link(s) end.

#### Returns

nothing is returned from this method.


#### Example

Given two entities with uuids x and y, the following removes all links originating on the entity with uuid x and ending on the entity with uuid y.
```python
Graph.api.removeEntityLink(x, y)
```



---- 


## removeEntityProperty

Removes a property from a particular entity..  

#### Parameters

This method has two positional parameters.

**entityID** - The entity uuid..
**propertyName** - The name of the property to be removed.

#### Returns

nothing is returned from this method.


#### Example

Given an entity with uuid x and property “toBeRemoved”, the following removes “toBeRemoved”,.
```python
Graph.api.removeEntityProperty(x, “toBeRemoved”)
```



---- 


## revertEntityPropertyValues

Reverts all entities defined in an entity’s meme to their original values, as defined in the meme.  It does not affect custom properties on the entity, that were not originally part of the meme definition.  To do that, you need to use [removeAllCustomPropertiesFromEntity()][7].  

#### Parameters

This method has one positional parameter.

**entityID** - The entity uuid.

#### Returns

nothing is returned from this method.


#### Example

Given an entity with uuid x and property “toBeRemoved”, the following removes “toBeRemoved”,.
```python
Graph.api.revertEntityPropertyValues(x)
```



---- 


## setEntityPropertyValue

Sets a property value on the given entity; altering its value if it is already there and creating it (with the given value) if it was not already present on the entity.  

#### Parameters

This method has three positional parameters.

**entityID** - The entity uuid.
**propertyName** - The name of the property, as a string value.
**propertyValue** - The value of the property.  

#### Returns

nothing is returned from this method.


#### Example

Adds (or updates) a property named “myProp” and a string value of “Hello World” on and entity with uuid x.
```python
Graph.api.setEntityPropertyValue(x, “myProp”)
```



---- 


## sourceMemeCreate

This method allows programmatic, live creation of memes at runtime (as opposed to being written in xml beforehand).  It creates an empty meme in the template repository, with the given metameme and meme parameters.  

#### Parameters
This method has three positional parameters.

**memeName** - The name of the newly created meme.
**modulePath** (default = *\<defaultModule\>*) - Every meme exists within a module.  If no module name is given with this command, then the current default module will be used.  This is “*Graphyne*”, unless it has been changed.
**metamemePath** (default = “*Graphyne.GenericMetaMeme*”) - If no specific metameme is given then the default metameme for free entity creation,  “*Graphyne.GenericMetaMeme*”, is used. 

#### Returns

This method returns a dict, with the following format:
```
{
    ValidationResults': \[<boolean>, <failurelist>\], 
    memeID': <modulePath.memeName>
}
```

The **ValidationResults** key and corresponding value is the results of meme validation against its parent metameme.  This method triggers a meme cataloging operation in the template repository and new memes are always validated against their metameme.  New, blank memes are always valid, because they’ve not yet had anything added that could make them invalid, vis-à-vis their parent metameme.  The value **[True, []]** should be expected.

The **memeID** key contains the concatenated template path of the new meme.


#### Examples

Creates a meme named “HelloWorld” in the default module (“Graphyne” in this example), using the metameme “Graphyne.GenericMetaMeme”.
```python
memeCreationResults = Graph.api.sourceMemeCreate(“HelloWorld”)
```

Creates a meme named “HelloWorld” in a module named “HelloModule”, using the metameme “Graphyne.GenericMetaMeme”.
```python
memeCreationResults = Graph.api.sourceMemeCreate(“HelloWorld”, “HelloModule”)
```

Creates a meme named “HelloWorld” in a module named “HelloModule”, using the metameme “HelloModule.HelloMetameme”.
```python
memeCreationResults = Graph.api.sourceMemeCreate(“HelloWorld”, “HelloModule”, “HelloModule.HelloMetameme”)
```



---- 


## sourceMemeEnhancementAdd

This method creates a Memetic enhance relationship between two memes.  This is an api counterpart to the MemeEnhancements element, when defining memes statically via xml. The usual memetic enhancement rules must be followed, but generic memes may enhance other generic memes, as the metameme Graphyne.GenericMetaMeme enhances itself.  

#### Parameters

This method has two positional parameters.

**sourceMemeID** - The source meme full template path.
**targetMemeID** - The target meme full template path.  

#### Returns

A list, containing validation results.  The meme will be validated when the property is added and the properties will be checked against the metameme.  If the validation results of the enhanced meme turns up invalid, then the meme is not updated; unless the meme’s metameme is Graphyne.GenericMetaMeme. in this case, the result list is always invalid and can be ignored, but the meme is created anyway.  The validation results are only relevant for memes not using a generic metameme.

#### Example

Presuming that we have a meme “Graphyne.EnhancingMeme” and meme “Graphyne.EnhancedMeme”, the following will use *enhancing* to enhance *enhanced*.
```python
valList = api.sourceMemeEnhancementAdd(“Graphyne.EnhancingMeme”, “Graphyne.EnhancedMeme”)
```



---- 


## sourceMemeEnhancementRemove

This method removes an existing Memetic enhance relationship between two memes.  

#### Parameters

This method has two positional parameters.

**sourceMemeID** - The source meme full template path.
**targetMemeID** - The target meme full template path.  

#### Returns

A list, containing validation results.  As with sourceMemeEnhancementAdd , the meme will be validated when the property is added and the properties will be checked against the metameme.  


#### Example

Presuming that we have a meme “Graphyne.EnhancingMeme” and meme “Graphyne.EnhancedMeme”, the following will use *enhancing* to enhance *enhanced*.
```python
valList = api.sourceMemeEnhancementRemove(“Graphyne.EnhancingMeme”, “Graphyne.EnhancedMeme”)
```



---- 


## sourceMemeMemberAdd

This method attaches a meme as a member meme of another.  This is an api counterpart to the MemberMeme element, when defining memes statically via xml.  

#### Parameters

This method has three positional parameters.

**fullTemplatePath** - The full template path of the meme.
**memberID** - The full template path of the meme being added as a member.  
**occurrence** - The occurrence count of the member meme.  

#### Returns

A list, containing validation results.  When memes are manipulated via API, they are validated afterwards..  


#### Example

Presuming that we have a meme “Graphyne.ParentMeme” and meme “Graphyne.MemberMeme”, the following will add * Graphyne.MemberMeme* as a member of * Graphyne.MemberMeme*.
```python
valList = api.sourceMemeMemberAdd(“Graphyne.ParentMeme”, “Graphyne.MemberMeme”, 1)
```



---- 


## sourceMemeMemberRemove

This method removes a meme from being a member meme of another.  

#### Parameters

This method has two positional parameters.

**fullTemplatePath** - The full template path of the meme.
**memberID** - The full template path of the meme being removed as a member.  

#### Returns

A list, containing validation results.  When memes are manipulated via API, they are validated afterwards..  


#### Example

Presuming that we have a meme “Graphyne.ParentMeme” and member meme “Graphyne.MemberMeme”, the following will remove *Graphyne.MemberMeme* as a member of * Graphyne.MemberMeme*.
```python
valList = api.sourceMemeMemberRemove(“Graphyne.ParentMeme”, “Graphyne.MemberMeme”, 1)
```



---- 


## sourceMemePropertyRemove

This method removes a property from a meme.
  

#### Parameters

This method has four positional parameters.

**fullTemplatePath** - The full template path of the meme.
**propName** - Name of the property to be added or updates.
**propValue** - The value to be set on the property.

#### Returns

A list, containing validation results.  When memes are manipulated via API, they are validated afterwards.


#### Example

Presuming that we have a meme “Graphyne.CustomMeme”, the following will remove an integer property called “hello”, if it exists..
```python
valList = api.sourceMemePropertyRemove(“Graphyne.CustomMeme”, “hello”)
```



---- 


## sourceMemePropertySet

This method sets a default value on a meme property, creating it if it is not already present.  

#### Parameters
This method has four positional parameters.

**fullTemplatePath** - The full template path of the meme.
**propName** - Name of the property to be added or updates.
**propValue** - The value to be set on the property.
**propType** (default = ‘string’) - The type of the property; one of 'string', 'list', 'integer', 'boolean' or 'decimal'

#### Returns
A list, containing validation results.  When memes are manipulated via API, they are validated afterwards.


#### Example
Presuming that we have a meme “Graphyne.CustomMeme”, the following will create an integer property called “hello”, with a value of 2.
```python
valList = api.sourceMemePropertySet(“Graphyne.CustomMeme”, “hello”, 2, 'integer')
```



---- 


## sourceMemeSetSingleton

This method sets the singleton property of a meme.
  

#### Parameters
This method has two positional parameters.

**fullTemplatePath** - The full template path of the meme.
**isSingleton** - True or False.  If true, then the meme will be set to singleton status.


#### Returns
A list, containing validation results.  When memes are manipulated via API, they are validated afterwards.


#### Example

Presuming that we have a meme “Graphyne.CustomMeme”, the following will set it to become a singleton.
```python
valList = api.sourceMemeSetSingleton(“Graphyne.CustomMeme”, True)
```


[1]:	https://github.com/davidhstocker/Graphyne#memeticdnastateeventscript-memes
[2]:	https://github.com/davidhstocker/Graphyne/blob/master/Docs/Cluster%20Visualization.md
[3]:	https://github.com/davidhstocker/Graphyne/blob/master/Docs/Graph%20API%20Methods.md#getcluster
[4]:	https://d3js.org/
[5]:	https://github.com/davidhstocker/Graphyne/blob/master/Docs/Graph%20API%20Methods.md#getcluster
[6]:	https://github.com/davidhstocker/Graphyne/blob/master/Docs/Graph%20API%20Methods.md#revertentitypropertyvalues
[7]:	https://github.com/davidhstocker/Graphyne/blob/master/Docs/Graph%20API%20Methods.md#removeallcustompropertiesfromentity
[8]:	https://github.com/davidhstocker/Graphyne/blob/master/Docs/Graph%20API%20Methods.md#gettraversereport

[image-1]:	https://raw.githubusercontent.com/davidhstocker/Graphyne/master/Docs/Images/GetCluster_Whole.png
[image-2]:	https://raw.githubusercontent.com/davidhstocker/Graphyne/master/Docs/Images/GetCluster_CAtomic.png
[image-3]:	https://raw.githubusercontent.com/davidhstocker/Graphyne/master/Docs/Images/GetCluster_CAtomicCrossSingletonBridge.png
[image-4]:	https://raw.githubusercontent.com/davidhstocker/Graphyne/master/Docs/Images/GetCluster_CSubAtomic.png
[image-5]:	https://raw.githubusercontent.com/davidhstocker/Graphyne/master/Docs/Images/GetCluster_EAtomic.png
[image-6]:	https://raw.githubusercontent.com/davidhstocker/Graphyne/master/Docs/Images/GetCluster_ESubAtomic.png
[image-7]:	https://raw.githubusercontent.com/davidhstocker/Graphyne/master/Docs/Images/Fastsearch1.png
[image-8]:	https://raw.githubusercontent.com/davidhstocker/Graphyne/master/Docs/Images/Fastsearch2.png
[image-9]:	https://raw.githubusercontent.com/davidhstocker/Graphyne/master/Docs/Images/Fastsearch3.png
[image-10]:	https://raw.githubusercontent.com/davidhstocker/Graphyne/master/Docs/Images/Fastsearch1.png
[image-11]:	https://raw.githubusercontent.com/davidhstocker/Graphyne/master/Docs/Images/Fastsearch2.png
[image-12]:	https://raw.githubusercontent.com/davidhstocker/Graphyne/master/Docs/Images/Fastsearch3.png