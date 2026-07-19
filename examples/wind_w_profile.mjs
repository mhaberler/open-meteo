#!/usr/bin/env node
// Query ICON vertical wind (W) on native model half levels.
//
// W (`wind_w_level<N>`) lives on DWD half levels 1..nFull+1 (icon-d2: 1..66,
// icon-eu: 1..75, icon global: 1..121). Half level N sits exactly at hhl[N];
// its height is exposed as `height_half_level<N>` (ASL) / `height_half_agl_level<N>`.
//
// Usage:  node wind_w_profile.mjs [lat] [lon]
// Env:    OM_API  base URL of the open-meteo server (default http://127.0.0.1:8080)

const BASE = process.env.OM_API ?? "http://127.0.0.1:8080";
const [lat = 47.8, lon = 16.2] = process.argv.slice(2).map(Number); // Austria / icon-d2

const N_HALF = 66; // icon-d2 half levels
const levels = Array.from({ length: 21 }, (_, i) => N_HALF - 20 + i);

const hourly = [
    ...levels.map((n) => `wind_w_level${n}`),
    ...levels.map((n) => `height_half_agl_level${n}`),
];

const url = `${BASE}/v1/dwd-icon?` + new URLSearchParams({
    latitude: lat,
    longitude: lon,
    hourly: hourly.join(","),
    forecast_days: 1,
});

console.log(`GET ${url}\n`);
const res = await fetch(url);
if (!res.ok) throw new Error(`HTTP ${res.status}: ${await res.text()}`);
const data = await res.json();

const h = data.hourly;
const hourIdx = 0;
console.log(`Vertical wind profile at ${data.latitude},${data.longitude} time=${h.time[hourIdx]} (icon-d2 half levels)\n`);
console.log("level  height AGL [m]  w [m/s]");

let prevHeight = Infinity;
for (const n of levels) {
    const height = h[`height_half_agl_level${n}`][hourIdx];
    const w = h[`wind_w_level${n}`][hourIdx];
    console.log(`${String(n).padStart(5)}  ${height.toFixed(1).padStart(14)}  ${w.toFixed(2).padStart(7)}`);
    // sanity: heights strictly decrease with level index (1 = model top)
    if (height >= prevHeight) throw new Error(`height not monotonic at level ${n}`);
    prevHeight = height;
}

// sanity: surface half level — AGL ≈ 0 and w ≈ 0 (lower boundary condition)
const surfAgl = h[`height_half_agl_level${N_HALF}`][hourIdx];
const surfW = h[`wind_w_level${N_HALF}`][hourIdx];
if (Math.abs(surfAgl) > 1.0) throw new Error(`surface half level AGL should be ~0, got ${surfAgl}`);
if (Math.abs(surfW) > 0.5) throw new Error(`surface w should be ~0, got ${surfW}`);
console.log("\nsanity OK: heights monotonic, surface AGL≈0, surface w≈0");
