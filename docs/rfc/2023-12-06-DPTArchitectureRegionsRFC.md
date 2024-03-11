# About DPT Architecture - Regions

## Context

Most Magnet clients are based in the Republic of Chile, and some of our requirements may require to store geographical information about users or customers such as region or commune where they're located. Storing them as a plain text field is prone to inconsistencies and not recommended.

## Proposed solution

A pre-populated database of regions and communes of Chile. Also, a simple JSON endpoint allows to search for communes
by name or region ID.

## Modeling

```plantuml
class regions.models.Region {
  name: CharField
  short_name: CharField
  order: PositiveIntegerField
  importance: PositiveIntegerField
}

class regions.models.Commune {
  region: ForeignKey
  name: CharField
}

base.models.BaseModel <|-- regions.models.Region
base.models.BaseModel <|-- regions.models.Commune
regions.models.Region *- regions.models.Commune

```
