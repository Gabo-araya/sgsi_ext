# Deployment Architecture
This document describes the standard deployment architecture for most DPT-based projects.

## Context
Django Project Template has a specific way to be deployed which is only defined in source form and not easily understandable to new users or people migrating from older versions. This document aims to describe it in a visual way.

## Proposed solution
Does not apply. Solution is already implemented.

## Infrastructure
The solution consists on several containerized components depending on each other:

- Nginx: serves requests to the world and forwards them to the Django application.
- Django: serves the app through the gunicorn WSGI server.
- Redis: provides cache and message broker services
- Celery: runs background and scheduled tasks
- PostgreSQL: database server.

Communication between service containers is done through a network set up by Docker compose. This architecture is used for simple deployments on several cloud providers.

```plantuml
!include <c4/C4_Container>

hide stereotype

System_Boundary(app, "Docker Compose Project") {
  Container(ngx, "Nginx", "Nginx 1.21.3", "Proxies and exposes the app to the Internet.")
  Container(dj, "Django", "Django 4.2 on Python 3.10", "Serves requests and provides the application.")
  Container(celery, "Celery", "Celery on Python 3.10", "Runs tasks in background.")
  Container(pg, "PostgreSQL", "PostgreSQL 15", "Database server")
  Container(redis, "Redis", "Redis 5.x", "In-memory store for caching and message broker.")
}

actor User as user

user -> ngx: Requests\nover HTTPS
ngx -> dj: HTTP requests
dj --> pg: SQL queries
dj -> redis: Cache requests
dj --> redis: Task messages
redis -> celery: Task messages
celery -> pg: SQL queries
```


### Simple development and production architecture on AWS
A simple architecture that **runs all the services described before in a single instance**. Most projects are deployed in this configuration due to the simplicity of its implementation and because it serves well for low traffic demands.

```plantuml
!include <awslib/AWScommon>
!include <awslib/AWSSimplified>

!include <awslib/Database/RDS>
!include <awslib/Database/ElastiCacheElastiCacheforRedis>
!include <awslib/General/Users>
!include <awslib/Compute/EC2Instance>
!include <awslib/Groups/AWSCloud>
!include <awslib/Groups/AvailabilityZone>
!include <awslib/Groups/Region>
!include <awslib/Groups/VPC>
!include <awslib/Storage/SimpleStorageService>

hide stereotype

AWSCloudGroup(aws) {
  RegionGroup(region, "us-east-1") {
    VPCGroup(vpc) {
       EC2Instance(ec2, "App server\n(container execution)", "requests")
    }
  }
}

Users(users, "Users", "hundreds of users")
Users(magnet, "Magnet staff", "manages app")

users -> ec2: Requests
magnet ..> ec2: SSH
```

### Advanced production architecture on AWS
A more advanced architecture will use managed database, storage and Redis services to ensure better availability levels and simplify maintenance. Projects with higher traffic demands are a good suit for this approach.

```plantuml
!include <awslib/AWScommon>
!include <awslib/AWSSimplified>

!include <awslib/Database/RDS>
!include <awslib/Database/ElastiCacheElastiCacheforRedis>
!include <awslib/General/Users>
!include <awslib/Compute/EC2Instance>
!include <awslib/Groups/AWSCloud>
!include <awslib/Groups/AvailabilityZone>
!include <awslib/Groups/Region>
!include <awslib/Groups/VPC>
!include <awslib/Storage/SimpleStorageService>

hide stereotype

AWSCloudGroup(aws) {
  RegionGroup(region, "us-east-1") {
    VPCGroup(vpc) {
       EC2Instance(ec2, "EC2\n(Django [+] Celery)", "requests")
       RDS(rds, "DB\nPostgreSQL", "database")
       ElastiCacheElastiCacheforRedis(redis, "Redis\nCache and\nCelery queues", "cache")
    }
    SimpleStorageService(s3, "S3 Bucket\n Media/Static\nresources", "files")
  }
}

Users(users, "Users", "hundreds of users")
Users(magnet, "Magnet staff", "manages app")

users -> ec2: Requests
ec2 --> s3: API Requests
ec2 -> redis: Cache
ec2 <-> redis: Task messages
ec2 --> rds: Queries
users -> s3: Requests
magnet ..> ec2: SSH
```

Optionally, the EC2 instance can be replaced with an Elastic Container Service cluster (either by using EC2 or Fargate as the execution engine) for increased elasticity. Celery workers can also be run in a separate ECS cluster with additional isolation if required.
