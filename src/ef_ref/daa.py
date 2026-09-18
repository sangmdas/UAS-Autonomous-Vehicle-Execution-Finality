from __future__ import annotations

import math

from .crypto import canonical_bytes, domain_hash
from .models import Track, Maneuver


def conflict_root(tracks: list[Track]) -> bytes:
    items = [
        {
            "track_ref": t.track_ref,
            "source_class": t.source_class,
            "position_xy": t.position_xy,
            "velocity_xy": t.velocity_xy,
            "uncertainty_m": t.uncertainty_m,
            "freshness_ms": t.freshness_ms,
            "encounter_class": t.encounter_class,
        }
        for t in sorted(tracks, key=lambda x: x.track_ref)
    ]
    return domain_hash("DAA-CONFLICT-SET", canonical_bytes(items))


def cpa_margin(track: Track, maneuver_velocity_xy: tuple[float, float], *, horizon_s: float, required_separation_m: float) -> tuple[float, float, float]:
    rx, ry = track.position_xy
    rvx = track.velocity_xy[0] - maneuver_velocity_xy[0]
    rvy = track.velocity_xy[1] - maneuver_velocity_xy[1]
    vv = rvx * rvx + rvy * rvy
    if vv == 0:
        t_cpa = 0.0
    else:
        t_cpa = max(0.0, min(horizon_s, -((rx * rvx + ry * rvy) / vv)))
    dx = rx + rvx * t_cpa
    dy = ry + rvy * t_cpa
    d_cpa = math.hypot(dx, dy)
    margin = d_cpa - (required_separation_m + track.uncertainty_m)
    return t_cpa, d_cpa, margin


def maneuver_safe(tracks: list[Track], maneuver_velocity_xy: tuple[float, float], *, horizon_s: float, required_separation_m: float, max_track_age_ms: int) -> bool:
    if not tracks:
        return True
    for t in tracks:
        if t.freshness_ms > max_track_age_ms:
            return False
        _, _, margin = cpa_margin(t, maneuver_velocity_xy, horizon_s=horizon_s, required_separation_m=required_separation_m)
        if margin < 0:
            return False
    return True


def accept_maneuver(m: Maneuver, current_tracks: list[Track], *, current_resolution_epoch: int, sink_id: str, horizon_s: float, required_separation_m: float, max_track_age_ms: int) -> bool:
    if m.resolution_epoch != current_resolution_epoch:
        return False
    if m.sink_id != sink_id:
        return False
    if m.conflict_root != conflict_root(current_tracks):
        return False
    return maneuver_safe(current_tracks, m.velocity_xy, horizon_s=horizon_s, required_separation_m=required_separation_m, max_track_age_ms=max_track_age_ms)
