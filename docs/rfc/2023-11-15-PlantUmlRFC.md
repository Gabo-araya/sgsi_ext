# Using PlantUML for Documentation

## Context

When documenting big changes in a project often diagrams become really useful for devs, especially diagrams that are able to succinctly demonstrate the infrastructure and modelling of the project.

Since for our documentation we'll take a plain text and close to code approach we need a solution for making easy to understand and easy to make infrastructure and modelling diagrams.

## Proposed Solution

For this we propose the use of [PlantUML](https://plantuml.com/en-dark/), as per its documentation:

> "PlantUML is a versatile component that enables swift and straightforward diagram creation"

This component uses a simple Markdown lang tag and allows to define a diagram using plain text, then we can use a PlantUML server to dynamically render these diagrams in VSCode, Obsidian, WikiJS, or any other markdown visualizer with PlantUML support.

There are many upsides to this:

1. Diagrams are represented in plain text
2. All diagrams would follow a standard design by default

There are a few downsides:

1. A PlantUML server is needed to easily see and edit the diagrams
2. It's really hard to make client-facing diagrams
3. Diagrams require some level of technical knowledge to be understood. 

As for the first downside we have added a plantuml server to the docker compose configuration which runs in http://localhost:8080/plantuml, we also added the PlantUML extension for VSCode, now if you open the Markdown preview of any documentation file you will see a hot-reloaded compilation of the diagram.

There is no real way to deal with the second downside without using tools that aren't plain text, therefore any client facing diagrams should use other tools.


### Infrastructure

The [PlantUML Standard Library](https://plantuml.com/stdlib) includes an Amazon AWS icon library, which has [its own documentation](https://github.com/awslabs/aws-icons-for-plantuml). Here is a simple example:

```plantuml
!include <awslib/AWSCommon>

!include <awslib/AWSSimplified>
!include <awslib/General/Users>
!include <awslib/ApplicationIntegration/APIGateway>
!include <awslib/SecurityIdentityCompliance/Cognito>
!include <awslib/Compute/Lambda>
!include <awslib/Database/DynamoDB>

left to right direction

Users(sources, "Events", "millions of users")
APIGateway(votingAPI, "Voting API", "user votes")
Cognito(userAuth, "User Authentication", "jwt to submit votes")
Lambda(generateToken, "User Credentials", "return jwt")
Lambda(recordVote, "Record Vote", "enter or update vote per user")
DynamoDB(voteDb, "Vote Database", "one entry per user")

sources --> userAuth
sources --> votingAPI
userAuth <--> generateToken
votingAPI --> recordVote
recordVote --> voteDb
```

### Modelling

PlantUML supports [Class Diagrams](https://plantuml.com/en-dark/class-diagram).

Interfaces an inheritance:

```plantuml
abstract class AbstractList
abstract AbstractCollection
interface List
interface Collection

List <|-- AbstractList
Collection <|-- AbstractCollection

Collection <|- List
AbstractCollection <|- AbstractList
AbstractList <|-- ArrayList

class ArrayList {
  Object[] elementData
  size()
}
```

Class relationships:

```plantuml
Class01 <|-- Class02
Class03 *-- Class04
Class05 o-- Class06
Class07 .. Class08
Class09 -- Class10
```

Labels and directions:

```plantuml
class Car

Driver - Car : drives >
Car *- Wheel : have 4 >
Car -- Person : < owns
```
