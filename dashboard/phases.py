"""Parse ICON ingest logs into phase intervals and store them in SQLite.

Live lines are stamped when they are read. A finished log has no per-line
clock, so a completed run is placed from the file mtime and the durations
in the log. Log timestamps are UTC.
"""

from __future__ import annotations

import os
import re
import sqlite3
import threading
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path

LOG_DIR = Path(os.environ.get("INGEST_LOG_DIR", "/open-meteo/log"))
DB_PATH = Path(os.environ.get("INGEST_DB", Path(__file__).resolve().parent / "data" / "phases.sqlite"))
RETENTION_DAYS = 7

# Filename stem -> (model, group). Order is the chart row order.
JOBS: list[tuple[str, str, str]] = [
    ("icon_heidivars.log", "icon", "heidiVars"),
    ("icon_model-level.log", "icon", "model-level"),
    ("icon-eu_heidivars.log", "icon-eu", "heidiVars"),
    ("icon-eu_model-level.log", "icon-eu", "model-level"),
    ("icon-d2_heidivars.log", "icon-d2", "heidiVars"),
    ("icon-d2_model-level.log", "icon-d2", "model-level"),
]

DUR = r"(\d+(?:\.\d+)?ms|\d+(?:\.\d+)?s|\d+(?:\.\d+)?m|\d+:\d{2})"
RE_START = re.compile(r"Downloading domain '([^']+)' run '([^']+)'")
RE_DL_DONE = re.compile(rf"Finished downloading .+ in {DUR}")
RE_CONVERT = re.compile(rf"Convert completed in {DUR} \[Time ([^\]]+)\]")
RE_PREV = re.compile(rf"Previous day convert in {DUR}")
RE_FINISHED = re.compile(rf"Finished in {DUR}")


def parse_duration(token: str) -> float:
    if token.endswith("ms"):
        return float(token[:-2]) / 1000.0
    if token.endswith("s"):
        return float(token[:-1])
    if token.endswith("m"):
        return float(token[:-1]) * 60.0
    hours, minutes = token.split(":")
    return int(hours) * 3600 + int(minutes) * 60


def parse_minute(stamp: str) -> datetime:
    return datetime.strptime(stamp, "%Y-%m-%dT%H:%M").replace(tzinfo=timezone.utc)


def iso(moment: datetime) -> str:
    return moment.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def job_id(model: str, group: str) -> str:
    return f"{model}/{group}"


def job_label(model: str, group: str) -> str:
    return f"{model} {group}"


@dataclass
class RunParse:
    run: str
    download_s: float | None = None
    converts: list[float] = field(default_factory=list)
    prevs: list[float] = field(default_factory=list)
    finished_s: float | None = None
    convert_stamp: str | None = None
    # Kinds after download, in order: convert | prev | finished
    tail: list[tuple[str, float]] = field(default_factory=list)

    @property
    def finished(self) -> bool:
        return self.finished_s is not None


@dataclass
class Phase:
    job: str
    run: str
    phase: str
    start: datetime
    end: datetime | None
    ok: bool


def parse_runs(text: str) -> list[RunParse]:
    runs: list[RunParse] = []
    current: RunParse | None = None
    for raw in text.splitlines():
        line = raw.strip()
        started = RE_START.search(line)
        if started:
            current = RunParse(run=started.group(2))
            runs.append(current)
            continue
        if current is None:
            continue
        downloaded = RE_DL_DONE.search(line)
        if downloaded:
            current.download_s = parse_duration(downloaded.group(1))
            continue
        converted = RE_CONVERT.search(line)
        if converted:
            dur = parse_duration(converted.group(1))
            current.converts.append(dur)
            current.convert_stamp = converted.group(2)
            current.tail.append(("convert", dur))
            continue
        prev = RE_PREV.search(line)
        if prev:
            dur = parse_duration(prev.group(1))
            current.prevs.append(dur)
            current.tail.append(("prev", dur))
            continue
        finished = RE_FINISHED.search(line)
        if finished:
            dur = parse_duration(finished.group(1))
            current.finished_s = dur
            current.tail.append(("finished", dur))
    return runs


def _trailing_prev(run: RunParse) -> float:
    trail = 0.0
    for kind, dur in reversed(run.tail):
        if kind == "finished":
            continue
        if kind == "prev":
            trail += dur
            continue
        break
    return trail


def _process_body(run: RunParse) -> float:
    """Seconds from the end of download to the last Convert completed."""
    body: list[tuple[str, float]] = []
    for kind, dur in run.tail:
        if kind == "finished":
            continue
        body.append((kind, dur))
    while body and body[-1][0] == "prev":
        body.pop()
    return sum(dur for kind, dur in body if kind in ("convert", "prev"))


