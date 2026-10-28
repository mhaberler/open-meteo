# ICON surface

Names for the single-level ICON fields that sit on the model orography, and for the pressure the API reduces away from it.

## Language

**Model elevation**:
The unmasked model orography. Open sea stays near 0 m.
_Avoid_: elevation, HSURF

**Model surface pressure**:
Pressure at the model orography. A requested elevation does not move it.
_Avoid_: surface pressure, sea-level pressure

**Surface pressure**:
Pressure reduced from sea-level pressure through the requested elevation.
_Avoid_: model surface pressure
