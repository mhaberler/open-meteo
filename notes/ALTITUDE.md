# ICON Model Levels to Geometric Altitude

Source: DWD "DWD Database Reference for the Global and Regional ICON and ICON-EPS Forecasting System", Version 2.5.5 (2026), Appendix A "ICON standard level heights" (file `icon_database_main.pdf`).

## Vertical Grid

ICON uses a **SLEVE** (smooth level vertical) height-based hybrid coordinate (Leuenberger et al.).

- Layers are defined by **half levels** (interfaces, `k+1/2`).
- Prognostic variables live at **full levels** (layer centres, `k`).
- Level 1 = top of model (highest).
- Highest level index = lowest layer (near surface).
- The coordinate is terrain-following near the ground and flattens to constant geometric height above ~16 km.

**Level counts (open-meteo `IconDomains`):**

| Domain       | Full levels (N) | Half levels | Top full (std) | Lowest full (std) |
|--------------|-----------------|-------------|----------------|-------------------|
| `icon`, `icon-eps` (global) | 120 | 121 | 74 210.3 m | 10.0 m |
| `icon-eu`, `icon-eu-eps` | 74 | 75 | 22 433.4 m (= global full 47) | 10.0 m |
| `icon-d2`, `icon-d2-15min`, `icon-d2-eps` | 65 | 66 | 20 700.9 m | 10.0 m |

(See also `Sources/App/Icon/Icon.swift`: `numberOfModelFullLevels` and the `modelLevel` download group.)

## Half levels vs. Full levels (detailed explanation)

ICON (like most modern NWP models) uses a **Lorenz-type vertical staggering** on its height-based grid:

- **Half levels** (also called interface levels, `k+1/2`):  
  These are the **boundaries** of the model layers.  
  - Vertical velocity (`w` or `ω`) is defined here.  
  - The geometric height of the coordinate surfaces is defined here (`HHL` = height of half levels).  
  - With `num_lev` layers there are always `num_lev + 1` half levels.  
  - Half level `num_lev + 1` coincides with the Earth's surface (in the model's topography).

- **Full levels** (also called main levels, layer centres, or mid-levels, `k`):  
  These are the **centres** of the model layers.  
  - Temperature `t`, horizontal wind components `u`/`v`, specific humidity `qv`, cloud variables, etc. live here.  
  - This is what open-meteo (and DWD "model-level" GRIB output) exposes when you ask for "model level 42".  
  - Full level `i` sits exactly between half level `i` and half level `i+1`.

Exact quote from the PDF:

> "The ICON grid employs a Lorenz-type staggering with the vertical velocity defined at the boundaries of layers (half levels) and the other prognostic variables in the center of the layer (full levels).  
> With `num_lev` layers, there are `num_lev + 1` so-called half levels. The half levels `k − 1/2`, `k + 1/2` enclose layer `k` at the centers of which are the corresponding full levels `k`, for `k = 1, …, num_lev`. Layer 1 is at the top of the atmosphere and layer n at the bottom of the atmosphere. Half level `num_lev + 1` coincides with the Earth’s surface."

### Visual (N=3 layers example, top → bottom)

```
Half level 1   (top of atmosphere, e.g. 30 km standard)
    Full level 1   ← temperature, u, v, qv, … live here
Half level 2
    Full level 2
Half level 3
    Full level 3
Half level 4   (model surface, 0 m in standard table)
```

### Height relationship (standard zero-topo case)

Full level height `i` (zero topography) is simply the arithmetic mean:

```text
zif0 = (zih0 + z(i+1)h0) / 2
```

(See the `get_actual_height_agl` implementation and the PDF formula in the "Actual Altitude" section below for the terrain-following version.)

### Practical consequences for users

- When you download or query ICON "model levels" (the 65/74/120 levels in open-meteo), you are getting data on **full levels**.
- The standard height tables (A.2 for global/EU, A.4 for D2) and the lists in this document / `untracked/icon_level_to_altitude.py` are **full-level** heights (what you normally want for temperature/wind profiles).
- `HHL` files from DWD contain heights on the **half levels** (one 2-D field per half level). To obtain the precise geometric height of a full level over real terrain you **must average the two adjacent actual half-level heights** (after subtracting `HSURF`).
- Near the surface the difference between half-level height and the full level below/above it is small (a few tens of metres for the lowest layers). Higher up the layer thickness grows to hundreds or thousands of metres.
- Vertical velocity (if ever exposed) would be on the half levels; almost everything else on full levels.

