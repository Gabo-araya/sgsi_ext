# Initial modelling

## Context

Magnet SGSI is a new project and the general idea for it is known but the modelling details are missing.

## Proposed Solution

The proposed solution is making an initial modelling of the application so errors can be discovered earlier and check that all features are taken into consideration.

### Infrastructure (Does not apply)

### Modelling

The modelling can be split into each module, starting with documents module, we have

```plantuml
package Documents {
    together {
        class Document {
            + id: int
            + title: char
            + description: text
        }
        together {
            class DocumentVersion {
                + id: int
                + document: Document
                + version: int
                + file: file
                + shasum: char
                + is_approved: bool
            }
            class DocumentVersionReadByUser {
                + id: int
                + document_version: DocumentVersion
                + user: User
            }
        }
    }
    class Control {
        + id: int
        + category: ControlCategory
        + title: char
        + description: text
        + document: Document
    }
    class ControlGuidingText {
        + id: int
        + control: Control
        + text: text
    }
    class ControlCategory {
        + id: int
        + name: char
    }
    class Evidence {
        + id: int
        + document_version: DocumentVersion
        + process_activity_instance: ProcessActivityInstance
        + file: file
        + shasum: char
    }
}

class Processes.ProcessActivityInstance {
    ...
}

class Users.User {
    ...
}

Documents.Control --* Documents.Document
Documents.Control -* Documents.ControlCategory
Documents.Control --* Documents.ControlGuidingText
Documents.DocumentVersion -up-* Documents.Document
Documents.DocumentVersion --* Documents.DocumentVersionReadByUser
Documents.Evidence -up-* Processes.ProcessActivityInstance
Documents.Evidence -* Documents.DocumentVersion
Documents.DocumentVersionReadByUser -* Users.User
```

Then we have the assets module

```plantuml
package Assets {
    class Asset {
        + id: int
        + owner: User
        + name: char
        + description: text
        + asset_type: AssetType
        + criticality: CriticalityChoices
        + classification: ClassificationChoices
    }
    class AssetType {
        + id: int
        + name: char
        + description: text
    }
    enum CriticalityChoices {
        VERY_LOW
        LOW
        MEDIUM
        HIGH
        VERY_HIGH
    }
    enum ClassificationChoices {
        PUBLIC
        INTERNAL
        PRIVATE
    }
}
class Users.User {
    ...
}

Assets.Asset -right* Users.User
Assets.Asset -left* Assets.AssetType
Assets.Asset --* Assets.CriticalityChoices
Assets.Asset --* Assets.ClassificationChoices
```

And the risk module

```plantuml
package Risks {
    class Risk {
        + id: int
        + asset: Asset
        + control: Control
        + title: char
        + description: text
        + responsible: User
        + severity: SeverityChoices
        + likelihood: LikelihoodChoices
        + treatment: TreatmentChoices
        + process: Process
        + residual_risk: Risk
    }
    enum LikelihoodChoices {
        VERY_LOW
        LOW
        MEDIUM
        HIGH
        VERY_HIGH
    }
    enum SeverityChoices {
        VERY_LOW
        LOW
        MEDIUM
        HIGH
        VERY_HIGH
    }
    enum TreatmentChoices {
        MITIGATE
        TRANSFER
        ACCEPT
        ELIMINATE
    }
}

class Assets.Asset {
    ...
}

class Documents.Control {
    ...
}

class Processes.Process {
    ...
}

Risks.Risk -up-* Assets.Asset
Risks.Risk -up-* Documents.Control
Risks.Risk -up-* Processes.Process
Risks.Risk -left* Risks.LikelihoodChoices
Risks.Risk --* Risks.TreatmentChoices
Risks.Risk --* Risks.SeverityChoices
Risks.Risk -* Risks.Risk
```

And lastly the processes module

```plantuml
package Processes {
    class ProcessDefinition {
        + id: int
        + name: char
        + control: Control
        + recurrency: TimeFrameChoices | None
    }
    class Process {
        + id: int
        + process_definition: ProcessDefinition
        + name: char
        + control: Control
        + completed: bool
        + completed_at: datetime
    }
    class ProcessActivityDefinition {
        + id: int
        + process_definition: ProcessDefinition
        + order: int
        + description: text
        + asignee: User
        + asignee_group: Group
    }
    class ProcessActivityInstance {
        + id: int
        + process: Process
        + activity_definition: ActivityDefinition
        + order: int
        + description: text
        + asignee: User
        + asignee_group: Group
        + completed: bool
        + completed_at: datetime
    }
    enum TimeFrameChoices {
        DAILY
        WEEKLY
        MONTHLY
        QUARTERLY
        SEMIANNUALLY
        ANNUALLY
    }
}

class Documents.Control {
    ...
}

class Documents.DocumentVersion {
    ...
}


Processes.ProcessDefinition -up-* Documents.Control
Processes.ProcessDefinition -left* Processes.TimeFrameChoices
Processes.Process -up-* Documents.DocumentVersion
Processes.Process -left* Processes.ProcessDefinition
Processes.ProcessActivityDefinition --* Processes.ProcessDefinition
Processes.ProcessActivityInstance -* Processes.ProcessActivityDefinition
Processes.ProcessActivityInstance -up-* Processes.Process
```
