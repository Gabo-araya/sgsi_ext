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
            + code: char
            + documented_controls: Control[]
        }
        together {
            class DocumentVersion {
                + id: int
                + document: Document
                + version: int
                + file: file
                + shasum: char
                + comment: text
                + is_approved: bool
                + approval_evidence: Evidence
                + approved_at: datetime
                + approved_by: User
                + verification_code: char
                + read_by: User[]
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
        + category: ControlCategory | None
        + title: char
        + description: text
    }
    class ControlCategory {
        + id: int
        + name: char
    }
    class Evidence {
        + id: int
        + file: file
        + url: URL
        + shasum: char
    }
}

class Users.User {
    ...
}

Documents.Control <--> Documents.Document
Documents.Control -> Documents.ControlCategory
Documents.DocumentVersion -up-> Documents.Document
Documents.DocumentVersion <-- Documents.DocumentVersionReadByUser
Documents.Evidence <- Documents.DocumentVersion
Documents.DocumentVersionReadByUser -> Users.User
```

Then we have the assets module

```plantuml
package Assets {
    class Asset {
        + id: int
        + owner: User
        + code: char
        + name: char
        + description: text
        + asset_type: AssetType
        + criticality: CriticalityChoices
        + classification: ClassificationChoices
        + is_archived: bool
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

Assets.Asset -right> Users.User
Assets.Asset -left> Assets.AssetType
Assets.Asset --> Assets.CriticalityChoices
Assets.Asset --> Assets.ClassificationChoices
```

And the risk module

```plantuml
package Risks {
    class Risk {
        + id: int
        + assets: Asset[]
        + controls: Control[]
        + title: char
        + description: text
        + responsible: User
        + severity: SeverityChoices
        + likelihood: LikelihoodChoices
        + treatment: TreatmentChoices
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

Risks.Risk <-up-> Assets.Asset
Risks.Risk <-up-> Documents.Control
Risks.Risk -left> Risks.LikelihoodChoices
Risks.Risk --> Risks.TreatmentChoices
Risks.Risk --> Risks.SeverityChoices
Risks.Risk -> Risks.Risk
```

And lastly the processes module

```plantuml
package Processes {
    class Process {
        + id: int
        + name: char
    }
    class ProcessVersion {
        + id: int
        + process: Process
        + version: int
        + defined_in: Document
        + controls: Control[]
        + comment_label: char
        + recurrency: TimeFrameChoices | None
        + is_published: bool
        + published_at: datetime
        + published_by: User
    }
    class ProcessInstance {
        + id: int
        + process_version: ProcessVersion
        + comment: text
        + is_completed: bool
        + completed_at: datetime
    }
    class ProcessActivity {
        + id: int
        + title: char
        + process_version: ProcessVersion
        + order: int
        + description: text
        + assignee_groups: Group[]
        + email_to_notify: email
    }
    class ProcessActivityInstance {
        + id: int
        + process_instance: ProcessInstance
        + activity: ProcessActivity
        + assignee: User
        + is_completed: bool
        + completed_at: datetime
        + evidence: Evidence
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

class Documents.Document {
    ...
}

class Documents.Control {
    ...
}

class Documents.Evidence {
    ...
}

class Users.User {
    ...
}

class Users.Group {
    ...
}


Processes.ProcessVersion --> Users.User
Processes.ProcessVersion -> Documents.Document
Processes.ProcessVersion <---> Documents.Control
Processes.ProcessVersion --> Processes.TimeFrameChoices
Processes.ProcessInstance -> Processes.ProcessVersion
Processes.ProcessActivity --> Processes.ProcessVersion
Processes.ProcessActivity -> Users.Group
Processes.ProcessVersion --> Processes.Process
Processes.ProcessActivityInstance -> Processes.ProcessActivity
Processes.ProcessActivityInstance -> Users.User
Processes.ProcessActivityInstance -> Documents.Evidence
Processes.ProcessActivityInstance --> Processes.ProcessInstance
```

```plantuml
package Users {
    class User {
        + id: int
        + email: email
        + password: char
        + first_name: char
        + last_name: char
        + is_active: bool
        + is_staff: bool
        + is_superuser: bool
        + date_joined: datetime
        + groups: Group[]
        + user_permissions: Permission[]
    }
}

package Auth {
    class Group {
        + id: int
        + name: char
        + permissions: Permission[]
    }
    class Permission {
        + id: int
        + content_type: ContentType
        + name: char
        + codename: char
    }
}

Users.User --> Auth.Group
Auth.Group -> Auth.Permission
Users.User -> Auth.Permission
```
