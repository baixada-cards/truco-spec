# Nature Nodes

This aspect covers exploration states that sit before the hand is dealt.

Initial scenario targets:

- start a fresh hand from an idle exact match state plus exact turnup
- specify one player's full hand before the deal and let the other hand come from chance
- leave both players unspecified and sample a full legal deal
- reject ranged pre-deal specs that omit the `pending_hand` section
- reject `pending_hand` when an active hand is already present