def phases_for_run(job: str, run: RunParse, end: datetime | None, anchor: datetime | None) -> list[Phase]:
    """Place one run.

    ``end`` is the process-exit time (file mtime) for a finished last run.
    ``anchor`` is the minute stamp of the last Convert completed, used when
    the run is not the last one in an appended file.
    """
    download = run.download_s or 0.0
    process_end: datetime | None
    if run.finished and end is not None:
        start = end - timedelta(seconds=run.finished_s or 0.0)
        ingest_end = start + timedelta(seconds=download)
        process_end = end - timedelta(seconds=_trailing_prev(run))
        if process_end < ingest_end:
            process_end = end
        ok = True
    elif anchor is not None and run.finished:
        process_end = anchor
        ingest_end = process_end - timedelta(seconds=_process_body(run))
        start = ingest_end - timedelta(seconds=download)
        ok = True
    elif end is not None and run.download_s is None:
        # Download still running. ``end`` here is when the log file was opened.
        return [Phase(job=job, run=run.run, phase="ingest", start=end, end=None, ok=True)]
    elif end is not None:
        # Download finished, convert still running. ``end`` is when the log was opened.
        start = end
        ingest_end = start + timedelta(seconds=download)
        process_end = None
        ok = True
    else:
        return []

    rows = [
        Phase(
            job=job,
            run=run.run,
            phase="ingest",
            start=start,
            end=ingest_end,
            ok=ok and run.download_s is not None,
        )
    ]
    if run.download_s is not None:
        rows.append(
            Phase(
                job=job,
                run=run.run,
                phase="process",
                start=ingest_end if ingest_end is not None else start,
                end=process_end,
                ok=ok,
            )
        )
    return rows


def phases_from_log(job: str, text: str, mtime: datetime | None, opened: datetime | None = None) -> list[Phase]:
    runs = parse_runs(text)
    if not runs:
        return []
    rows: list[Phase] = []
    last = len(runs) - 1
    for index, run in enumerate(runs):
        is_last = index == last
        if is_last and run.finished and mtime is not None:
            rows.extend(phases_for_run(job, run, mtime, None))
            continue
        anchor = parse_minute(run.convert_stamp) if run.convert_stamp else None
        if is_last and not run.finished:
            rows.extend(phases_for_run(job, run, opened or mtime, None))
            continue
        if anchor is None:
            continue
        placed = phases_for_run(job, run, None, anchor)
        if index < last and not run.finished:
            nxt = runs[index + 1]
            nxt_rows = phases_for_run(
                job,
                nxt,
                mtime if index + 1 == last and nxt.finished else None,
                parse_minute(nxt.convert_stamp) if nxt.convert_stamp else None,
            )
            if nxt_rows:
                for row in placed:
                    row.end = nxt_rows[0].start
                    row.ok = False
        rows.extend(placed)
    return rows


def format_duration(seconds: float) -> str:
    if seconds < 10:
        return f"{seconds:.1f}s"
    if seconds < 90:
        return f"{int(round(seconds))}s"
    if seconds < 90 * 60:
        return f"{int(round(seconds / 60))}m"
    hours, minutes = divmod(int(round(seconds / 60)), 60)
    return f"{hours:02d}:{minutes:02d}"


def tooltip(model: str, group: str, phase: Phase) -> str:
    if phase.end is None:
        span = f"{iso(phase.start)} – in progress"
        dur = "in progress"
    else:
        span = f"{iso(phase.start)} – {iso(phase.end)}"
        dur = format_duration((phase.end - phase.start).total_seconds())
    state = phase.phase if phase.ok else f"{phase.phase} failed"
    return "<br>".join(
        [
            job_label(model, group),
            f"run {phase.run}Z",
            state,
            span,
            dur,
        ]
    )


