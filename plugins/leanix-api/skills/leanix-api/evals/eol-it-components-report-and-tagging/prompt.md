---
tags: [leanix-api]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Our architecture board wants a monthly list of IT Components in LeanIX whose lifecycle reaches end of life within the next 12 months, together with the applications that depend on them and the responsible person of each application, exported as a CSV. For the ones that are already past end of life they also want the tag "EOL Risk" (tag group "Risk") added to the affected applications automatically, but only after someone has reviewed a dry run. Write eol_report.py that does both (report by default, tagging behind a flag) plus a short NOTES.md describing exactly which LeanIX queries/mutations it uses and what permissions the token needs.
