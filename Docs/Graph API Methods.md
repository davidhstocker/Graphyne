# Graph API Methods

This is an overview of the api methods for interrogating and manipulating graphs in Graphyne.

## addEntityBooleanProperty
Adds/Updates a boolean True/False value to an entity.  If the property does not yet exist on the entity, then it will be created, with the new value.  If the property already exists, it will be updated.

#### Parameters
In order…
- **entityUUID** (mandatory) - The UUID (as a string) of the graph entity that you want to add the new property to. 
- **name** (mandatory) - The name of the property.
- **value** (mandatory) - The boolean value, True or False.

#### Example
Suppose you want to add a new boolean property to an entity.  
- The uuid (in string form) is 'a38f34bc-769f-4bff-9815-1c28222da555'.
- The name of the new property will be 'myNewProperty'.
- The value will be True

	'python
Graph.api.addEntityBooleanProperty('a38f34bc-769f-4bff-9815-1c28222da555', 'myNewProperty', True)
	'





## addEntityDecimalProperty

Adds/Updates a Decimal value to an entity.  If the property does not yet exist on the entity, then it will be created, with the new value.  If the property already exists, it will be updated.  The value will be cast to a Decimal when added.

#### Parameters
**entityUUID** - The UUID (as a string) of the graph entity that you want to add the new property to. 
**name** - The name of the property.
**value** - The Decimal value, 88.8.  It can also be a string, or float.  It will be cast to a Decimal, if it is not already.

#### Example

Suppose you want to add a new Decimal property to an entity.  
The uuid (in string form) is 'a38f34bc-769f-4bff-9815-1c28222da555'.
The name of the new property will be 'myNewProperty'.
The value will be 88.8

	'python
Graph.api.addEntityDecimalProperty('a38f34bc-769f-4bff-9815-1c28222da555', 'myNewProperty', '88.8')
	'
or
	'python
Graph.api.addEntityDecimalProperty('a38f34bc-769f-4bff-9815-1c28222da555', 'myNewProperty', 88.8)
	'



## addEntityIntegerProperty

Adds/Updates a Integer value to an entity.  If the property does not yet exist on the entity, then it will be created, with the new value.  If the property already exists, it will be updated.  The value will be cast to a Integer when added.

#### Parameters
**entityUUID** - The UUID (as a string) of the graph entity that you want to add the new property to. 
**name** - The name of the property.
**value** - The Integer value, 88.  It can also be a string or float, as it will be cast to int.

#### Example

Suppose you want to add a new Integer property to an entity.  
The uuid (in string form) is 'a38f34bc-769f-4bff-9815-1c28222da555'.
The name of the new property will be 'myNewProperty'.
The value will be 88

	'python
Graph.api.addEntityIntegerProperty('a38f34bc-769f-4bff-9815-1c28222da555', 'myNewProperty', '88')
	'
 or 
	'python
Graph.api.addEntityIntegerProperty('a38f34bc-769f-4bff-9815-1c28222da555', 'myNewProperty', 88)
	'





## addEntityLink

Adds/Updates a String value to an entity.  If the property does not yet exist on the entity, then it will be created, with the new value.  If the property already exists, it will be updated.  The value will be cast to a String when added.  All links are directional and have a source + target entity combination.  Traverse queries can choose to ignore directionality.

#### Parameters
1. **entityUUID1** - The entity that the link originates from.
2. **entityUUID2** - The target entity.
3. **linkAttributes** (default = {} ) - A python dictionary, containing the values to be added to the link.  The keys will become the attribute names and the values will be the attribute values.  They are all handled as strings.
4. **linkType** (default = 0) - The type of link to be created.  There are two possible codes for these link types; 0 (atomic) and 1 (subatomic).  Subatomic links can only be traversed from within the same cluster.


#### Example

Suppose you want to add a link between two entities.  
- The uuid (in string form) of the source entity (where the link is originating from) is 'a38f34bc-769f-4bff-9815-1c28222da555'.
- The uuid (in string form) of the target entity (where the link is originating from) is 'b49f34bc-769f-4bff-9815-1c28222da555'.
- There are no link attributes.
- The link type is atomic.

	'python
