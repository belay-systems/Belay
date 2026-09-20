"""The market data boundary. ADR-013, ROADMAP Stage 2.

Everything Belay had computed before this package existed was fed in by hand,
and every metric artifact said so inside its own signature. This is what makes
that sentence false.

**Why it is not in `framework/services/`.** That package is ten four-line
placeholders for the departmental services, and a data boundary is not a
department. ADR-002 puts new code in `framework/`; this is its own concern.

**Why it does not share anything with a broker.** ADR-013 rule 2, on
`constitution/Immutable_Laws.md:45` — "Research and execution remain
independent." Market data is a read; an execution adapter writes to the world
and the write moves money irreversibly. Retrying is *how* a data fetch recovers
from a dropped connection, and a retried order submit doubles a position. A
shared base class must pick one default and be wrong for the other.
"""