class Store:
    def __init__(self, path: Path = DB_PATH) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._db = sqlite3.connect(self.path, check_same_thread=False)
        self._db.row_factory = sqlite3.Row
        self._db.execute("PRAGMA journal_mode=WAL")
        self._db.execute(
            """
            CREATE TABLE IF NOT EXISTS phases (
                id INTEGER PRIMARY KEY,
                job TEXT NOT NULL,
                run TEXT NOT NULL,
                phase TEXT NOT NULL,
                start TEXT NOT NULL,
                end TEXT,
                ok INTEGER NOT NULL,
                UNIQUE (job, run, phase)
            )
            """
        )
        self._db.commit()

    def upsert(self, row: Phase) -> None:
        with self._lock:
            self._db.execute(
                """
                INSERT INTO phases (job, run, phase, start, end, ok)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT (job, run, phase) DO UPDATE SET
                    start = excluded.start,
                    end = excluded.end,
                    ok = excluded.ok
                """,
                (row.job, row.run, row.phase, iso(row.start), iso(row.end) if row.end else None, 1 if row.ok else 0),
            )
            self._db.commit()

    def latest_open_run(self, job: str) -> str | None:
        with self._lock:
            row = self._db.execute(
                """
                SELECT run FROM phases
                WHERE job = ? AND end IS NULL
                ORDER BY start DESC
                LIMIT 1
                """,
                (job,),
            ).fetchone()
        return None if row is None else row["run"]

    def has_phase(self, job: str, run: str, phase: str) -> bool:
        with self._lock:
            row = self._db.execute(
                "SELECT 1 FROM phases WHERE job = ? AND run = ? AND phase = ?",
                (job, run, phase),
            ).fetchone()
        return row is not None

    def close_open(self, job: str, run: str, end: datetime, ok: bool) -> None:
        with self._lock:
            self._db.execute(
                """
                UPDATE phases
                SET end = COALESCE(end, ?), ok = ?
                WHERE job = ? AND run = ? AND end IS NULL
                """,
                (iso(end), 1 if ok else 0, job, run),
            )
            self._db.commit()

    def import_log(self, filename: str, model: str, group: str) -> int:
        path = LOG_DIR / filename
        if not path.exists():
            return 0
        text = path.read_text(errors="replace")
        st = path.stat()
        mtime = datetime.fromtimestamp(st.st_mtime, timezone.utc)
        opened = datetime.fromtimestamp(st.st_ctime, timezone.utc)
        rows = phases_from_log(job_id(model, group), text, mtime, opened)
        for row in rows:
            self.upsert(row)
        return len(rows)

    def backfill(self) -> None:
        for filename, model, group in JOBS:
            self.import_log(filename, model, group)

    def prune(self, now: datetime | None = None, days: int = RETENTION_DAYS) -> int:
        now = now or datetime.now(timezone.utc)
        cutoff = iso(now - timedelta(days=days))
        with self._lock:
            cur = self._db.execute(
                "DELETE FROM phases WHERE end IS NOT NULL AND end < ?",
                (cutoff,),
            )
            self._db.commit()
            return cur.rowcount

    def query(self, now: datetime | None = None, days: int = RETENTION_DAYS) -> dict:
        now = now or datetime.now(timezone.utc)
        cutoff = iso(now - timedelta(days=days))
        groups = []
        labels = {}
        for order, (_, model, group) in enumerate(JOBS):
            key = job_id(model, group)
            labels[key] = (model, group)
            groups.append({"id": key, "content": job_label(model, group), "order": order})
        with self._lock:
            cur = self._db.execute(
                """
                SELECT id, job, run, phase, start, end, ok
                FROM phases
                WHERE end IS NULL OR end >= ? OR start >= ?
                ORDER BY start
                """,
                (cutoff, cutoff),
            )
            raw = cur.fetchall()
        items = []
        for row in raw:
            model, group = labels.get(row["job"], ("?", "?"))
            phase = Phase(
                job=row["job"],
                run=row["run"],
                phase=row["phase"],
                start=datetime.strptime(row["start"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc),
                end=(
                    datetime.strptime(row["end"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
                    if row["end"]
                    else None
                ),
                ok=bool(row["ok"]),
            )
            items.append(
                {
                    "id": row["id"],
                    "group": row["job"],
                    "start": row["start"],
                    "end": row["end"],
                    "className": " ".join(
                        [
                            "phase-bar",
                            phase.phase,
                            "ok" if phase.ok else "failed",
                            "open" if phase.end is None else "closed",
                        ]
                    ),
                    "title": tooltip(model, group, phase),
                    "type": "range",
                }
            )
        return {"generated": iso(now), "groups": groups, "items": items}


class Follower:
    """Apply live log lines for one file. Timestamps are the read time, UTC."""

    def __init__(self, store: Store, model: str, group: str) -> None:
        self.store = store
        self.model = model
        self.group = group
        self.job = job_id(model, group)
        self.run: str | None = None
        self.saw_download = False
        self.saw_finished = False

    def line(self, text: str, now: datetime) -> None:
        started = RE_START.search(text)
        if started:
            if self.run is not None and not self.saw_finished:
                self.store.close_open(self.job, self.run, now, ok=False)
            self.run = started.group(2)
            self.saw_download = False
            self.saw_finished = False
            self.store.upsert(Phase(self.job, self.run, "ingest", now, None, True))
            return
        if self.run is None:
            return
        if RE_DL_DONE.search(text):
            self.saw_download = True
            self.store.upsert(Phase(self.job, self.run, "ingest", self._ingest_start(now), now, True))
            self.store.upsert(Phase(self.job, self.run, "process", now, None, True))
            return
        if RE_CONVERT.search(text):
            self.store.upsert(Phase(self.job, self.run, "process", self._process_start(now), now, True))
            return
        if RE_FINISHED.search(text):
            self.saw_finished = True
            if not self.saw_download:
                self.store.close_open(self.job, self.run, now, ok=True)
            else:
                # Keep the end set by the last Convert completed.
                self.store.close_open(self.job, self.run, now, ok=True)

    def _ingest_start(self, fallback: datetime) -> datetime:
        with self.store._lock:
            row = self.store._db.execute(
                "SELECT start FROM phases WHERE job = ? AND run = ? AND phase = 'ingest'",
                (self.job, self.run),
            ).fetchone()
        if row is None:
            return fallback
        return datetime.strptime(row["start"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)

    def _process_start(self, fallback: datetime) -> datetime:
        with self.store._lock:
            row = self.store._db.execute(
                "SELECT start FROM phases WHERE job = ? AND run = ? AND phase = 'process'",
                (self.job, self.run),
            ).fetchone()
        if row is None:
            return fallback
        return datetime.strptime(row["start"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
