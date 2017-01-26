
When an event script is called, it is always called with two positional parameters.  Position 0 holds the UUID of the entity and position one holds a dictionary with the event specific runtime parameters.  Below is an enumeration of the runtime parameter keys for each event.  


---- 
# execute

## When Triggered
Whenever [evaluateEntity()][1] is called for a given entity.  This is the only event that is manually trigged; as opposed to being automatically triggered by the graph framework.

## Parameter Keys
**runtimeVariables** = A dictionary containing any custom parameter information that the designer wishes to pass to the ex=valuate script.
**actionID** = A uuid (as a string) for a calling entity.  E.g. if and event script on entity A is triggering evaluateEntity() for entity B, then entity A is the action.  There is no requirement that the event script do anything with this parameter and it defaults to None, but it is there if you need it.
**subjectID** = A uuid (as a string) for an entity that is the subject of the script.  The subject may or may not be the entity for which the event is running.  As with actionID, there is no requirement that the event script do anything with this parameter and it defaults to None, but it is there if you need it.  [This parameter is used when evaluating agent (and multi-agent) attribute conditions][2].
**objectID** = A uuid (as a string) for an entity that is the subject of the script.  The subject may or may not be the entity for which the event is running.  As with actionID, there is no requirement that the event script do anything with this parameter and it defaults to None, but it is there if you need it.  [This parameter is used when evaluating multi-agent attribute conditions][2].


---- 
# initialize

## When Triggered
This event is called during entity creation, at the very end of the initialization phase.  The entity’s properties and links have been put into place and are available.

## Parameter Keys
This event is called with an empty rumtime parameter dictionary.


---- 
# linkAdd

## When Triggered
Whenever and entity with a defined linkAdd event is linked to another entity, then this event is triggered.  If both entities have a defined linkAdd event, then it will be triggered for both entities.  In the link events, the uuid at position 0 might be either the source or target uuid and she developer can’t be certain which it is.  The uuids passed in the runtime parameters should be used instead.  

## Parameter Keys
**sourceEntityID** - The uuid (as a string) of the entity at the originating position in the link.
**targetEntityID** - The uuid (as a string) of the entity at the terminal position in the link.
**linkAttributes** - A dictionary containing the link attributes.  The attribute names are the keys and the attribute values are the corresponding values.  


---- 
# linkRemove

## When Triggered
Whenever and entity with a defined linkRemove event is de-linked from another entity, then this event is triggered.  If both entities have a defined linkRemove event, then it will be triggered for both entities.  In the link events, the uuid at position 0 might be either the source or target uuid and she developer can’t be certain which it is.  The uuids passed in the runtime parameters should be used instead.  

## Parameter Keys
**sourceEntityID** - The uuid (as a string) of the entity at the originating position in the link.
**targetEntityID** - The uuid (as a string) of the entity at the terminal position in the link.


---- 

# propertyChanged

## When Triggered
Whenever the assigned property’s value is altered, including when it is reverted to the default state, set in the model.  This event is assigned to a specific property in the schema and therefore cannot be triggered on dynamically added properties at runtime.  This event is not called during entity initialization and is only called when a property value is changed after initialization.  

## Parameter Keys
**oldValue** - The prior value of the property, as a string.
**newValue** - The new value applied to the property, again as a string.


---- 
# terminate

## When Triggered
This event is called during entity deletion, before any steps to actually start removing the entity from the graph have been made.  The entity’s properties and links are still available when this event is triggered.  The entity will be unlinked from its link counterparts and removed from the graph as soon as this script event is finished executing.

## Parameter Keys
This event is called with an empty rumtime parameter dictionary.



[1]:	https://github.com/davidhstocker/Graphyne/blob/master/Docs/Graph%20API%20Methods.md#evaluateentity
[2]:	https://github.com/davidhstocker/Graphyne/blob/master/Docs/Conditions.md#argument