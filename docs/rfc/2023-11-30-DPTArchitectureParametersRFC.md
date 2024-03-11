# About DPT Architecture - Parameters

## Context

Some applications require to be configured in runtime with zero downtime. This eliminates any chance of using environment variables or modifying the settings module. Therefore, a system that allows for changing configuration on the fly is highly desirable.

## Proposed solution

A parameters system that is stored on the database and cached for fast access.

A statically defined parameter definition list defines the available parameters, their data types, default values and special validation logic. Validation is implemented using standard functions.

Two management commands, `showparameters` an `setparameter` allow to view and set parameters without having to use the Django admin. This is useful in case the application is down.

## Modeling

```plantuml
enum parameters.enums.ParameterKind {
  INT
  FLOAT
  TIME
  DATE
  JSON
  URL
  HOSTNAME
  IP_NETWORK
  HOSTNAME_LIST
  IP_NETWORK_LIST
  BOOL
  STR
}

class parameters.models.Parameter {
  raw_value: TextField
  name: CharField
  kind: CharField
  cache_seconds: PositiveIntegerField
  __
  clean()
  save()
  store_in_cache()
  run_validators(value)
  .. Properties ..
  value: Any
  .. Class methods ..
  process_value(kind, raw_value)
  cache_key(name)
  value_for(name)
  process_cached_parameter(cached_parameter)
  create_all_parameters()
  create_parameter(name)
  __ Private methods __
  _get_value()
  _set_value(value)
}

class parameters.definitions.ParameterDefinition <<namedtuple>> {
  name: str
  default: Any
  kind: str
  verbose_name: str
  validators: tuple[callable]
}

class parameters.definitions.ParameterDefinitionList {
  definitions: list[ParameterDefinition]
 .. Class methods ..
 get_definition(name)
}

parameters.definitions.ParameterDefinitionList o-- parameters.definitions.ParameterDefinition

base.models.BaseModel <|-- parameters.models.Parameter
parameters.enums.ParameterKind - parameters.models.Parameter

```