This distinction is why the code in `icon_level_to_altitude.py` (and the `get_actual...` helpers) works with a list of half-level heights and derives full-level altitudes by averaging.

## Standard Heights (zero topography)

Tables A.1–A.4 in the PDF give **standard heights above ground** (`z_h0`, `z_f0`) that are exact only for grid points with zero surface elevation (e.g. open ocean).

- Full level `i` (standard) = average of half levels `i` and `i+1`.
- These are the values used for quick lookups and were previously transcribed (with some transcription errors in mid-levels) into `notes/icon-model-levels.txt`.

Over real terrain the actual geometric height of a given model level index **varies** from point to point.

## Actual Altitude at a Location (recommended)

The PDF (p. 173 and A.2) gives the precise method:

```
half-level height AGL at x:
    zih(x) = HHL(x, i) − HSURF(x)

full-level height AGL at x (level i):
    zif(x) = ( zih(x) + z(i+1)h(x) ) / 2
```

- `HSURF(x)`: surface elevation (m ASL) — stored by open-meteo as the elevation field.
- `HHL(x, *)`: geometric height of half levels ASL (one field per half level). These are time-invariant fields distributed by DWD (search `HHL` + `HSURF`/`hsurf` under the time-invariant GRIB directories for the grid type: icosahedral for global, regular lat-lon for nests).

Upper levels (roughly above the 16 km transition) are nearly identical to the standard table. Lower levels are compressed over orography; the "surface" in the model is always the local model topography + a small offset for the lowest layer.

**Note on open-meteo data layout**: As of 2026-06, `HHL` is ingested by the download pipeline
(`convertHhlHeights` in `DownloadIconCommand.swift`) and stored alongside `HSURF` as a single 3D
static file `<domain>/static/hhl.om` with dimensions `[ny, nx, nHalfLevels]` (half-level dimension
last, raw ASL metres, no sea mask). Verified for `icon` (121 levels), `icon-eu` (75) and `icon-d2`
(66). Per-location vertical columns are read in one I/O via `Gridable.readColumnFromStaticFile`, and
`IconReader.fullLevelHeightASL/AGL` derive full-level geometric heights by averaging adjacent halves.
There is not yet an HTTP variable exposing these (e.g. `height_levelN`) — that is gated on the
model-level (`_levelN`) variable rollout. See `notes/plan-hhl-ingest-and-serve.md`.

## Representative Standard Full-Level Heights (m AGL, zero topography)

### ICON-D2 (65 levels)
```
level   height (m)
1      20700.9
10     12132.4
20      7715.4
30      4773.3
40      2678.9
50      1196.5
55       654.5
60       247.2
63        77.7
64        37.6
65        10.0
```

### ICON-EU (74 levels)
Level 1 = 22 433.4 m (maps to global full level 47). Lowest = 10.0 m.

### ICON global (120 levels)
Level 1 = 74 210.3 m. Level 120 = 10.0 m.

The EU nest re-uses global levels 47–120 (EU level `k` == global level `k+46` for full levels).

Full exact tables (all half + full for the three domains) live in executable form in `untracked/icon_level_to_altitude.py`, derived directly from the PDF via text extraction + de-interleaving of the 3-column table layout. The same lists (plus the helpers below) are embedded in this document for easy copy-paste.

## Python Code Fragment

Self-contained helpers + the authoritative lists (copy from the companion `untracked/icon_level_to_altitude.py` for the latest verified copy).

