
Graphyne 1.2 introduces Conditions.  The Condition family of Metamemes gives the designer a potentially script free way of creating runtime value checks.  At runtime, these checks are made via an evaluateEntity() call on the Condition entity.

The metamemes involved in creating Conditions follow a fairly complex pattern and it is not entirely true that hand editing the xml to create conditions this way is faster or easier than just writing [SES scripts][1] (provided the designer is proficient in Python), but they do enable graphical editors to create easy and usable workflows, while hiding the plumbing behind the scenes.  So if you want to hand edit conditions as an alternative to scripting, or are designing an editor, then this documentation will walk you through creating conditions.

# Overview

Conditions are defined in a file in the Graphyne directory, alongside the Graph.py module.  This directory is mounted as a repository if the [useDefaultSchema][2] option is set to True on graph initialization.  Conditions always have a single, public facing entity of type Graphyne.Condition.Condition.  At runtime, this entity has an active evaluate event script, as if it had an SES script attached and this event script returns True or False, depending on the results of the conditional test.  Graphyne.Condition.Condition is a switch and has a single child entity of one of four types; ConditionString, ConditionNumeric, ConditionScript and ConditionSet and each of these in turn have their own child structures.  Having a shared parent Meme allows designers to have a single face to the world, Condition, regardless of the underlying structure.

It is a best practice to [define the links within Condition memes as subatomic][3].  This [keeps the subgraph private in searches not explicitly for subatomic links][4] and shows a single “spokesperson” Condition entity.


## Argument

All Condition types except the ConditionScript use an Argument metameme.  As it is critical to Condition behavior, we’ll discuss it first.  At its core, a Condition determines whether something compares against a  rule is true or false.  The Argument defines what is being compared.  Arguments can be designed to look for a particular key in the runtimeVariables parameter evaluateEntity() call, they can be designed to look for a particular property on an entity, or they can be designed to look for properties on a pair of entities; known as the subject and object respectively.  

The Argument metameme defined no properties and has a single member.  It is a switch and Argument memes will have one of three types of memes to govern these rules:
- **SimpleArgument** - Defines the key to look for in runtimeVariables in the evaluateEntity() call.
- **AgentAttributeArgument** - Defines the property on the subject entity to be tested.
- **MultiAgentAttributeArgument** - Defines the properties on the subject and object entities to be tested.


#### SimpleArgument

SimlpleArgument is used when you want to dynamically compare an arbitrary value against the condition rule at runtime.  The argument value will be supplied in the evaluateEntity()  runtimeVariables parameter.  Argument memes using SimpleArgument have a very simple structure.  The *SimpleArgument* meme defines a single string property, **ArgumentTag**.  When evaluateEntity() is called, this key will be looked for and the value will be compared to the rules defined in the exception.  

![][image-1]

In the example code, below, we define an Argument meme, called ExampleArgument and it has a SimpleArgument child called ExampleSimpleArgument .  The ArgumentTag is “Animal”.  

xxx

When we want to test the parent condition entity (presuming that the uuid in string form is entityID) at runtime, we would execute the following:

xxx


#### AgentAttributeArgument

Argument memes using AgentAttributeArgument also have a very simple structure.  The * AgentAttributeArgument* meme defines a single string property, **SubjectArgumentPath**, which defines the property that will be used from the subject.  When evaluateEntity() is called, this property value is read from the subject and its value will be compared to the rules defined in the condition.  

![][image-2]

In the example code, below, we define an Argument meme, called ExampleArgument and it has an AgentAttributeArgument child called Example AgentAttributeArgument .  The SubjectArgumentPath is “Animal”.  

xxx

When we want to test the parent condition entity (presuming that the uuid in string form is entityID) with subject uuid (in string form) subjectID at runtime, we would execute the following:

xxx


#### MultiAgentAttributeArgument

