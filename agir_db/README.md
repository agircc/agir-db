# AGIR Database

This document provides an overview of the database schema for the AGIR platform.

## Table of Contents
- [Overview](#overview)
- [User Management](#user-management)
- [Scenario System](#scenario-system)
- [Task Management](#task-management)
- [Chat System](#chat-system)
- [Memory System](#memory-system)
- [Custom Fields](#custom-fields)
- [Entity Relationship Diagrams](#entity-relationship-diagrams)

## Overview

The AGIR database is organized into several interconnected systems:

1. **User Management**: Handles user accounts, verification, and capabilities
2. **Scenario System**: Manages scenarios, states, transitions, roles, episodes, and steps
3. **Task Management**: Tracks tasks, comments, and attachments
4. **Chat System**: Facilitates conversations between users
5. **Memory System**: Stores user memories for personalized experiences
6. **Custom Fields**: Allows for extensible user properties

## User Management

| Table | Description |
|-------|-------------|
| `users` | Stores user account information including authentication details, personal info, and preferences |
| `verification_codes` | Manages email verification codes for account verification |
| `user_capability` | Tracks user capabilities and permissions |

## Scenario System

| Table | Description |
|-------|-------------|
| `scenarios` | Defines simulation scenarios with metadata and structure |
| `states` | Represents states within a scenario (nodes in the scenario graph) |
| `state_transitions` | Defines valid transitions between states |
| `agent_roles` | Defines roles that agents can assume in a scenario |
| `state_roles` | Maps which roles can participate in which states |
| `episodes` | Represents instances of scenarios that are being executed |
| `steps` | Records individual steps taken within an episode |
| `agent_assignments` | Maps users to agent roles for specific episodes |

## Task Management

| Table | Description |
|-------|-------------|
| `tasks` | Stores tasks with title, description, status, priority, etc. |
| `task_comments` | Stores comments on tasks |
| `task_attachments` | Manages files attached to tasks |

## Chat System

| Table | Description |
|-------|-------------|
| `chat_conversations` | Represents chat conversations between users |
| `chat_messages` | Stores individual messages within conversations |
| `chat_participants` | Tracks participants in conversations |

## Memory System

| Table | Description |
|-------|-------------|
| `user_memories` | Stores persistent memories about users for personalized experiences |

## Custom Fields

| Table | Description |
|-------|-------------|
| `custom_fields` | Provides a flexible way to add custom attributes to users |

## Entity Relationship Diagrams

### User Management

```mermaid
erDiagram
    User {
        uuid id PK
        string email
        string username
        string first_name
        string last_name
        string avatar
        datetime birth_date
        string gender
        boolean is_active
        datetime created_at
        uuid created_by FK
    }
    
    VerificationCode {
        uuid id PK
        uuid user_id FK
        string code
        datetime expires_at
    }
    
    UserCapability {
        uuid id PK
        uuid user_id FK
        string capability
        float score
        datetime created_at
    }
    
    User ||--o{ VerificationCode : "has"
    User ||--o{ UserCapability : "has"
    User ||--o{ User : "creates"
```

### Scenario System

```mermaid
erDiagram
    Scenario {
        uuid id PK
        string name
        string description
        string learner_role
        uuid created_by FK
        datetime created_at
    }
    
    State {
        uuid id PK
        uuid scenario_id FK
        string name
        string description
        string node_type
        datetime created_at
    }
    
    StateTransition {
        uuid id PK
        uuid scenario_id FK
        uuid from_state_id FK
        uuid to_state_id FK
        string condition
        datetime created_at
    }
    
    AgentRole {
        uuid id PK
        uuid scenario_id FK
        string name
        string description
        string model
    }
    
    StateRole {
        uuid state_id PK,FK
        uuid agent_role_id PK,FK
        datetime created_at
    }
    
    Episode {
        uuid id PK
        uuid scenario_id FK
        uuid current_state_id FK
        uuid initiator_id FK
        string status
        json config
        string evolution
        datetime created_at
    }
    
    Step {
        uuid id PK
        uuid episode_id FK
        uuid state_id FK
        uuid user_id FK
        string action
        string generated_text
        datetime created_at
    }
    
    AgentAssignment {
        uuid id PK
        uuid user_id FK
        uuid role_id FK
        uuid episode_id FK
        string description
        datetime created_at
    }
    
    Scenario ||--|{ State : "contains"
    Scenario ||--|{ StateTransition : "defines"
    Scenario ||--|{ AgentRole : "has"
    State ||--|{ StateRole : "has"
    AgentRole ||--|{ StateRole : "participates in"
    State ||--o{ StateTransition : "source of"
    State ||--o{ StateTransition : "target of"
    Scenario ||--o{ Episode : "instantiated as"
    State ||--o{ Episode : "current state"
    Episode ||--|{ Step : "contains"
    Episode ||--|{ AgentAssignment : "has"
    AgentRole ||--|{ AgentAssignment : "assigned to"
    User ||--|{ AgentAssignment : "participates as"
    User ||--|{ Episode : "initiates"
    State ||--|{ Step : "references"
    User ||--|{ Step : "takes"
```

### Task Management

```mermaid
erDiagram
    Task {
        uuid id PK
        string title
        string description
        string status
        string priority
        uuid created_by FK
        uuid assigned_to FK
        datetime created_at
    }
    
    TaskComment {
        uuid id PK
        uuid task_id FK
        uuid user_id FK
        string content
        datetime created_at
    }
    
    TaskAttachment {
        uuid id PK
        uuid task_id FK
        uuid user_id FK
        string filename
        string url
        datetime created_at
    }
    
    User ||--o{ Task : "creates"
    User ||--o{ Task : "assigned to"
    Task ||--o{ TaskComment : "has"
    Task ||--o{ TaskAttachment : "has"
    User ||--o{ TaskComment : "creates"
    User ||--o{ TaskAttachment : "uploads"
```

### Chat System

```mermaid
erDiagram
    ChatConversation {
        uuid id PK
        string title
        uuid created_by FK
        datetime created_at
    }
    
    ChatMessage {
        uuid id PK
        uuid conversation_id FK
        uuid sender_id FK
        string content
        string status
        datetime created_at
    }
    
    ChatParticipant {
        uuid id PK
        uuid conversation_id FK
        uuid user_id FK
        datetime last_read_at
        datetime created_at
    }
    
    User ||--o{ ChatConversation : "creates"
    User ||--o{ ChatMessage : "sends"
    User ||--o{ ChatParticipant : "participates as"
    ChatConversation ||--|{ ChatMessage : "contains"
    ChatConversation ||--|{ ChatParticipant : "has"
```

### Memory System

```mermaid
erDiagram
    UserMemory {
        uuid id PK
        uuid user_id FK
        string content
        string source
        float relevance
        datetime created_at
    }
    
    User ||--o{ UserMemory : "has"
```

### Custom Fields

```mermaid
erDiagram
    CustomField {
        uuid id PK
        uuid user_id FK
        string field_name
        string field_value
        datetime created_at
    }
    
    User ||--o{ CustomField : "has"
```

## Key Relationships

1. **User → AgentAssignment → AgentRole**: Users are assigned to agent roles within episodes
2. **Scenario → State → StateTransition**: Scenarios contain states connected by transitions
3. **Scenario → Episode → Step**: Episodes are instances of scenarios with sequential steps
4. **State → StateRole ← AgentRole**: States define which agent roles can participate
5. **User → Task**: Users create and are assigned tasks