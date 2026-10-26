---
tags: [leanix-api]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Write a Python script that reads servers.csv (columns: hostname, serial, os, environment, app_id, app_name) from our CMDB export and keeps our SAP LeanIX workspace in sync: each row should become an IT Component fact sheet (hardware) linked to the Application fact sheet given by app_id/app_name, and re-running the job every night must not create duplicates or wipe data that other teams maintain by hand. Credentials come from environment variables. Save it as sync_servers.py with a short README.md explaining what it does, what has to be configured in LeanIX first, and how to test it safely before the first real run.

   Input files: servers.csv
