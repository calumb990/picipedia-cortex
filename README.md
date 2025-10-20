# Picipedia Cortex
The Cortex Kubeflow pipeline for the Picipedia project, containing an incremental CNN.

## Architecture
```mermaid
architecture-beta
    service mobile(mdi:cellphone)[Mobile App]
    service desktop(mdi:desktop-windows)[Web App]

    group system[System]
    service webapi(mdi:internet)[Web API] in system
    service gateway(mdi:boom-gate)[API Gateway] in system

    junction jun1 in system
    junction jun2 in system
    junction jun3 in system
    junction jun4 in system
    junction jun5 in system
    junction jun6 in system

    service auth(mdi:key)[Auth] in system
    service user(mdi:user)[User] in system
    service cort(mdi:brain)[Cortex] in system
    service pred(mdi:magnify)[Prediction] in system
    
    service lambda(logos:aws-lambda)[Lambda MQ] in system
    service s3-model(logos:aws-s3)[Model Bucket] in system
    service s3-hold(logos:aws-s3)[Holding Bucket] in system
    service s3-train(logos:aws-s3)[Training Bucket] in system
    service dynamo-db(logos:aws-dynamodb)[DynamoDB] in system

    desktop:R <--> L:webapi
    mobile:R <--> L:gateway
    
    jun1:B -- T:jun2
    jun2:B -- T:jun3
    gateway:R <-- L:jun2
    jun3:B -- T:jun4
    webapi:R <-- L:jun5
    jun5:T -- B:jun4
    jun6:T -- B:jun5

    jun1:R --> L:auth
    jun2:R --> L:user
    jun6:R --> L:pred

    user:R --> L:s3-hold
    s3-hold:B --> T:s3-train
    s3-train:B --> T:lambda
    lambda:L --> R:cort
    cort:T <-- L:s3-train
    cort:B --> T:s3-model
    s3-model:B <--> T:pred
    lambda:B <--> T:dynamo-db

```
