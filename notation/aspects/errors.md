# Errors

This aspect covers parser failures that should expose stable metadata:

- parser code
- message substring
- line
- column

Current scope:

- unknown player aliases
- malformed exact cards
- malformed `deal(...)` arguments
- conflicting multi-line assignments like duplicate `seed` or duplicate seat ranges
- duplicate completed hidden-play targets
- unsupported statements

Non-errors in current scope:

- blank lines are ignored
- `#` comments are ignored
