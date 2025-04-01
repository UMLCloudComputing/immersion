---
sidebar_position: 1
description: Immersion Product Onboarding abstract flow
---

# Onboarding

Recurrent:
-
- Per School Year
    - Populate Club Info DB


Steps:
-
1. Search onboarding DB for Club Name
    - If not found, ask if new
    - Make Service API call to search for club - LAMBDA FUNCTION
    - Repeat until found - LAMBDA FUNCTION
    - Once found, create onboarding DB entry for club in SQS queue. - LAMBDA FUNCTION
        - Leave marked as *unregistered*
2. Get Club data object, validate unregistered
3. Mark as registered
4. Associate Discord Server ID (WIP?)
5. Call Lambda function to make service API call and place parsed object into SQS queue service for prod DB
6. Add Discord Service DB entry with secondary key of production DB club ID.