Graph.api.addEntityLink('a38f34bc-769f-4bff-9815-1c28222da555', 'b49f34bc-769f-4bff-9815-1c28222da555')
	'

In the second example, we'll add link attributes.
- The uuid (in string form) of the source entity (where the link is originating from) is 'a38f34bc-769f-4bff-9815-1c28222da555'.
- The uuid (in string form) of the target entity (where the link is originating from) is 'b49f34bc-769f-4bff-9815-1c28222da555'.
- There are two link attributes.  "textValue" = "Hello World" and "attribCount" = 2
- The link type is still atomic.

	'python
Graph.api.addEntityLink('a38f34bc-769f-4bff-9815-1c28222da555', 'b49f34bc-769f-4bff-9815-1c28222da555', {"textValue" : "Hello World", "attribCount" : 2})
	'

In the third example, we'll add make the link subatomic.
- The uuid (in string form) of the source entity (where the link is originating from) is 'a38f34bc-769f-4bff-9815-1c28222da555'.
- The uuid (in string form) of the target entity (where the link is originating from) is 'b49f34bc-769f-4bff-9815-1c28222da555'.
- There are two link attributes.  "textValue" = "Hello World" and "attribCount" = 2
- The link type is subatomic.

	'python
Graph.api.addEntityLink('a38f34bc-769f-4bff-9815-1c28222da555', 'b49f34bc-769f-4bff-9815-1c28222da555', {"textValue" : "Hello World", "attribCount" : 2}, 1)
	'
 





## addEntityStringProperty

Adds/Updates a String value to an entity.  If the property does not yet exist on the entity, then it will be created, with the new value.  If the property already exists, it will be updated.  The value will be cast to a String when added.

#### Parameters
**entityUUID** - The UUID (as a string) of the graph entity that you want to add the new property to. 
**name** - The name of the property.
**value** - The String value, 88.  It can also be a string or float, as it will be cast to int.

#### Example

Suppose you want to add a new String property to an entity.  
The uuid (in string form) is 'a38f34bc-769f-4bff-9815-1c28222da555'.
The name of the new property will be 'myNewProperty'.
The value will be 'Hello World'

	'python
Graph.api.addEntityStringProperty('a38f34bc-769f-4bff-9815-1c28222da555', 'myNewProperty', 'Hello World')
	'






## createEntity

Creates a new, blank entity of type Graphyne.Generic.

#### Parameters
none

#### Returns
The uuid (as string) of the newly created entity.


#### Example


	'python
Graph.api.createEntity()
	'





## createEntityFromMeme

Creates a new, blank entity of type Graphyne.Generic.

#### Parameters
none

#### Returns
The uuid (as string) of the newly created entity.


#### Example

If you wanted to create an Entity of type Graphyne.Generic (the type of Entity created by createEntity()), but explicitly declare the meme.

	'python
Graph.api.createEntityFromMeme("Graphyne.Generic")
	'




## getCluster

Initiates a traverse from a given entity  and returns a subgraph.  This subgraph can be limited to specific link types (atomic or subatomic) and to specific traverse parameters.   Because of this traverse parameter filtering, these subgraph fragments are referred to as clusters.  value to an entity.  If the property does not yet exist on the entity, then it will be created, with the new value.  If the property already exists, it will be updated.  The value will be cast to a Decimal when added.

#### Parameters
**entityUUID** - The UUID (as a string) of the graph entity that you want to add the new property to. 
**name** - The name of the property.
**value** - The Decimal value, 88.8.  It can also be a string, or float.  It will be cast to a Decimal, if it is not already.

#### Example

Suppose you want to add a new Decimal property to an entity.  
The uuid (in string form) is 'a38f34bc-769f-4bff-9815-1c28222da555'.
The name of the new property will be 'myNewProperty'.
The value will be 88.8

	'python
Graph.api.addEntityDecimalProperty('a38f34bc-769f-4bff-9815-1c28222da555', 'myNewProperty', '88.8')
	'
or
	'python
Graph.api.addEntityDecimalProperty('a38f34bc-769f-4bff-9815-1c28222da555', 'myNewProperty', 88.8)
	'


