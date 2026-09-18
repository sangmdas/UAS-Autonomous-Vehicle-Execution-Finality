from ef_ref.daa import conflict_root, accept_maneuver, maneuver_safe
from ef_ref.models import Track, Maneuver


def base_tracks():
    return [
        Track("T1", "ADS-B", (200.0, 20.0), (-5.0, 0.0), 5.0, 100),
        Track("T2", "RADAR", (-180.0, -40.0), (4.0, 0.5), 6.0, 80),
    ]


def test_current_conflict_set_safe_maneuver_can_pass():
    tracks = base_tracks()
    m = Maneuver("M1", (0.0, 8.0), 21, conflict_root(tracks), "motion-sink")
    assert accept_maneuver(m, tracks, current_resolution_epoch=21, sink_id="motion-sink", horizon_s=20, required_separation_m=30, max_track_age_ms=500)


def test_new_intruder_invalidates_old_resolution():
    tracks = base_tracks()
    m = Maneuver("M1", (0.0, 8.0), 21, conflict_root(tracks), "motion-sink")
    new = tracks + [Track("T3", "VISION", (0.0, 25.0), (0.0, -2.0), 3.0, 20)]
    assert not accept_maneuver(m, new, current_resolution_epoch=21, sink_id="motion-sink", horizon_s=20, required_separation_m=30, max_track_age_ms=500)


def test_stale_resolution_epoch_rejected():
    tracks = base_tracks()
    m = Maneuver("M1", (0.0, 8.0), 21, conflict_root(tracks), "motion-sink")
    assert not accept_maneuver(m, tracks, current_resolution_epoch=22, sink_id="motion-sink", horizon_s=20, required_separation_m=30, max_track_age_ms=500)


def test_wrong_motion_sink_rejected():
    tracks = base_tracks()
    m = Maneuver("M1", (0.0, 8.0), 21, conflict_root(tracks), "sink-A")
    assert not accept_maneuver(m, tracks, current_resolution_epoch=21, sink_id="sink-B", horizon_s=20, required_separation_m=30, max_track_age_ms=500)


def test_stale_track_fails_closed():
    tracks = [Track("T1", "RADAR", (100,0), (-1,0), 2, 2000)]
    assert not maneuver_safe(tracks, (0,5), horizon_s=20, required_separation_m=30, max_track_age_ms=500)


def test_multi_intruder_one_unsafe_means_whole_maneuver_unsafe():
    tracks = base_tracks() + [Track("T3", "VISION", (0,10), (0,0), 2, 10)]
    assert not maneuver_safe(tracks, (0,8), horizon_s=20, required_separation_m=30, max_track_age_ms=500)