```python
from typing import List, Literal

# Full authoritative lists extracted from icon_database_main.pdf Appendix A (Tables A.1-A.4)
ICON_D2_HALF_LEVELS_STD: List[float] = [
    22000.000, 19401.852, 18013.409, 16906.264, 15958.169, 15118.009, 14358.139,
    13661.439, 13016.363, 12414.654, 11850.143, 11318.068, 10814.653, 10336.841,
    9882.112, 9448.359, 9033.796, 8636.893, 8256.329, 7890.952, 7539.748, 7201.825,
    6876.388, 6562.725, 6260.200, 5968.239, 5686.321, 5413.976, 5150.773, 4896.323,
    4650.265, 4412.272, 4182.043, 3959.301, 3743.791, 3535.279, 3333.549, 3138.402,
    2949.656, 2767.143, 2590.708, 2420.213, 2255.527, 2096.537, 1943.136, 1795.234,
    1652.748, 1515.610, 1383.761, 1257.155, 1135.760, 1019.556, 908.539, 802.721,
    702.132, 606.827, 516.885, 432.419, 353.586, 280.598, 213.746, 153.438, 100.277,
    55.212, 20.000, 0.000,
]  # 66 values, Table A.3

ICON_GLOBAL_HALF_LEVELS_STD: List[float] = [
    75000.000, 73420.604, 71869.610, 70328.192, 68805.917, 67302.897, 65819.234,
    64355.018, 62910.329, 61485.239, 60079.812, 58694.107, 57328.172, 55982.053,
    54655.788, 53349.411, 52062.951, 50796.435, 49549.882, 48323.311, 47116.737,
    45930.172, 44763.626, 43617.107, 42490.621, 41384.171, 40297.761, 39231.393,
    38185.067, 37158.783, 36152.542, 35166.342, 34200.183, 33254.064, 32327.985,
    31421.947, 30535.948, 29669.993, 28824.082, 27998.221, 27192.413, 26406.667,
    25640.990, 24895.393, 24169.889, 23463.917, 22770.331, 22096.568, 21435.487,
    20795.107, 20175.457, 19576.575, 18998.498, 18441.271, 17908.405, 17400.463,
    16920.113, 16467.114, 16039.909, 15637.031, 15257.093, 14898.789, 14560.888,
    14242.227, 13933.170, 13633.170, 13333.170, 13033.170, 12733.170, 12433.170,
    12133.170, 11833.170, 11533.170, 11233.170, 10933.170, 10633.170, 10333.170,
    10033.170, 9733.170, 9433.170, 9133.170, 8833.170, 8533.170, 8233.170, 7933.170,
    7633.170, 7333.170, 7033.170, 6733.170, 6433.170, 6133.170, 5833.170, 5533.170,
    5233.170, 4933.170, 4633.170, 4333.170, 4033.170, 3735.917, 3448.582, 3171.241,
    2903.980, 2646.890, 2400.076, 2163.652, 1937.746, 1722.498, 1518.070, 1324.640,
    1142.413, 971.624, 812.540, 665.478, 530.811, 408.988, 300.565, 206.253, 126.999,
    64.166, 20.000, 0.000,
]  # 121 values, Table A.1

ICON_GLOBAL_FULL_LEVELS_STD: List[float] = [
    74210.302, 72645.107, 71098.901, 69567.054, 68054.407, 66561.065, 65087.126,
    63632.673, 62197.784, 60782.526, 59386.959, 58011.140, 56655.113, 55318.921,
    54002.599, 52706.181, 51429.693, 50173.158, 48936.596, 47720.024, 46523.454,
    45346.899, 44190.367, 43053.864, 41937.396, 40840.966, 39764.577, 38708.230,
    37671.925, 36655.663, 35659.442, 34683.262, 33727.124, 32791.024, 31874.966,
    30978.948, 30102.970, 29247.037, 28411.151, 27595.317, 26799.540, 26023.829,
    25268.192, 24532.641, 23816.903, 23117.124, 22433.449, 21766.028, 21115.297,
    20485.282, 19876.016, 19287.537, 18719.885, 18174.838, 17654.434, 17160.288,
    16693.613, 16253.512, 15838.470, 15447.062, 15077.941, 14729.839, 14401.558,
    14087.699, 13783.170, 13483.170, 13183.170, 12883.170, 12583.170, 12283.170,
    11983.170, 11683.170, 11383.170, 11083.170, 10783.170, 10483.170, 10183.170,
    9883.170, 9583.170, 9283.170, 8983.170, 8683.170, 8383.170, 8083.170, 7783.170,
    7483.170, 7183.170, 6883.170, 6583.170, 6283.170, 5983.170, 5683.170, 5383.170,
    5083.170, 4783.170, 4483.170, 4183.170, 3884.543, 3592.249, 3309.912, 3037.610,
    2775.435, 2523.483, 2281.864, 2050.699, 1830.122, 1620.284, 1421.355, 1233.526,
    1057.019, 892.082, 739.009, 598.144, 469.899, 354.776, 253.409, 166.626, 95.582,
    42.083, 10.000,
]  # 120 values, Table A.2

ICON_EU_FULL_LEVELS_STD: List[float] = ICON_GLOBAL_FULL_LEVELS_STD[46:]  # global full 47..120 = EU 1..74

def _full_from_half(half: List[float]) -> List[float]:
    return [(half[i] + half[i + 1]) / 2 for i in range(len(half) - 1)]

ICON_D2_FULL_LEVELS_STD: List[float] = _full_from_half(ICON_D2_HALF_LEVELS_STD)

Domain = Literal["icon", "icon-eu", "icon-d2", "icon-global"]

_DOMAIN_MAP = {
    "icon":        {"full": ICON_GLOBAL_FULL_LEVELS_STD, "half": ICON_GLOBAL_HALF_LEVELS_STD, "nfull": 120},
    "icon-global": {"full": ICON_GLOBAL_FULL_LEVELS_STD, "half": ICON_GLOBAL_HALF_LEVELS_STD, "nfull": 120},
    "icon-eu":     {"full": ICON_EU_FULL_LEVELS_STD,     "half": ICON_GLOBAL_HALF_LEVELS_STD[46:], "nfull": 74},
    "icon-d2":     {"full": ICON_D2_FULL_LEVELS_STD,     "half": ICON_D2_HALF_LEVELS_STD,     "nfull": 65},
}

def get_standard_height(domain: Domain, level: int, *, half_level: bool = False) -> float:
    """Return standard (zero-topography) height above ground [m] for the given model level.
    level: 1-based (1 = top of atmosphere / uppermost full level).
    """
    key = "half" if half_level else "full"
    data = _DOMAIN_MAP[domain][key]
    if not (1 <= level <= len(data)):
        raise ValueError(f"level {level} out of range for {domain} ({key}, 1..{len(data)})")
    return data[level - 1]

def get_number_of_full_levels(domain: Domain) -> int:
    return _DOMAIN_MAP[domain]["nfull"]

def get_actual_height_agl(
    hhl_half_levels_asl: List[float],  # HHL column (ASL), len = #half-levels for domain, [0]=top
    hsurf: float,                      # HSURF at the location (m ASL)
    level: int,
    *,
    half_level: bool = False,
) -> float:
    """Actual geometric height above ground using the model's HHL + HSURF (exact per PDF formulas)."""
    if len(hhl_half_levels_asl) < 2:
        raise ValueError("need at least two half-level heights")
    n_half = len(hhl_half_levels_asl)
    half_agl = [h - hsurf for h in hhl_half_levels_asl]
    if half_level:
        if not (1 <= level <= n_half):
            raise ValueError(f"half level {level} out of range 1..{n_half}")
        return half_agl[level - 1]
    n_full = n_half - 1
    if not (1 <= level <= n_full):
        raise ValueError(f"full level {level} out of range 1..{n_full}")
    # PDF: full i = average of half i and half i+1 (1-based)
    return (half_agl[level - 1] + half_agl[level]) / 2.0

def get_actual_height_asl(hhl_half_levels_asl: List[float], hsurf: float, level: int, **kw) -> float:
    """Actual height above sea level (convenience wrapper)."""
    return hsurf + get_actual_height_agl(hhl_half_levels_asl, hsurf, level, **kw)
```

