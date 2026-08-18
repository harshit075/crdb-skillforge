# Project Governance — CrDB SkillForge

## Overview

CrDB SkillForge is an open-source, community-driven repository of executable CockroachDB skills for AI agents.

This document describes the project's governance model, decision-making process, maintainer roles, and technical review requirements.

> **Disclaimer**: CrDB SkillForge is a community-maintained agent skills project and is not official CockroachDB documentation unless explicitly stated otherwise.

---

## Roles and Responsibilities

### Maintainers
Maintainers are responsible for reviewing pull requests, ensuring skill validity, managing releases, and guiding project direction.

### Technical Reviewers
Because skills in CrDB SkillForge execute queries and diagnostics against real database clusters, every skill submission requires **Technical Review** by a maintainer familiar with CockroachDB internals, safety boundaries, and query optimizer behavior.

---

## Decision-Making Process

- Minor improvements, documentation formatting, and bug fixes require 1 maintainer approval.
- New canonical skills or changes to skill schemas require technical review and automated evaluation verification (`make eval`).
- Architectural modifications to adapter or tool execution layers require consensus among core maintainers.

---

## Skill Staleness Policy

All canonical skills contain a `last_verified` date in YYYY-MM-DD format.
Skills unverified for > 6 months are flagged as `STALE` by `tools/validate-skill.py` and trigger automated CI warnings during nightly evaluation workflows.
