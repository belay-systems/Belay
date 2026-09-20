"""Evidence-producing computations.

Per ADR-002 this is where the mechanics layer turns observations into numbers
that the governance layer can act on. Every public entry point here returns a
signed Artifact, never a bare value.
"""
