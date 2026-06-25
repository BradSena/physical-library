# Review Prompt Template

```text
You are reviewing a change to Avatra.

Read:
- CLAUDE.md
- AGENTS.md
- affected docs

Review the diff for:
- architecture violations;
- business logic in wrong layer;
- Kodi metadata ownership violations;
- Home Assistant coupling;
- barcode workflow regressions;
- location/loan rule regressions;
- missing tests;
- unnecessary dependencies;
- unclear naming.

Return:
- critical issues;
- suggestions;
- approval status.
```