Argument memes using MultiAgentAttributeArgument also have a very simple structure.  The * MultiAgentAttributeArgument* meme defines two string properties, **SubjectArgumentPath** and **ObjectArgumentPath**, which defines the properties that will be used from the subject and object respectively.  When evaluateEntity() is called, these property values are read from the subject and object and their values will be compared to the rules defined in the condition.

![][image-3]

xxx

When we want to test the parent condition entity (presuming that the uuid in string form is entityID) with subject uuid (in string form) subjectID and object uuid (in string form) objectID at runtime, we would execute the following:

xxx  


## ConditionString

ConditionString is about evaluating strings.  It is generally composed of:
- An Argument member.
- One or more ValueString members.  Each value string is composed of a single property.  The name of the property should be “Value” and the value can be whatever is being tested for.
- A MemeProperty element with the name StringOperator, which will govern the type of test.  The value of this operator can be one of the following types:
Equal
NotEqual
Longer
Shorter
SameLength
NotSameLength
StartsWith
EndsWith

The Condition meme (and its descendants) below demonstrates a StringCondition element that creates a test for whether a passed string ends with “s” or “S”.  For the sake of simplicity, we are re-using the SimpleArgument from above.

![][image-4]


## ConditionNumeric

ConditionString is about evaluating numbers.  It is generally composed of:
- An Argument member.
- One or more Graphyne.Numeric.Formula members.  Each formula is composed of a single property.  The name of the property should be “ValueNumeric” and the value can be whatever is being tested for.
- A MemeProperty element with the name NumericOperator, which will govern the type of test.  The value of this operator can be one of the following types:
Equal
NotEqual
GreaterThan
LessThan
EqualOrGreaterThan
EqualOrLessThan

The Condition meme (and its descendants) below demonstrates a ConditionNumeric element that creates a test for whether a passed string ends with “s” or “S”.  For the sake of simplicity, we are re-using the SimpleArgument from above.

![][image-5]

## ConditionScript

This is the simplest kind of condition of all, from a meme perspective.  It contains a single state event script member.  That’s it!  ConditionString entities behave a bit differently from most SES parents.  During meme bootstrapping, the evaluate() script is installed directly onto the Condition, which is the grandparent of the SES entity, whereas normally it would be installed on the parent.

![][image-6]


## ConditionSet

This is a three part cluster.  The ConditionSet is a container for multiple conditions.  It is generally composed of:
A ConditionSetChildren member, which in turns holds one or more Conditions.    A single property.  The name of the property should be “SetOperator” and the value of this operator can be one of the following types:
AND
OR
NOT

The nested Condition elements are evaluated and if the combination of their values and the SetOperator match, then it is true.

![][image-7]

[1]:	https://github.com/davidhstocker/Graphyne#memetic-scripting
[2]:	https://github.com/davidhstocker/Graphyne#usedefaultschema
[3]:	https://github.com/davidhstocker/Graphyne#links
[4]:	https://github.com/davidhstocker/Graphyne#subgraphs-and-link-type

[image-1]:	https://raw.githubusercontent.com/davidhstocker/Graphyne/master/Docs/Images/ConditonsArgumentSimple.png
[image-2]:	https://raw.githubusercontent.com/davidhstocker/Graphyne/master/Docs/Images/ConditonsArgumentAAA.png
[image-3]:	https://raw.githubusercontent.com/davidhstocker/Graphyne/master/Docs/Images/ConditonsArgumentMAAA.png
[image-4]:	https://raw.githubusercontent.com/davidhstocker/Graphyne/master/Docs/Images/Conditions1.png
[image-5]:	https://raw.githubusercontent.com/davidhstocker/Graphyne/master/Docs/Images/Conditions2.png
[image-6]:	https://raw.githubusercontent.com/davidhstocker/Graphyne/master/Docs/Images/ConditonsScript.png
[image-7]:	https://raw.githubusercontent.com/davidhstocker/Graphyne/master/Docs/Images/ConditonsSet.png