**Usage example**

```python
# After you have a vertical column of HHL (ASL) + scalar HSURF for a (lat,lon)
# (obtained by interpolating the DWD time-invariant HHL/HSURF GRIBs, or nearest grid point)
hhl_asl = [22000.0 + 1500, ...]  # 66 (or 75/121) values for the domain; top first
hsurf = 1500.0

print("D2 level 1 (top) standard:     ", get_standard_height("icon-d2", 1))
print("D2 level 65 (lowest) standard: ", get_standard_height("icon-d2", 65))

# Real altitude at this location
print("Actual AGL (level 50):", get_actual_height_agl(hhl_asl, hsurf, 50))
print("Actual ASL (level 50):", get_actual_height_asl(hhl_asl, hsurf, 50))
```

Run `python untracked/icon_level_to_altitude.py` to see a full demo (including synthetic compression of lower levels over a mountain that shows how actual AGL diverges from the standard table).

## References

- PDF: `untracked/icon_database_main.pdf` (Appendix A, especially pp. 173–178 and Tables A.1–A.6)
- Prior transcription: `notes/icon-model-levels.txt` (JS arrays; contained some duplication errors around the 8–9 km transition)
- Implementation detail: `Sources/App/Icon/Icon.swift`, `IconVariableDownloadable.swift`, `DownloadIconCommand.swift` (the `modelLevel` group and `numberOfModelFullLevels`)
- Related: `docs/adr/0001-icon-model-level-naming.md`, `untracked/plan.md`, `untracked/hires.md`

For precise work (aviation profiles, balloon trajectories, etc.) always prefer the HHL/HSURF-based computation over the standard table when the location has significant topography.

See `notes/plan-hhl-ingest-and-serve.md` for the implementation plan to ingest HHL as a single 3D static `hhl.om` (with lazy column read) and serve derived full-level heights. Phases 1+2 are independent of the model-level variable work; near-term win is heights for the existing fixed 80m/120m/180m/5500m variables.