# Invariant-to-Test Traceability Matrix

| ID | Invariant / attack | Expected result | Test |
|---|---|---|---|
| EF-01 | valid exact act/current state | ALLOW + receipt + capability | `test_valid_act_allows` |
| EF-02 | nonce replay | DENY(REPLAY) | `test_replay_denied` |
| EF-03 | parameter substitution | DENY | `test_argument_substitution_denied` |
| EF-04 | sink substitution | DENY(SINK_MISMATCH) | `test_sink_substitution_denied` |
| EF-05 | context substitution | DENY | `test_context_substitution_denied` |
| EF-06 | policy changes after early check | DENY at commit | `test_policy_change_after_precheck_denied_at_commit` |
| EF-07 | revocation changes after early check | DENY at commit | `test_revocation_change_after_precheck_denied_at_commit` |
| EF-08 | receipt store unavailable | DENY; no capability | `test_receipt_store_failure_fails_closed` |
| EF-09 | 50 concurrent identical consumes | exactly one ALLOW | `test_50_way_same_nonce_concurrency_allows_exactly_once` |
| FR-01 | missing fragment | incomplete/no reconstruction | `test_missing_fragment_is_incomplete` |
| FR-02 | cross-session fragment mix | reject | `test_mixed_session_rejected` |
| FR-03 | payload corruption | reject | `test_corrupted_fragment_rejected` |
| AER-01 | valid interval-0 delayed disclosure | verify | `test_valid_interval0_verifies_after_disclosure` |
| AER-02 | derive interval-0 tag from public K0 | fail | `test_public_k0_cannot_derive_interval0_valid_tag` |
| AER-03 | valid old record injected after disclosure | discard | `test_late_record_rejected_even_if_tag_valid` |
| AER-04 | intermediate KDRs lost | recover from later KDR | `test_loss_of_intermediate_kdr_recovered_by_later_disclosure` |
| AER-05 | wrong epoch/device | reject | `test_wrong_epoch_record_rejected`, `test_wrong_device_record_rejected` |
| DAA-01 | new relevant intruder appears | old maneuver invalid | `test_new_intruder_invalidates_old_resolution` |
| DAA-02 | resolution epoch superseded | reject old maneuver | `test_stale_resolution_epoch_rejected` |
| DAA-03 | any relevant intruder unsafe | whole maneuver unsafe | `test_multi_intruder_one_unsafe_means_whole_maneuver_unsafe` |
| ES-01 | q-of-n independent scene corroboration | allow only when threshold met | `test_two_independent_sources_satisfy_q2` |
| ES-02 | two channels, same physical source | count once / fail q=2 | `test_two_channels_same_physical_source_count_once` |
| ES-03 | scene exit / expiry / epoch change | deny | emergency-scene negative tests |
| HO-01 | crash after PREPARE/COMMIT/ENABLE | never dual authority | `test_crash_injection_never_yields_dual_authority` |
| HO-02 | randomized 1000 handover schedules | exclusivity always holds | `test_randomized_handover_sequences_preserve_exclusivity` |
| SAFE-01 | ordinary authority unavailable | safe action remains available | `test_brake_remains_available_when_ordinary_authority_fails` |
