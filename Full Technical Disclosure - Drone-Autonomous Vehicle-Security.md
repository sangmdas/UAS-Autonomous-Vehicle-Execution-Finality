## ABSTRACT

Unmanned aerial vehicles, autonomous ground vehicles, autonomous robots, mobile cyber-physical systems, constrained Internet-of-Things devices, and similar platforms may be required to communicate authority, freshness, geographic scope, mission scope, device state, and intended-action information over communication channels having severe payload-size, bandwidth, latency, energy, or duty-cycle constraints. Existing authentication, identification, telemetry, and authorization objects may be too large or computationally expensive to carry directly within such constrained broadcast or beacon channels. Conventional beaconing may identify a device or report state but does not necessarily cryptographically bind authorization to the exact physical or externally consequential act that is about to become effective. The invention provides a constrained-beacon execution-finality architecture in which a proposed externally consequential operation is first represented as a Candidate Act and maintained in a Non-Effective State. A protected execution domain canonicalizes the Candidate Act together with selected authority, destination, geographic, temporal, policy, sink, and live-context parameters and derives an act-bound cryptographic commitment, preferably keyed under a binding key that is unavailable to the mission computer, transmitter, or other untrusted component. A compact representation of the commitment, together with freshness information, an authority reference, a policy or revocation epoch, an act class, a destination or Finality Sink identifier, and integrity or authentication evidence, is encoded into one or more constrained beacon frames. Where the complete cryptographic evidence cannot fit within a single beacon, the invention provides deterministic authenticated fragmentation, chained multi-frame reconstruction, compact authority references, dictionary-based field compression, time and geographic delta encoding, truncated commitments selected according to both a collision-risk budget and an attacker-work budget, and optional resolver-assisted verification. Partial or ambiguous beacon reception does not authorize execution. A downstream Finality Sink, such as a flight controller, electronic speed controller, drive-by-wire controller, actuator controller, payload-release controller, radio controller, sensor controller, or secure bus gateway, reconstructs or resolves the compact evidence, reads current policy and revocation state inside an atomic finality commit, verifies freshness and anti-replay state, recomputes the act-bound commitment from the actual action about to become effective, commits a Finality Receipt, and permits effectuation only when the reconstructed evidence matches the actual Candidate Act and all required authority predicates. In a further aspect, the protected execution domain broadcasts compact Act Evidence Records authenticated with a reverse one-way key chain whose seed never leaves the protected domain, with keys disclosed after a delay and the chain anchored once to the device identity, so that a third-party observer can verify, over a lossy constrained channel and without a per-act public-key signature, that an observed act was decided by the protected domain before it became effective, and so that an identification transmitter or compromised mission computer cannot forge such evidence. The architecture therefore allows compact beacon transport to carry or reference execution-specific authority, and to evidence execution-specific decisions, while preserving the invariant that identification, possession of a token, prior authorization, broadcast evidence, or partial beacon reception is not by itself sufficient to produce the physical or externally effective result.

## 1. TECHNICAL FIELD

The invention relates generally to secure control of autonomous and cyber-physical systems. More particularly, the invention relates to:

Page 2

- unmanned aerial vehicles(UAVs), unmanned aircraft systems (UAS), and drones;
- autonomous aerial platforms;
- autonomous and highly automated ground vehicles, including road vehicles, shuttles, delivery vehicles, and agricultural and mining vehicles;
- vehicle-to-everything (V2X) cooperative driving and manoeuvre coordination;
- remote assistance and remote operation of automated vehicles;
- autonomous mobile robots and robotic vehicles;
- industrial cyber-physical devices and remotely operated systems;
- constrained IoT devices and low-power radio devices;
- airspace-aware and road-zone-aware control systems;
- electronic speed controller, flight-controller, and drive-by-wire interfaces;
- actuator and payload controllers;
- secure embedded controllers and hardware-rooted authorization systems;
- short-range and broadcast radio protocols, including remote-identification-adjacent communications, Bluetooth Low Energy, Wi-Fi-based broadcast or discovery, UWB, sidelink, mesh radio, LPWAN, and constrained satellite or non-terrestrial links;
- in-vehicle and on-board buses having small frame payloads;
- broadcast source authentication for third-party observers;
- protected command and actuation systems; and
- cryptographically verifiable authorization and evidence of physical effects. The invention is particularly directed to circumstances in which a full authorization object, certificate, capability, attestation record, signed policy object, execution descriptor, or verification receipt cannot economically or technically be transmitted in every radio frame because of packet-size, energy, latency, duty-cycle, airtime, or protocol-format constraints.

## 2. TECHNICAL BACKGROUND

Autonomous systems increasingly generate commands capable of producing direct physical or externally consequential effects. Examples include:

- arming propulsion;
- changing rotor speed or modifying thrust;
- changing flight mode or driving mode;
- executing a waypoint transition;
- crossing an airspace boundary or entering a restricted road zone;
- entering a restricted operational corridor;
- accepting a cooperative manoeuvre such as joining a platoon, merging, or taking an intersection slot;
- executing a path approved by a remote assistance operator;
- transmitting over a radio interface or changing transmitter power;
- activating a camera or sensor, or operating a gimbal;
- releasing cargo, opening a payload latch, or operating a gripper;
- initiating a landing operation;
- accepting a swarm or fleet command;
- changing a route;
- invoking an emergency mode;

Page 3

- enabling a high-power subsystem; or
- communicating an instruction to another autonomous system. Authentication of a source does not necessarily establish that every particular requested action is authorized. Likewise:
- identifying a UAV or vehicle does not authorize every manoeuvre;
- identifying an operator does not authorize every payload operation;
- a valid mission credential does not necessarily authorize an act after a geofence or zone changes;
- a valid signature does not necessarily establish that the signed command remains fresh;
- a valid token does not necessarily establish that the actual downstream actuator command still matches the act originally authorized;
- a broadcast beacon may contain identity or position information without containing execution-specific authority;
- a full authorization object may be too large for a highly constrained broadcast frame; and
- a third party who can verify a device's identity from a broadcast generally cannot verify whether an act it observes was decided by a protected enforcement component before the act became effective. A practical systems problem therefore exists. A high-assurance control system may possess detailed execution-finality evidence internally, while the communication path available to a remote verifier, neighbouring UAV or vehicle, flight controller, actuator controller, reader, base station, roadside unit, gateway, or other downstream enforcement component may carry only a small number of bytes. Simply transmitting the entire authorization object may be impossible, inefficient, or incompatible with the available transport. Simply omitting the evidence weakens downstream verification. Simply transmitting a token identifier may create ambiguity or permit substitution unless the identifier is cryptographically and semantically bound to the exact act. Simply truncating a cryptographic hash without defining collision risk, attacker work, context binding, freshness, receiver reconstruction, and failure behaviour may not provide a sufficiently deterministic enforcement mechanism. In particular, an unkeyed truncated hash whose inputs are known to an attacker can be searched offline for a substituted act that produces the same truncated value. Simply signing each act with the identification key held by a transmitter does not establish that the protected enforcement component decided the act. The invention addresses these technical problems through a compact, act-bound, freshness-bound, sinkbound beacon representation with deterministic verification behaviour, and through delayed-disclosure act evidence whose origin is the protected domain.

## 3. TECHNICAL PROBLEM

The principal technical problem addressed by the invention is:

How can execution-specific cryptographic authority for a consequential cyber-physical act **be communicated or referenced over a highly constrained beacon or broadcast channel**

### without converting that channel into a bearer-token mechanism and without permitting

Page 4

**partial, stale, substituted, replayed, offline-searched, or ambiguously reconstructed information to authorize physical effectuation; and how can the decision on such an act be evidenced to third parties over the same constrained channel with origin in the protected enforcement component?**

Sub-problems include:

1. full authorization evidence may exceed the available beacon payload;
2. cryptographic signatures may consume a substantial portion of the available radio frame;
3. transmission of a full authorization object at every control cycle may increase latency, radio airtime, and energy consumption;
4. a compact token may become replayable if freshness state is omitted;
5. a compact token may authorize the wrong actuator if the intended effectuation boundary is omitted;
6. a compact token may authorize a different action if the exact Candidate Act is not cryptographically

bound;

7. truncated digests introduce collision considerations that must be explicitly bounded;
8. truncated unkeyed digests are exposed to offline search by a party that knows or can predict the inputs;
9. beacon fragmentation creates the risk that an incomplete frame set could accidentally be treated as valid;
10. cached authority information may become stale following policy update or revocation, including in the interval between a check and the effect;
11. an upstream mission computer may describe one action while a downstream motor, actuator, payload, steering, braking, or radio interface receives a materially different action;
12. geofence, corridor, road-zone, payload, sensor, mission-phase, or policy state may change between authorization and effectuation;
13. a receiver may lack sufficient bandwidth or computational capability to process full certificate chains or complex policy objects in the hot path;
14. the final actuator may require a deterministic, low-latency allow/deny decision;
15. transport constraints may differ across BLE, Wi-Fi broadcast, UWB, mesh, sidelink, V2X, telemetry, or proprietary aviation radio systems;
16. a standard identification beacon may not have been designed to serve as a cryptographic execution

permit;

17. third-party observers cannot verify per-act decisions without per-act signatures that do not fit constrained, lossy broadcasts; and
18. in road vehicles and other systems where withholding an action can itself be unsafe, enforcement must never block a safety-increasing action.

## 4. INVENTIVE CONTRIBUTION

The invention introduces a constrained representation of execution-finality evidence in which a beacon does not merely identify an aircraft, vehicle, device, user, mission, or credential. Instead, the beacon carries or references cryptographic evidence bound to a specific Candidate Act and to the component that is expected to make that act externally effective, and, in a further aspect, carries evidence of decisions made by the protected domain that third parties can verify. The contribution may include one or more of the following technical mechanisms:

Page 5

# 4.1 Act-bound compact commitment

A cryptographic commitment is computed over the actual Candidate Act and selected context. In a preferred embodiment the commitment is keyed under a binding key available only to the protected execution domain and the Finality Sink.

# 4.2 Finality-Sink binding

The commitment includes an identifier or class corresponding to the downstream component that will produce the physical or externally consequential effect.

# 4.3 Freshness binding

The compact beacon includes or cryptographically commits to one or more of: nonce; sequence number; monotonic counter; time slot; validity interval; epoch; rolling session value; or challenge.

# 4.4 Authority-reference compression

A long authority object may be replaced in the beacon by a compact reference that can be resolved from protected cache, local storage, gateway state, or a trusted authority service.

# 4.5 Context commitment

Relevant live or semi-live context may be bound into the commitment, including: geofence or road-zone version; corridor identifier; mission phase; payload state; flight or driving mode; policy epoch; revocation epoch; geographic cell; altitude band or lane group; radio mode; destination; sink identity; or safety-state reference.

# 4.6 Authenticated fragmentation

Where a complete compact proof cannot fit in one frame, the proof is divided across multiple frames in a manner that prevents an incomplete or mixed frame set from being interpreted as authorization.

# 4.7 Truncation according to explicit risk budgets

Instead of arbitrary digest truncation, the number of retained bits is selected according to an expected number of candidate commitments and a defined acceptable collision probability and, where the commitment is unkeyed, according to an attacker offline-work budget.

# 4.8 Resolver-assisted verification

The constrained beacon may contain a short cryptographic commitment and compact reference while the verifier retrieves or reads a fuller authority object from authenticated storage.

# 4.9 Exact-act reconstruction

The downstream sink independently reconstructs the actual Candidate Act from local command state, actuator state, flight-control or vehicle-control state, protected registers, payload state, or radio-control state.

# 4.10 No effectuation from incomplete evidence

Failure to obtain or reconstruct the complete required evidence leaves the Candidate Act non-effective.

# 4.11 Currentness inside the atomic commit

Current policy and revocation state are read inside the same atomic section in which freshness state is consumed and the execution capability is committed, closing the interval between check and effect.

Page 6

# 4.12 Receipt before release

A Finality Receipt recording the decision is committed before the execution capability becomes usable.

# 4.13 Observer-verifiable delayed-disclosure act evidence

Decisions are evidenced by compact records authenticated with a reverse one-way key chain whose seed is held only in the protected domain, with delayed key disclosure, an observer safety condition, loss-tolerant key recovery, and a single signed anchor bound to the device identity.

# 4.14 Safety asymmetry

In platforms where withholding an action can be unsafe, gating applies to expansions of permission and consequential non-safety acts, while a pre-authorized set of safety-increasing actions remains always available.

## 5. DEFINITIONS

The following definitions are used for clarity. The invention is not limited to the exact names used.

# 5. DEFINITIONS

The following definitions are used for clarity and to describe functional roles within the disclosed architecture. The invention is not limited to the exact terminology used, and an equivalent function may be implemented under another name, abstraction, protocol, hardware component, software component, controller, or system architecture.

### 5.1 Candidate Act

A Candidate Act is a proposed, requested, computed, received, negotiated, selected, or otherwise formed operation, state transition, control decision, communication, trajectory, command, permission expansion, configuration change, or other action capable of producing a physical, operational, communicative, persistent, geographic, sensing, safety-significant, financial, legal, access-related, or other externally consequential effect, where the operation has been identified sufficiently to permit verification but has not yet been permitted to produce the relevant effect.

A Candidate Act may originate from, without limitation:

x x x x x x x x x x x x x x x x x an autonomous planner; artificial-intelligence or machine-learning component; mission computer; flight computer; vehicle planner; motion planner; autopilot; automated-driving system; remote operator; remote-assistance service; fleet controller; swarm controller; V2X or cooperative-driving participant; navigation system; policy engine; application software; external network service;

Page 7

| x | safety controller; |
|---|---|
| x | human operator; or |
| x | another machine, controller, or decision source. |

A Candidate Act may represent a discrete operation or a bounded permitted envelope within which multiple lower-level operations may occur.

For an unmanned aerial vehicle, aerial autonomous platform, or drone, non-limiting Candidate Acts

include:

x x x x x x x x x x x x x x x x x x x x x x x x takeoff; landing; flight-mode transition; waypoint transition; route or corridor transition; change in altitude; change in heading; change in velocity vector; thrust or propulsion request; motor or rotor-control command; ESC enable; geofence-sensitive movement; restricted-airspace entry; payload release; cargo delivery; payload-latch opening; sensor activation; camera or gimbal activation; RF transmission; transmitter-power change; swarm operation; return-to-home transition; protected configuration change; or activation of another flight, payload, sensing, or communication function.

For an autonomous, highly automated, remotely assisted, or remotely operated ground vehicle, nonlimiting Candidate Acts include:

| x | a planned trajectory; |
|---|---|
| x | admission of a trajectory to a motion controller; |
| x | steering request; |
| x | braking request; |
| x | acceleration request; |
| x | propulsion or torque request; |
| x | speed-envelope change; |
| x | lane change; |
| x | merge; |
| x | intersection traversal; |
| x | overtaking manoeuvre; |
| x | platoon join or leave operation; |
| x | acceptance of a cooperative manoeuvre; |
| x | road-zone entry; |
| x | operational-design-domain transition; |

Page 8

| x | automated-driving-mode transition; |
|---|---|
| x | activation of a higher automation mode; |
| x | execution of a remotely approved path; |
| x | execution of a fleet-issued movement instruction; |
| x | V2X-coordinated movement; |
| x | parking manoeuvre; |
| x | sensor-recording operation; |
| x | high-power communication; |
| x | actuator operation; or |
| x | another movement, mode, sensing, communication, or vehicle-control action. |

For robotics or other cyber-physical systems, a Candidate Act may include:

| x | robotic-arm movement; |
|---|---|
| x | gripper operation; |
| x | actuator movement; |
| x | power switching; |
| x | valve operation; |
| x | machinery activation; |
| x | sensor activation; |
| x | transmission of protected data; |
| x | admission of a command to a protected bus; |
| x | release of stored energy; |
| x | configuration change; or |
| x | another consequence-bearing operation. |

A Candidate Act is not limited to a high-level instruction such as "go to destination X" or "release payload." It may include the concrete or load-bearing parameters that materially determine what will actually occur, including one or more of:

| x | target; |
|---|---|
| x | destination; |
| x | route; |
| x | trajectory; |
| x | geographic region; |
| x | lane; |
| x | corridor; |
| x | altitude; |
| x | velocity; |
| x | acceleration; |
| x | heading; |
| x | steering angle; |
| x | braking level; |
| x | thrust; |
| x | torque; |
| x | time window; |
| x | device; |
| x | actuator; |
| x | payload; |
| x | sensor; |
| x | communication channel; |
| x | power level; |
| x | participant identity; |

Page 9

| x | sink identity; |
|---|---|
| x | operational mode; |
| x | policy state; or |
| x | another parameter material to the resulting effect. |

A Candidate Act may therefore represent an exact operation, a parameterized operation, or a bounded actuation or trajectory envelope, provided that the representation is sufficiently defined to permit comparison between the authorized operation and the operation actually presented for effectuation.

### 5.2 Non-Effective State

A Non-Effective State is a technical condition in which a Candidate Act may have been generated, received, computed, negotiated, staged, buffered, stored, transmitted internally, validated in part, or otherwise exist within the system, but remains incapable of producing its designated external consequence until one or more required verification or release conditions are satisfied.

The Non-Effective State may be established or maintained by hardware, firmware, software, protected memory, access control, capability control, power gating, bus gating, command admission, register protection, actuator gating, trajectory admission, mode-transition control, transmission gating, or another mechanism capable of withholding effectuation.

A Candidate Act may remain in a Non-Effective State even though upstream software has classified, approved, selected, generated, signed, transmitted, or otherwise processed the act.

For an unmanned aerial vehicle or drone, non-limiting examples include:

| x | a motor or ESC command staged but not released to the motor-control path; |
|---|---|
| x | a PWM value buffered but not committed to an effective output register; |
| x | a waypoint transition computed but not admitted to the flight controller; |
| x | a route or corridor change held before navigation effectuation; |
| x | a payload-release command buffered while the latch or solenoid remains disabled; |
| x | a camera or sensor activation request held before enablement; |
| x | an RF packet prepared but held before transmit-enable; |
| x | a flight-mode transition pending protected admission; or |
| x | an actuator command present in memory but blocked from the actuator bus. |

For an autonomous or highly automated vehicle, non-limiting examples include:

| x | a planned trajectory present in a vehicle planner but not admitted to the motion controller; |
|---|---|
| x | a steering command staged but not released to the drive-by-wire controller; |
| x | a braking or propulsion envelope calculated but not activated; |
| x | a lane-change or merge manoeuvre negotiated but not admitted to vehicle control; |
| x | a higher automation mode requested but not committed to the mode-transition controller; |
| x | a remotely approved path received but not released to the vehicle motion stack; |
| x | a cooperative V2X manoeuvre accepted at a negotiation layer but not admitted to actuation; |
| x | a road-zone or operational-design-domain transition awaiting verification; or |
| x | a vehicle command present on an upstream bus but blocked by a secure gateway or motion- admission component. |

Page 10

For another cyber-physical system, a Non-Effective State may include an actuator command held behind a secure gateway, a motor output held behind a power or enable gate, a robot movement staged but not admitted to motion control, or a protected communication held before transmission.

The term Non-Effective State describes the practical inability of the Candidate Act to produce the protected consequence, rather than merely a software label indicating that an operation is "pending," "unapproved," or "not yet executed."

A Candidate Act ceases to be in a Non-Effective State only when the required effectuation conditions are satisfied and the relevant enforcement path permits the act, or a permitted portion or envelope thereof, to become effective.

### 5.3 Effectuation

**Effectuation means the technical transition by which a Candidate Act, or a permitted portion or**

bounded envelope of the Candidate Act, crosses an enforcement boundary and becomes capable of producing, or actually produces, its intended physical, operational, communicative, persistent, geographic, sensing, or other external consequence.

Effectuation may occur at a physical actuator, controller, bus, register, communication interface, trajectory-admission gate, mode-transition interface, power-control path, command-acceptance boundary, or another point at which the Candidate Act ceases to be merely proposed or staged and begins to control or alter the external system.

Effectuation does not require completion of the ultimate physical consequence. It may occur at the technical point at which control is irreversibly or operationally released toward that consequence.

For a UAV or aerial autonomous platform, Effectuation may include:

| x | a motor command becoming effective at an ESC; |
|---|---|
| x | PWM or another propulsion-control value being released to a motor controller; |
| x | propulsion power being enabled; |
| x | a flight controller accepting a waypoint, trajectory, corridor, or mode transition; |
| x | a payload actuator becoming powered; |
| x | a payload latch opening; |
| x | an RF transmission being enabled; |
| x | a camera or sensor becoming active; |
| x | an actuator moving; |
| x | a geofence-sensitive flight transition being admitted; or |
| x | another aviation-system command being accepted by the component capable of producing the corresponding effect. |

For an autonomous or highly automated ground vehicle, Effectuation may include:

| x | admission of a trajectory from a planner to a motion controller; |
|---|---|
| x | release of a steering command to a drive-by-wire controller; |
| x | release of a braking command; |
| x | release of a propulsion or torque command; |
| x | activation of a speed or motion envelope; |
| x | acceptance of a lane-change, merge, intersection, or cooperative manoeuvre; |
| x | admission of a remotely approved route or trajectory; |
| x | activation of a higher automation or driving mode; |

Page 11

| x | acceptance of a road-zone or operational-design-domain transition; |
|---|---|
| x | release of a command through a protected vehicle gateway; or |
| x | activation of a sensing, recording, communication, or body-function operation. |

For communication or sensing operations, Effectuation may occur when:

| x | a packet reaches a transmit-enable boundary; |
|---|---|
| x | RF energy is permitted to be emitted; |
| x | a protected message is released onto a network or bus; |
| x | a camera begins recording; |
| x | a sensor begins acquisition; or |
| x | data becomes accessible to an external recipient. |

For robotic or industrial systems, Effectuation may occur when an actuator command is admitted to a motion controller, power reaches an actuator, a robotic joint begins to move, a valve is activated, a gripper is enabled, or another controlled physical operation becomes effective.

The point of Effectuation may therefore differ by implementation. It is the relevant consequence

**boundary at which the system can no longer treat the Candidate Act solely as a proposed, staged,**

or non-effective operation.

Where a Candidate Act authorizes a bounded envelope rather than one individual low-level command, Effectuation may comprise release of the bounded envelope, after which individual commands satisfying that envelope may be admitted according to the disclosed verification rules without requiring full reauthorization for every control-cycle update.

The term Effectuation is therefore functional and does not depend on a particular actuator technology, processor, vehicle architecture, aircraft architecture, communication protocol, control bus, or physical implementation.

Page 12

### 5.4 Finality Sink

A Finality Sink is a hardware, firmware, software, mixed hardware-software, controller, gateway, secure processing component, actuator interface, motion-admission component, communicationpath controller, or other enforcement element positioned at, incorporated into, or sufficiently close to an effectuation boundary such that it has the technical ability to prevent, withhold, constrain, modify to an authorized envelope, or otherwise control whether a Candidate Act becomes physically, operationally, communicatively, persistently, or otherwise externally effective.

A Finality Sink need not itself be the physical actuator. It may instead control a signal, register, capability, bus transaction, power path, command-admission path, trajectory-admission path, mode transition, actuator envelope, transmit-enable path, or other prerequisite without which the relevant effect cannot occur.

The Finality Sink may be implemented as a distinct protected component or may be integrated into another device, controller, processor, electronic control unit, domain controller, zonal controller, autopilot, safety processor, actuator controller, secure gateway, or communication subsystem.

For an unmanned aerial vehicle or other aerial autonomous platform, non-limiting examples

include:

x x x x x x x x x x x x x x x x x x x a flight controller; autopilot controller; electronic speed controller; motor or propulsion controller; motor gate driver; rotor or thrust-control interface; payload controller; payload-release or latch controller; servo controller; gimbal controller; landing or takeoff controller; geofence or corridor-admission controller; RF transmit-enable controller; sensor or camera controller; protected avionics bus gateway; swarm-command admission controller; secure microcontroller; FPGA-based safety controller; or another component capable of withholding a flight, propulsion, payload, sensing, communication, or other consequential operation.

For an autonomous, highly automated, remotely assisted, or remotely operated ground vehicle, nonlimiting examples include:

| x | a vehicle motion-admission controller; |
|---|---|
| x | trajectory-admission gate; |
| x | drive-by-wire controller; |
| x | steering controller; |
| x | braking controller; |
| x | propulsion or torque controller; |
| x | transmission controller; |
| x | vehicle domain controller; |

Page 13

| x | zonal controller; |
|---|---|
| x | automated-driving controller; |
| x | mode-transition controller; |
| x | operational-design-domain enforcement component; |
| x | speed-envelope controller; |
| x | lane or road-zone admission component; |
| x | V2X manoeuvre-admission controller; |
| x | remote-assistance command gate; |
| x | secure in-vehicle network gateway; |
| x | CAN, automotive Ethernet, or equivalent protected bus gateway; |
| x | sensor or recording controller; |
| x | telematics security module; |
| x | body-function actuator controller; or |
| x | another component capable of preventing or constraining a vehicle operation before it becomes effective. |

For robotics and other cyber-physical systems, a Finality Sink may similarly comprise a robotic motion controller, gripper controller, industrial actuator interface, power controller, secure bus gateway, sensor controller, communications controller, or another enforcement point at which an operation can still be prevented from producing its external consequence.

The term Finality Sink denotes the enforcement function rather than any particular product, processor, communication protocol, physical location, or implementation technology.

A component remains a Finality Sink where it performs the required enforcement indirectly, including by issuing or withholding a bounded execution capability that a downstream actuator must possess before performing the Candidate Act.

### 5.5 Execution-Finality Evidence

**Execution-Finality Evidence means machine-verifiable information sufficient, alone or together**

with protected local state, to determine whether a particular Candidate Act satisfies one or more conditions required before the Candidate Act may become effective.

Execution-Finality Evidence may establish or bind one or more of:

| x | the identity or class of the Candidate Act; |
|---|---|
| x | the concrete parameters of the Candidate Act; |
| x | the intended Finality Sink; |
| x | the authorized device, vehicle, aircraft, robot, actuator, or subsystem; |
| x | applicable authority; |
| x | freshness; |
| x | anti-replay state; |
| x | validity period; |
| x | policy state; |
| x | revocation state; |
| x | operational context; |
| x | geographic or spatial scope; |
| x | geofence, road-zone, lane, corridor, route, or operational-design-domain state; |
| x | flight mode or driving mode; |
| x | mission or journey phase; |
| x | payload state; |

Page 14

| x | sensor state; |
|---|---|
| x | radio or communication state; |
| x | permitted actuation envelope; |
| x | permitted trajectory or motion envelope; |
| x | participant identity in a coordinated or cooperative manoeuvre; |
| x | safety-state information; or |
| x | another condition material to whether effectuation is permitted. |

Execution-Finality Evidence may be represented directly or indirectly and may comprise or reference one or more cryptographic commitments, authentication tags, signatures, messageauthentication codes, Authority References, freshness values, counters, nonces, policy epochs, revocation epochs, Context Commitments, protected-state identifiers, capability identifiers, fragment-root commitments, or equivalent machine-verifiable values.

Execution-Finality Evidence does not require that all authorization or policy information be transmitted to the Finality Sink in full. A compact representation may instead be combined with protected local state, cached authority information, resolver-returned information, or other authenticated information.

Execution-Finality Evidence is distinguished from mere identity, telemetry, status, or advisory information because it is associated with verification of whether a concrete Candidate Act may become effective.

### 5.6 Authority Object

An Authority Object is a machine-verifiable object, record, data structure, credential, capability, permit, policy representation, or protected-state entry expressing one or more permissions, limitations, conditions, scopes, or prohibitions relevant to a Candidate Act.

An Authority Object may identify or constrain one or more of:

x x x x x x x x x x x x x x x x x x x x x an authorized act class; particular act parameters; an authorized device; vehicle or aircraft; Finality Sink; operator; controller; mission; journey; route; trajectory; geographic area; airspace volume; road segment; lane group; operational corridor; operational-design domain; permitted speed or propulsion envelope; payload; sensor; radio function;

Page 15

| x | communication function; |
|---|---|
| x | validity interval; |
| x | policy epoch; |
| x | revocation state; |
| x | safety condition; or |
| x | another property relevant to authorization. |

An Authority Object may comprise, without limitation:

x x x x x x x x x x x x x x x x x x x x x x x x x x x x x a signed token; certificate; cryptographic capability; capability grant; policy record; access-control record; mission authorization; flight permit; airspace authorization; corridor authorization; geofence authorization; payload authorization; drop-zone authorization; vehicle operational-design-domain authorization; road-zone authorization; lane or route authorization; cooperative-manoeuvre authorization; remote-assistance authorization; fleet authorization; V2X authorization; operator authorization; radio permit; sensor-use permit; actuator envelope; secure database record; hardware-security-module-protected record; secure-element record; trusted-execution-environment record; or a combination thereof.

An Authority Object may be stored locally, remotely, or distributively and may be transmitted in full or represented by an Authority Reference.

Possession, presentation, or successful verification of an Authority Object does not necessarily itself cause effectuation. The Finality Sink may additionally require verification that the Authority Object applies to the actual Candidate Act presented for effectuation and remains current at the effectuation boundary.

### 5.7 Constrained Beacon

A Constrained Beacon is any message, frame, packet, record, advertisement, discovery object, telemetry object, broadcast, multicast, sidelink transmission, V2X message, mesh message, remote-

Page 16

identification-related message, on-board or in-vehicle bus message, short-range message, lowpower transmission, or other communication unit subject to a practical limitation on one or more of:

| x | payload size; |
|---|---|
| x | bandwidth; |
| x | airtime; |
| x | transmission frequency; |
| x | energy consumption; |
| x | latency; |
| x | processing cost; |
| x | duty cycle; |
| x | memory; |
| x | radio spectrum; |
| x | bus capacity; |
| x | message format; |
| x | security overhead; or |
| x | protocol-imposed field size. |

A Constrained Beacon may be wireless or wired.

Non-limiting transport environments include:

| x | Bluetooth Low Energy; |
|---|---|
| x | Wi-Fi advertisement, discovery, or direct communication; |
| x | UWB; |
| x | IEEE 802.15.4-type communication; |
| x | mesh communication; |
| x | LPWAN; |
| x | cellular sidelink; |
| x | V2X; |
| x | direct vehicle communication; |
| x | remote-identification broadcast; |
| x | aviation telemetry; |
| x | proprietary UAV data links; |
| x | satellite or non-terrestrial links; |
| x | CAN or equivalent vehicle buses; |
| x | automotive Ethernet; |
| x | avionics buses; |
| x | robotics buses; |
| x | industrial field buses; and |
| x | other current or future constrained transport mechanisms. |

The term Constrained Beacon does not require that a message be periodically broadcast, does not require a particular radio technology, and does not require that the message be visible to the public.

A message may constitute a Constrained Beacon because of limitations arising from the transport, receiving hardware, energy budget, real-time deadline, safety architecture, or implementation environment even where the underlying communication technology is otherwise capable of carrying larger messages.

### 5.8 Beacon Proof Capsule

Page 17

A Beacon Proof Capsule, abbreviated BPC, is a compact machine-verifiable data structure that carries, represents, commits to, or references Execution-Finality Evidence for one or more Candidate Acts over a Constrained Beacon or other constrained communication path.

A Beacon Proof Capsule may contain explicitly, implicitly, directly, or by reference one or more of:

| x | version information; |
|---|---|
| x | profile identifier; |
| x | Candidate Act class; |
| x | Finality Sink identifier or class; |
| x | Authority Reference; |
| x | policy epoch; |
| x | revocation epoch; |
| x | freshness value; |
| x | nonce; |
| x | counter; |
| x | validity or expiry information; |
| x | Context Commitment; |
| x | geographic or operational-scope reference; |
| x | act-binding commitment; |
| x | device or participant reference; |
| x | fragment information; |
| x | risk profile; |
| x | authentication tag; |
| x | digital signature; or |
| x | another integrity or verification field. |

A Beacon Proof Capsule need not contain the complete Authority Object or complete Execution- Finality Evidence. It may instead contain a compact commitment, truncated value, cryptographic reference, dictionary index, session-relative value, delta-encoded value, cache reference, resolver reference, or other compact representation from which the necessary verification information can be securely obtained or reconstructed.

A Beacon Proof Capsule may occupy:

| x | a single message or frame; |
|---|---|
| x | part of a message or frame; |
| x | multiple authenticated fragments; |
| x | multiple temporally related transmissions; or |
| x | a logical data structure distributed across more than one transport unit. |

Where fragmented, incomplete receipt of the Beacon Proof Capsule does not constitute authorization unless the applicable verification profile expressly defines sufficient reconstruction and all required integrity conditions are satisfied.

A Beacon Proof Capsule may be generated for an individual Candidate Act, a bounded set of Candidate Acts, a permitted actuator envelope, trajectory envelope, propulsion envelope, time window, geographic scope, or another expressly bounded execution scope.

The Beacon Proof Capsule is not, merely by being received or possessed, an instruction to execute the corresponding Candidate Act. The relevant Finality Sink independently determines whether the actual impending operation corresponds to the evidence represented by the Beacon Proof Capsule.

Page 18

### 5.9 Act Commitment

An Act Commitment is a cryptographic commitment derived from a deterministic or canonical representation of a Candidate Act or of selected effect-determining properties of the Candidate Act.

The Act Commitment may bind the operation as a whole or a defined set of load-bearing fields, meaning fields whose modification can change the physical, operational, communicative, persistent, geographic, sensing, or other externally consequential result.

Such fields may include, without limitation:

For UAV or aerial-system acts:

| x | waypoint; |
|---|---|
| x | trajectory; |
| x | velocity vector; |
| x | altitude; |
| x | heading; |
| x | yaw rate; |
| x | flight mode; |
| x | corridor; |
| x | geofence state; |
| x | thrust envelope; |
| x | motor or rotor set; |
| x | payload identifier; |
| x | payload-release location; |
| x | radio parameters; |
| x | sensor parameters; or |
| x | intended Finality Sink. |

For autonomous or highly automated vehicle acts:

| x | trajectory; |
|---|---|
| x | planned path; |
| x | lane or lane group; |
| x | road segment; |
| x | target speed; |
| x | speed envelope; |
| x | acceleration or deceleration envelope; |
| x | steering envelope; |
| x | braking envelope; |
| x | propulsion or torque envelope; |
| x | manoeuvre identifier; |
| x | cooperative-manoeuvre parameters; |
| x | remote-assistance path; |
| x | operational-design-domain state; |
| x | road-zone state; |
| x | driving mode; |
| x | automation mode; |
| x | V2X participant information; or |
| x | intended motion-admission or drive-by-wire Finality Sink. |

Page 19

For robotic or other cyber-physical operations:

| x | actuator identity; |
|---|---|
| x | target state; |
| x | movement envelope; |
| x | power level; |
| x | sensor state; |
| x | communication state; |
| x | destination; |
| x | timing; |
| x | operational context; or |
| x | intended effectuation component. |

A representative Act Commitment may be expressed as:

DA=H(DOMA∥C(A))D\_A = H(DOM\_A \\parallel C(A))

where AA is the Candidate Act, C(A)C(A) is a deterministic representation of the Candidate Act, DOMADOM\_A is a domain-separation value, and HH is a cryptographic hash or other cryptographic commitment function.

The Act Commitment may alternatively be keyed, combined with a keyed Binding Commitment, generated using a message-authentication function, or implemented using another cryptographic construction providing the required binding property.

An Act Commitment is intended to cause a material change in the Candidate Act to produce a corresponding change in the commitment, subject to the security properties of the selected cryptographic construction.

The term does not require the commitment to expose the Candidate Act itself and therefore permits privacy-preserving, compact, cached, resolver-assisted, or truncated representations suitable for constrained UAV, vehicle, robotic, and other cyber-physical environments.

### 5.1 Binding Commitment

A Binding Commitment is a cryptographic commitment that binds an Act Commitment to one or more additional properties relevant to whether a Candidate Act may become effective.

The additional bound properties may include, without limitation:

| x | a Finality Sink identifier or class; |
|---|---|
| x | Authority Object or Authority Reference; |
| x | device, vehicle, aircraft, robot, subsystem, or participant identity; |
| x | policy epoch; |
| x | revocation epoch; |
| x | freshness value; |
| x | nonce; |
| x | sequence number; |
| x | time slot; |
| x | validity or expiry information; |
| x | Context Commitment; |

Page 20

| x | geographic region; |
|---|---|
| x | geofence or road-zone version; |
| x | airspace corridor; |
| x | lane or lane group; |
| x | operational-design domain; |
| x | route or trajectory; |
| x | mission or journey phase; |
| x | flight or driving mode; |
| x | payload state; |
| x | sensor state; |
| x | radio or communication state; |
| x | actuation envelope; |
| x | speed, thrust, torque, steering, braking, or motion envelope; |
| x | cooperative-manoeuvre identifier; |
| x | remote-assistance session; |
| x | fleet or swarm scope; |
| x | safety state; or |
| x | another value defining the permitted scope of effectuation. |

A representative Binding Commitment may be expressed as:

B=FK(DA∥S∥R∥EP∥ER∥DC∥N∥T)B = F\_K( D\_A \\parallel S \\parallel R \\parallel E\_P \\parallel E\_R \\parallel D\_C \\parallel N \\parallel T )

where DAD\_A is an Act Commitment, SS identifies or characterizes the Finality Sink, RR represents authority, EPE\_P and ERE\_R represent policy and revocation state, DCD\_C is a Context Commitment, NN represents freshness, TT represents temporal scope, and FKF\_K is a keyed or otherwise authenticated cryptographic function.

The Binding Commitment is preferably keyed so that a component that merely knows the Candidate Act and other public fields cannot efficiently construct a different Candidate Act having an acceptable compact binding.

The term does not require that all bound values be transmitted. One or more values may be implicit, cached, locally protected, derived from session state, or represented by compact references.

### 5.2 Authority Reference

An Authority Reference is a compact identifier, digest, index, locator, keyed identifier, pseudonymous identifier, cache key, table entry, capability reference, or other machine-resolvable value by which a verifier can identify, retrieve, select, or validate an Authority Object or corresponding authority state relevant to a Candidate Act.

An Authority Reference may point to authority held:

| x | within the Finality Sink; |
|---|---|
| x | within the Protected Execution Domain; |
| x | in secure local storage; |
| x | in an HSM or secure element; |
| x | in a vehicle domain or zonal controller; |
| x | in an aircraft avionics controller; |
| x | in a protected gateway; |
| x | in a trusted resolver; |

Page 21

| x | in a local or remote authority service; or |
|---|---|
| x | in another authenticated repository. |

The Authority Reference may be derived from the Authority Object using a cryptographic hash, keyed hash, deterministic identifier, database index, opaque token, session-relative identifier, or equivalent mechanism.

For example:

R=Truncr(HMACKR(AuthorityObject))R = Trunc\_r(HMAC\_{K\_R}(AuthorityObject))

or another compact derivation may be used.

The Authority Reference may identify authority concerning, without limitation:

| x | a flight mission; |
|---|---|
| x | airspace corridor; |
| x | geofence; |
| x | payload; |
| x | road zone; |
| x | operational-design domain; |
| x | autonomous-driving mode; |
| x | cooperative vehicle manoeuvre; |
| x | remotely approved path; |
| x | fleet instruction; |
| x | sensor operation; |
| x | radio operation; or |
| x | actuator envelope. |

An Authority Reference does not by itself constitute authority, and successful resolution of an Authority Reference does not by itself permit effectuation. The corresponding Candidate Act may still require Finality Sink verification of act identity, scope, freshness, current policy, revocation state, context, and other required conditions.

### 5.3 Policy Epoch

A Policy Epoch is a machine-verifiable version, generation, revision, state identifier, monotonic value, digest, or equivalent indicator representing the policy state applicable to one or more Candidate Acts.

A Policy Epoch may correspond to policy governing, without limitation:

| x | aircraft mission authority; |
|---|---|
| x | geofence or corridor access; |
| x | payload operation; |
| x | flight mode; |
| x | vehicle operational-design domain; |
| x | road-zone access; |
| x | lane or route permissions; |
| x | driving-mode authorization; |
| x | remote-assistance authority; |
| x | cooperative manoeuvres; |

Page 22

| x | fleet or swarm operation; |
|---|---|
| x | sensor use; |
| x | communication permissions; |
| x | speed or actuation envelopes; or |
| x | another execution condition. |

The value may identify a complete policy set or a relevant subset thereof.

A Finality Sink may require the Policy Epoch associated with a Beacon Proof Capsule or Candidate Act to correspond to the current applicable policy state before effectuation.

For safety- or security-sensitive implementations, the deciding Policy Epoch may be read from protected state at or immediately before the final effectuation decision rather than relying solely on an earlier policy check.

### 5.4 Revocation Epoch

A Revocation Epoch is a machine-verifiable version, generation, monotonic value, digest, state identifier, or equivalent representation of the revocation state applicable to one or more Authority Objects, Candidate Acts, devices, operators, missions, sessions, vehicles, aircraft, routes, corridors, payloads, permissions, or execution scopes.

Advancement or modification of the Revocation Epoch may indicate that previously issued authority has been:

| x | withdrawn; |
|---|---|
| x | superseded; |
| x | suspended; |
| x | restricted; |
| x | replaced; or |
| x | otherwise rendered unusable. |

For example, a change in Revocation Epoch may invalidate authority relating to:

| x | an aircraft mission; |
|---|---|
| x | payload release; |
| x | airspace access; |
| x | vehicle ODD operation; |
| x | road-zone entry; |
| x | cooperative manoeuvre; |
| x | remote-assistance session; |
| x | fleet command; |
| x | sensor operation; or |
| x | radio permission. |

A Finality Sink may require the Revocation Epoch associated with a Candidate Act to correspond to current protected revocation state at the time of effectuation.

### 5.5 Context Commitment

Page 23

A Context Commitment is a cryptographic commitment to one or more environmental, operational, geographic, temporal, mission, vehicle, aircraft, payload, sensor, communication, safety, or policy conditions relevant to whether a Candidate Act may become effective.

The committed context may include, without limitation:

x x x x x x x x x x x x x x x x x x x x x x x x x x x x geographic location or geographic cell; geofence version; road-zone version; airspace volume; corridor; lane or lane group; route segment; altitude band; speed; direction; vehicle or aircraft attitude; flight mode; driving mode; automation mode; operational-design domain; mission phase; journey phase; payload state; sensor state; radio state; environmental condition; participant state in a cooperative manoeuvre; remote-assistance state; fleet or swarm state; policy state; revocation state; safety mode; or other condition material to effectuation.

A representative Context Commitment may be expressed as:

DC=H(DOMC∥C(Context))D\_C = H(DOM\_C \\parallel C(Context))

where C(Context)C(Context) is a deterministic representation of the selected context.

The Context Commitment may protect privacy by committing to detailed state without broadcasting the state itself. For example, a beacon may carry a commitment to an exact location while transmitting only a coarse geographic cell or zone identifier.

The Finality Sink may independently obtain current context and reject effectuation where the current context does not correspond to the committed context.

### 5.6 Beacon Session

Page 24

A Beacon Session is a bounded operational, cryptographic, temporal, mission, journey, device, or communication state during which one or more related Beacon Proof Capsules may share or derive common information.

Shared session information may include:

| x | cryptographic keys; |
|---|---|
| x | Binding Keys; |
| x | authentication keys; |
| x | dictionaries; |
| x | Authority References; |
| x | policy epochs; |
| x | revocation epochs; |
| x | freshness state; |
| x | counters; |
| x | session nonces; |
| x | device or sink identifiers; |
| x | context baselines; |
| x | time bases; |
| x | compression tables; |
| x | fragmentation state; |
| x | cached Authority Objects; |
| x | resolver state; or |
| x | reconstruction state. |

A Beacon Session may correspond, without limitation, to:

| x | a UAV flight; |
|---|---|
| x | portion of a flight; |
| x | payload-delivery mission; |
| x | vehicle journey; |
| x | autonomous-driving session; |
| x | road segment; |
| x | remote-assistance session; |
| x | cooperative manoeuvre; |
| x | fleet operation; |
| x | swarm mission; |
| x | communication association; |
| x | key lifetime; or |
| x | another bounded operational interval. |

A Beacon Session need not correspond to a network-layer session and need not require a connection-oriented transport.

Different Candidate Acts within a Beacon Session may remain separately bound and separately verifiable.

### 5.7 Protected Execution Domain

A Protected Execution Domain is a hardware, firmware, software, or mixed hardware-software execution environment having isolation, integrity, access-control, non-bypassability, protectedstate, or equivalent security properties sufficient to perform one or more execution-finality functions

Page 25

without permitting an untrusted component to synthesize, alter, or bypass the resulting authority decision.

A Protected Execution Domain may comprise or be implemented using:

| x | secure microcontroller; |
|---|---|
| x | safety processor; |
| x | secure coprocessor; |
| x | secure element; |
| x | hardware security module; |
| x | trusted execution environment; |
| x | protected hypervisor partition; |
| x | isolated processor core; |
| x | FPGA region; |
| x | ASIC; |
| x | vehicle domain controller; |
| x | automotive zonal controller; |
| x | protected gateway; |
| x | avionics safety controller; |
| x | protected autopilot partition; |
| x | baseband security processor; |
| x | lock-step processor; |
| x | attested software partition; |
| x | or another isolated execution mechanism. |

The Protected Execution Domain may hold or control one or more of:

| x | Binding Keys; |
|---|---|
| x | session keys; |
| x | sealed Authority Objects; |
| x | Authority References; |
| x | policy state; |
| x | revocation state; |
| x | freshness state; |
| x | nonce state; |
| x | replay state; |
| x | Context Commitments; |
| x | receipt-chain state; |
| x | delayed-disclosure evidence keys; |
| x | counters; |
| x | protected dictionaries; |
| x | Finality Sink configuration; |
| x | Safe-Action Set definitions; |
| x | protected execution capabilities; or |
| x | effectuation-release signals. |

In a UAV, the Protected Execution Domain may be located in or associated with the flight controller, autopilot, secure avionics controller, ESC controller, payload controller, or secure gateway.

In an autonomous or highly automated vehicle, the Protected Execution Domain may be located in or associated with an automated-driving controller, vehicle domain controller, zonal controller,

Page 26

motion controller, drive-by-wire safety controller, telematics security module, secure gateway, or another protected vehicle-processing component.

The Protected Execution Domain need not be physically separate from the Finality Sink, provided the required isolation and enforcement properties are preserved.

A mission computer, autonomous planner, AI component, vehicle planner, application processor, network transmitter, or other untrusted or less-trusted component may communicate with the Protected Execution Domain but is not thereby able to read protected secret state, forge protected predicates, fabricate valid release signals, or bypass the effectuation decision.

### 5.8 Binding Key

A Binding Key, denoted for example KbindK\_{bind}, is cryptographic secret material used directly or indirectly to generate or verify a keyed Binding Commitment.

The Binding Key may be:

| x | a symmetric key; |
|---|---|
| x | derived symmetric key; |
| x | session key; |
| x | device-specific key; |
| x | Finality-Sink-specific key; |
| x | act-class-specific key; |
| x | mission-specific key; |
| x | vehicle-session key; |
| x | fleet or swarm key; |
| x | key derived from a hardware root of trust; or |
| x | equivalent protected secret material. |

A representative derivation may be:

Kbind=HKDF(Kroot,DOMbind∥SessionNonce∥DeviceID∥SinkID)K\_{bind}=HKDF(K\_{root},DOM\_{bind }\\parallel SessionNonce\\parallel DeviceID\\parallel SinkID)

The Binding Key is preferably available only to components authorized to generate or verify the relevant Binding Commitment and unavailable to an untrusted mission computer, autonomous planner, AI component, transmitter, application processor, or other component capable of proposing or modifying the Candidate Act.

The Binding Key may be shared between a Protected Execution Domain and a Finality Sink, derived independently by both from common protected root material, or held within a single component where the Protected Execution Domain and Finality Sink are integrated.

Different Binding Keys may be used for different devices, vehicles, aircraft, Finality Sinks, sessions, act classes, missions, risk classes, or operational domains.

### 5.9 Finality Receipt

A Finality Receipt is a protected machine-verifiable record of an execution-finality decision produced or committed by a Protected Execution Domain or Finality Sink.

Page 27

A Finality Receipt may record an:

| x | ALLOW decision; |
|---|---|
| x | DENY decision; |
| x | SAFE-ACTION decision; |
| x | constrained-envelope decision; |
| x | degraded-mode decision; or |
| x | other finality outcome. |

A Finality Receipt may contain or cryptographically bind one or more of:

| x | decision value; |
|---|---|
| x | Candidate Act identifier or commitment; |
| x | Binding Commitment; |
| x | Finality Sink identifier; |
| x | Context Commitment; |
| x | policy epoch; |
| x | revocation epoch; |
| x | freshness value; |
| x | monotonic counter; |
| x | timestamp or interval identifier; |
| x | execution capability identifier; |
| x | Safe-Action Set selection; |
| x | reason or failure code; |
| x | previous receipt digest; or |
| x | other audit-relevant state. |

A representative receipt chain may satisfy:

Rn=AuthK(Headern∥Bn∥Countern∥H(Rn-1))R\_n = Auth\_K(Header\_n \\parallel B\_n \\parallel Counter\_n \\parallel H(R\_{n-1}))

or an equivalent authenticated chaining construction.

For an allowed Candidate Act, the Finality Receipt is preferably committed before the associated execution capability or release signal becomes usable.

For a denied Candidate Act, the Finality Receipt may record the denial without enabling the requested operation.

A Finality Receipt may later support:

| x | audit; |
|---|---|
| x | forensic reconstruction; |
| x | regulatory evidence; |
| x | fleet supervision; |
| x | aircraft or vehicle incident analysis; |
| x | observer-evidence correlation; or |
| x | conformance testing. |

A Finality Receipt is evidence of a decision and is not itself authority to perform an act.

Page 28

### 5.10 Act Evidence Record

An Act Evidence Record is a compact machine-verifiable record representing that a Protected Execution Domain made a particular execution-finality decision during a defined interval.

The Act Evidence Record may identify or encode one or more of:

| x | act class; |
|---|---|
| x | decision; |
| x | Finality Sink class; |
| x | device or pseudonymous device identity; |
| x | interval identifier; |
| x | monotonic receipt counter; |
| x | mission or session reference; |
| x | policy epoch; |
| x | privacy mode; or |
| x | another compact decision attribute. |

The record is authenticated using cryptographic evidence whose origin is controlled by the Protected Execution Domain.

In a preferred delayed-disclosure embodiment, the Act Evidence Record is authenticated with a key derived from a reverse one-way key chain, where the corresponding verification key material is disclosed only after a defined delay.

An Act Evidence Record may be broadcast or otherwise transmitted through:

| x | Remote ID; |
|---|---|
| x | V2X; |
| x | roadside communication; |
| x | UAV telemetry; |
| x | Wi-Fi; |
| x | BLE; |
| x | sidelink; |
| x | mesh; |
| x | fleet communication; |
| x | roadside infrastructure; |
| x | or another constrained transport. |

The Act Evidence Record may permit a third-party observer, infrastructure device, auditor, fleet operator, or authorized authority later to verify that the Protected Execution Domain issued the stated decision.

An Act Evidence Record does not itself prove that the physical effect actually occurred and is not accepted as execution authority.

### 5.11 Key Disclosure Record

A Key Disclosure Record is a compact machine-verifiable message carrying or identifying cryptographic key material that is intentionally disclosed after a predetermined interval to permit verification of one or more earlier Act Evidence Records.

Page 29

A Key Disclosure Record may comprise:

| x | record type; |
|---|---|
| x | epoch identifier; |
| x | interval index; |
| x | disclosed key; |
| x | key-chain position; |
| x | integrity information; or |
| x | other verification information. |

In a reverse one-way chain:

Ki=F(Ki+1)K\_i=F(K\_{i+1})

disclosure of KiK\_i may permit verification or derivation of earlier chain values while not revealing later undisclosed keys.

Key disclosure may occur periodically, opportunistically, redundantly, through more than one communication path, or after loss of an earlier disclosure message.

A Key Disclosure Record provides verification material only and does not authorize a Candidate Act.

### 5.12 Evidence Anchor

An Evidence Anchor is a cryptographically authenticated object that establishes a trusted starting point or trust association for later verification of Act Evidence Records or Key Disclosure Records.

An Evidence Anchor may bind one or more of:

| x | device identity; |
|---|---|
| x | pseudonymous device identity; |
| x | aircraft identity; |
| x | vehicle identity; |
| x | Protected Execution Domain key; |
| x | key-chain commitment; |
| x | evidence epoch; |
| x | initial interval; |
| x | timing parameters; |
| x | disclosure delay; |
| x | chain length; |
| x | starting receipt counter; |
| x | policy epoch; or |
| x | other parameters required for verification. |

The Evidence Anchor may be signed by:

| x | the Protected Execution Domain; |
|---|---|
| x | a device identity key; |
| x | vehicle or aircraft manufacturer credential; |
| x | fleet credential; |
| x | authority credential; |

Page 30

| x | hardware root of trust; or |
|---|---|
| x | another trusted signing entity. |

The Evidence Anchor may be transmitted repeatedly without being regenerated so that observers joining after the beginning of an evidence epoch can establish verification state.

A new Evidence Anchor may be generated when:

| x | a key chain is exhausted; |
|---|---|
| x | an evidence epoch changes; |
| x | policy state changes; |
| x | device identity changes; |
| x | privacy pseudonym changes; |
| x | ownership or fleet assignment changes; or |
| x | another trust transition occurs. |

The Evidence Anchor establishes evidence provenance and does not itself authorize effectuation.

### 5.13 Safe-Action Set

A Safe-Action Set is a protected, pre-authorized, bounded set of actions that are considered safetyincreasing, risk-reducing, state-preserving, or necessary to place or maintain a cyber-physical system in a defined safe or minimal-risk condition when a requested Candidate Act cannot be verified or permitted.

The Safe-Action Set may include different actions according to platform type, operating context, and safety architecture.

For a UAV or aerial platform, non-limiting Safe Actions may include:

| x | hover; |
|---|---|
| x | loiter; |
| x | altitude hold; |
| x | return to a defined safe waypoint; |
| x | return-to-home; |
| x | reduce speed; |
| x | reduce propulsion envelope; |
| x | terminate payload operation; |
| x | payload lock; |
| x | controlled landing; |
| x | emergency landing; |
| x | maintain current corridor where safe; |
| x | RF receive-only mode; |
| x | hazard or emergency signalling; or |
| x | another protected risk-reducing flight action. |

For an autonomous or highly automated vehicle, non-limiting Safe Actions may include:

| x | braking; |
|---|---|
| x | controlled deceleration; |
| x | lane keeping; |
| x | maintaining a safe lane; |

Page 31

| x | maintaining or reducing speed; |
|---|---|
| x | controlled stop; |
| x | minimal-risk manoeuvre; |
| x | hazard-light activation; |
| x | transition to a lower automation mode; |
| x | driver handover request; |
| x | pulling over where safely feasible; |
| x | maintaining a presently safe trajectory temporarily; or |
| x | another protected risk-reducing vehicle action. |

For robots or industrial devices, Safe Actions may include:

| x | stopping motion; |
|---|---|
| x | holding position; |
| x | reducing actuator energy; |
| x | retracting to a safe pose; |
| x | isolating power; |
| x | disabling a payload or tool; or |
| x | entering another bounded safe state. |

The Safe-Action Set is preferably:

| x | defined in protected firmware, protected configuration, or protected policy; |
|---|---|
| x | included in or associated with an attested system state; |
| x | unavailable for arbitrary widening by an untrusted mission computer, vehicle planner, AI component, remote operator, transmitter, or application; |

| x | bounded according to the safety capabilities of the device; and |
|---|---|
| x | separately distinguishable from ordinary authorized Candidate Acts. |

A Safe Action may remain available without fresh authority where withholding the Safe Action would increase risk.

The existence of a Safe-Action Set therefore permits the architecture to fail closed with respect to

**consequential or permission-expanding acts without requiring the system to fail unsafe.**

An operation outside the Safe-Action Set remains a Candidate Act and may require ordinary execution-finality verification before becoming effective.

## 6. SYSTEM ARCHITECTURE

A representative implementation comprises:

```
+ ------------------------------------------------------------------------------------------------------------------- +
```

| \| | HIGH-LEVEL CONTROL PLANE | \| |
|---|---|---|
| \| | AI Mission Computer / Pilot / Autonomy / Route Planner / | \| |
| \| | Vehicle Planner / Remote Assistance Interface | \| |

```
+----------------------------+--------------------------------------------------------------- +
| Proposed action
```

```
v
+ ------------------------------------------------------------------------------------------------------------------- +
```

| \| | CANDIDATE ACT CANONICALIZER | \| |
|---|---|---|
| \| | action class \| parameters \| target \| mission phase \| sink | \| |

Page 32

```
+----------------------------+--------------------------------------------------------------- +
|
v
+ ------------------------------------------------------------------------------------------------------------------- +
```

| \| | PROTECTED EXECUTION DOMAIN |  | \| |
|---|---|---|---|
| \| | Authority verification | Policy / revocation state | \| |
| \| | Freshness state | Context binding | \| |
| \| | Keyed act binding (K_bind) | Receipt chain | \| |
| \| | Compact-beacon encoder | Evidence key chain (K_N) | \| |

```
+---------------+---------------------------+ ----------------------------------- +
```

| \| | \| |
|---|---|
| \| Full protected state | \| Beacon Proof Capsule |
| \| | \| Act Evidence Records |
| v | v |

| +----------------+ |  | +------------------------------------------+ |  |
|---|---|---|---|
| \| Protected | \| | \| Beacon Transmitter | \| |
| \| State Store | \| | \| BLE/Wi-Fi/UWB/V2X | \| |
| +----------------+ |  | +----------+----------------------+ |  |

```
|
constrained radio or bus path
|
+------------------------+-------------------------------- +
v v
+------------------------------------------+ +------------------------------------------- +
| RECEIVING VERIFIER | | THIRD-PARTY OBSERVER |
```

| \| Beacon reconstruction | \| | \| | Anchor verification | \| |
|---|---|---|---|---|
| \| Authority-reference resolution | \| | \| | Safety condition | \| |
| \| Freshness / replay verification | \| | \| | Delayed key check | \| |
| \| Commitment verification | \| | \| | Record verification | \| |

```
+--------------------+----------------------------------------- + + -------------------------------------------+
v
+ ------------------------------------------------------------------------------------------------------------------- +
| FINALITY SINK |
```

Page 33

```
| Independently determines actual act |
| Reads current epochs inside atomic commit |
| Recomputes keyed binding; consumes nonce; commits receipt |
| Releases bounded execution capability only on match |
+----------------------------+--------------------------------------------------------------- +
| verification succeeds
v
+ ------------------------------------------------------------------------------------------------------------------- +
```

| \| | EFFECTUATION HARDWARE \| ESC / motor / payload latch / RF / camera / actuator / | \| \| |
|---|---|---|
| \| drive-by-wire permission envelope |  | \| |

```
+ ------------------------------------------------------------------------------------------------------------------- +
```

The receiving verifier and the Finality Sink may be the same component. The Act Evidence Records flow outward to observers and are never an input to authorization.

## 7. CANDIDATE ACT REPRESENTATION

A Candidate Act may be represented as a deterministic object. For example:

```
CandidateAct = {
version,
device_id,
mission_id,
action_class,
action_parameters,
target,
route_segment,
flight_or_driving_mode,
payload_state,
radio_state,
requested_time,
sink_id
}
```

The fields used depend on the action. For a flight manoeuvre:

| action_class | = FLIGHT_VECTOR |
|---|---|
| vx, vy, vz | = requested velocity components |
| yaw_rate | = requested yaw rate |
| altitude_target | = requested altitude |
| route_segment | = current corridor segment |
| sink_id | = flight-control sink |

For cargo release:

| action_class | = PAYLOAD_RELEASE |
|---|---|
| payload_id | = payload reference |
| release_zone | = zone identifier |
| release_altitude | = altitude |
| release_state | = latch state |

Page 34

# 7A. MATHEMATICAL AND CRYPTOGRAPHIC NOTATION

This section defines the principal symbols used by the mathematical constructions that follow. A locally redefined symbol in a later embodiment controls within that embodiment. The notation is descriptive of functional relationships and does not require a particular cryptographic library or processor implementation.

### 7A.1 General operators

**H(X): a collision-resistant cryptographic hash of X. Where a concrete profile is required, SHA-256 or another**

security-appropriate hash may be used.

**HMAC\_K(X): a keyed message-authentication code over X under protected key K. MAC\_K(X): a message-authentication function under K; HMAC is one non-limiting realization. HKDF(K, info): a key-derivation function deriving domain-separated key material from protected key K and**

context string info.

**Trunc\_b(X): the b-bit retained portion of X according to the profile-defined truncation convention. C(X): the deterministic or canonical byte serialization of X. X || Y: byte-string concatenation of X followed by Y. := definition or assignment of the expression on the right to the symbol on the left. => logical implication. X => Y means that whenever X holds, Y is required to hold. AND / OR / NOT: logical conjunction, disjunction, and negation. |S|: cardinality of set S. ||x||: the applicable vector or spatial norm; unless otherwise stated, Euclidean distance is a representative**

implementation.

### 7A.2 Core execution-finality values

**A: the Candidate Act. C(A) is its canonical representation. D\_A: the Act Commitment, for example H(DOM\_A || C(A)). D\_C: the Context Commitment over selected live or semi-live context. B: the full Binding Commitment joining the act to its sink, authority, epochs, context, freshness, and temporal**

scope.

**B\_t: the t-bit compact representation Trunc\_t(B). K\_root: protected root key material from which session- or role-specific keys may be derived. K\_bind: the protected act-binding key used to create or verify a keyed Binding Commitment. K\_B: a protected beacon- or capsule-authentication key distinct from K\_bind. K\_R: a protected key used to derive a compact Authority Reference where a keyed reference is selected. K\_frag: a protected key used to authenticate individual fragments in an authenticated multi-frame reconstruction**

profile.

**R\_n: Finality Receipt number n; H(R\_(n-1)) binds receipt n to the previous committed receipt where receipt**

chaining is used.

Page 34A

# 7A.3 RISK, SPATIAL, AND ORDERING NOTATION

### Compact-binding and authenticator sizing

**t: number of retained bits in B\_t = Trunc\_t(B). q: approximate number of distinct commitments in the relevant accidental-collision domain. W: attacker offline trial budget against an unkeyed compact commitment. A\_online: number of online substitution attempts admitted before lockout, key rotation, escalation, or equivalent**

response.

**m: retained authentication-tag length in bits. epsilon\_c: target upper bound allocated to accidental compact-commitment collision probability. epsilon\_s: target upper bound allocated to targeted substitution probability. epsilon\_f: target aggregate forgery-probability budget for a compact authenticator.**

```
P_coll ~= q(q-1) / 2^(t+1)
```

| P_sub | ~= W / 2^t P_sub <= A_online / 2^t | (unkeyed offline search) (keyed online attempts) |
|---|---|---|

### Spatial revalidation notation

**d(t): distance at time t from the current position to the nearest relevant boundary of the permitted region, positive**

on the permitted side.

**epsilon\_pos: protected position-uncertainty bound used for spatial authority. v\_max: maximum outward speed permitted by the current execution envelope. tau: worst-case enforcement-to-actuator reaction latency used by the profile. a\_brk: guaranteed magnitude of available deceleration used by the stopping-distance bound. s\_stop(v\_max): stopping-distance allowance v\_max\*tau + v\_max^2/(2\*a\_brk). Delta\_r: maximum interval before required spatial revalidation. p\_i, sigma\_i: position estimate from source i and its associated uncertainty measure. k: profile-selected positive uncertainty multiplier defining the required consistency/confidence margin. q\_min: minimum number of sufficiently independent or partially independent position sources required to satisfy**

the position-consistency rule.

### Bounded execution capability and atomic ordering

**K\_S: a protected sink-local capability-authentication key held by, derived within, or otherwise available only to the**

Protected Execution Domain, the applicable Finality Sink, and any specifically authorized downstream verifier of the bounded execution capability. K\_S is unavailable to the untrusted act-proposing component.

**E: a short-lived bounded execution capability. One representative form is:**

```
E = MAC_KS( B || SinkID || ActuatorEnvelope || Counter )
```

**X < Y: in the ordering expressions below, written in the specification with the strict-before symbol, X must**

complete before Y can occur.

**X <= Y: in the ordering expressions below, written in the specification with the no-later-than symbol, X occurs no**

later than Y; X and Y may be ordered within the same protected atomic transaction where the implementation provides equivalent crash-safe semantics. Thus, receipt commitment and replay-state consumption are not merely logging operations. They are ordered protected-state transitions that precede release of the capability and physical effectuation.

Page 34B

```
sink_id = payload-latch sink
```

For RF transmission:

```
action_class
channel
power_class
duration_class
traffic_class
sink_id
```

```
= RF_TRANSMISSION
= radio channel
= permitted power
= transmission duration
= communication class
= RF transmission sink
```

For a vehicle cooperative manoeuvre:

```
action_class
manoeuvre_id
trajectory_digest = digest of planned trajectory envelope
lane_group
speed_envelope
time_slot
sink_id
```

```
= COOPERATIVE_MANOEUVRE
= negotiated manoeuvre reference
```

```
= lane or lane-group identifier
= permitted speed band
= manoeuvre window
= vehicle motion-admission sink
```

## 8. CANONICALIZATION

The Candidate Act is converted into a deterministic byte representation.

Let () denote the canonical serialization of Candidate Act .

Canonicalization may use: fixed-width binary encoding; deterministic CBOR; deterministic protocol buffers; ASN.1 DER; canonical JSON; packed bit fields; deterministic TLV; a domain-specific beacon encoding; or another representation producing the same bytes for the same semantic act.

The Act Commitment is:

= (

where is a collision-resistant cryptographic hash, concatenation.

∥ ())

is a domain-separation constant, and ∥ denotes

Only load-bearing fields, meaning fields that change the resulting effect, are included, so that the Finality Sink can reconstruct () from the act actually pending at the sink.

## 9. CONTEXT COMMITMENT

A Context Object may comprise:

```
Context = {
geofence_or_zone_version,
corridor_id,
geographic_cell,
altitude_band_or_lane_group,
mission_phase,
payload_state,
radio_mode,
flight_or_driving_mode,
```

Page 35

```
policy_epoch,
revocation_epoch,
time_slot
}
```

The Context Commitment is:

= ( ∥ ( ))

A context field need not reveal precise coordinates. For privacy-sensitive operation, exact location may remain inside the protected domain while the beacon carries only: geographic cell; zone identifier; corridor digest; geofence-version hash; or context commitment.

## 10. BINDING COMMITMENT

In a preferred embodiment, the Protected Execution Domain computes a keyed binding commitment:

= ( ∥ ∥ ∥ ∥ ∥ ∥ ∥ ∥ )

where:

- = Binding Key, held by the Protected Execution Domain and the Finality Sink and not available to the mission computer, transmitter, or other untrusted component;
- = Act Commitment;
- = Finality Sink identifier;
- = Authority Reference;
- = Policy Epoch;
- = Revocation Epoch;
- = Context Commitment;
- = nonce, sequence, or freshness value;
- = expiry or validity information. may be provisioned per sink, derived per session (Section 33), or derived per device and sink class. In an alternative embodiment, an unkeyed commitment is used:

= ( ∥ ∥ ∥ ∥ ∥ ∥ ∥ ∥ )

in which case the retained length is selected against attacker offline work as described in Section 11.2. This prevents the beacon from being transferable merely because the bearer possesses the beacon bytes. Changing the act, sink, authority, policy epoch, context, nonce, or expiry changes .

## 11. COMPACT COMMITMENT

The constrained beacon may not carry the full value . Accordingly, a compact commitment is generated:

Page 36

= ()

where is the number of retained bits. The value is selected according to explicit budgets rather than arbitrarily.

# 11.1 Collision budget (accidental coincidence)

If approximately distinct commitments may exist within the relevant collision domain, the approximate birthday-collision probability is:

( - 1) ≈

2+1

For target collision probability , a deployment may select:

( - 1))⌉ ≥ ⌈log2 (

# 11.2 Attacker-work budget (targeted substitution)

The birthday bound addresses accidental coincidence only. A compromised mission computer, transmitter, or other party that knows or can predict every input to an unkeyed commitment may search offline for a substituted act ' with (( ' )) = . With offline work of hash evaluations, the success probability is approximately:

W

≈

For an unkeyed commitment and target substitution probability :

≥ ⌈log2 ( )⌉

For a keyed commitment (Section 10), offline search is not possible without . A targeted substitution then requires online attempts, each of which consumes freshness state, and:

≤

where is the number of online verification attempts permitted before lockout, key rotation, or escalation.

# 11.3 Selection

This allows the field size to be selected according to: fleet size; action rate; beacon-session lifetime; replaycache duration; safety class; acceptable collision probability; whether the commitment is keyed; and attacker work or attempt budget. High-consequence actions may use a longer commitment than low-risk telemetry.

Page 37

## 12. BEACON PROOF CAPSULE

A representative Beacon Proof Capsule may contain:

```
BPC {
version
profile_id
action_class
sink_class
authority_ref
policy_epoch
revocation_epoch
freshness
expiry_delta
context_ref_or_digest
act_binding_commitment
flags
authenticator
}
```

Not all fields need be transmitted explicitly.

Some fields may be: implicit from radio channel; cached from session establishment; dictionary indexed; delta encoded; combined; omitted where statically configured; or recovered from protected local state.

## 13. REPRESENTATIVE COMPACT SINGLE-FRAME PROFILE

One non-limiting implementation may allocate approximately 24 to 48 bytes.

For example:

```
Field                        Example Length
```

| Version + Profile | 1 byte |
|---|---|
| Action Class | 1 byte |
| Sink Class | 1 byte |
| Flags | 1 byte |
| Authority Reference | 4 bytes |
| Policy Epoch | 2 bytes |
| Revocation Epoch | 2 bytes |
| Freshness / Sequence | 4 bytes |
| Expiry Delta | 2 bytes |
| Context Commitment | 4-8 bytes |
| Act Binding Commitment (keyed) | 8-12 bytes |
| Authenticator | 8-16 bytes |

This layout is illustrative only. The invention is not limited to any particular byte count.

## 14. FIELD COMPRESSION METHODS

# 14.1 Dictionary Compression

Repeated strings are replaced by compact indices.

Page 38

Example:

```
0x01 = FLIGHT_CONTROL_SINK
0x02 = PAYLOAD_LATCH_SINK
0x03 = RF_TX_SINK
0x04 = CAMERA_SINK
0x05 = VEHICLE_MOTION_ADMISSION_SINK
```

Similarly:

```
0x01 = FLIGHT_VECTOR
0x02 = LAND
0x03 = PAYLOAD_RELEASE
0x04 = SENSOR_ACTIVATE
0x05 = RF_TRANSMIT
0x06 = COOPERATIVE_MANOEUVRE
0x07 = REMOTE_ASSIST_PATH
```

# 14.2 Authority-Reference Compression

Instead of transmitting an entire mission authorization of several hundred bytes, the beacon may contain a 32-bit or 64-bit protected reference, which the receiver resolves from a protected cache. The cached object is preferably indexed by a keyed reference:

= ( ( ℎ ))

where is a domain-specific secret not available to the transmitter or mission computer. A keyed reference prevents an attacker from constructing, offline, a different authority object whose truncated reference collides with a cached one. An unkeyed reference (( ℎ )) may be used where is sized under the attacker-work budget of Section 11.2.

# 14.3 Time Delta Encoding

Instead of transmitting a full timestamp , the beacon may carry:

Δ = - ℎ\_

or a time-slot identifier.

# 14.4 Geographic Compression

Exact latitude and longitude need not be transmitted. The system may bind the act to: corridor index; geographic tile; geohash; airspace-cell identifier; roadsegment or lane-group identifier; altitude band; zone digest; or permitted-drop-zone reference.

# 14.5 State Compression

Multiple Boolean predicates may be represented in a bitmap. Example:

```
Bit 0 authority_valid
Bit 1 geofence_valid
```

Page 39

| Bit 2 | payload_authority_valid |
|---|---|
| Bit 3 | remote_identification_required |
| Bit 4 | radio_authority_valid |
| Bit 5 | quorum_required |
| Bit 6 | degraded_mode |
| Bit 7 | fragmentation_present |
| The bitmap | itself is not trusted unless covered by the cryptographic authenticator, and it never substitutes for |
| the sink's | own evaluation of the predicates it represents. |

## 15. AUTHENTICATION OF THE COMPACT CAPSULE

A Beacon Proof Capsule may be authenticated using: HMAC; AES-CMAC; GMAC; Poly1305; EdDSA; ECDSA; post-quantum signatures; one-time signatures; hash-based authentication; TESLA-like delayed authentication (Section 67A); group authentication; pairwise keys; derived session keys; or another integrity mechanism. A compact symmetric implementation may calculate:

= ( ( ))

For desired forgery probability, in the idealized single-attempt case:

The selected tag size may depend on: risk class; attacker attempt budget; beacon lifetime; fleet size; and transport capacity.

## 16. MULTI-FRAME AUTHENTICATED FRAGMENTATION

Where the required evidence exceeds a single beacon frame, the Beacon Proof Capsule may be fragmented. Let be the encoded proof. For each fragment:

A root commitment may be:

Each fragment authenticator may bind:

≤ 2 -

= 0 ∥ 1 ∥ ⋯ ∥ -1

= ( , , , , , ℎ )

= ( ∥ )

Page 40

ℎ = ( ∥ ∥ ∥ ∥ )

The receiver SHALL NOT treat any fragment individually as execution authority. Only after obtaining a sufficient authenticated fragment set does the receiver reconstruct

' = 0 ∥ ∥ ⋯ ∥

1 -1

and verify

( ∥ ' ) =

Only then may normal finality verification continue.

## 17. PROTECTION AGAINST CROSS-SESSION FRAGMENT MIXING

A fragment from one Beacon Proof Capsule must not be combinable with fragments from another. Accordingly, each fragment is bound to: session ID; root commitment; fragment count; fragment index; freshness state; policy epoch; and/or device-specific value. For two fragment sets and ' , either

≠ or ≠

' '

causes reconstruction failure.

## 18. PARTIAL-RECEPTION RULE

A central safety invariant is:

⇒

Formally:

( ) ≠ ⇒ () =

Thus a missing fragment, corrupted fragment, unknown authority reference, unresolved context reference, stale epoch, invalid tag, ambiguous sink, collision condition, missing nonce state, or incomplete reconstruction does not silently degrade into authorization. "No effectuation" of a consequential act does not remove access to the Safe-Action Set (Section 51 and Section 67B).

## 19. ACTUAL-ACT RECONSTRUCTION AT THE FINALITY SINK

The receiver does not rely solely on the sender's claimed act.

Page 41

The Finality Sink independently derives the actual requested effect. For example, a flight-control sink may read:

```
actual_pwm
actual_target_velocity
actual_yaw_rate
actual_flight_mode
actual_route_segment
```

A payload sink may read:

```
actual_latch
actual_payload_id
actual_release_request
actual_altitude
actual_attitude
```

A vehicle motion-admission sink may read:

```
actual_planned_trajectory_envelope
actual_lane_group
actual_speed_band
actual_driving_mode
```

The actual Candidate Act is canonicalized as and

= ( ∥ ( ))

The sink reconstructs using the same binding rules, including The effect is authorized only if

( ) =

and every other required predicate succeeds.

## 20. CORE FINALITY PREDICATE

A representative decision predicate is:

= ℎ

∧ ∧

∧

ℎ ℎ ∧ ∧

∧ ℎ ∧

∧

Effectuation occurs only if = , where evaluated inside the atomic finality commit (Section 44).

## 21. REPLAY PREVENTION

The Finality Sink maintains protected replay state.

Page 42 where the binding is keyed.

ℎ ∧

ℎ

and are

For a freshness identifier :

```
if N in consumed_nonce_set:
deny
```

Upon successful verification:

```
consume(N)
```

Consumption is atomically committed before the act becomes effective:

() ≺ ()

where ≺ means "must occur before."

## 22. POLICY-EPOCH VALIDATION

The Beacon Proof Capsule may contain representing the policy epoch. The sink maintains . The beacon may be accepted only if

=

or satisfies an explicitly permitted epoch-compatibility rule. Where policy state is unavailable, for high-assurance profiles:

⇒

The value SHALL be read inside the same atomic section in which the nonce is consumed and the capability is committed. An earlier read may be used only as a fast pre-check and never as the deciding read.

## 23. REVOCATION-EPOCH VALIDATION

Similarly,

= may be required, with read inside the atomic finality commit. A stale Beacon Proof Capsule therefore becomes unusable following revocation-state advancement, including a revocation that arrives between an early pre-check and the commit.

## 24. CONTEXT REVALIDATION

The system may recompute live context immediately before effectuation. Example:

Page 43

ℎ =

∧ ℎ ∧ ℎ ∧ ℎ ℎ

∧

A beacon generated before a context change may therefore fail later even if cryptographically authentic.

# 24.1 Boundary-proximity revalidation bound

Where authority covers a spatial volume or corridor and is revalidated periodically, let () be the distance from the current position to the nearest boundary of the permitted volume (positive inside), the positionuncertainty bound, the permitted speed, the enforcement-to-actuator reaction latency, and the guaranteed deceleration. The stopping distance is

2

( ) = +

2 and a sufficient condition for never leaving the volume undetected is

Δ + ( ) + ≤ ()

so the revalidation interval is scheduled as

() - - ( ) Δ () ≤

If the right-hand side is less than or equal to zero, no further outward motion is released; the protected domain reduces (which increases the bound) or selects an action from the Safe-Action Set. Revalidation frequency therefore rises automatically near boundaries.

Worked example (illustrative): = 60 m, = 5 m, = 15 m/s, = 5 m/s2, = 0.1 s gives

= 24 m and Δ ≤ 2.07 s. At = 30 m the bound falls to 0.07 s, and reducing to 8 m/s gives = 7.2 m and Δ ≤ 2.23 s.

# 24.2 Multi-source position consistency

Given position sources with estimates and one-sigma uncertainties , the protected domain may require

∀,∶ ‖ - ‖ ≤ ( + ), ∶= max with at least ≥ 2 agreeing sources. Disagreement is treated as insufficient location confidence, which

removes authority for spatially scoped acts rather than steering them.

## 25. UAV EMBODIMENT

A UAV may include: mission computer; autopilot; secure microcontroller; flight controller; ESC; motor controller; GNSS/RTK receiver; IMU; barometer; visual-inertial odometry; geofence database; payload controller; radio; camera or sensor subsystem; Beacon Proof Capsule transmitter; Act Evidence Record transmitter; and Finality Sink verification logic. A mission computer proposes:

Page 44

```
Move from waypoint W1 to W2
```

The protected domain creates:

```python
CandidateAct {
action_class = WAYPOINT_TRANSITION
from = W1
to = W2
corridor = C7
altitude_band = A3
sink = FLIGHT_CONTROLLER
}
```

The context includes: geofence version; mission phase; policy epoch; revocation epoch; and current flight state.

A Beacon Proof Capsule is emitted. The flight-controller-side Finality Sink verifies that the actual waypoint transition still corresponds to the committed act. The mission computer cannot reuse the beacon to authorize: a different waypoint; another altitude band; another corridor; another flight controller; another mission phase; or another time window. Because the binding is keyed, the mission computer also cannot search offline for a different waypoint that produces the same compact commitment.

## 26. ESC EMBODIMENT

The Candidate Act may represent a permitted thrust or PWM envelope. For example:

≤ ≤

The beacon may bind: ESC identifier; motor set; PWM envelope; flight mode; time slot; policy epoch; and nonce. The ESC-side Finality Sink verifies the Beacon Proof Capsule before enabling the requested motor command. Within an authorized envelope, individual setpoints at the control rate are admitted by range comparison without per-setpoint beacon verification, and leaving the envelope or its time window ends the authorization. If validation fails:

```
ESC_ENABLE = 0
```

or the output may be clamped to a protected safe envelope.

## 27. PAYLOAD-RELEASE EMBODIMENT

For non-weapon cargo, inspection, emergency-supply, sensor, agricultural, logistics, or equivalent payload systems, the Candidate Act may represent a physical payload operation. Example:

Page 45

```
CandidateAct {
action_class = PAYLOAD_RELEASE
payload_id = P7
drop_zone = DZ4
altitude_class = A2
sink = PAYLOAD_CONTROLLER
}
```

The protected context may include: airspace authorization; drop-zone validity; attitude stability; mission phase; customer authorization; operator authorization; and policy epoch. The payload controller remains locked unless verification succeeds.

## 28. GEOFENCE EMBODIMENT

The geofence state may be represented by , where is the active geofence version. The binding commitment includes () or a protected geofence-version identifier. If

≠

the Candidate Act remains non-effective. This prevents a previously valid beacon from authorizing entry after a geofence update.

## 29. REMOTE-IDENTIFICATION-ADJACENT EMBODIMENT

The invention may operate: alongside an existing remote-identification broadcast; in a separate vendor extension; in a parallel protected beacon; through a link-layer extension; in a companion discovery frame; through an authenticated reference carried by an existing beacon; through a resolver keyed from information available in the identification transmission; or as an authentication payload type carried within, or covered by, the authentication or manifest structures of an identification protocol. The invention does not require modification of any particular remote-identification standard. The identification function and execution-finality function may remain logically distinct. A remote identification message may answer:

```
Which aircraft is this?
```

while the Beacon Proof Capsule may answer:

```
Is this exact impending effect cryptographically permitted at this sink,
under this freshness state and this authority context?
```

and the Act Evidence Record (Section 67A) may answer:

```
Did this aircraft's protected domain decide this act before it happened?
```

## 30. CACHE-ASSISTED VERIFICATION

The sink may cache verified Authority Objects.

Page 46

For example:

```
AuthorityCache[AuthorityRef] = {
authority_object,
authority_digest,
expiry,
policy_epoch,
revocation_epoch
}
```

The Beacon Proof Capsule then carries only the short AuthorityRef. A cached entry is usable only where its epoch and expiry remain current.

## 31. CACHE-MISS BEHAVIOUR

Where the AuthorityRef is not found, the sink may:

1. deny immediately;
2. request the full Authority Object;
3. enter a non-effective waiting state;
4. permit only an explicitly defined safe degraded mode; or
5. resolve the reference through an authenticated gateway. A cache miss is not equivalent to authorization.

## 32. RESOLVER-ASSISTED MODE

A protected resolver may receive:

```
AuthorityRef
BindingCommitment
DeviceRef
PolicyEpoch
```

and return:

```
ResolvedAuthorityObject
ResolverProof
```

The resolver does not determine the final physical effect. The downstream Finality Sink still checks the actual Candidate Act.

## 33. SESSION KEY DERIVATION

A beacon-session key and a session binding key may be derived as:

= ( , "BEACON" ∥ ∥ ∥ ℎ ∥ )

= ( , "BIND" ∥ ∥ ∥ )

Page 47

This permits low-cost symmetric verification during the constrained hot path while preserving separation between sessions and between authentication and binding functions.

## 34. KEY EVOLUTION ACROSS BEACON CYCLES

Two distinct key-evolution structures are used, and they are not interchangeable.

**Forward ratchet (erasure of past state). Where keys are never disclosed and the aim is that compromise**

of current state does not expose past session keys, keys may evolve as with erased after use. Because anyone who learns can compute every later key, a forward ratchet SHALL NOT be used where any key value is disclosed for verification or may be exposed to a verifier.

**Reverse one-way chain (delayed disclosure). Where key values are disclosed so that verifiers can authen-**

ticate earlier records, the chain SHALL run in reverse:

+1 =

= (+1),

( )

= - 1,…,0 so that disclosure of reveals only earlier keys and no later key (Section 67A). The receiver may reject prior key states after advancement. This limits replay of old beacons.

## 35. QUORUM EMBODIMENT

A high-consequence Candidate Act may require more than one authority.

Let = {1, 2, … , } and threshold .

The act is authorized only if

∣{ ∶ ( ) = }∣ ≥

The Beacon Proof Capsule may carry: quorum-set reference; quorum digest; aggregate-signature reference; threshold proof reference; or compact quorum bitmap.

## 36. SWARM AND FLEET EMBODIMENT

In a swarm or fleet, each UAV or vehicle may receive a common high-level proposal while maintaining its own locally verified Beacon Proof Capsule. Unit computes

= ( ∥ ∥ ∥ )

,

Thus a beacon valid for Unit 1 does not automatically authorize Unit 2. For a coordinated act requiring every participating unit to act or none to act, each unit prepares by reserving its freshness state and verifying predicates for the post-act state without moving, and releases its capability

Page 48

only after reading a single committed decision for the coordinated act from a decision log that accepts exactly one of COMMIT or ABORT. If the decision log is unreachable, each unit holds its current safe state and never commits on silence.

## 37. FAILURE MODES

The system may distinguish:

```
INVALID_SIGNATURE
UNKNOWN_AUTHORITY_REF
EXPIRED
REPLAY
POLICY_EPOCH_MISMATCH
REVOCATION_EPOCH_MISMATCH
SINK_MISMATCH
ACT_MISMATCH
CONTEXT_MISMATCH
FRAGMENT_MISSING
FRAGMENT_ROOT_MISMATCH
UNSUPPORTED_PROFILE
AMBIGUOUS_RECONSTRUCTION
COLLISION_GUARD_TRIGGERED
LOCATION_CONFIDENCE_INSUFFICIENT
RECEIPT_STORE_UNAVAILABLE
RECEIPT_PRESENTED_AS_AUTHORITY
EVIDENCE_PRESENTED_AS_AUTHORITY
```

Each may result in: deny; hold; request refresh; safe hover; safe landing; payload lock; RF silent mode; limited flight; reduced actuation; minimal-risk manoeuvre; or other protected safe behaviour. Each denial produces a Finality Receipt.

## 38. COLLISION-GUARD MECHANISM

Where a truncated commitment is used, a receiver may detect ambiguity. For example, if two cached full commitments satisfy the same short value

(1) = (2), 1 ≠ 2

the sink classifies the short commitment as ambiguous. Then

⇒

and the sink may request a longer commitment profile.

## 39. ADAPTIVE COMMITMENT LENGTH

The commitment length may increase with risk. For example:

Page 49

```
Risk Class 0 -> 48-bit commitment (keyed binding only)
Risk Class 1 -> 64-bit commitment
Risk Class 2 -> 96-bit commitment
Risk Class 3 -> 128-bit commitment
```

The values are illustrative. Short commitments such as 48 bits are used only with a keyed binding (Section 10); an unkeyed commitment is sized under Section 11.2. A payload operation may therefore carry stronger compact evidence than routine telemetry.

## 40. ADAPTIVE AUTHENTICATOR LENGTH

Likewise:

```
tag_bits = f(risk_class, expected_attempts, session_duration, fleet_size)
```

A representative lower bound may be

≥ ⌈log2 ( )⌉ where is the expected number of attacker verification attempts and is the permitted aggregate forgery probability.

## 41. LATENCY ARCHITECTURE

The architecture separates the following.

**Cold-path operations: certificate-chain verification; authority ingestion; policy parsing; resolver synchro-**

nization; geofence-map or zone-map verification; authority-cache creation; key establishment; evidencechain generation and anchor signing.

**Hot-path operations: parse compact beacon; look up Authority Reference; verify compact authenticator; re-**

compute keyed Candidate Act binding; compare commitment; inside the atomic section, read current epochs, check and consume nonce, and commit receipt; release or withhold bounded capability; compute evidence record tag. This separation enables strong authority semantics without placing full public-key or policy processing in every actuation cycle.

## 42. REPRESENTATIVE HOT-PATH COMPLEXITY

A representative verification operation may have approximate complexity

= + + + + + +

ℎℎ

Remote network access is not required where the authority information is cached locally.

## 43. BOUNDED EXECUTION CAPABILITY

Successful Beacon Proof Capsule verification need not directly execute the Candidate Act.

Page 50

Instead, the Finality Sink may issue a short-lived internal execution capability

= ( ∥ ∥ ∥ )

The actuator executes only if verifies. This creates distinct steps:

```
Beacon verification
-> atomic commit (current epochs, nonce consumed, receipt committed)
-> local bounded execution capability
-> physical effect
```

## 44. ATOMIC STATE UPDATE AND RECEIPT BEFORE RELEASE

Current-epoch reading, replay-state consumption, receipt commitment, and capability release are performed in one atomic finality commit. Representative invariants:

⇒ ∧ ℎ ⪯ ⪯ () ≺ ≺ ()

The Finality Receipt contains at least: decision; binding commitment ; sink identifier; context digest; monotonic counter ; previous receipt digest; and, for denials, the selected safe action. It is signed or authenticated by the Protected Execution Domain. Denials also produce receipts. A crash between verification and replay-state update must not result in duplicate effectuation. If the receipt or replay store is unavailable, the decision is DENY. A Finality Receipt is evidence and is never accepted as authorization.

## 45. REPRESENTATIVE PSEUDOCODE - BEACON GENERATION

```
FUNCTION GenerateBeaconProofCapsule(candidate_act, sink_id,
authority_object, live_context):
ENTER_PROTECTED_DOMAIN()
IF NOT VerifyAuthority(authority_object):
RETURN DENY
IF NOT AuthorityAllows(authority_object, candidate_act, live_context):
RETURN DENY
```

| policy_epoch | = ReadPolicyEpoch() |
|---|---|
| revocation_epoch | = ReadRevocationEpoch() |
| nonce | = ReserveFreshNonce() |

Page 51

```
act_digest = HASH("ACT" || Canonicalize(candidate_act))
context_digest = HASH("CTX" ||
Canonicalize(SelectBoundContext(live_context)))
authority_ref = TRUNCATE(HMAC(K_R, authority_object), ref_bits)
```

```
binding = HMAC(K_bind(sink_id),
"BIND" || act_digest || sink_id || authority_ref ||
policy_epoch || revocation_epoch || context_digest ||
nonce || Expiry(candidate_act))
```

```
commitment_length = SelectCommitmentLength(candidate_act.risk_class,
keyed = TRUE)
compact_binding = TRUNCATE(binding, commitment_length)
```

```
unsigned_bpc = EncodeCompact(version, profile_id,
candidate_act.action_class,
SinkClass(sink_id), authority_ref,
policy_epoch, revocation_epoch, nonce,
ExpiryDelta(candidate_act),
CompactContext(context_digest),
compact_binding, flags)
```

```
tag = TRUNCATE(HMAC(BeaconSessionKey(), unsigned_bpc),
SelectTagLength(candidate_act.risk_class))
```

```
bpc = unsigned_bpc || tag
IF Size(bpc) <= TransportFrameBudget():
RETURN bpc
RETURN AuthenticatedFragment(bpc)
```

## 46. REPRESENTATIVE PSEUDOCODE - FINALITY VERIFICATION

```
FUNCTION VerifyAndEffectuate(received_beacon_data, actual_sink_state):
bpc = ReconstructBeaconProofCapsule(received_beacon_data)
IF bpc == INCOMPLETE OR bpc == INVALID:
RETURN DenyWithReceipt(FRAGMENT_OR_FORMAT_FAILURE)
IF NOT VerifyBeaconAuthenticator(bpc):
RETURN DenyWithReceipt(INVALID_SIGNATURE)
IF IsExpired(bpc):
RETURN DenyWithReceipt(EXPIRED)
# Fast pre-checks only; the deciding reads occur inside the atomic
# section below.
IF PolicyEpoch(bpc) != CurrentPolicyEpoch_PreCheck():
RETURN DenyWithReceipt(POLICY_EPOCH_MISMATCH)
IF IsConsumed_PreCheck(bpc.nonce):
```

Page 52

```
RETURN DenyWithReceipt(REPLAY)
authority = ResolveAuthority(bpc.authority_ref)
IF authority == UNKNOWN:
RETURN DenyWithReceipt(UNKNOWN_AUTHORITY_REF)
candidate_act = ReconstructActualCandidateAct(actual_sink_state)
live_context = ReadLiveContext()
IF NOT PositionConsistent(live_context):
RETURN DenyWithReceipt(LOCATION_CONFIDENCE_INSUFFICIENT)
IF NOT AuthorityAllows(authority, candidate_act, live_context):
RETURN DenyWithReceipt(CONTEXT_MISMATCH)
```

```
act_digest = HASH("ACT" || Canonicalize(candidate_act))
context_digest = HASH("CTX" ||
Canonicalize(SelectBoundContext(live_context)))
sink_id = SinkID(actual_sink_state)
```

```
expected_binding = HMAC(K_bind(sink_id),
"BIND" || act_digest || sink_id ||
bpc.authority_ref || bpc.policy_epoch ||
bpc.revocation_epoch || context_digest ||
bpc.nonce || bpc.expiry)
```

```
IF TRUNCATE(expected_binding, bpc.commitment_length)
!= bpc.compact_binding:
RETURN DenyWithReceipt(ACT_MISMATCH)
```

```
BEGIN_ATOMIC_FINALITY_COMMIT()
```

```
# Deciding currentness reads, inside the atomic section.
IF bpc.policy_epoch != CurrentPolicyEpoch():
ABORT; RETURN DenyWithReceipt(POLICY_EPOCH_MISMATCH)
IF bpc.revocation_epoch != CurrentRevocationEpoch():
ABORT; RETURN DenyWithReceipt(REVOCATION_EPOCH_MISMATCH)
```

```
IF NOT ConsumeNonce(bpc.nonce):
ABORT; RETURN DenyWithReceipt(REPLAY)
```

```
receipt = MakeFinalityReceipt(decision = ALLOW,
IF NOT CommitReceipt(receipt):
ABORT; RETURN DENY_RECEIPT_STORE_UNAVAILABLE
capability = DeriveLocalExecutionCapability(expected_binding,
```

```
binding = expected_binding,
```

| sink | = sink_id, |
|---|---|
| context | = context_digest, |
| counter | = NextCounter(), |
| prev | = LastReceiptDigest()) |

```
candidate_act)
```

Page 53

```
CommitCapabilityState(capability)
END_ATOMIC_FINALITY_COMMIT()
EmitActEvidence(receipt) # Section 67A, optional
```

```
RETURN ReleaseToFinalitySink(capability, candidate_act)
FUNCTION DenyWithReceipt(code):
receipt = MakeFinalityReceipt(decision = DENY, code = code,
counter = NextCounter(),
prev = LastReceiptDigest(),
safe_action = SelectSafeAction(code))
CommitReceipt(receipt) # if unavailable, remain denied
EmitActEvidence(receipt)
RETURN DENY_NO_EFFECT
```

## 47. REPRESENTATIVE PSEUDOCODE - FRAGMENT RECONSTRUC- TION

```
FUNCTION ReconstructBeaconProofCapsule(fragment_set):
IF fragment_set is empty:
RETURN INCOMPLETE
```

| session_id | = fragment_set[0].session_id |
|---|---|
| root | = fragment_set[0].root |
| expected_count | = fragment_set[0].fragment_count |

```
FOR fragment IN fragment_set:
IF fragment.session_id != session_id: RETURN INVALID
IF fragment.root != root: RETURN INVALID
IF fragment.fragment_count != expected_count: RETURN INVALID
IF NOT VerifyFragmentAuth(fragment): RETURN INVALID
IF NumberOfUniqueFragments(fragment_set) != expected_count:
RETURN INCOMPLETE
ordered = SortByFragmentIndex(fragment_set)
payload = CONCAT(ordered.payloads)
IF HASH("FRAGMENT_ROOT" || payload) != root:
RETURN INVALID
RETURN payload
```

## 48. NON-BEARER PROPERTY

Possession of the Beacon Proof Capsule alone is not sufficient to produce the effect.

Page 54

The capsule is bound to

+ + ℎ + + ℎ

under a key that the bearer does not hold. Therefore copying the beacon to another device, another actuator, another time, or another operation produces a binding mismatch, and constructing a different operation with the same compact commitment requires the binding key.

## 49. DESIGN-AROUND RESISTANCE

The invention is not avoided merely by:

- calling the message telemetry, a status message, or a manoeuvre message instead of a beacon;
- using BLE instead of Wi-Fi, Wi-Fi instead of UWB, or V2X sidelink instead of either;
- using mesh instead of broadcast;
- using a proprietary aviation or vehicle link;
- replacing a hash or HMAC with another collision-resistant commitment or pseudorandom function;
- replacing CBOR with fixed-width binary encoding;
- using a token index instead of an Authority Reference;
- using a gateway instead of an onboard resolver;
- storing the full authority object in the sink;
- using one frame instead of several, or multiple fragments instead of a single capsule;
- moving verification from a microcontroller to an FPGA;
- moving the sink into the ESC, the flight controller, the payload controller, the RF chain, or a vehicle domain controller;
- using software where protected software satisfies the required non-bypassability;
- transmitting the compact proof adjacent to rather than inside an identification message;
- replacing delayed key disclosure with another time-bounded symmetric broadcast authentication in which the evidence key is held only by the protected domain; or
- carrying Act Evidence Records inside, or under the manifest of, an identification protocol.

## 50. SECURITY PROPERTIES

The architecture may provide one or more of the following properties.

**Exact-act binding. A beacon for act 1 is not valid for materially different act 2. Offline-search resistance. Without the binding key, no party can compute a substituted act matching a**

compact commitment.

**Sink binding. A beacon for sink 1 is not valid at sink 2. Freshness. A stale beacon is rejected. Replay resistance. A consumed nonce cannot authorize another effect. Policy continuity. A prior policy epoch does not automatically authorize operation under a newer policy**

epoch, and the deciding read occurs inside the atomic commit.

**Revocation continuity. Revocation-state change invalidates stale proof, including between pre-check and**

commit.

Page 55

**Context continuity. A geofence, zone, or corridor change can invalidate an otherwise authentic beacon. Fragment integrity. Fragments from different proofs cannot be mixed. Partial-evidence safety. Incomplete evidence cannot authorize effectuation. Collision awareness. Digest truncation is managed according to explicit collision and attacker-work budgets. Receipt-before-release. Every released capability has a committed receipt. Evidence origin. Broadcast act evidence can be produced only by the protected domain. Safety asymmetry. Safe actions remain available when consequential acts are denied.**

## 51. SAFE-DEGRADATION MODES

Failure need not result in catastrophic shutdown. Depending on system class, the protected domain may allow: hover; loiter; altitude hold; return-to-home; controlled landing; route freeze; motor-output limiting; payload lock; RF receive-only mode; diagnosticonly communication; low-power mode; reduced sensor capability; braking; lane keeping; speed reduction; minimal-risk manoeuvre; hazard signalling; or operator escalation. These actions form the Safe-Action Set. The Safe-Action Set is fixed in protected firmware or logic, is part of the attested measurement, and cannot be widened by the mission computer. Any degraded action outside the Safe-Action Set may itself be represented as a new Candidate Act.

## 52. EXEMPLARY USE CASE

A delivery UAV approaches a customer delivery zone. The mission computer proposes:

```
release cargo at DZ-207
```

The protected domain determines:

| geofence version | = 151 |
|---|---|
| mission phase | = DELIVERY |
| payload ID | = PKG-31 |
| drop-zone ref | = DZ-207 |
| altitude class | = LOW |
| sink | = payload latch controller |
| policy epoch | = 409 |
| revocation epoch | = 93 |
| nonce | = 0x88310271 |
| A keyed binding commitment | is generated. |
| The beacon contains only: | action class; sink class; authority reference; epochs; nonce; drop-zone context |
| reference; 96-bit keyed | binding commitment; and authentication tag. |
| The payload controller | independently reads: actual payload ID; actual altitude; actual latch state; and actual |

geographic zone. It recomputes the binding.

Page 56

If the UAV has moved outside DZ-207 since issuance, ℎ = and the payload latch remains locked; a denial receipt is committed. If the checks pass, the receipt is committed, the latch is powered for its window, and an Act Evidence Record (PAYLOAD\_RELEASE, ALLOW) is broadcast, which a nearby observer can verify a few seconds later under Section 67A.

## 53. SECOND EXEMPLARY USE CASE - FLIGHT-CORRIDOR TRANSI- TION

A UAV receives authority to transition from corridor segment C12 to C13. The beacon commits to: device; C12; C13; altitude band; flight mode; sink; geofence version; nonce; and policy epoch. If malicious software changes the request to C12 → C18:

≠ ℎ ⇒ ≠

and the flight transition is rejected. Because the binding is keyed, the malicious software cannot search for an alternative corridor whose compact commitment matches.

## 54. THIRD EXEMPLARY USE CASE - RF MODE CHANGE

A UAV requests activation of a higher-power communication mode. The Candidate Act binds: frequency class; power class; duration class; traffic class; radio sink; jurisdictional zone; and nonce. The RF controller verifies the Beacon Proof Capsule before activating the relevant transmit path.

## 55. HARDWARE IMPLEMENTATION

The Protected Execution Domain may comprise: secure microcontroller; Trusted Execution Environment; secure element; HSM; FPGA; lock-step processor; safety processor; secure coprocessor; isolated RISC-V core; ARM TrustZone component; ASIC; protected flight-controller or vehicle-controller partition; secure baseband processor; or equivalent protected computation environment. The Finality Sink may use: hardware register gate; secure bus gateway; PWM gate; ESC enable gate; MOS- FET gate; power-domain controller; solenoid gate; motor-driver enable; RF transmit-enable; camera-enable line; sensor-power gate; motion-admission gate in a vehicle domain controller; or protected software interface backed by equivalent non-bypassable controls.

## 56. COMMUNICATION IMPLEMENTATION

The Beacon Proof Capsule and Act Evidence Records may be transported using: Bluetooth Low Energy; Bluetooth advertisement; Wi-Fi; Wi-Fi Aware; Wi-Fi Direct discovery; UWB; IEEE 802.15.4; Zigbee-like networks; Thread-like networks; mesh networks; sidelink; V2X; cellular direct communication; 5G; 6G; nonterrestrial networks; satellite; LPWAN; LoRa-like systems; proprietary telemetry; aviation data link; CAN or CAN FD or other on-board buses; optical communication; acoustic communication; or other constrained

Page 57

communication media.

## 57. PRIVACY-PRESERVING EMBODIMENT

The Beacon Proof Capsule and Act Evidence Records need not expose: exact coordinates; operator identity; customer identity; payload contents; mission details; authority document; or full device identity. A pseudonymous or session-scoped identifier may be used, and an Act Evidence Record may carry an unspecified act class so that only the decision, sink class, counter, and tag are broadcast. Only the protected verifier, or an authorized auditor holding the receipt chain, needs sufficient information to resolve the authority.

## 58. OFFLINE EMBODIMENT

All information required for hot-path verification may be preloaded. The sink may possess: authority cache; public keys; session keys; binding keys; geofence digest; policy epoch; revocation epoch; dictionary; replay store; and receipt store. Therefore external connectivity is not required for every Candidate Act.

## 59. INTERMITTENT-CONNECTIVITY EMBODIMENT

Where connectivity exists intermittently, a device may periodically refresh: authority cache; policy epoch; revocation state; geofence or zone version; and key material. Between refreshes, the constrained beacon architecture continues locally within bounded validity windows.

# 59.1 Bounded offline exposure

At loss of connectivity at time , cached authority may continue to be honoured only for act classes designated for offline use by the Authority Object, and only until

, = min( + , , (ℎ) for each cached authority ℎ)

after which only the Safe-Action Set is available. The residual exposure to a revocation or restriction issued after is therefore bounded:

≤ , ≤

, ,

Payload release and sensor activation are preferably not designated for offline use. Receipts produced offline are held in a sealed local store protected by the monotonic counter and reconciled when connectivity returns.

## 60. IMPLEMENTATION OF PROTECTED STATE

Protected state may include:

```
current_policy_epoch
current_revocation_epoch
nonce_cache
monotonic_counter
```

Page 58

```
receipt_chain_head
authority_cache
geofence_or_zone_version
active_session_keys
binding_keys
evidence_chain_seed_and_index
fragment_sessions
collision_guard_table
sink_registry
safe_action_set
```

State may be protected using: secure flash; monotonic counter; anti-rollback storage; secure element; TPM; TEE sealed storage; HSM; hash-linked log; or redundant safety memory.

# 61. INDUSTRIAL APPLICABILITY, PRESENT TECHNICAL SOLUTIONS, AND TECHNICAL CONTRIBUTION

### 61.1 Industrial Problem Addressed

The disclosed architecture is industrially applicable to autonomous, remotely operated, semiautonomous, safety-critical, and cyber-physical systems in which a proposed digital command can produce a physical, communicative, persistent, financial, sensing, mobility, or other externally consequential effect.

Modern industrial systems increasingly separate the component that decides or proposes an action from the component that ultimately performs that action. A mission computer may propose a UAV manoeuvre; an autonomous-driving computer may propose a trajectory; a fleet service may request a payload release; an operator may request a radio-mode change; a robotic planner may request movement of an actuator; or a satellite, gateway, roadside unit, control station, or remote service may provide authority information relevant to an act.

At the same time, the communication path between the source of authority and the final actuator or effectuation boundary may be highly constrained. The available path may comprise, without limitation:

| x | Bluetooth Low Energy advertisements; |
|---|---|
| x | Wi-Fi or Wi-Fi Aware discovery frames; |
| x | UWB frames; |
| x | Remote Identification broadcasts; |
| x | aviation telemetry; |
| x | V2X or cellular sidelink; |
| x | CAN or CAN FD; |
| x | automotive Ethernet; |
| x | avionics buses; |
| x | industrial field buses; |
| x | mesh networks; |
| x | LPWAN; |
| x | satellite or non-terrestrial links; |
| x | secure-element interfaces; |
| x | actuator-control buses; or |

Page 59

x another link having restricted message size, bandwidth, energy budget, latency budget, duty

cycle, or processing capacity.

The technical problem is therefore not merely whether a system can identify an aircraft, authenticate a sender, authorize a flight, authenticate a bus message, or verify that software booted correctly. The industrial problem addressed by this disclosure is how a downstream enforcement component can determine, using a compact and machine-verifiable representation, whether the specific physical or

**externally consequential act actually pending at that boundary may become effective now,**

while preventing replay, parameter substitution, sink substitution, stale-policy use, stale-revocation use, incomplete-fragment acceptance, ambiguous compact-proof reconstruction, and unauthorized effectuation.

The provisional specification addresses this problem by keeping the Candidate Act non-effective while compact authority evidence is constructed, transported, reconstructed or resolved, checked against the actual impending operation, and consumed at the Finality Sink.

### 61.2 Relationship to Present Remote Identification Solutions

Present Remote Identification systems are principally designed to provide identification and location information concerning an unmanned aircraft. For example, the FAA describes Remote ID as enabling a drone in flight to provide identification and location information by broadcast, and Standard Remote ID broadcasts information including aircraft identification, position, altitude, velocity, control-station information, time, and emergency status.

DRIP strengthens the trustworthiness of this identification layer. RFC 9575 defines mechanisms by which an Observer can authenticate Broadcast RID material and obtain stronger assurance that received RID information originates from the registered owner of the claimed DRIP Entity Tag.

These mechanisms provide an important identity and message-provenance foundation.

They do not, by themselves, express or enforce the following distinct question:

**Was this particular actuator-level or effect-producing act independently authorized by the protected enforcement component, for this Finality Sink, against the current policy, revocation, geographic, temporal, context, and freshness state, before the act became effective?**

Accordingly, the disclosed invention may operate adjacent to Remote ID or DRIP without replacing either system.

A Remote ID or DRIP message may continue to answer:

### Which aircraft is this?

The disclosed constrained-beacon execution-finality mechanism may separately answer:

**Does the compact authority evidence presented for this Candidate Act match the concrete operation actually pending at the designated Finality Sink, and do all current execution-time predicates still permit effectuation?**

A further Act Evidence Record may subsequently allow an Observer to verify that the protected enforcement component made a particular allow, deny, or safe-state decision before disclosure of the corresponding evidence key.

Page 60

Thus identification, execution authority, and observer-verifiable act evidence remain separate technical functions.

### 61.3 Relationship to Present UTM and U-Space Solutions

Present UAS Traffic Management and U-space systems provide important strategic and tactical services concerning flight operations.

For example, current EASA U-space services include UAS flight authorization, geo-awareness, network identification, and traffic information. UAS flight authorization determines whether a flight may operate in the relevant airspace, while geo-awareness supplies information concerning current airspace constraints and geographical zones.

Those services can provide authority information consumed by the present invention.

The disclosed architecture does not replace flight authorization or geo-awareness. Instead, it provides a technical enforcement layer capable of carrying or referencing the resulting authority into a later execution boundary.

For example:

1. a U-space service may authorize a flight corridor;
2. the corridor authorization may be represented by an Authority Object;
3. a compact Authority Reference may identify that object;
4. the protected execution domain may bind that Authority Reference to a particular Candidate Act, Finality Sink, policy epoch, revocation epoch, context commitment, freshness value, and expiry;
5. the resulting compact representation may travel over a constrained channel;
6. immediately before effectuation, the Finality Sink or protected verifier may reconstruct the actual requested act;
7. current policy, revocation, geofence, context, and freshness state may be read;
8. the compact binding may be recomputed against the actual operation;
9. a Finality Receipt may be committed; and
10. only after successful verification may the relevant enablement condition be released.

This converts a strategic or upstream authorization into a technically enforceable execution-time condition without requiring the entire authority object to be retransmitted at every actuator event.

### 61.4 Relationship to Present Command and Message Authentication

Industrial and aviation communication protocols may authenticate commands or messages.

For example, MAVLink 2 message signing enables a receiving MAVLink system to determine that a message originated from a trusted source.

Automotive Secure Onboard Communication mechanisms similarly support authentication and freshness protection. AUTOSAR SecOC, for example, uses message-authentication information and freshness values, including profiles using truncated authentication information where vehiclenetwork payload size is constrained.

These mechanisms are valuable and may be used together with the disclosed invention.

Page 61

However, authentication of the sender or message is technically distinct from execution-finality verification.

A correctly authenticated command can still request:

x x x x x x x x x x x the wrong actuator; a different payload; a changed trajectory; a stale corridor; an outdated geofence; a revoked authority; an expired action; a different radio power; a different destination; a different operational mode; or another effect that is outside the authority originally granted.

The constrained-beacon architecture therefore does not merely authenticate a command.

It binds authority to the semantic effect of the Candidate Act, the Finality Sink at which that

**effect becomes possible, and the current execution context.**

The disclosed Binding Commitment may therefore bind, without limitation:

```
Act Commitment || Finality Sink || Authority Reference || Policy Epoch ||
Revocation Epoch || Context Commitment || Freshness || Expiry
```

preferably under a protected binding key unavailable to the untrusted mission computer, transmitter, or ordinary application software.

This produces a property that is different from ordinary message-source authentication: possession of the transmitted bytes is insufficient to transfer authority to a different act, sink, context, device, or time.

### 61.5 Constrained-Beacon Execution-Finality Architecture

In one industrial implementation, a Candidate Act A is first converted into a deterministic canonical representation C(A).

An Act Commitment may be derived as:

```
D_A = H(DOM_A || C(A))
```

A protected execution domain may further derive a Binding Commitment:

```
B = HMAC_Kbind(DOM_B || D_A || S || R || E_P || E_R || D_C || N || T_exp)
```

where:

| x | D _A represents the Candidate Act; |
|---|---|
| x | S identifies or characterizes the Finality Sink; |
| x | R is an Authority Reference; |
| x | E _P identifies applicable policy state; |
| x | E _R identifies applicable revocation state; |

Page 62

| x | D _C represents relevant execution context; |
|---|---|
| x | N provides freshness, nonce, or sequence state; and |
| x | T _exp defines the permitted temporal scope. |

The provisional specifically discloses this type of keyed binding, with the binding key held by protected components rather than the mission computer or transmitter.

The full value B need not be transmitted.

A compact value may be transmitted:

```
B_t = Trunc_t(B)
```

together with one or more of:

| x | profile identifier; |
|---|---|
| x | act class; |
| x | sink class; |
| x | Authority Reference; |
| x | policy epoch; |
| x | revocation epoch; |
| x | freshness or sequence value; |
| x | expiry delta; |
| x | Context Commitment; |
| x | flags; and |
| x | cryptographic authenticator. |

The resulting machine-verifiable object is referred to in this disclosure as a Beacon Proof Capsule

**(BPC).**

A representative BPC is expressly disclosed with these fields and may occupy approximately 24 to 48 bytes in one non-limiting implementation.

### 61.6 Difference From Mere Token Compression

The invention should not be understood merely as:

| x | compressing an existing authorization token; |
|---|---|
| x | encoding an authorization object using CBOR; |
| x | truncating a MAC; |
| x | placing a hash into a beacon; |
| x | using an index instead of a certificate; |
| x | fragmenting a large message; |
| x | signing an actuator command; or |
| x | using delayed disclosure for ordinary broadcast authentication. |

The industrial technical contribution lies in the coordinated execution sequence.

In representative form:

```
Candidate Act
→ exact-act canonicalization
```

Page 63

```
→ protected act commitment
→ sink-specific binding
→ compact Authority Reference
→ current policy/revocation/context binding
→ freshness binding
→ risk-budgeted compact commitment
→ constrained transport
→ authenticated fragmentation where required
→ protected reconstruction or resolution
→ reconstruction of the actual impending act at the Finality Sink
```

```
→ current-state read within the final atomic decision
→ replay-state consumption
→ Finality Receipt commitment
→ bounded enablement release
→ physical or externally consequential effect
```

The provisional expressly identifies this combination as the important technical distinction rather than the isolated use of compression, CBOR, truncation, or known authentication primitives.

### 61.7 Industrial Importance of Explicit Truncation Security

Constrained industrial networks often require shortened identifiers, digests, or authenticators.

The disclosed architecture recognizes that shortening a cryptographic value introduces at least two different engineering questions.

The first is accidental collision risk.

For approximately q values in the relevant collision domain, the provisional uses the birthday approximation:

```
P_coll ≈ q(q - 1) / 2^(t+1)
```

where t is the retained bit length.

The second is deliberate substitution search.

If an unkeyed truncated commitment is predictable to compromised software, the software may search offline for a different Candidate Act that produces the same retained compact value.

For offline work W:

Page 64

```
P_sub ≈ W / 2^t
```

The provisional therefore selects the compact field size according not merely to available bytes but according to:

| x | expected action population; |
|---|---|
| x | fleet size; |
| x | beacon lifetime; |
| x | safety class; |
| x | collision-risk budget; |
| x | attacker work budget; |
| x | whether the commitment is keyed; |
| x | permitted online attempts; and |
| x | available transport capacity. |

For keyed commitments, offline substitution search is prevented by lack of the binding key, converting the attack into bounded online attempts.

This is industrially relevant because different deployments can select different compact-proof lengths without abandoning deterministic security criteria.

For example:

| x | low-risk telemetry may use a shorter compact commitment; |
|---|---|
| x | payload release may use a longer commitment; |
| x | high-power RF activation may require a stronger profile; |
| x | motion-control admission may use a profile appropriate to vehicle latency; |
| x | an 8-byte CAN transport may fragment the capsule; |
| x | a larger V2X, Wi-Fi, or satellite transport may carry the capsule directly. |

### 61.8 Authenticated Fragmentation for Industrial Constrained Links

Where a complete BPC cannot fit within one transport unit, the disclosure provides authenticated fragmentation rather than treating each fragment as independent authority.

For encoded proof:

```
P = p_0 || p_1 || ... || p_(n-1)
```

a fragment may comprise:

```
F_i = (SessionID, Root, i, n, p_i, Auth_i)
```

with:

```
Root = H(DOM_F || P)
```

and a fragment authenticator binding at least:

```
SessionID || Root || i || n || p_i
```

The receiver does not treat a fragment as execution authority.

Page 65

Only after the complete required set has been authenticated, reconstructed, and checked against the root commitment may finality verification continue. Fragments from different sessions or different proof roots cannot validly be mixed.

The resulting industrial invariant is:

```
IncompleteEvidence ⇒ NoEffectuation
```

This property is particularly relevant to:

x x x x x x x x

Classic CAN; constrained UAV telemetry; Remote-ID-adjacent transport; BLE advertising; LPWAN; satellite narrowband control; intermittent radio links; and other transports where proof material may span more than one frame.

Loss of one fragment therefore does not silently convert incomplete evidence into authority.

The system can instead request retransmission, use a larger profile, invoke an authenticated resolver, or remain in a Safe-Action Set.

### 61.9 Authority-Reference and Resolver-Assisted Industrial Operation

Industrial systems often possess an authority object too large to transmit on every action.

The invention therefore permits a compact Authority Reference.

In one preferred form:

```
R = Trunc_r(HMAC_KR(AuthorityObject))
```

where K\_R is unavailable to ordinary transmitting software.

The reference can identify an Authority Object stored:

| x | in the protected execution domain; |
|---|---|
| x | at the Finality Sink; |
| x | in secure local storage; |
| x | in a hardware security module; |
| x | in a secure element; |
| x | in an avionics controller; |
| x | in a vehicle domain controller; |
| x | in a trusted gateway; |
| x | in a protected cache; or |
| x | through an authenticated resolver. |

The provisional expressly discloses compact keyed Authority References and protected-cache resolution.

A cache miss is not authorization.

Page 66

An unresolved reference is not authorization.

An ambiguous reference is not authorization.

A resolver may return the complete Authority Object and associated proof, but the resolver does not itself determine the physical effect. The Finality Sink still reconstructs the actual impending act and independently decides whether effectuation is permitted.

This permits a cold path to perform expensive certificate-chain validation, authority ingestion, policy parsing, map verification, key establishment, or resolver synchronization, while a hot actuation path performs only compact reference lookup, bounded authentication, commitment comparison, current-state checks, replay consumption, and receipt commitment.

Such separation is industrially useful for safety processors, microcontrollers, FPGA gates, ESC controllers, zonal controllers, vehicle motion-admission gates, and other latency-sensitive components.

### 61.10 UAV and UAS Industrial Application

A UAV implementation may comprise:

| x | mission computer; |
|---|---|
| x | flight controller; |
| x | secure microcontroller or protected PED; |
| x | ESC or motor controller; |
| x | GNSS/RTK receiver; |
| x | inertial sensors; |
| x | barometric sensors; |
| x | visual-inertial odometry; |
| x | geofence database; |
| x | payload controller; |
| x | camera or other sensor controller; |
| x | radio subsystem; |
| x | Beacon Proof Capsule transport; |
| x | Act Evidence Record transport; and |
| x | one or more Finality Sinks. |

The invention can govern, for example:

| x | motor arming; |
|---|---|
| x | propulsion envelope changes; |
| x | waypoint acceptance; |
| x | corridor transitions; |
| x | altitude-band transitions; |
| x | payload release; |
| x | winch actuation; |
| x | camera activation; |
| x | sensor-resolution changes; |
| x | RF transmission; |
| x | power-class changes; |
| x | flight-mode transitions; |
| x | Remote-ID state changes; or |
| x | coordinated multi-aircraft manoeuvres. |

Page 67

In the delivery example already disclosed, a UAV approaching a delivery zone receives compact evidence binding the payload, geographic scope, policy/revocation state, nonce, sink and context. The payload controller independently reads the actual payload, altitude, latch condition and geographic state before release. Movement outside the authorized zone causes the context comparison to fail and the latch remains locked.

Thus the invention is not limited to detecting a violation after flight. It can technically prevent the consequential actuator transition before the payload latch, motor path, radio path or sensing path becomes effective.

### 61.11 Autonomous Vehicle and V2X Industrial Application

In an automated road vehicle, a Candidate Act may comprise:

| x | lane transition; |
|---|---|
| x | cooperative merge; |
| x | negotiated intersection crossing; |
| x | platoon join or leave; |
| x | remote-assistance trajectory; |
| x | speed-envelope change; |
| x | automated parking path; |
| x | steering envelope; |
| x | braking command; |
| x | propulsion enable; |
| x | road-zone entry; |
| x | door or cargo operation; or |
| x | another externally consequential vehicle act. |

A BPC may bind:

| x | planned trajectory; |
|---|---|
| x | lane group; |
| x | road segment; |
| x | speed envelope; |
| x | manoeuvre identifier; |
| x | participant identity; |
| x | time slot; |
| x | operational-design-domain state; |
| x | policy epoch; |
| x | freshness; |
| x | and the vehicle motion-admission Finality Sink. |

The verifier may be placed in a safety controller, domain controller, zonal controller, drive-by-wire gateway, braking interface, steering interface, or propulsion-admission component.

Present V2X or authenticated in-vehicle messaging can supply authenticated data to this architecture. The additional disclosed function is the execution-time verification that the actual trajectory or drive-by-wire operation pending at the sink remains the exact authorized act under the present road, policy, freshness and safety state.

### 61.12 Robotics and Industrial Automation

Page 68

In an industrial robot, warehouse robot, port robot, mining vehicle, agricultural robot or automated material-handling system, Candidate Acts may include:

| x | movement of a robotic arm; |
|---|---|
| x | motion into a protected work cell; |
| x | gripper closure; |
| x | load release; |
| x | autonomous route change; |
| x | high-power tool activation; |
| x | conveyor activation; |
| x | hazardous-zone entry; |
| x | machine mode transition; or |
| x | transfer of control to another automation component. |

The Finality Sink may comprise a motor controller, safety PLC, robotic motion controller, power gate, gripper controller, secure bus gateway, actuator interface or protected software-enforcement boundary.

The compact proof approach permits strong act-specific authority even where the actuator controller has limited memory, compute capability or communication bandwidth.

### 61.13 Satellite, NTN and Remote Infrastructure Application

The same constrained-beacon architecture is industrially applicable where the authority path

includes:

| x | satellite links; |
|---|---|
| x | non-terrestrial networks; |
| x | intermittent gateway visibility; |
| x | remote autonomous equipment; |
| x | maritime platforms; |
| x | isolated infrastructure; |
| x | remote sensors; or |
| x | geographically distributed cyber-physical systems. |

A compact proof may authorize or constrain a bounded operation without requiring the downstream controller to repeatedly receive a full authority document.

The Authority Object can be validated and cached on a cold path, while a compact Authority Reference, epochs, freshness and act binding are transmitted on the constrained operational link.

This is particularly relevant where airtime, propagation delay, energy, or available message size makes transmission of large certificates and policy objects on every act impractical.

### 61.14 Low-Power IoT and Edge Devices

The architecture is further applicable to constrained IoT and edge systems whose controllers

possess:

| x | limited RAM; |
|---|---|
| x | limited flash; |
| x | low-power processors; |
| x | strict sleep cycles; |

Page 69

| x | limited radio duty cycle; |
|---|---|
| x | small frame sizes; or |
| x | intermittent connectivity. |

The disclosed architecture permits expensive verification material to remain cached or resolveraccessible while only compact execution-specific evidence travels on the hot path.

A device may therefore avoid treating possession of a long-lived bearer token as sufficient authority for every subsequent physical operation.

### 61.15 Protected Hardware and Manufacturability

The invention is implementable using presently available classes of industrial hardware.

The Protected Execution Domain may comprise, for example:

| x | secure microcontroller; |
|---|---|
| x | Trusted Execution Environment; |
| x | secure element; |
| x | HSM; |
| x | FPGA; |
| x | lock-step processor; |
| x | safety processor; |
| x | secure coprocessor; |
| x | isolated processor core; |
| x | ARM TrustZone component; |
| x | ASIC; |
| x | secure baseband processor; or |
| x | protected controller partition. |

The Finality Sink may control, for example:

| x | secure register gate; |
|---|---|
| x | PWM gate; |
| x | ESC enable; |
| x | MOSFET or power-domain gate; |
| x | solenoid supply; |
| x | motor-driver enable; |
| x | RF transmit-enable; |
| x | camera-enable line; |
| x | actuator command-admission interface; |
| x | secure bus transaction; |
| x | trajectory-admission gate; or |
| x | another effectuation prerequisite. |

The provisional expressly identifies such implementations, demonstrating that the architecture is not dependent on a hypothetical processor, cryptographic primitive, or communication medium.

### 61.16 Safe Industrial Failure Behaviour

Industrial applicability also requires that loss of authorization or communication need not cause an unsafe uncontrolled shutdown.

Page 70

The invention therefore separates consequential actions from a protected Safe-Action Set.

Depending on platform type, Safe Actions may include:

| x | hover; |
|---|---|
| x | loiter; |
| x | altitude hold; |
| x | return-to-home; |
| x | controlled landing; |
| x | route freeze; |
| x | motor-output limitation; |
| x | payload lock; |
| x | RF receive-only mode; |
| x | reduced sensor operation; |
| x | braking; |
| x | lane keeping; |
| x | speed reduction; |
| x | minimal-risk manoeuvre; |
| x | hazard signalling; or |
| x | operator escalation. |

The Safe-Action Set is protected and cannot be widened by the untrusted mission computer.

Accordingly:

```
Failure to verify consequential act ≠ uncontrolled system failure
```

Instead:

```
Failure to verify consequential act → consequential act remains non-effective +
protected safe action remains available
```

This property makes the architecture applicable to physical systems where simply switching everything off could itself increase risk.

### 61.17 Observer-Verifiable Act Evidence as a Separate Industrial Function

The invention further provides an optional evidence plane distinct from execution authority.

A protected domain may generate an Act Evidence Record after or with commitment of the underlying Finality Receipt.

A delayed-disclosure key chain may permit a nearby third-party Observer to verify, after a bounded delay, that the protected domain emitted a decision record before the corresponding symmetric key was disclosed.

This mechanism can reduce the need for a separate public-key signature on every act while preserving protected-domain origin.

Importantly:

```
Act Evidence Record ≠ Execution Authority
```

and:

Page 71

```
Finality Receipt ≠ Execution Authority
```

Neither evidence artifact is accepted by the Finality Sink as authorization.

The evidence plane can therefore serve:

| x | regulators; |
|---|---|
| x | fleet auditors; |
| x | insurers; |
| x | infrastructure operators; |
| x | accident investigators; |
| x | airspace observers; |
| x | public-safety personnel; or |
| x | cooperating automated systems, |

without turning the publicly observable evidence into a transferable execution credential.

### 61.18 Industrial Technical Effects

The disclosed architecture can produce one or more concrete technical effects, including:

1. reduction of authority-transport size while retaining act-specific cryptographic binding;
2. actuator-level or effectuation-boundary verification of a proposed operation;
3. prevention of reuse of compact authority at an unintended Finality Sink;
4. prevention of reuse for a materially different Candidate Act;
5. prevention or reduction of replay through protected nonce, sequence or consume state;
6. enforcement of current policy and revocation state at the final decision boundary;
7. binding of changing geofence, corridor, road-zone, mission, payload, radio or operational context into execution authority;
8. reduction of hot-path computational and parsing requirements by moving heavy authority processing to a cold path;
9. support for constrained transports where the full Authority Object cannot practically be carried per act;
10. deterministic failure when compact proof material is incomplete or ambiguous;
11. prevention of cross-session fragment mixing;
12. security-driven sizing of truncated commitments rather than arbitrary truncation;
13. resistance to offline parameter-substitution search through keyed binding;
14. resolver-assisted authority verification without making the resolver the final effectuation authority;
15. reduced radio airtime and energy relative to retransmission of complete authority objects;
16. exact-act reconstruction from the operation actually pending at the Finality Sink;
17. closure of the interval between an earlier authorization check and the later physical effect by reading current state within the atomic finality decision;
18. commitment of a Finality Receipt before release of the protected enablement condition;
19. third-party verification of protected-domain decisions without requiring a public-key signature on every act; and
20. preservation of safety-increasing actions while unverified consequential actions remain noneffective.

These effects correspond to technical effects already identified in the present provisional specification.

### 61.19 Technical Delta Introduced by the Disclosed Architecture

Page 72

Present solutions individually provide important functions:

| x | Remote ID provides identity and location broadcasting; |
|---|---|
| x | DRIP adds stronger identity and message-provenance authentication; |
| x | UTM and U-space provide flight authorization, geo-awareness and operational coordination; |
| x | message-signing mechanisms authenticate command origin; |
| x | Secure Onboard Communication mechanisms protect message integrity and freshness; |
| x | secure boot and attestation establish properties of software or platform state; |
| x | audit logs establish what occurred after an event. |

The disclosed constrained-beacon execution-finality architecture introduces a different technical boundary.

Its disclosed delta is the combination of:

**a concrete Candidate Act held non-effective;**

**deterministic exact-act canonicalization;**

**binding to the Finality Sink at which the effect becomes possible;**

**a preferably keyed commitment unavailable to the untrusted proposer;**

**compact Authority References instead of mandatory retransmission of the complete authority object;**

**binding to freshness, policy, revocation and relevant live context;**

**risk-budgeted commitment truncation;**

**authenticated fragmentation and deterministic reconstruction where one frame is insufficient;**

**ambiguity and collision handling that fails closed or escalates to a stronger proof;**

**optional resolver-assisted verification in which the resolver does not itself cause effectuation;**

**independent reconstruction of the actual impending act at the Finality Sink;**

**current-state verification and freshness consumption within the final atomic decision;**

**receipt commitment before release;**

**release of only a bounded enablement condition after successful verification; and**

**optional delayed-disclosure evidence originating in the protected enforcement domain.**

Accordingly, the architecture is not merely an identity mechanism, transport-security mechanism, geofence, flight-authorization service, compact token, communication authenticator, or post-event logging system.

Its technical purpose is to make the transition:

```
proposed digital act → externally effective consequence
```

Page 73

depend on successful verification of compact, current, exact-act-bound authority at the effectuation boundary.

### 61.20 Industrial Applicability Conclusion

The invention is capable of being manufactured, integrated, deployed, and used using existing classes of processors, protected execution environments, cryptographic modules, radios, control buses, actuator interfaces, flight controllers, vehicle controllers and industrial control hardware.

It is applicable, without limitation, to:

| x | commercial delivery UAVs; |
|---|---|
| x | industrial and infrastructure inspection UAVs; |
| x | agricultural UAVs; |
| x | emergency-response and public-safety aircraft; |
| x | aerial mapping platforms; |
| x | automated passenger and goods vehicles; |
| x | autonomous shuttles; |
| x | agricultural, mining and port vehicles; |
| x | warehouse and logistics robots; |
| x | industrial robots; |
| x | autonomous ground vehicles; |
| x | maritime autonomous systems; |
| x | V2X cooperative systems; |
| x | remote-assistance systems; |
| x | constrained IoT devices; |
| x | edge controllers; |
| x | smart infrastructure; |
| x | satellite-controlled autonomous devices; |
| x | non-terrestrial-network connected systems; and |
| x | other cyber-physical systems in which a constrained message path must carry or reference strong execution-specific authority or evidence. |

The industrial applicability arises not from an abstract rule or administrative policy but from the technical control of real computing, communication and actuator resources: cryptographic state is generated and verified, constrained messages are encoded and reconstructed, protected state is read and consumed, physical or logical enablement conditions are withheld or released, actuator interfaces are gated, and consequence-bearing operations remain non-effective unless the defined verification sequence succeeds.

The architecture therefore provides a concrete engineering mechanism for carrying strong execution-specific authority across constrained industrial communication paths and enforcing that authority immediately before physical or externally consequential effectuation.

## 62. TECHNICAL EFFECTS

The technical effects may include:

1. reducing beacon size while retaining cryptographic act binding;
2. permitting downstream actuator-level verification;
3. preventing replay of stale beacon authorization;

Page 74

4. preventing reuse at another sink;
5. preventing parameter substitution after authorization, including by offline search;
6. binding geofence, zone, or corridor state into compact authority evidence;
7. supporting authorization over low-bandwidth links;
8. reducing hot-path parsing cost;
9. enabling cached cold-path authority validation;
10. preventing partial fragment reception from authorizing execution;
11. defining deterministic collision handling for truncated commitments;
12. reducing radio airtime and energy consumption relative to transmitting full authority objects on every act;
13. maintaining a non-effective state until exact-act verification;
14. permitting scalable deployment across heterogeneous constrained transports;
15. closing the interval between currentness check and effect;
16. guaranteeing a committed receipt for every released capability;
17. enabling third-party verification of per-act decisions without per-act public-key signatures, with tolerance to loss of key disclosures;
18. preventing an identification transmitter or mission computer from forging evidence of authorized conduct; and

Page 75

19. preserving access to safety-increasing actions in platforms where withholding action can be unsafe.

## 63. IMPORTANT INVENTIVE DISTINCTION

The invention should not be understood merely as compressing a token, placing CBOR in a beacon, truncating a MAC, or applying a known broadcast authentication scheme. The technical architecture is instead the combination of:

```
Candidate Act
+ exact-act canonicalization
+ sink binding
+ keyed binding commitment
+ authority reference
+ freshness
+ policy/revocation continuity read inside the atomic commit
+ context commitment
+ risk- and attacker-work-bounded compact commitment
+ authenticated constrained-beacon transport
+ optional authenticated fragmentation
+ sink-side reconstruction of the actual impending act
+ replay-resistant state transition
+ receipt committed before release
+ effectuation only after successful verification
+ (optionally) delayed-disclosure act evidence originating in the
protected domain
```

## 64. REPRESENTATIVE INVARIANTS

### Invariant 1 - No verified proof, no effect.

¬ ( ,,) ⇒ ¬ ()

### Invariant 2 - Act substitution resistance.

' ≠ ⇒ (( ' )) ≠ (())

except with probability at most /2 for a keyed binding, or approximately /2 for an unkeyed binding against offline work , together with negligible full-length collision probability.

### Invariant 3 - Sink substitution resistance.

' ≠ ⇒ (, ' ) ≠ (, )

### Invariant 4 - Replay resistance.

() = ⇒ () =

### Invariant 5 - Fragment completeness.

< ⇒ () =

Page 76

### Invariant 6 - Epoch continuity.

ℎ ≠ ℎ ( ) ⇒ () = unless an expressly defined backward-compatible rule applies.

### Invariant 7 - Evidence origin.

---

NOT Holds(Transmitter, K\_(i+1)) before I\_(i+d) => NOT Forge(Record\_i)

---

### Invariant 8 - Late-record rejection.

≥ + ⇒ ( )

### Invariant 9 - Disclosure-loss tolerance.

---

there exists j > i: Receive(K\_(j+1)) => Recover(K\_(i+1))

---

### Invariant 10 - Receipt before release.

⇒

### Invariant 11 - Safety asymmetry.

∈ ⇒ () regardless of ( )

### Invariant 12 - Evidence is not authority.

( , ) ⇒ ∉ { , ,

, ℎ}

## 65. EXAMPLE DRAWINGS TO ACCOMPANY THE COMPLETE SPECI- FICATION

The following figures may be prepared:

- FIG. 1 - Overall constrained-beacon execution-finality architecture.
- FIG. 2 - Candidate Act lifecycle from generation to physical effectuation.
- FIG. 3 - Beacon Proof Capsule logical field layout.
- FIG. 4 - Single-frame compact encoding.
- FIG. 5 - Multi-frame authenticated fragmentation and reconstruction.
- FIG. 6 - UAV flight-controller Finality Sink.
- FIG. 7 - ESC/PWM enforcement embodiment.
- FIG. 8 - Payload-latch enforcement embodiment.
- FIG. 9 - Geofence-version binding.
- FIG. 10 - Resolver-assisted authority-reference mode.
- FIG. 11 - Cold-path/hot-path separation.

Page 77

- FIG. 12 - Atomic commit: currentness read, nonce consumption, receipt before release.
- FIG. 13 - Swarm-specific per-unit beacon binding and coordinated-act decision log.
- FIG. 14 - Collision-guard workflow for truncated commitments.
- FIG. 15 - Keyed versus unkeyed binding and attacker-work budget.
- FIG. 16 - Reverse key chain and delayed disclosure timeline.
- FIG. 17 - Act Evidence Record and Key Disclosure Record layouts.
- FIG. 18 - Observer verification with safety condition and lost-key recovery.
- FIG. 19 - Boundary-proximity revalidation geometry.
- FIG. 20 - Autonomous ground vehicle embodiment with safety asymmetry.
- FIG. 21 - Vehicle cooperative manoeuvre binding across participants.

## 66. CLAIM-ORIENTED INVENTION STATEMENTS FOR LATER COM- PLETE SPECIFICATION

The following are not intended to restrict the provisional disclosure but identify important claim directions.

**Statement 1. A system in which a Candidate Act is held non-effective while a compact constrained-beacon**

representation cryptographically binds the Candidate Act to a downstream Finality Sink.

**Statement 2. The system wherein a full Authority Object is replaced in the constrained beacon by a compact**

Authority Reference.

**Statement 3. The system wherein the Finality Sink independently reconstructs the actual Candidate Act**

immediately before effectuation.

**Statement 4. The system wherein a truncated binding commitment is selected according to an explicit**

collision-risk criterion and, where unkeyed, an attacker-work criterion.

**Statement 5. The system wherein ambiguous truncated commitments cause denial or escalation to a longer**

proof profile.

**Statement 6. The system wherein execution-finality evidence is fragmented across multiple authenticated**

beacon frames and partial reconstruction cannot authorize effectuation.

**Statement 7. The system wherein fragments are cryptographically bound to a common root commitment**

and session identifier.

**Statement 8. The system wherein geofence version, zone version, or corridor state is included in the act-**

bound commitment.

**Statement 9. The system wherein a stale policy or revocation epoch invalidates the constrained beacon, the**

deciding epoch read being performed inside the atomic finality commit.

**Statement 10. The system wherein successful verification produces a separate sink-local bounded execution**

capability.

**Statement 11. The system wherein nonce consumption and commitment of a Finality Receipt are atomically**

performed before the bounded execution capability becomes usable.

**Statement 12. The system wherein the constrained beacon is transported adjacent to or in association with**

a remote-identification message without requiring the identification message itself to constitute execution authority.

Page 78

**Statement 13. The system wherein the constrained beacon controls at least one of a flight-controller com-**

mand, ESC command, payload latch, sensor activation, radio transmission, geofence-sensitive flight transition, vehicle cooperative manoeuvre, or remotely approved vehicle path.

**Statement 14. The system wherein the binding commitment is computed under a binding key held by the**

protected execution domain and the Finality Sink and unavailable to the component that proposes or transmits the Candidate Act.

**Statement 15. A system in which records of act decisions made by a protected execution domain are broad-**

cast with tags computed from a reverse one-way key chain whose seed is held only in that domain, keys are disclosed after a delay, the chain is anchored by a signed object bound to a device identity, and an observer accepts a record only if it arrived before its key could have been disclosed.

**Statement 16. The system of Statement 15 wherein each record carries a monotonic counter and a header**

that is also contained in a Finality Receipt committed by the protected domain, enabling one-to-one matching of broadcast evidence to later-audited receipts.

**Statement 17. The system wherein, in an autonomous ground vehicle, enforcement gates acceptance of**

permission expansions and consequential non-safety acts while a pre-authorized Safe-Action Set comprising at least braking and a minimal-risk manoeuvre remains available irrespective of verification outcome.

**Statement 18. The system wherein a revalidation interval for spatially scoped authority is scheduled from**

distance to boundary, position uncertainty, speed, reaction latency, and guaranteed deceleration, and outward motion is withheld when the interval bound is non-positive.

## 67A. OBSERVER-VERIFIABLE ACT-DECISION EVIDENCE USING DE- LAYED KEY DISCLOSURE

# 67A.1 Technical problem

A third party near a device - for example a public-safety officer, facility operator, roadside unit, auditor, or member of the public - may be able to verify the device's identity from an identification broadcast. That third party cannot verify whether an act it observes, such as a payload release or camera activation, was decided by the device's Protected Execution Domain before it became effective. Per-act public-key signatures are too large for constrained broadcast frames and too costly at typical decision rates. Evidence signed with the identification key proves only that the identification transmitter or flight software sent it, not that the Protected Execution Domain decided it. A compromised mission computer holding that key could broadcast false evidence of authorized conduct.

# 67A.2 Reverse one-way key chain held in the protected domain

---

At the start of an evidence epoch, the Protected Execution Domain generates a protected master seed K\_seed that never leaves the protected domain. From that seed it derives a terminal chain value K\_N for the epoch, and from K\_N it derives the reverse one-way chain:

```
K_N = H( DOM_SEED || K_seed || EpochID )
K_i = F(K_(i+1)), i = N-1, ..., 0
K'_i = F'(K_(i+1))
```

---

Detailed notation and the distinction between K\_seed and K\_N are stated in Section 67A.2A on Page 79A.

---

Page 79

# 67A.2A DELAYED-DISCLOSURE KEY NOTATION AND INDEXING

For avoidance of ambiguity, the following notation applies to the delayed-disclosure embodiment of Sections 67A.2 through 67A.8. The master seed is distinguished from the values of the disclosed reverse chain.

### Protected master seed and reverse chain

```
K_seed <- random lambda-bit protected secret
K_N = H( DOM_SEED || K_seed || EpochID )
K_i = F(K_(i+1)), i = N-1, ..., 0
```

K\_seed is the non-disclosed master seed and never leaves the Protected Execution Domain. K\_N is the terminal value of the evidence chain, derived from K\_seed for the evidence epoch. K\_N is not the master seed and, if the final evidence interval uses it, may be disclosed only according to the same delayed-disclosure rule that governs other chain values.

**K\_0: the public chain commitment carried in or bound to the Evidence Anchor. K\_0 authenticates later-disclosed**

chain values. It is not an AER authentication secret and is not used directly or through F' as an AER tag key.

**F: the domain-separated one-way chain function. A representative form is Trunc\_128(H("CHAIN" || x)). F': a distinct domain-separated one-way derivation used only to obtain an AER authentication key from an**

undisclosed chain value. A representative form is Trunc\_128(H("TAG" || x)).

### Evidence-interval indexing

```
K'_i = F'(K_(i+1))
I_i = [ T_0 + i*Delta, T_0 + (i+1)*Delta )
```

K'\_i denotes the AER authentication key associated with evidence interval I\_i. K'\_i is not itself a member of the reverse chain. T\_0 is the evidence-epoch start time, Delta is the interval duration, i is the evidence-interval index, N is the terminal chain index, and d >= 1 is the disclosure delay measured in intervals.

```
TAG_i = Trunc_m( HMAC_K'i( DOM_E || DeviceID || EpochID || Header_i ) )
```

m is the retained tag length in bits; DOM\_E is the evidence-authentication domain-separation value; Header\_i is the canonical AER header for interval i. The Act Evidence Record is Header\_i || TAG\_i.

### Disclosure and loss recovery

For a record emitted in interval I\_i, the corresponding chain value K\_(i+1) is not released until the profile-defined disclosure time associated with delay d. A Key Disclosure Record identifies the evidence interval and carries K\_(i+1).

```
F^((j+1)-k)(K_(j+1)) = K_k (chain authentication)
K_(i+1) = F^(j-i)(K_(j+1)), for i <= j (loss recovery)
```

Here K\_k is the last authenticated chain state, initially K\_0 from the Anchor. A later disclosure therefore permits recovery of earlier required chain values without revealing any still-later undisclosed value. This indexing also preserves the observer safety condition x < i + d: a record arriving after the corresponding disclosure could have been forged after disclosure and is rejected.

Page 79A

() = 128(("CHAIN" ∥ )), ' () = 128(("TAG" ∥ ))

Time is divided into intervals

= [ 0 + Δ, 0 + ( + 1)Δ )

---

# 67A.3 Act Evidence Record

For each decision (allow, deny, or safe-action selection) committed by the Protected Execution Domain in interval , the protected domain forms a header containing: version and record kind; act class, or an unspecified value in privacy mode; decision; sink class; interval index , optionally modulo 216; and monotonic receipt counter . It computes

= ( ' ( ∥ ∥ ℎ ∥ ))

---

One non-limiting layout of 16 octets is:

```
0 1 2 3
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|Ver|Knd| Act Class |Dec| SinkC | Interval Index (mod 2^16) |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

| \| | Receipt Counter n (32 bits) | \| |
|---|---|---|
| \| | Tag (64 bits, truncated HMAC) | \| |
| \| |  | \| |

```
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
Ver 2 bits | Knd 2 bits (0 = evidence record) | Act Class 6 bits
Dec 2 bits (DENY, ALLOW, SAFE_ACTION, reserved) | SinkC 4 bits
```

---

A Key Disclosure Record carries the record kind, the evidence-interval index i, and K\_(i+1); one non-limiting layout uses 19 octets (1 octet header, 2 octets index, 16 octets key).

---

A variant uses a 128-bit tag in a 24-octet record for higher-assurance deployments.

# 67A.4 Evidence Anchor and endorsement

---

The Protected Execution Domain signs, once per epoch, an Evidence Anchor containing DeviceID, EpochID, protected-domain key identifier, T0, Delta, d, N, chain commitment K\_0, and the first receipt counter of the epoch. K\_0 authenticates subsequently disclosed chain values; it is not an AER tag secret and is not used to derive an AER tag key.

---

An Endorsement signed with the device's identification key binds the protected-domain public key to the device identity. Alternatively, the Protected Execution Domain holds the identification key. The Evidence Anchor is re-broadcast unchanged, without re-signing, so that late-arriving observers can verify. A new anchor may be issued at epoch change, policy-epoch change, or key-chain exhaustion.

Page 80

# 67A.5 Emission rules

```
ON RECEIPT_COMMITTED(receipt): # inside protected domain
IF receipt.act_class NOT IN evidence_classes: RETURN
i = FLOOR((now - T_0) / Delta)
header = PACK(version, kind = 0,
class = PrivacyMap(receipt.act_class),
```

```
decision = receipt.decision,
sink_class = receipt.sink_class,
index = i MOD 65536,
counter = receipt.counter)
```

| tag = TRUNC_m(HMAC(F'(K_(i+1)), DOM_E \|\| DeviceID \|\| EpochID \|\| header)) |
|---|
| QUEUE_TO_TRANSMITTER(header \|\| tag) RECORD_HEADER_IN_RECEIPT(receipt, header) |
| EVERY INTERVAL j >= d: i = j - d QUEUE_TO_TRANSMITTER(KDR(index = i MOD 65536, key = K_(i+1))) |
| PERIODICALLY AND AT EPOCH START: QUEUE_TO_TRANSMITTER(SIGNED_ANCHOR) # same bytes each time |
| The transmitter forwards queued records but never holds K_(i+1) for evidence interval i before its disclosure. Evidence traffic does not displace messages that regulation requires to be transmitted. |

---

# 67A.6 Observer safety condition

Let bound the difference between the observer's clock and the time base of 0. An observer receiving a record for interval at local time computes

+ - 0 = ⌊ ⌋

Δ

and retains the record for later verification only if

< +

---

For evidence interval i, the corresponding disclosed chain value is K\_(i+1). If x >= i + d, that value may already be public, so the record is discarded. The full interval index is resolved from the transmitted index modulo 2^16 as the value nearest to (t\_r - T0)/Delta.

---

# 67A.7 Verification and loss recovery

---

On receiving a KDR for evidence interval j carrying K\_(j+1), the observer checks it against the last authenticated chain value K\_k (initially K\_0 from the anchor):

F^((j+1)-k)(K\_(j+1)) = K\_k If this holds, the chain value required for any retained evidence interval i <= j is recovered as

K\_(i+1) = F^(j-i)(K\_(j+1)) and each retained record for those intervals is verified by recomputing its tag with F'(K\_(i+1)).

---

Page 81

```
ON_KEY_DISCLOSURE(kdr):
j = RESOLVE_INDEX(kdr.index) # evidence interval
# kdr.key is K_(j+1); initialize last_i = -1 and last_K = K_0
IF j <= last_i: RETURN
IF ITERATE(F, kdr.key, j - last_i) != last_K: DISCARD; RETURN
FOR i FROM last_i + 1 TO j:
K_for_i = ITERATE(F, kdr.key, j - i) # K_(i+1)
FOR record IN PENDING[i]:
IF TRUNC_m(HMAC(F'(K_for_i), DOM_E || DeviceID || EpochID
|| record.header)) == record.tag:
MARK_VERIFIED(record)
ELSE:
MARK_INVALID(record)
last_i = j; last_K = kdr.key
```

---

Loss of any number of Key Disclosure Records is tolerated provided a later one is received.

With Δ = 1 s, = 3, and ≤ 1 s (illustrative), a record becomes verifiable approximately three to four

seconds after emission.

# 67A.8 Origin property

---

The identification transmitter, mission computer, and radio forward records but never hold K\_(i+1) for evidence interval I\_i before its disclosure. They therefore cannot generate a valid tag for a decision the Protected Execution Domain did not make. After disclosure, a forged record for an old interval is rejected by the safety condition of Section 67A.6.

---

# 67A.9 Receipt matching and meaning of a verified record

The Finality Receipt with counter contains the same header as the broadcast record. An auditor who later obtains the receipt chain can match broadcast evidence to receipts one-to-one; a later-produced receipt with counter but a different header contradicts the broadcast record.

A verified record establishes that the protected domain endorsed for the device emitted, during interval , decision record with the stated class, decision, and sink class. Combined with authenticated position broadcasts from the same interval, an observer can associate the decision with the device's location. It does not by itself establish that a physical effect occurred or that every decision was received; counter gaps are visible to an observer but are not by themselves proof of misconduct.

# 67A.10 Evidence is not authority

No Finality Sink accepts an Act Evidence Record, Key Disclosure Record, Evidence Anchor, or Finality Receipt as authorization to act.

| 67A.11 Cost characteristics |  |
|---|---|
| Approach Identification-key signature per act | Per-act on air Per-act operation >= 64-octet sig + one public-key identifiers; often signature multi-frame |
| Delayed-disclosure evidence record (this section) | one HMAC 16 octets + one 19-octet disclosure per interval, shared Page 82 |

# 67A.12 Variants

Variants include: tag length selected by risk class; multiple key chains per act class or per sink; re-anchoring on policy-epoch change; relay of records through network identification or roadside services; privacy mode with an unspecified act class; coverage of the records by an identification-layer manifest signature in addition to delayed-disclosure authentication; carriage as an authentication payload type within an identification protocol; and use in ground vehicles, robots, and maritime platforms.

## 67B. AUTONOMOUS GROUND VEHICLE EMBODIMENT

# 67B.1 Overview

The architecture applies to automated and autonomous road vehicles, shuttles, delivery vehicles, and agricultural, mining, and port vehicles. The Protected Execution Domain may be located in a vehicle domain controller, zonal controller, safety microcontroller, gateway, or telematics security module, and the Finality Sink may be a motion-admission gate that admits planned trajectory envelopes to the motion controller, a mode-transition register, a V2X transmit path, a sensor or recording enable, or a body function actuator.

# 67B.2 Safety asymmetry

In a road vehicle, withholding an action can itself be unsafe. Accordingly, enforcement in this embodiment gates:

- expansions of permission (higher speed envelope, entry to a restricted zone, activation of a higher automation mode, operation outside a designated operational domain);
- acceptance of cooperative manoeuvres negotiated with other road users or infrastructure;
- execution of paths or instructions supplied by a remote assistance or remote operation service;
- fleet-issued movement commands to an unoccupied vehicle; and
- consequential non-motion acts such as sensor recording in protected areas or high-power transmission, while a pre-authorized Safe-Action Set comprising at least braking, lane keeping, speed reduction, hazard signalling, and a minimal-risk manoeuvre to a stop remains available irrespective of verification outcome (Invariant 11). Denial of a gated act results in continuation within the last valid envelope or in a minimal-risk manoeuvre, never in loss of vehicle control.

# 67B.3 Cooperative manoeuvre binding

Where two or more vehicles, or a vehicle and roadside infrastructure, agree a manoeuvre (for example a lane merge with a yield agreement, joining or leaving a platoon, or taking a reserved intersection slot), each participant's protected domain computes

= ( ∥ ∥ ∥

,

∥ ∥ ∥ ∥ ∥ )

where is the digest of the agreed manoeuvre and is the digest of the trajectory envelope assigned to vehicle . The compact commitment is carried in the constrained V2X manoeuvre messages. The motion-admission sink of vehicle reconstructs the trajectory envelope actually produced by its planner and admits it only if the reconstructed binding matches. A planner that has been misled or compromised into producing a different trajectory, lane, speed, or time slot than the agreed one does not have that trajectory admitted, and the vehicle continues within its prior envelope or executes a minimal-risk manoeuvre.

Page 83

Where all participants must act or none, the coordinated-act rule of Section 36 applies, with holding the current lane and speed envelope as the hold state.

# 67B.4 Remote assistance and remote commands

A remote assistance operator may approve a path around an obstruction. The approval is expressed as a Candidate Act bound to: vehicle identity; path corridor digest; speed envelope; validity window; operator authority reference; policy and revocation epochs; and nonce. The vehicle's motion-admission sink reconstructs the actual planned path and admits it only on match. A validly authenticated but different path, a replayed approval, an approval for another vehicle, or an approval issued before a zone or policy change is not admitted.

# 67B.5 In-vehicle constrained buses

Where the Finality Sink is reached over a bus with small frames (for example classic CAN with 8 data octets or CAN FD with up to 64), the bounded execution capability of Section 43 may be carried as a compact frame containing a sink identifier, a capability counter, an envelope reference, and a truncated keyed MAC. A physical enable condition controlled directly by the protected domain is preferred where available. The distinguishing feature relative to generic authenticated bus messaging is that the capability is derived from, and bound to, the reconstructed Candidate Act, current epochs, consumed freshness, and a committed receipt.

# 67B.6 Zone and operational-domain binding

Road zones (for example school zones, construction zones, restricted-access areas, or designated operational domains) are represented by versioned zone data. The zone version is bound into the commitment as in Section 28, and the boundary-proximity revalidation bound of Section 24.1 schedules revalidation from distance to the zone boundary, localization uncertainty, speed, reaction latency, and guaranteed deceleration.

# 67B.7 Vehicle act evidence

Act Evidence Records(Section 67A) may be broadcast for designated act classes, for example activation of a higher automation mode or execution of a remotely approved path, and relayed by roadside units to authorized parties. Because vehicle broadcasts can enable tracking, privacy mode with pseudonymous identifiers and unspecified act class is preferred, with detail confined to receipts available to authorized auditors.

## 67C. SATELLITE AND NON-TERRESTRIAL NETWORK EXECUTION- FINALITY EMBODIMENT

# 67C.1 Overview

The disclosed execution-finality architecture may be applied to satellite communication systems, non-terrestrial networks (NTNs), satellite user terminals, satellite gateways, satellite payloads, intersatellite communication systems, electronically steered antenna systems, and hybrid terrestrial/nonterrestrial communication systems.

The embodiment is applicable, without limitation, to:

| x | low-Earth-orbit satellite constellations; |
|---|---|
| x | medium-Earth-orbit satellite constellations; |
| x | geostationary satellite systems; |
| x | mixed-orbit constellations; |

Page 84

| x | satellite broadband systems; |
|---|---|
| x | direct-to-device satellite systems; |
| x | satellite IoT systems; |
| x | non-terrestrial cellular systems; |
| x | user terminals having electronically steered or phased-array antennas; |
| x | fixed or mobile satellite terminals; |
| x | aircraft, maritime, vehicle, or portable satellite terminals; |
| x | terrestrial gateways communicating with satellites; |
| x | inter-satellite radio or optical links; |
| x | satellite routing and switching systems; |
| x | satellite beamforming systems; |
| x | regenerative satellite payloads; |
| x | transparent or bent-pipe satellite payloads having protected control elements; |
| x | hybrid terrestrial/satellite networks; and |
| x | future non-terrestrial communication platforms having equivalent communication-control boundaries. |

In such systems, network-control software, routing software, modem software, beam-selection logic, machine-learning components, mobility controllers, satellite schedulers, gateway controllers, or other upstream components may calculate, recommend, or select a communication operation.

The fact that such a component has computed or selected the operation does not, by itself, constitute authority for the corresponding RF, beam, modem, routing, gateway, or inter-satellite action to become effective.

The selected operation may therefore be represented as a Candidate Act and maintained in a Non- Effective State until verified at a communication Finality Sink.

# 67C.2 Technical Problem

Satellite and non-terrestrial communication systems may perform frequent consequential transitions including:

| x | selection of a satellite; |
|---|---|
| x | selection of a communication beam; |
| x | reassignment from one beam to another; |
| x | handover from one satellite to another; |
| x | activation of a new RF carrier; |
| x | change of frequency; |
| x | change of transmit power; |
| x | change of polarization; |
| x | activation of an electronically steered antenna direction; |
| x | gateway reassignment; |
| x | feeder-link reassignment; |
| x | service-link reassignment; |
| x | route change; |
| x | inter-satellite link establishment; |
| x | inter-satellite next-hop change; |
| x | transition between terrestrial and satellite communication paths; |
| x | activation of a higher-throughput or higher-power transmission mode; or |
| x | communication into a geographic or regulatory region having different restrictions. |

Page 85

These decisions may be generated rapidly and may depend on changing information such as:

| x | satellite visibility; |
|---|---|
| x | terminal position; |
| x | predicted link duration; |
| x | obstruction; |
| x | signal strength; |
| x | propagation conditions; |
| x | satellite loading; |
| x | gateway availability; |
| x | geographic service area; |
| x | frequency authorization; |
| x | policy; |
| x | routing state; |
| x | traffic class; |
| x | mobility; |
| x | network congestion; |
| x | weather information; |
| x | satellite ephemeris; |
| x | link failure; |
| x | terminal state; or |
| x | service-level requirements. |

A valid network credential or authenticated command does not necessarily establish that the concrete communication operation presented to the RF or routing hardware remains the operation that was authorized.

Similarly, authority to use a first satellite, beam, gateway, path, frequency, or geographic service region does not necessarily authorize a second satellite, beam, gateway, path, frequency, or region.

The disclosed architecture therefore separates:

selection or computation of a communication operation\\text{selection or computation of a communication operation} from:

authority to make that exact communication operation effective.\\text{authority to make that exact communication operation effective}.

# 67C.3 Representative Satellite/NTN Architecture

A representative implementation comprises:

```
+------------------------------------------------------------+
| NETWORK / MOBILITY / ROUTING CONTROL PLANE
|
| satellite selector | beam selector | route controller
| gateway selector | modem scheduler | AI/ML controller
+------------------------------+-----------------------------+
```

```
|
| proposed communication act
```

```
|
|
|
|
```

```
v
+------------------------------------------------------------+
| CANDIDATE ACT CANONICALIZER |
```

Page 86

```
| |
| target satellite / beam / gateway / route / RF parameters |
+------------------------------+-----------------------------+
|
```

```
v
+------------------------------------------------------------+
| PROTECTED EXECUTION DOMAIN |
```

```
|
| authority verification
| policy + revocation state
| geographic / spectrum context
| freshness + anti-replay
| keyed Binding Commitment
| receipt state
+----------------------+---------------------+---------------+
|
```

```
|
|
|
|
|
|
|
|
```

```
|
v
+----------------+
| Protected |
| State Store |
+----------------+
```

```
| compact BPC
v
+----------------------+
| Control / Beacon / |
| Management Transport |
+----------------------+
|
```

```
v
+------------------------------------------------------------+
| COMMUNICATION FINALITY SINK |
```

```
|
| independently reconstruct actual pending operation
| verify act/sink/context/currentness
| consume freshness state
| commit Finality Receipt
| release bounded communication capability
+------------------------------+-----------------------------+
|
```

```
|
|
|
|
|
|
```

```
v
+------------------------------------------------------------+
| EFFECTUATION BOUNDARY |
```

```
| |
| phased array / beamformer / modem / RF chain / gateway |
| router / switch / optical ISL / baseband / transmit enable |
+------------------------------------------------------------+
```

The Protected Execution Domain and communication Finality Sink may be separate components or may be integrated into a secure modem, secure baseband processor, satellite payload processor, user-terminal controller, gateway controller, FPGA, ASIC, secure microcontroller, or equivalent protected subsystem.

# 67C.4 Satellite/NTN Candidate Acts

A Candidate Act in a satellite or non-terrestrial system may represent any communication operation whose effect is intended to be controlled.

Non-limiting act classes include:

```
SATELLITE_SELECT
SATELLITE_HANDOVER
BEAM_SELECT
BEAM_HANDOVER
BEAM_ACTIVATE
BEAM_STEER
```

Page 87

```
RF_TRANSMIT
RF_MODE_CHANGE
POWER_CHANGE
FREQUENCY_CHANGE
POLARIZATION_CHANGE
GATEWAY_SELECT
GATEWAY_HANDOVER
FEEDER_LINK_CHANGE
SERVICE_LINK_CHANGE
TERRESTRIAL_NTN_PATH_SWITCH
INTER_SATELLITE_LINK_ESTABLISH
INTER_SATELLITE_LINK_CHANGE
ROUTE_NEXT_HOP_CHANGE
TRAFFIC_PATH_CHANGE
OPTICAL_LINK_ACTIVATE
TERMINAL_ASSOCIATION
```

The act class names are non-limiting.

# 67C.5 Satellite Selection Candidate Act

A satellite-selection Candidate Act may be represented as:

```
CandidateAct {
version,
act_class = SATELLITE_SELECT,
terminal_id,
current_satellite_ref,
target_satellite_ref,
service_region,
frequency_profile,
beam_profile,
traffic_class,
validity_window,
sink_id
}
```

The target satellite may be represented using:

| x | satellite identifier; |
|---|---|
| x | constellation-relative index; |
| x | ephemeral identifier; |
| x | cryptographic satellite reference; |
| x | orbital-plane and slot reference; |
| x | locally assigned session identifier; or |
| x | another deterministic identifier. |

The Candidate Act need not expose the target satellite publicly where privacy or network-security considerations favor a compact or pseudonymous reference.

# 67C.6 Satellite Handover Candidate Act

A handover from satellite S1S\_1 to satellite S2S\_2 may be represented as:

```
CandidateAct {
act_class = SATELLITE_HANDOVER,
```

Page 88

```
terminal_ref,
source_satellite = S1,
destination_satellite = S2,
destination_beam = B2,
frequency_profile = F2,
handover_window = TW,
service_region = G,
sink = TERMINAL_LINK_FINALITY_SINK
}
```

The handover Candidate Act may further bind:

| x | source beam; |
|---|---|
| x | destination beam; |
| x | source frequency; |
| x | destination frequency; |
| x | channel; |
| x | polarization; |
| x | session reference; |
| x | expected link class; |
| x | terminal geographic region; |
| x | maximum transmit-power envelope; |
| x | traffic class; |
| x | network slice; |
| x | service class; |
| x | gateway reference; or |
| x | routing context. |

A handover authorization for S1→S2S\_1 \\rightarrow S\_2 is not valid for:

S1→S3S\_1 \\rightarrow S\_3

unless separately authorized or expressly covered by a bounded authority object.

# 67C.7 Beam-Selection Candidate Act

For an electronically steered or phased-array terminal, a beam Candidate Act may comprise:

```
CandidateAct {
act_class = BEAM_SELECT,
terminal_ref,
satellite_ref,
beam_ref,
steering_region,
frequency_profile,
polarization_profile,
transmit_power_envelope,
time_window,
sink = BEAMFORMER_FINALITY_SINK
}
```

The steering\_region may comprise:

| x | beam index; |
|---|---|
| x | azimuth/elevation envelope; |

Page 89

| x | direction-cosine envelope; |
|---|---|
| x | antenna-panel identifier; |
| x | subarray identifier; |
| x | cell identifier; |
| x | satellite-relative pointing reference; |
| x | coarse angular region; or |
| x | cryptographic commitment to a more detailed steering solution. |

The Candidate Act may authorize a bounded steering envelope rather than an individual antennaweight update.

Individual low-level beamformer coefficients may then be admitted while remaining inside the authorized envelope.

# 67C.8 RF Transmission Candidate Act

A satellite RF transmission Candidate Act may comprise:

```
CandidateAct {
act_class = RF_TRANSMIT,
terminal_or_payload_ref,
link_type,
satellite_or_peer_ref,
frequency_class,
bandwidth_class,
polarization,
power_envelope,
traffic_class,
geographic_scope,
start_window,
expiry,
sink = RF_FINALITY_SINK
}
```

The RF Finality Sink may control:

| x | transmit-enable; |
|---|---|
| x | power-amplifier enable; |
| x | modem transmit state; |
| x | baseband-to-RF admission; |
| x | carrier activation; |
| x | beamformer enable; |
| x | RF switch; |
| x | frequency synthesizer admission; |
| x | protected baseband register; |
| x | antenna-panel enable; or |
| x | another signal prerequisite to transmission. |

A valid upstream routing or modem decision does not by itself cause RF transmission.

# 67C.9 Gateway-Selection Candidate Act

A gateway-selection Candidate Act may comprise:

Page 90

```
CandidateAct {
act_class = GATEWAY_SELECT,
satellite_ref,
source_gateway_ref,
target_gateway_ref,
feeder_link_ref,
service_region,
traffic_class,
route_scope,
validity_window,
sink = GATEWAY_ADMISSION_SINK
}
```

The gateway Finality Sink may be positioned:

| x | within a satellite payload; |
|---|---|
| x | within gateway routing infrastructure; |
| x | in a protected network controller; |
| x | at a feeder-link modem; |
| x | at a switching or forwarding element; or |
| x | at another point where the gateway selection becomes operationally effective. |

A change from gateway G1G\_1 to gateway G2G\_2 may therefore require a distinct Candidate Act.

# 67C.10 Inter-Satellite Link Candidate Act

For satellites supporting inter-satellite communication, an inter-satellite link Candidate Act may comprise:

```
CandidateAct {
act_class = INTER_SATELLITE_LINK_ESTABLISH,
local_satellite_ref,
peer_satellite_ref,
link_ref,
link_type,
frequency_or_optical_profile,
pointing_or_terminal_ref,
traffic_scope,
validity_window,
sink = ISL_FINALITY_SINK
}
```

The Finality Sink may control:

| x | optical terminal activation; |
|---|---|
| x | RF inter-satellite transmitter; |
| x | pointing acquisition; |
| x | link admission; |
| x | switching fabric; |
| x | routing table activation; |
| x | forwarding permission; or |
| x | another link-effectuation boundary. |

# 67C.11 Inter-Satellite Routing Candidate Act

Page 91

A routing Candidate Act may represent the admission of a next hop or bounded route.

For example:

```
CandidateAct {
act_class = ROUTE_NEXT_HOP_CHANGE,
local_node,
destination_prefix_or_service,
current_next_hop,
proposed_next_hop,
link_ref,
traffic_class,
route_epoch,
validity_window,
sink = ROUTING_FINALITY_SINK
}
```

A route Candidate Act may alternatively contain a route digest:

DR=H(C(Route))D\_R = H(C(Route))

where Route comprises an ordered or otherwise deterministic representation of authorized next hops or path constraints.

The routing Finality Sink may be implemented at:

| x | a forwarding table commit boundary; |
|---|---|
| x | switching fabric; |
| x | packet scheduler; |
| x | optical link scheduler; |
| x | protected router; |
| x | secure network processor; or |
| x | equivalent routing-effectuation component. |

# 67C.12 Hybrid Terrestrial/NTN Path Candidate Act

Where a terminal can use both terrestrial and non-terrestrial communication, a path transition may be represented as:

```
CandidateAct {
act_class = TERRESTRIAL_NTN_PATH_SWITCH,
device_ref,
source_path,
destination_path,
service_class,
destination_scope,
traffic_class,
validity_window,
sink = PATH_FINALITY_SINK
}
```

Thus authority to use a terrestrial link is not automatically authority to use a satellite path, and authority to use one satellite path is not automatically authority to use a different satellite path.

Page 92

# 67C.13 Satellite Context Object

The context bound to a satellite Candidate Act may comprise:

```
SatelliteContext {
terminal_region,
satellite_visibility_epoch,
satellite_ref,
beam_ref,
gateway_ref,
frequency_policy_epoch,
spectrum_region,
link_state,
obstruction_class,
mobility_state,
routing_epoch,
policy_epoch,
revocation_epoch,
time_slot
}
```

The Context Commitment may be:

DC=H(DOMC∥C(SatelliteContext))D\_C = H(DOM\_C \\parallel C(SatelliteContext))

Not every field is required for every act.

The selected fields are those material to the particular effect.

# 67C.14 Binding Commitment for Satellite Acts

A representative keyed Binding Commitment is:

B=HMACKbind(DOMSAT∥DA∥S∥R∥DC∥EP∥ER∥N∥Texp)B = HMAC\_{K\_{bind}} ( DOM\_{SAT} \\parallel D\_A \\parallel S \\parallel R \\parallel D\_C \\parallel E\_P \\parallel E\_R \\parallel N \\parallel T\_{exp} )

where:

| x | DAD_A is the Act Commitment; |
|---|---|
| x | SS identifies the communication Finality Sink; |
| x | RR is the Authority Reference; |
| x | DCD_C is the satellite Context Commitment; |
| x | EPE_P is the Policy Epoch; |
| x | ERE_R is the Revocation Epoch; |
| x | NN is freshness information; |
| x | TexpT_{exp} is the expiry or validity bound. |

For a satellite handover:

DA=H(C(Terminal,Ssource,Starget,Beamtarget,FrequencyProfile,PowerEnvelope,Window))D\_A = H( C( Terminal, S\_{source}, S\_{target}, Beam\_{target}, FrequencyProfile, PowerEnvelope, Window ) )

Accordingly, alteration of the destination satellite, beam, RF profile, time window, or sink produces a different binding.

Page 93

# 67C.15 Compact Satellite Beacon Proof Capsule

A representative satellite/NTN BPC may contain:

```
SAT_BPC {
version_profile,
act_class,
sink_class,
authority_ref,
target_ref,
policy_epoch,
revocation_epoch,
freshness,
expiry_delta,
context_ref,
compact_binding,
authenticator
}
```

Representative compact fields may use:

| x | target satellite dictionary index; |
|---|---|
| x | beam dictionary index; |
| x | gateway index; |
| x | short-lived satellite-session identifier; |
| x | frequency-profile index; |
| x | power-envelope class; |
| x | geographic-cell index; |
| x | traffic-class bitmap; |
| x | truncated keyed commitment; |
| x | truncated message-authentication tag. |

The invention is not limited to a fixed field size.

# 67C.16 Handover Workflow

A representative terminal handover proceeds as follows.

### Stage 1 - Candidate selection

A mobility controller determines candidate destination satellite S2S\_2.

The mobility controller may use:

| x | visibility; |
|---|---|
| x | link quality; |
| x | expected dwell time; |
| x | obstruction; |
| x | network load; |
| x | terminal mobility; |
| x | latency; |
| x | gateway reachability; or |
| x | another metric. |

Page 94

This selection is advisory at this stage.

### Stage 2 - Candidate Act creation

The proposed handover is represented as:

AH=(Terminal,S1,S2,B2,F2,Pmax,TH,Sink)A\_H = ( Terminal, S\_1, S\_2, B\_2, F\_2, P\_{max}, T\_H, Sink )

### Stage 3 - Authority verification

The Protected Execution Domain verifies that applicable authority permits:

| x | use of destination satellite S2S_2; |
|---|---|
| x | use of beam B2B_2; |
| x | relevant frequency profile; |
| x | geographic service region; |
| x | permitted power; |
| x | traffic class; |
| x | handover period. |

### Stage 4 - Binding

A keyed Binding Commitment is generated.

### Stage 5 - Non-Effective staging

The modem or phased-array controller may prepare:

| x | receive synchronization; |
|---|---|
| x | candidate beam weights; |
| x | timing; |
| x | acquisition parameters; |
| x | routing state. |

However, transmit or committed handover effectuation remains blocked.

### Stage 6 - Finality Sink reconstruction

Immediately before effectuation, the Finality Sink independently reads the operation actually pending at the modem, beamformer, or RF chain:

```
actual_target_satellite
actual_target_beam
actual_frequency_profile
actual_power_envelope
actual_terminal_region
actual_time_window
```

### Stage 7 - Currentness check

The Finality Sink obtains current:

```
policy_epoch
revocation_epoch
frequency_policy_epoch
service_region
freshness state
```

### Stage 8 - Comparison and atomic commit

Page 95

The Finality Sink recomputes the expected binding.

If it matches, the nonce is consumed, a Finality Receipt is committed, and a bounded handover capability is released.

### Stage 9 - Effectuation

Only then may the modem, phased-array controller, or RF path activate the new satellite/beam configuration.

# 67C.17 Representative Handover Pseudocode

```
FUNCTION AuthorizeSatelliteHandover(
source_sat,
target_sat,
target_beam,
rf_profile,
terminal_state
):
```

```
context = ReadProtectedSatelliteContext()
act = CandidateAct(
class = SATELLITE_HANDOVER,
source_satellite = source_sat,
target_satellite = target_sat,
target_beam = target_beam,
rf_profile = rf_profile,
region = context.service_region,
sink = TERMINAL_LINK_FINALITY_SINK
)
```

```
authority = ResolveAuthority(act)
IF authority == UNKNOWN:
RETURN DENY
```

```
IF NOT AuthorityAllows(authority, act, context):
RETURN DENY
```

```
nonce = ReserveFreshNonce()
act_digest =
HASH("SAT_ACT" || Canonicalize(act))
context_digest =
HASH("SAT_CTX" || Canonicalize(
SelectBoundSatelliteContext(context)
))
binding =
HMAC(K_bind,
"SAT_BIND" ||
act_digest ||
TERMINAL_LINK_FINALITY_SINK ||
authority.ref ||
context.policy_epoch ||
context.revocation_epoch ||
context_digest ||
nonce ||
Expiry(act)
)
```

Page 96

```
RETURN EncodeSatelliteBPC(
act.class,
target_sat,
target_beam,
authority.ref,
context.policy_epoch,
context.revocation_epoch,
nonce,
context_digest,
TRUNCATE(binding, BindingBits(act)),
AuthenticateBeacon(...)
)
```

# 67C.18 Final Handover Verification Pseudocode

```
FUNCTION VerifyAndCommitHandover(bpc):
```

```
IF NOT AuthenticateBPC(bpc):
RETURN SAFE_LINK_STATE
```

```
IF IsExpired(bpc):
RETURN SAFE_LINK_STATE
IF IsConsumed(bpc.nonce):
RETURN SAFE_LINK_STATE
```

```
actual =
ReadPendingLinkConfiguration()
```

```
actual_act =
CanonicalizeSatelliteAct(actual)
```

```
authority =
ResolveAuthority(bpc.authority_ref)
```

```
IF authority == UNKNOWN:
RETURN SAFE_LINK_STATE
context =
ReadCurrentSatelliteContext()
```

```
expected =
HMAC(K_bind,
"SAT_BIND" ||
HASH("SAT_ACT" || actual_act) ||
ActualFinalitySink() ||
bpc.authority_ref ||
CurrentPolicyEpoch() ||
CurrentRevocationEpoch() ||
HASH("SAT_CTX" ||
Canonicalize(
SelectBoundSatelliteContext(context)
)) ||
bpc.nonce ||
bpc.expiry
)
```

```
IF TRUNCATE(expected, bpc.binding_bits)
!= bpc.compact_binding:
RETURN SAFE_LINK_STATE
```

```
BEGIN_ATOMIC_FINALITY_COMMIT()
IF bpc.policy_epoch != CurrentPolicyEpoch():
```

Page 97

```
ABORT
RETURN SAFE_LINK_STATE
```

```
IF bpc.revocation_epoch != CurrentRevocationEpoch():
ABORT
RETURN SAFE_LINK_STATE
```

```
IF NOT ConsumeNonce(bpc.nonce):
ABORT
RETURN SAFE_LINK_STATE
```

```
receipt =
MakeFinalityReceipt(
decision = ALLOW,
binding = expected,
sink = ActualFinalitySink(),
counter = NextCounter()
)
```

```
IF NOT CommitReceipt(receipt):
ABORT
RETURN SAFE_LINK_STATE
```

```
capability =
DeriveCommunicationCapability(
target_satellite = actual.target_satellite,
beam = actual.target_beam,
rf_envelope = actual.rf_profile,
expiry = bpc.expiry
)
```

```
CommitCapability(capability)
END_ATOMIC_FINALITY_COMMIT()
RETURN ENABLE_HANDOVER(capability)
```

# 67C.19 Beamformer Enforcement

A phased-array or electronically steered antenna may calculate antenna coefficients at a rate substantially higher than the rate at which complete authority objects are processed.

Accordingly, authority may be granted over a bounded beam-steering envelope.

For example:

θmin≤θ≤θmax\\theta\_{min} \\le \\theta \\le \\theta\_{max} ϕmin≤ϕ≤ϕmax\\phi\_{min} \\le \\phi \\le \\phi\_{max} Ptx≤PmaxP\_{tx} \\le P\_{max}

and:

t∈[T0,T1]t \\in [T\_0,T\_1]

The Candidate Act may bind these limits together with:

| x | satellite identity; |
|---|---|
| x | antenna panel; |
| x | frequency profile; |
| x | service region; |

Page 98

x Finality Sink.

The beamformer may update individual antenna coefficients without a new full BPC where the resulting beam remains inside the authorized envelope.

Leaving the envelope ends the authorization.

# 67C.20 Beam-Level Finality Predicate

A representative beam activation predicate is:

ALLOWbeam=TargetMatch∧BeamEnvelopeMatch∧FrequencyAllowed∧PowerAllowed∧RegionAllowed∧F resh∧NotReplayed∧PolicyCurrent∧RevocationCurrent∧SinkMatchALLOW\_{beam} = TargetMatch \\land BeamEnvelopeMatch \\land FrequencyAllowed \\land PowerAllowed \\land RegionAllowed \\land Fresh \\land NotReplayed \\land PolicyCurrent \\land RevocationCurrent \\land SinkMatch

Beam activation occurs only when:

ALLOWbeam=TRUEALLOW\_{beam}=TRUE

# 67C.21 Handover Context Change

A BPC generated for a handover may become invalid before effectuation.

Examples include:

| x | target satellite becomes unavailable; |
|---|---|
| x | destination beam changes; |
| x | service-region authorization changes; |
| x | spectrum policy changes; |
| x | terminal crosses into another jurisdictional or service region; |
| x | satellite or gateway is revoked; |
| x | allowed transmit power changes; |
| x | routing epoch changes; |
| x | terminal enters a restricted mode. |

Accordingly:

Contextissued≠Contextcurrent⇒Revalidate or DenyContext\_{issued} \\ne Context\_{current} \\Rightarrow Revalidate \\; or \\; Deny

depending on the deployment profile.

# 67C.22 Fast Handover Profile

For latency-sensitive operation, a complete authority object need not be verified for each handover.

A cold-path process may verify and cache:

```
AuthorityCache {
```

Page 99

```
authority_ref,
permitted_satellite_set,
permitted_beam_classes,
permitted_regions,
frequency_profiles,
power_limits,
traffic_classes,
expiry,
policy_epoch,
revocation_epoch
}
```

The hot path performs:

```
lookup AuthorityRef
check current epochs
verify freshness
read actual pending handover
recompute keyed binding
compare compact binding
consume nonce
commit receipt
release bounded link capability
```

This permits frequent handover decisions without treating cached authority as unrestricted bearer authority.

# 67C.23 Satellite-Set Authority

An Authority Object may authorize a bounded satellite set:

Sallowed={S1,S2,…,Sn}\\mathcal{S}\_{allowed} = \\{S\_1,S\_2,\\ldots,S\_n\\}

A Candidate Act must still identify the selected target satellite.

The Finality Sink checks:

Starget∈SallowedS\_{target}\\in\\mathcal{S}\_{allowed}

and verifies the exact act binding.

Thus membership in an authorized satellite set does not remove exact handover verification.

# 67C.24 Beam-Set Authority

Similarly, authority may permit:

Ballowed={B1,B2,…,Bm}\\mathcal{B}\_{allowed} = \\{B\_1,B\_2,\\ldots,B\_m\\}

or a bounded steering region.

The actual beam selected at effectuation must remain inside the permitted set or region.

Page 100

# 67C.25 Gateway Authority

A gateway Authority Object may specify:

```
GatewayAuthority {
permitted_gateway_set,
service_region,
traffic_class,
feeder_link_profiles,
routing_scope,
policy_epoch,
expiry
}
```

A gateway transition outside this scope is denied even where the terminal or satellite otherwise possesses valid network credentials.

# 67C.26 Inter-Satellite Route Verification

A route controller may compute:

```
Satellite A -> Satellite B -> Satellite C -> Gateway G
```

The route may be represented by:

Route=(A,B,C,G)Route = (A,B,C,G)

and:

DR=H(C(Route))D\_R = H(C(Route))

Alternatively, each next-hop transition may be separately represented as a Candidate Act.

For a next-hop act:

```
CandidateAct {
class = ROUTE_NEXT_HOP_CHANGE,
local_satellite = B,
destination_scope = D,
proposed_next_hop = C,
link = L_BC,
traffic_class = TC,
route_epoch = RE,
sink = ROUTING_FINALITY_SINK
}
```

The routing Finality Sink independently reads the forwarding or switching state about to be committed.

A route proposed for next hop CC cannot be substituted with next hop XX without causing a binding mismatch.

# 67C.27 Inter-Satellite Link Establishment Workflow

Page 101

For establishment of an optical or RF inter-satellite link:

1. link-management software proposes peer satellite SPS\_P;
2. a Candidate Act is formed;
3. authority for the peer, link class, frequency or optical terminal, traffic class, and validity interval is verified;
4. a Binding Commitment is generated;
5. acquisition and pointing may be prepared while link effectuation remains non-effective;
6. the ISL Finality Sink reads the peer and link configuration actually pending;
7. the Finality Sink recomputes and verifies the binding;
8. freshness is consumed and a receipt is committed;
9. only then is forwarding or transmit authority released.

# 67C.28 RF Power Enforcement

Where an Authority Object grants a transmit-power envelope:

0≤Ptx≤Pmax0 \\le P\_{tx} \\le P\_{max} the Finality Sink may allow power-control updates inside the envelope without requiring a full authorization exchange for every update.

If:

Prequested>PmaxP\_{requested} > P\_{max}

then:

Effectuate(RF\_POWER\_CHANGE)=FALSEEffectuate(RF\\\_POWER\\\_CHANGE)=FALSE or the hardware may clamp the requested value:

Peffective=min⁡(Prequested,Pmax)P\_{effective} = \\min(P\_{requested},P\_{max})

where such clamping is permitted by the applicable safety profile.

# 67C.29 Geographic/Spectrum Binding

A satellite communication authority may be geographically scoped.

For example:

```
SpectrumContext {
region_ref,
frequency_profile,
power_limit,
polarization,
service_type,
policy_epoch
}
```

The BPC may commit to:

Page 102

Dspectrum=H(C(SpectrumContext))D\_{spectrum} = H(C(SpectrumContext))

Where a terminal moves into a region having a different permitted profile, a previously valid BPC may require revalidation.

# 67C.30 Terminal Mobility

For a mobile terminal, location may be represented by:

| x | geographic cell; |
|---|---|
| x | coarse region; |
| x | route segment; |
| x | maritime zone; |
| x | aviation region; |
| x | regulatory zone; |
| x | geohash; |
| x | pseudonymous spatial reference; or |
| x | protected Context Commitment. |

Exact location need not be transmitted.

# 67C.31 Safe-Action Set for Satellite/NTN Systems

Failure of a permission-expanding communication Candidate Act need not cause immediate loss of all communication.

A protected Safe-Action Set may comprise one or more of:

| x | continue an already verified existing link for a bounded interval; |
|---|---|
| x | retain a presently verified satellite; |
| x | retain a presently verified beam; |
| x | reduce transmit power; |
| x | reduce bandwidth; |
| x | disable a high-power mode; |
| x | receive-only operation; |
| x | bounded link reacquisition; |
| x | use a previously verified fallback link; |
| x | use a protected emergency signalling channel; |
| x | suspend non-essential traffic; |
| x | restrict operation to management traffic; |
| x | return to a known-safe RF profile; or |
| x | cease transmission. |

The Safe-Action Set is protected and cannot be widened by an untrusted network controller.

# 67C.32 Break-Before-Make and Make-Before-Break Handover

The invention supports both break-before-make and make-before-break handover.

Page 103

### Break-before-make

The source communication path is released before the destination path becomes effective.

The destination path remains non-effective until final verification.

### Make-before-break

A destination receive path or limited preparatory state may be established before source-link termination, while consequence-bearing destination transmission or routing remains subject to Finality Sink verification.

Accordingly, preparatory acquisition does not itself constitute authority for unrestricted destinationlink effectuation.

# 67C.33 Parallel Candidate Links

A terminal may prepare multiple potential links: L1,L2,...,LnL\_1,L\_2,\\ldots,L\_n Each may have a distinct Candidate Act or a common bounded Authority Object.

Only the selected link that satisfies final verification receives an execution capability.

Thus:

Prepared(Li)⇏Authorized(Li)Prepared(L\_i) \\not\\Rightarrow Authorized(L\_i)

# 67C.34 Multi-Beam Operation

Where a terminal or satellite simultaneously operates multiple beams, each beam may be:

| x | independently authorized; |
|---|---|
| x | authorized under a bounded multi-beam Candidate Act; or |
| x | grouped into an authorized beam set. |

A multi-beam Candidate Act may comprise:

```
CandidateAct {
class = MULTI_BEAM_ACTIVATE,
beam_set,
satellite_ref,
aggregate_power_limit,
per_beam_power_limits,
frequency_profiles,
geographic_scope,
time_window,
sink
}
```

The Finality Sink may enforce:

Page 104

∑i=1nPi≤Paggregate,max\\sum\_{i=1}^{n}P\_i \\le P\_{aggregate,max} together with:

Pi≤Pi,maxP\_i \\le P\_{i,max}

for each beam.

# 67C.35 Resource-Budget Binding

A Candidate Act may bind not only identity and destination but also bounded shared-resource consumption.

For example:

BWused≤BWauthorizedBW\_{used} \\le BW\_{authorized} Paggregate≤PauthorizedP\_{aggregate} \\le P\_{authorized} Nactive beams≤NauthorizedN\_{active\\ beams} \\le N\_{authorized}

Such budget state may be maintained in protected state and atomically updated when a capability is released.

# 67C.36 Aggregate Power Atomicity

For multiple beams or transmitters sharing a power budget, the Finality Sink may atomically verify and update:

Pcurrent+Prequested≤PbudgetP\_{current}+P\_{requested}\\le P\_{budget}

before enabling the new transmission.

The budget update and capability release may occur in the same atomic finality commit.

# 67C.37 Constellation or Fleet Binding

Where a network controller issues one high-level operation to multiple satellites or terminals, the operation may result in unit-specific Candidate Acts:

Bi=HMACKi(DAi∥Sinki∥Contexti∥Ni)B\_i = HMAC\_{K\_i} ( D\_{A\_i} \\parallel Sink\_i \\parallel Context\_i \\parallel N\_i )

Authority for satellite or terminal ii therefore does not automatically authorize satellite or terminal jj.

# 67C.38 Gateway Failover

If gateway G1G\_1 fails, a controller may propose G2G\_2.

Page 105

The failover is a new Candidate Act unless a prior authority expressly defines a bounded permitted gateway set.

A stale gateway authorization does not automatically make the new path effective.

# 67C.39 Terrestrial/Satellite Failover

A device may have:

```
primary_path = terrestrial
fallback_path = satellite
```

or vice versa.

A fallback Candidate Act may bind:

| x | destination path; |
|---|---|
| x | network class; |
| x | traffic class; |
| x | geographic region; |
| x | time window; |
| x | applicable data or service policy; |
| x | Finality Sink. |

The fallback may be pre-authorized for emergency or continuity use but remains constrained to the defined scope.

# 67C.40 Intermittent Connectivity

Satellite systems may experience temporary inability to reach an authority service.

Verified cached authority may therefore be used within a bounded offline interval:

Toffline≤Toffline,maxT\_{offline} \\le T\_{offline,max}

and:

Teffective=min⁡(Toffline,max,Tauthority-expiry)T\_{effective} = \\min( T\_{offline,max}, T\_{authorityexpiry} )

After expiry, only the Safe-Action Set remains available.

High-consequence operations may be configured as non-offline-capable.

# 67C.41 Protected State for Satellite/NTN Embodiments

Protected state may include:

```
current_policy_epoch
```

Page 106

```
current_revocation_epoch
frequency_policy_epoch
routing_epoch
nonce_cache
satellite_authority_cache
beam_authority_cache
gateway_authority_cache
session_binding_keys
satellite_session_ids
beam_session_ids
current_link_ref
current_satellite_ref
current_beam_ref
current_gateway_ref
aggregate_power_budget
replay_store
receipt_chain_head
safe_action_set
```

Protected state may be held in:

| x | secure baseband memory; |
|---|---|
| x | TEE-sealed storage; |
| x | secure element; |
| x | HSM; |
| x | protected FPGA memory; |
| x | anti-rollback flash; |
| x | redundant safety memory; |
| x | satellite payload processor; or |
| x | equivalent protected storage. |

# 67C.42 Representative Terminal Hardware Implementation

A terminal embodiment may comprise:

```
Network/Mobility Processor
|
```

```
v
Protected Execution Domain
|
```

```
v
Link Finality Sink
|
+-----+------+
| |
v v
Baseband Beamformer
| |
+-----+------+
|
```

```
v
RF Front End / Phased Array
```

The Finality Sink may be integrated:

| x | inside the modem; |
|---|---|
| x | between modem and beamformer; |
| x | inside the beamformer controller; |

Page 107

| x | inside a secure baseband processor; |
|---|---|
| x | in an FPGA controlling RF enable; |
| x | in a secure antenna controller; or |
| x | across multiple protected components. |

# 67C.43 Representative Satellite Hardware Implementation

A satellite embodiment may comprise:

```
Routing / Resource Controller
|
v
Protected Execution Domain
|
v
```

|  | Satellite Finality Sink |  |
|---|---|---|
| / | \| | \\ |
| v | v | v |
| Beamformer | RF Path | ISL Router |

```
|
v
Optical/RF ISL
```

The architecture applies whether routing and beam decisions are computed onboard, on the ground, or jointly.

# 67C.44 Failure Conditions

A satellite or NTN Candidate Act may be denied for:

```
TARGET_SATELLITE_MISMATCH
TARGET_BEAM_MISMATCH
GATEWAY_MISMATCH
ROUTE_MISMATCH
SINK_MISMATCH
RF_PROFILE_MISMATCH
POWER_ENVELOPE_EXCEEDED
FREQUENCY_NOT_AUTHORIZED
REGION_NOT_AUTHORIZED
POLICY_EPOCH_MISMATCH
REVOCATION_EPOCH_MISMATCH
ROUTING_EPOCH_MISMATCH
STALE_HANDOVER
REPLAY
UNKNOWN_AUTHORITY_REFERENCE
CONTEXT_MISMATCH
BINDING_MISMATCH
INCOMPLETE_FRAGMENT_SET
AGGREGATE_POWER_BUDGET_EXCEEDED
```

Denial does not imply arbitrary shutdown; the protected Safe-Action Set is selected according to the operational state.

# 67C.45 Example 1 - Terminal Satellite Handover

Page 108

A user terminal is communicating through:

```
Satellite = SAT-41
Beam = B-18
```

The mobility controller proposes:

```
SAT-41 / B-18
->
SAT-57 / B-07
```

The Protected Execution Domain forms:

```
CandidateAct {
class = SATELLITE_HANDOVER,
source_sat = SAT-41,
target_sat = SAT-57,
target_beam = B-07,
frequency_profile = FP-3,
max_power = P4,
region = R-22,
sink = LINK_FINALITY_SINK
}
```

The binding includes:

```
authority_ref
policy_epoch = 812
revocation_epoch = 76
nonce = 0xA32F91D4
expiry_delta = 800 ms
```

The modem prepares SAT-57 acquisition.

Immediately before transmit-path activation, the Finality Sink reads the actual target.

If malicious or faulty software substitutes:

```
SAT-62 / B-11
```

then:

DA,actual≠DA,authorizedD\_{A,actual} \\ne D\_{A,authorized} and therefore:

Bactual≠BBPCB\_{actual} \\ne B\_{BPC}

The destination transmit path remains non-effective.

# 67C.46 Example 2 - Beam Power Escalation

A BPC permits:

Ptx≤20WP\_{tx}\\le 20W

Page 109

for Beam B-22 during a defined interval.

Upstream software requests:

Prequested=28WP\_{requested}=28W

The Finality Sink determines:

28W>20W28W>20W and either denies the power increase or, where explicitly permitted, clamps the effective value to the authorized maximum.

The upstream software cannot reinterpret the 20-W authorization as unrestricted power authority.

# 67C.47 Example 3 - Gateway Failover

Traffic is routed through Gateway G-1.

A network controller proposes failover to G-4.

The Candidate Act binds:

```
source_gateway = G-1
target_gateway = G-4
traffic_class = USER_DATA
region = REGION-3
route_epoch = 92
sink = GATEWAY_ADMISSION_SINK
```

If the actual switching state points instead to G-8, verification fails.

# 67C.48 Example 4 - Inter-Satellite Next-Hop Change

Satellite S-14 currently forwards a traffic class to S-15.

Routing software proposes S-14 → S-19.

The Candidate Act binds:

```
local_satellite = S-14
next_hop = S-19
link = L-1419
traffic_class = TC-4
routing_epoch = 1108
sink = ROUTING_FINALITY_SINK
```

A forwarding-table write substituting S-21 causes an act mismatch and is rejected before the route becomes effective.

# 67C.49 Example 5 - Hybrid Path Transition

Page 110

A mobile terminal loses terrestrial connectivity.

The system possesses pre-authorized fallback authority for satellite service limited to:

```
traffic_class = emergency_and_control
region = R5
max_power = P2
duration = 10 minutes
```

The fallback Candidate Act is verified.

Normal bulk traffic remains non-authorized because the fallback Authority Object does not permit that traffic class.

Thus network continuity does not expand authorization.

# 67C.50 Security Invariants for Satellite/NTN Operation

The satellite embodiment may maintain the following invariants.

### Exact link binding

Authorized(S1,B1)⇏Authorized(S2,B2)Authorized(S\_1,B\_1) \\not\\Rightarrow Authorized(S\_2,B\_2)

### Exact sink binding

Binding(A,Sink1)≠Binding(A,Sink2)Binding(A,Sink\_1) \\ne Binding(A,Sink\_2)

for distinct protected sinks except with negligible cryptographic probability.

### Handover freshness

Expired(Handover)⇒NoEffectuationExpired(Handover) \\Rightarrow NoEffectuation

### Replay resistance

Consumed(N)⇒Reject(N)Consumed(N) \\Rightarrow Reject(N)

### Currentness

PolicyBPC≠Policycurrent⇒Revalidate or DenyPolicy\_{BPC} \\ne Policy\_{current} \\Rightarrow Revalidate\\;or\\;Deny

### Route substitution resistance

NextHopactual≠NextHopauthorized⇒NoRouteCommitNextHop\_{actual} \\ne NextHop\_{authorized} \\Rightarrow NoRouteCommit

### Beam substitution resistance

Beamactual≠Beamauthorized⇒NoBeamEffectuationBeam\_{actual} \\ne Beam\_{authorized} \\Rightarrow NoBeamEffectuation

### Power budget enforcement

Prequested>Pauthorized⇒NoUnauthorizedPowerIncreaseP\_{requested}>P\_{authorized} \\Rightarrow NoUnauthorizedPowerIncrease

### Evidence completeness

IncompleteEvidence⇒NoPermissionExpansionIncompleteEvidence \\Rightarrow NoPermissionExpansion

# 67C.51 Additional Claim-Oriented Statements

The following statements identify additional claim directions and do not limit the disclosure.

**Statement 19. A satellite or non-terrestrial communication system in which selection of a satellite,**

beam, gateway, route, frequency, RF power, or communication path is represented as a Candidate Act and independently verified at a communication Finality Sink before effectuation.

Page 111

**Statement 20. The system of Statement 19 wherein an electronically steered or phased-array**

antenna is prevented from activating a selected beam or transmit configuration unless an actual pending beam configuration corresponds to a cryptographically bound Candidate Act.

**Statement 21. The system wherein a satellite handover Candidate Act binds at least a source**

satellite, target satellite, target beam or link, freshness state, and communication Finality Sink.

**Statement 22. The system wherein a selected handover may be prepared by a modem or antenna**

controller while transmission through the destination satellite or beam remains non-effective pending Finality Sink verification.

**Statement 23. The system wherein authority covers a bounded beam-steering, RF-power,**

frequency, bandwidth, route, or communication envelope and lower-level control updates are admitted while remaining inside said envelope.

**Statement 24. The system wherein authority applicable to a first satellite, beam, gateway, route,**

frequency, terrestrial path, or non-terrestrial path is insufficient by itself to authorize a second satellite, beam, gateway, route, frequency, or path.

**Statement 25. The system wherein an inter-satellite routing operation is represented as a Candidate**

Act bound to a next-hop satellite or route commitment and verified at a forwarding, switching, routing, optical-link, or RF-link Finality Sink.

**Statement 26. The system wherein an inter-satellite link establishment operation is held non-**

effective while acquisition or pointing is prepared and becomes effective only following verification of peer identity, link parameters, authority, freshness, context, and sink binding.

**Statement 27. The system wherein a satellite user terminal or payload enforces an aggregate**

transmit-power, bandwidth, active-beam, or equivalent resource budget in protected state and atomically updates said budget before releasing an additional communication capability.

**Statement 28. The system wherein verified Authority Objects are processed on a cold path while**

satellite-, beam-, route-, or RF-specific Candidate Act bindings are verified on a lower-latency hot path.

**Statement 29. The system wherein a Safe-Action Set for a satellite or non-terrestrial**

communication device preserves a previously verified link, receive-only mode, reduced-power mode, bounded reacquisition, fallback communication, or communication shutdown when a permission-expanding Candidate Act cannot be verified.

**Statement 30. The system wherein multiple candidate satellites, beams, gateways, or routes may be**

prepared but only the candidate associated with a successfully verified execution-finality capability becomes effective.

## 68. CONCLUSION

The disclosed architecture solves the technical problem of carrying or referencing execution-specific authority through a constrained beacon without reducing strong execution authorization to a transferable identifier or simple bearer token, and of evidencing execution-specific decisions to third parties over the same constrained channels with origin in the protected domain.

Page 112

The Candidate Act remains non-effective while the system creates and transmits a compact, keyed, cryptographically bound representation of the act, sink, authority, freshness, context, and policy state. Where the available radio payload is insufficient, the system provides deterministic compression, authenticated references, budgeted truncation, authenticated fragmentation, and protected resolver mechanisms. The downstream Finality Sink independently determines the actual impending effect, reads current policy and revocation state inside an atomic commit, consumes freshness state, commits a receipt, and only then makes the act physically or externally effective. The protected domain may further broadcast compact act-decision evidence authenticated by a delayed-

Page 113

disclosure key chain that only it holds, verifiable by observers without per-act signatures and tolerant of loss. Accordingly, the architecture preserves the central technical invariants:

---

Compact communication of authority ≠ automatic authority to effectuate

---

No complete, fresh, act-bound, sink-bound, currently valid verification ⇒ No effectuation

---

Broadcast evidence of a decision ≠ authority to act

---

The invention therefore enables execution-finality enforcement and evidence in UAV, UAS, drone, autonomous vehicle, robotic, IoT, autonomous-system, and other cyber-physical environments where the available beacon, discovery, telemetry, V2X, bus, or control channel is too constrained to carry a full conventional authorization object at every consequential operation.

Page 114

# NARROW AUTONOMOUS-MOTION EXECUTION-FINALITY EMBODIMENTS

**Conflict-Set-Bound Detect-and-Avoid Finality; Emergency-Scene Temporary Authority Finality; and Atomic Control-Authority Handover Finality**

*Technical Disclosure and Draft Claim Set*

Inventor: Sangam Das Independent Inventor Balasore, Odisha, India Email: info@sangamdas.com

*Prepared as additional detailed embodiments for incorporation into the preceding provisional specification. Broader execution-finality subject matter is not restated except where needed to enable these narrower mechanisms. Draft technical/patent text for review; not a legal opinion on patentability, validity, freedom to operate, or claim scope.*

Page 1

# PROBLEM AND SOLUTION

## Problem

The preceding provisional specification provides the broader execution-finality and constrained-beacon foundation. These additional embodiments address three narrower autonomous-motion failure modes that can remain even when identity, authentication, authorization, planning, geofencing, collision-avoidance computation, and remote-control credentials are otherwise valid: (i) a detect-and-avoid maneuver can become stale because the conflict set changes before motion admission; (ii) an autonomous vehicle can require a legitimate but temporary first-responder exception without granting standing or unrestricted remote-driving authority; and (iii) two individually authorized controllers can create split-brain actuation during takeover, failover, or handover.

## Solution

The disclosed additions apply execution finality specifically to those three boundaries. A DAA resolution is bound to the relevant conflict set, ownship state, uncertainty, resolution epoch, and motion-admission sink and is revalidated against a current pre-effect snapshot. Emergency-scene authority is made vehicle-, incident-, scene-, act-, time-, and sink-specific and is conditioned on local corroboration and automatic extinction. Control transfer is treated as a protected Candidate Act performed through a prepare-commit-enable transaction in which a monotonic authority epoch makes stale commands non-effective and enforces exclusive ordinary controller authority at the governed sink.

# 1. SCOPE AND COMMON DEFINITIONS

The embodiments are directed to autonomous or highly automated cyber-physical platforms, including unmanned aircraft, aerial robots, automated road vehicles, robotaxis, shuttles, delivery vehicles, agricultural vehicles, mining vehicles, port vehicles, mobile robots, and related motion-control systems. Each embodiment treats a proposed consequential motion or authority transition as a Candidate Act that remains non-effective until a protected executionfinality condition is satisfied at or immediately upstream of the boundary where the act can become operationally effective.

## 1.1 Common Terms

**Candidate Act. A proposed maneuver, trajectory, path, control-authority transition, temporary rule exception, or other**

consequence-bearing operation that may be computed, received, authenticated, approved, or staged but is not yet permitted to become physically or operationally effective.

**Non-Effective State. A state in which the Candidate Act is prevented from reaching the governed actuator, motion**

controller, path-admission interface, mode-transition register, or equivalent consequence-bearing boundary.

**Protected Finality Domain. A hardware-rooted, safety-isolated, cryptographically isolated, or otherwise protected**

domain that maintains authority state, freshness state, epochs, nonces, commitments, and finality records and that cannot be bypassed by ordinary autonomy software.

**Finality Sink. The interface at which the Candidate Act first becomes capable of producing the governed consequence,**

including a motion-admission gate, flight-control trajectory gate, steering/braking/throttle controller, actuator-enable interface, mode-transition register, or comparable boundary.

**Scoped Capability. A sink-verifiable artifact or protected enable condition bound to the exact Candidate Act or**

permitted envelope, target sink, authority state, freshness condition, and expiry. Possession alone is insufficient if the actual effectuation state does not match the binding.

**Safe-Action Set. A pre-authorized set of stabilizing or risk-reducing actions that remains available when ordinary or**

expanded authority is withheld. Examples include braking, holding lane, hover, controlled deceleration, speed reduction, controlled descent, minimal-risk stop, or maintenance of basic stability.

**Authority Epoch. A monotonic protected value identifying a particular authority state. Commands bound to a prior**

epoch become stale when the epoch advances.

Page 2

**Finality Receipt. A protected record, optionally signed, MAC-protected, hash-linked, or remotely auditable, recording**

the Candidate Act or commitment, authority state, decision, relevant context commitment, epoch, sink, and monotonic state transition.

## 1.2 Common Atomic Ordering

Where a capability or enable condition is released, the preferred ordering is:

read current state <= validate <= reserve/consume freshness <= commit protected finality state < release capability <=

effectuate A protected implementation may combine reserve, commit, and capability creation in a single atomic record or may use a write-ahead or two-phase transaction, provided that a capability not associated with a committed protected state cannot cause effectuation.

# 2. EMBODIMENT 1 - CONFLICT-SET-BOUND DETECT-AND-AVOID MANEUVER FINALITY

## 2.1 Technical Problem

A detect-and-avoid system may correctly identify an intruder and compute a valid resolution maneuver at an initial time, yet the traffic picture can change before that maneuver reaches the flight-control or trajectory-admission boundary. A second intruder may appear, an existing track may move or be reclassified, uncertainty may expand, a surveillance source may become stale, ownship state may diverge from the state used for the resolution, or an independent DAA source may supersede the earlier resolution. Authentication of the original DAA output does not establish that the maneuver remains safe at the moment it becomes motion-effective. The narrower technical contribution is therefore not generic collision avoidance. It is the binding of a concrete DAA resolution to the conflict set and safety state for which that resolution was calculated, followed by sink-adjacent verification that the relevant conflict set and margins remain valid before the motion envelope is admitted.

## 2.2 Technical Solution and Architecture



tracks

Sensors / Traffic Tracks

+ Ownship State

DAA Engine rroidate

Maneuver candidate Protected Finality Domain bound capability

Motion-Admission

Conflict-Set Root Finalink

+ Resolution Epoch match + safe

release after verify

mismatch / risk fail pre-effect snapshot Flight Controller /

Safe-Action Set Current Conflict Snapshot

Recompute / Hold + Ownship Snapshot Authorzd Actuator

+ Risk Re-evaluation Eneope

Invariant: an avoidance maneuver is not motion authority unless the relevant conflict set and required safety margins remain valid at effectuation.

**Figure 1 - Conflict-set-bound DAA finality architecture**

Page 3

A representative system includes: (i) one or more traffic and environment sources; (ii) an ownship-state source; (iii) a DAA computation engine; (iv) a Protected DAA Finality Domain; (v) a protected Conflict-Set State Store; (vi) a Resolution-Epoch Register; (vii) a motion-admission Finality Sink; and (viii) a Safe-Action Controller. The DAA computation engine may remain ordinary or high-performance software. The Protected DAA Finality Domain, rather than the DAA engine, controls whether a proposed resolution obtains authority to enter the motion-control path.

## 2.3 Canonical Conflict Set and Resolution Descriptor

For each policy-relevant intruder j, a canonical intruder descriptor may include track reference, source class, cooperative or non-cooperative class, relative position, relative velocity, acceleration estimate where used, covariance or bounded uncertainty, time of last trusted observation, freshness class, closest-point-of-approach quantities, track confidence class, sensor provenance reference, and any airspace or right-of-way class relevant to the applicable safety rule. The protected domain deterministically sorts the descriptors, for example by a stable track reference or canonical digest, and forms a Conflict-Set Root:

C\_root = H( CanonicalSort( I\_1 || I\_2 || ... || I\_n ) ) A DAA Resolution Descriptor may bind:

- ownship state commitment and ownship-state epoch;
- Conflict-Set Root and, where appropriate, a compact membership structure or Merkle root;
- resolution epoch;
- proposed maneuver or trajectory-tube digest;
- time horizon and latest admissible effectuation time;
- required separation class and uncertainty treatment;
- DAA algorithm or policy profile identifier;
- sensor-source and surveillance-state epochs;
- target motion-admission sink identifier;
- policy epoch, revocation epoch, nonce, and monotonic counter.

## 2.4 Safety Mathematics

One non-limiting kinematic check may use relative position r\_j and relative velocity v\_j for intruder j. For a bounded horizon T, the predicted closest-point time is:

t\_CPA,j = clamp( -(r\_j . v\_j) / ||v\_j||^2 , 0 , T ) d\_CPA,j = || r\_j + v\_j \* t\_CPA,j ||

Let D\_req,j be the required separation for the applicable encounter class and epsilon\_j be a conservative uncertainty margin derived from surveillance, state-estimation, latency, and model error. Define:

m\_j = d\_CPA,j - (D\_req,j + epsilon\_j)

A candidate maneuver M satisfies the simple multi-intruder margin rule when:

min\_j m\_j(M) >= 0

The embodiment is not limited to constant-velocity CPA. A certified or implementation-specific trajectory predictor, probabilistic conflict model, reachable-set model, velocity-obstacle model, well-clear logic, or standards-defined DAA logic may supply the predicate. The finality property is the binding of the accepted result to the verified conflict state, not a particular collision-avoidance equation.

### Conflict-Set Equivalence

Exact set equality is a strong profile but is not required in every implementation. A deterministic equivalence predicate may allow bounded changes that are proven not to invalidate the resolution. For example:

Eq(C\_auth, C\_now) = SameRelevantMembers AND FreshEnough AND DeltaUncertainty <= U\_max AND NoNewHigherRiskTrack

For high-assurance operation, any newly appearing conflict-relevant intruder, removed track without a validated tracktermination reason, stale source, material uncertainty expansion, or changed right-of-way class may force recomputation rather than equivalence acceptance.

Page 4

## 2.5 Resolution Epoch and Split-Brain DAA Prevention

When multiple DAA sources can propose resolutions - for example airborne DAA, ground-based DAA, UTM conflict services, autopilot obstacle avoidance, or a remote pilot - the protected domain maintains a monotonic Resolution Epoch. Only the resolution selected for the current epoch may obtain motion authority. When a new resolution supersedes the old one, the protected domain increments the epoch and invalidates all capabilities bound to the prior epoch.

Accept(M) => M.resolution\_epoch = CurrentResolutionEpoch

This prevents two individually authenticated or individually valid DAA outputs from simultaneously steering the aircraft under different traffic snapshots.

## 2.6 Detailed Workflow

1. Acquire ownship state from protected or attested navigation and inertial sources and assign an ownship-state epoch.
2. Acquire cooperative and non-cooperative traffic tracks, source provenance, timestamps, uncertainty values, and source-health state.
3. Classify which tracks are policy-relevant to the resolution horizon and canonicalize each relevant intruder descriptor.
4. Compute the Conflict-Set Root and store the associated canonical set or authenticated membership structure in protected state.
5. Permit the DAA engine to compute one or more candidate resolution maneuvers, but keep those maneuvers noneffective.
6. For the selected maneuver, form a DAA Resolution Descriptor binding the Conflict-Set Root, ownship state, trajectory or maneuver digest, safety profile, resolution epoch, horizon, sink, and freshness state.
7. Validate the selected maneuver against every relevant intruder under the applicable DAA safety predicate; deny or require recomputation if any required margin fails.
8. Reserve the descriptor nonce and resolution epoch and create a prepared finality record; no motion capability is yet usable.
9. Immediately before motion admission, resample or reconstruct the current policy-relevant conflict set and current ownship state.
10. Evaluate the deterministic conflict-set equivalence predicate and freshness bounds; treat newly relevant tracks, material uncertainty expansion, or stale source state as invalidating conditions unless a profile expressly proves equivalence.
11. Re-evaluate the accepted maneuver against the current conflict set, or validate a current risk certificate generated from the same protected snapshot.
12. If validation succeeds, atomically commit the finality record and release a trajectory-envelope capability bound to the current resolution epoch and motion-admission sink.
13. The motion-admission sink reconstructs the actual trajectory envelope supplied by the flight planner and compares it with the authorized trajectory digest or bounds.
14. If the path matches, the sink admits the envelope to the flight controller. If it does not match, the sink denies and invokes the Safe-Action Set.
15. On any conflict-set change, sensor-health failure, policy change, epoch advance, or expiry event occurring before effectuation, invalidate the outstanding capability and require recomputation.

## 2.7 Non-Limiting Pseudocode

```
FUNCTION FINALIZE_DAA_RESOLUTION(candidate_M, proposed_descriptor):
DISABLE_MOTION_EXPANSION()
own_auth := READ_PROTECTED_OWNSHIP()
C_auth := READ_CANONICAL_CONFLICT_SET(proposed_descriptor.conflict_root)
REQUIRE proposed_descriptor.resolution_epoch == CURRENT_RESOLUTION_EPOCH()
REQUIRE FRESH(own_auth)
REQUIRE ALL_REQUIRED_TRACKS_FRESH(C_auth)
REQUIRE HASH(candidate_M) == proposed_descriptor.maneuver_digest
REQUIRE TARGET_SINK(candidate_M) == proposed_descriptor.sink_id
FOR each intruder j IN C_auth:
REQUIRE SAFETY_MARGIN(candidate_M, own_auth, j) >= 0
```

Page 5

```
PREPARE_FINALITY_RECORD(proposed_descriptor)
ATOMIC SNAPSHOT:
own_now := READ_PROTECTED_OWNSHIP()
```

| C_now | := BUILD_CURRENT_RELEVANT_CONFLICT_SET() |
|---|---|
| epoch | := CURRENT_RESOLUTION_EPOCH() |

```
IF epoch != proposed_descriptor.resolution_epoch:
ABORT_AND_RECOMPUTE("RESOLUTION_EPOCH_CHANGED")
IF NOT CONFLICT_EQUIVALENT(C_auth, C_now):
ABORT_AND_RECOMPUTE("CONFLICT_SET_CHANGED")
FOR each intruder j IN C_now:
IF SAFETY_MARGIN(candidate_M, own_now, j) < 0:
ABORT_AND_RECOMPUTE("CURRENT_MARGIN_FAIL")
receipt := COMMIT_DAA_FINALITY(
descriptor_digest = HASH(proposed_descriptor),
current_conflict_root = ROOT(C_now),
current_ownship_digest = HASH(own_now),
decision = ALLOW)
capability := RELEASE_TRAJECTORY_CAPABILITY(
maneuver_digest = HASH(candidate_M),
conflict_root = ROOT(C_now),
resolution_epoch = epoch,
sink_id = proposed_descriptor.sink_id,
receipt_digest = HASH(receipt),
expiry = SHORT_HORIZON())
RETURN capability
```

## 2.8 Variants and Narrow Sub-Embodiments

- Multi-intruder atomicity: a maneuver is denied when it resolves one conflict while causing an unacceptable margin against another relevant intruder.
- Conflict-root membership proofs: the sink or verifier can verify that a specified high-risk track was included in the authorized conflict set without receiving the full set.
- Degraded-surveillance profile: when one required surveillance source fails, the permitted maneuver envelope automatically shrinks or falls back to a predefined safe action instead of treating stale absence as clearance.
- Trajectory-tube binding: a resolution authorizes a bounded tube, not a single geometric centerline, allowing lowerlevel stabilization while preventing route substitution.
- Resolution supersession receipts: when one DAA source supersedes another, the protected record links the old and new epochs and records why the old capability became stale.
- Observer evidence: a compact external record may attest that a DAA decision was made against a particular conflict-set commitment, without itself granting motion authority.

## 2.9 Security and Design-Around Closure

The embodiment is not avoided by calling the conflict set a traffic picture, track table, well-clear state, encounter set, object list, surveillance map, occupancy set, or threat list. If the maneuver is admitted because of a safety state derived from multiple intruder observations, and the protected boundary binds effectuation to the continuing validity of that state, the functional mechanism is the same. Nor is the embodiment avoided by authenticating the DAA source, because source authentication does not establish continuing validity of the conflict state at effectuation. A cached maneuver, signed maneuver, remote maneuver, AI-generated maneuver, or standards-compliant maneuver remains non-effective when its conflict-set basis has materially changed.

Page 6

# 3. EMBODIMENT 2 - EMERGENCY-SCENE TEMPORARY AUTHORITY FINALITY FOR AUTONOMOUS ROAD VEHICLES

## 3.1 Technical Problem

An autonomous vehicle may encounter an active emergency scene in which an authorized police officer, firefighter, road authority, incident commander, or other recognized responder needs the vehicle to perform a temporary exception to ordinary driving policy. The vehicle may need to cross a lane marking, reverse, enter a temporarily restricted lane, proceed around a blocked area, stop in an unusual position, traverse a red-signal boundary under direction, or perform another narrowly bounded movement. Treating responder authentication as unrestricted remote-driving authority creates excessive privilege; refusing all exceptions may impede emergency response. The disclosed mechanism therefore creates a scene-bound, incident-bound, vehicle-bound and act-bound temporary authority that is verified against local physical evidence and automatically extinguishes when its scope ends.

## 3.2 Technical Solution and Architecture



signed / referenced Responder / Incident Emergency Scene

temporary authority

Authority Capsule (ESAC)

Protected Motion Finality Domain scoped capability

Motion-Admission

Finality Sink scene match execute once / bounded

Vehicle Sensors + Local Scene Corroboration physical evidence

+ Incident State

Bounded Emergency

Maneuver

Invariant: temporary emergency authority is act-, vehicle-, incident-, scene-, time-, and sink-bound and automatically extinguishes when any required scope condition ceases to hold

**Figure 2 - Emergency-scene temporary-authority finality**

A representative system comprises a responder credential or authority source, an incident-state source, an Emergency Scene Authority Capsule (ESAC), a vehicle-local scene-corroboration module, a protected motion-finality domain, a motion-admission Finality Sink, and a Safe-Action Set. The responder or authority service does not directly steer the vehicle. It authorizes a bounded exception or bounded path which the vehicle independently reconstructs and verifies against local scene state before admitting the motion.

## 3.3 Emergency Scene Authority Capsule

The ESAC may include or cryptographically commit to:

- vehicle identifier or pseudonymous vehicle binding;
- responder or emergency-authority role reference;
- incident identifier and incident epoch;
- emergency-scene identifier;
- scene polygon or corridor commitment; Page 7

- instruction class;
- path, lane, direction, or trajectory-envelope digest;
- maximum speed, acceleration, reverse-distance, stop-location, or other motion bounds;
- specific traffic-rule exception or temporary ODD exception;
- start time and hard expiry;
- required local scene-corroboration predicate;
- policy and revocation epochs;
- single-use or bounded-use nonce;
- target motion-admission sink. A responder credential can therefore prove who may issue the ESAC, but the ESAC separately defines what may become effective. A credential without a matching ESAC does not grant actuation authority.

## 3.4 Scene Commitment and Physical Corroboration

The vehicle constructs a local Scene Commitment from the subset of physical evidence required by policy. Non-limiting elements include emergency-vehicle presence, authenticated emergency beacon, emergency-light pattern, responder presence, road closure, cone or barrier geometry, temporary signage, blocked-lane state, fire or smoke classification, incident-zone map, and local road topology. A representative commitment is:

S\_scene = H( IncidentID || ScenePolygon || LocalEvidenceDigest || TemporaryControlDigest || SceneEpoch ) The temporary authority is valid only when the ESAC scene reference and the vehicle-local scene state satisfy a deterministic scene-match predicate. Exact image or raw-sensor equality is not required. The scene match may be a thresholded evidence predicate, a quorum of independent sensor classes, an authenticated infrastructure signal combined with local confirmation, or another conservative rule.

### Example q-of-n Corroboration

For independent evidence channels e\_i with binary protected validation results v\_i, a profile may require:

sum\_i v\_i >= q The profile should prevent multiple messages from the same physical source from being miscounted as independent corroboration. Higher-risk exceptions may require both a verified responder authority and at least one independent local physical confirmation.

## 3.5 Temporary Exception Mathematics and Automatic Extinction

Let E(t) denote whether temporary emergency authority is effective. One representative rule is: E(t) = CredentialValid AND IncidentCurrent AND SceneMatch AND t <= t\_exp AND NotRevoked AND NotConsumed For a location-bounded scene, the authority may additionally require:

position(t) in Dilate(ScenePolygon, delta\_loc) where delta\_loc is a conservative localization margin. The authority is automatically invalid when any required term becomes false. The permitted motion M must satisfy both the emergency exception and non-waivable hard-safety predicates:

Allow(M) = E(t) AND M in EmergencyEnvelope AND HardSafety(M, state) HardSafety may include collision-imminence constraints, pedestrian protection, mechanical limits, minimum controllability, sensor-integrity floors, or another safety predicate that the responder instruction is not permitted to override.

## 3.6 Detailed Workflow

16. Detect or receive indication of an emergency or temporary traffic-control scene; maintain ordinary vehicle motion under the normal safety policy until additional authority is verified.
17. Receive a responder credential, incident reference, or authority-service assertion and validate its signature, role, jurisdiction or organizational scope, revocation state, and freshness.
18. Receive or construct an ESAC that specifies the exact temporary exception, vehicle binding, incident, scene, path or motion envelope, bounds, time window, nonce, and target sink.
19. Acquire vehicle-local sensor evidence and infrastructure evidence relevant to the claimed emergency scene. Page 8

20. Canonicalize the local scene evidence and compute or resolve the Scene Commitment.
21. Validate that the incident remains current and that the claimed responder or authority role is permitted to issue the requested instruction class for the scene.
22. Evaluate the scene-match predicate, including required independence or q-of-n corroboration rules.
23. Convert the responder instruction into a Candidate Emergency Maneuver and keep it non-effective.
24. Reconstruct the actual planner-generated path or motion envelope that would be used to satisfy the instruction.
25. Compare the reconstructed motion with the ESAC path, corridor, direction, speed, reverse-distance, stop-location, and traffic-rule-exception bounds.
26. Apply non-waivable hard-safety predicates using current vehicle, pedestrian, object, actuator, localization, and roadstate information.
27. Reserve or consume the ESAC nonce and commit a protected decision record only if the incident, scene, authority, motion, and safety predicates all match.
28. Release a single-use or short-lived emergency-motion capability to the motion-admission Finality Sink.
29. At the sink, re-check the authority epoch, incident epoch, scene epoch where required, capability expiry, and actual motion envelope before admission.
30. After completion, expiry, scene exit, incident closure, authority revocation, loss of required scene corroboration, policy change, or nonce consumption, automatically extinguish the temporary authority and restore ordinary road authority.

## 3.7 Non-Limiting Pseudocode

```
FUNCTION FINALIZE_EMERGENCY_SCENE_ACT(ESAC, planned_path):
KEEP_NORMAL_SAFE_ACTIONS_AVAILABLE()
BLOCK_TEMPORARY_EXCEPTION_EXPANSION()
REQUIRE VERIFY_RESPONDER_AUTHORITY(ESAC.authority_ref)
REQUIRE INCIDENT_CURRENT(ESAC.incident_id, ESAC.incident_epoch)
REQUIRE VEHICLE_MATCH(ESAC.vehicle_binding)
REQUIRE NOT_REVOKED(ESAC)
REQUIRE NOW() <= ESAC.expiry
local_scene := BUILD_PROTECTED_LOCAL_SCENE_STATE()
scene_result := EVALUATE_SCENE_MATCH(ESAC.scene_commitment, local_scene)
REQUIRE scene_result == PASS
actual_path := RECONSTRUCT_ACTUAL_MOTION(planned_path)
REQUIRE PATH_WITHIN_EMERGENCY_ENVELOPE(actual_path, ESAC)
REQUIRE TRAFFIC_EXCEPTION_IS_EXPLICIT(ESAC, actual_path)
REQUIRE HARD_SAFETY_PREDICATES_PASS(actual_path, local_scene)
ATOMIC:
REQUIRE NONCE_UNUSED(ESAC.nonce)
CONSUME(ESAC.nonce)
receipt := COMMIT_EMERGENCY_FINALITY(
ESAC_digest = HASH(ESAC),
scene_digest = HASH(local_scene),
path_digest = HASH(actual_path),
decision = ALLOW)
capability := RELEASE_TEMPORARY_MOTION_CAPABILITY(
incident_id = ESAC.incident_id,
scene_epoch = ESAC.scene_epoch,
path_digest = HASH(actual_path),
exception_class = ESAC.exception_class,
sink_id = ESAC.sink_id,
receipt_digest = HASH(receipt),
expiry = ESAC.expiry)
RETURN capability
ON any of {COMPLETION, EXPIRY, INCIDENT_CHANGE, SCENE_EXIT,
REVOCATION, CORROBORATION_LOSS, POLICY_EPOCH_CHANGE}:
INVALIDATE_ALL_SCENE_CAPABILITIES(incident_id)
RESTORE_ORDINARY_AUTHORITY()
```

Page 9

## 3.8 Non-Verbal or Locally Perceived Responder Instructions

In another variant, the responder instruction is not transmitted as a digitally signed path. A vehicle may perceive a recognized hand signal, illuminated baton, temporary sign, cone channel, or responder gesture. Perception alone is treated as evidence, not authority. The protected domain may require a corresponding responder identity or sceneauthority reference obtained through V2X, infrastructure, short-range credential exchange, trusted emergency beacon, or another channel. The finality step binds the interpreted instruction to the observed responder/scene evidence and to the concrete planned maneuver. A perception-model classification such as "officer directs vehicle left" does not itself unlock steering authority.

## 3.9 Security and Design-Around Closure

The embodiment is not avoided by naming the artifact an emergency permit, incident token, responder credential, temporary traffic-control message, remote-assistance instruction, police override, road-worker instruction, or incidentscene clearance. The distinguishing mechanism is that temporary authority is constrained by the particular incident and scene, requires vehicle-local verification of the requested consequence, and expires automatically rather than creating a standing remote-control privilege. A stolen, replayed, validly signed, or otherwise authentic responder credential remains insufficient when the scene, vehicle, incident, path, epoch, or hard-safety state does not match.

Page 10

# 4. EMBODIMENT 3 - ATOMIC CONTROL-AUTHORITY HANDOVER AND SPLIT- BRAIN PREVENTION

## 4.1 Technical Problem

An autonomous motion platform may have multiple controllers that are individually legitimate: an autonomy stack, a remote pilot, a remote-assistance service, a fleet controller, a DAA safety controller, a minimal-risk controller, an emergency authority, or a local human operator. The critical failure is not limited to an unauthorized controller. Two authorized controllers may simultaneously believe they control the same steering, thrust, braking, trajectory-admission, or mode-transition boundary. Network delay, partial handover, retries, failover, duplicated sessions, stale credentials, or crash recovery can create split-brain actuation. The disclosed mechanism treats control transfer itself as a Candidate Act. Protected state records the controller identity and Authority Epoch for each governed sink or sink class. A prepare-commit-enable handover changes this state atomically, and every ordinary control command is accepted only when its controller and epoch match the current protected authority state.

## 4.2 Technical Solution and Architecture



Controller A

Curtorit

old commands

PHASE 1 - PREPARE

Validate B; Freeze New Authority Expansion by A

prepare

Protected Authority State

Controller ID + Epoch

+ Handover State

handover request epoch-checked act

PHASE 2 - COMMIT Advance Epoch; Revoke A; Atomically Bind B

Finality Sink

Controller B Requested Authority

PHASE 3 - ENABLE Enable B; Reject All Stale A Commands

Invariant: for each governed sink and authority epoch, at most one ordinary controller has effectuation authority; separately defined safe-action authority may remain available.

**Figure 3 - Atomic controller handover state machine**

The Protected Authority State may be maintained per vehicle, per actuator class, per motion-admission sink, or per control domain. A high-assurance embodiment permits separate current controllers for independent non-conflicting sinks while enforcing exclusivity for sinks whose simultaneous control could conflict.

## 4.3 Protected Authority State

For sink s, protected state may include:

```
AuthorityState[s] = {
current_controller_id,
authority_epoch,
permitted_act_classes,
current_envelope_digest,
```

Page 11

```
handover_state,
prepared_new_controller_id,
prepared_envelope_digest,
expiry,
revocation_epoch,
monotonic_counter,
prior_receipt_digest
}
```

Each ordinary control act binds at least ControllerID, AuthorityEpoch, SinkID, action class, act or envelope digest, expiry, nonce or sequence state, and any required policy/revocation state.

## 4.4 Exclusivity Mathematics

Let A(c,s,e,t) be 1 when controller c possesses ordinary effectuation authority over sink s in authority epoch e at time t, and 0 otherwise. The principal exclusivity invariant is:

For all s,e,t: sum\_c A(c,s,e,t) <= 1 A separately defined Safe-Action Set may remain available to a safety controller without violating the invariant because it does not include ordinary authority expansion and is explicitly constrained to stabilizing or risk-reducing actions. Command acceptance at the sink may be expressed as:

Accept(cmd) => cmd.controller\_id = CurrentController[s] AND cmd.epoch = CurrentEpoch[s] AND cmd.act in CurrentEnvelope[s]

## 4.5 Transactional Handover

A preferred transaction has three logical phases: PREPARE, COMMIT, and ENABLE. PREPARE validates the proposed new controller and its authority envelope while the old controller remains responsible for continuity. The system may freeze authority expansion by the old controller during PREPARE while allowing bounded continuity or the Safe-Action Set. COMMIT atomically advances the Authority Epoch, revokes the old ordinary-control binding, records the new controller and envelope, and commits a handover receipt. ENABLE allows the new controller to submit commands under the new epoch. A stale command from the old controller is thereafter rejected even if its credential remains cryptographically valid.

### Partial Failure Rule

If the system crashes after PREPARE but before COMMIT, the new controller has no effectuation authority. If the system commits the new epoch but cannot prove the new controller is ready, the system may enter a bounded safe state and require a new handover rather than resurrecting the old epoch. Recovery never infers authority from whichever command source transmits first.

## 4.6 Detailed Workflow

31. Maintain protected per-sink authority state identifying the current controller and Authority Epoch.
32. Receive a handover request identifying the proposed new controller, requested sink set, act classes, control envelope, duration, authority basis, and reason for transfer.
33. Authenticate and attest the proposed controller or remote session and validate its permitted role and current revocation state.
34. Validate the requested control envelope against current vehicle state, operational domain, safety limits, and policy.
35. Enter PREPARE state and record the proposed controller and envelope in protected storage without yet granting effectuation authority.
36. Optionally freeze new authority expansion by the old controller while preserving bounded continuity and the Safe- Action Set.
37. Confirm readiness of the proposed controller and, where required, establish a fresh session or proof-of-possession bound to the pending handover.
38. Atomically increment the Authority Epoch, mark the old controller stale for ordinary actuation, bind the new controller and envelope, and commit a handover receipt.
39. Only after the committed epoch exists, issue or enable the new controller capability.
40. At every governed Finality Sink, reject any command whose controller identifier, epoch, sink, act class, envelope, expiry, or nonce state does not match protected authority state. Page 12

41. Invalidate queued or precomputed commands from prior epochs unless they belong to the separately permitted Safe- Action Set and are reclassified under current protected state.
42. If a handover fails before commit, retain the prior committed controller or transition to the Safe-Action Set according to the safety profile.
43. If recovery detects an ambiguous or incomplete transaction, perform recovery-completes-first semantics before admitting any new ordinary control command.
44. When handing authority back, repeat the same transaction; a previous controller does not automatically regain its former epoch or command rights.

## 4.7 Non-Limiting Pseudocode

```
FUNCTION HANDOVER_AUTHORITY(sink_set, controller_B, envelope_B):
FOR each sink s IN sink_set:
state[s] := READ_PROTECTED_AUTHORITY_STATE(s)
REQUIRE VERIFY_CONTROLLER(controller_B)
REQUIRE VERIFY_ROLE_SCOPE(controller_B, sink_set)
REQUIRE ENVELOPE_SAFE_NOW(envelope_B)
ATOMIC PREPARE:
FOR each sink s IN sink_set:
WRITE_PREPARED(s,
new_controller = controller_B.id,
new_envelope = HASH(envelope_B),
base_epoch = state[s].authority_epoch)
FREEZE_OLD_AUTHORITY_EXPANSION(s)
REQUIRE CONTROLLER_READY(controller_B)
ATOMIC COMMIT:
FOR each sink s IN sink_set:
old_epoch := CURRENT_EPOCH(s)
new_epoch := old_epoch + 1
SET_CURRENT_CONTROLLER(s, controller_B.id)
SET_CURRENT_ENVELOPE(s, HASH(envelope_B))
SET_CURRENT_EPOCH(s, new_epoch)
INVALIDATE_ORDINARY_COMMANDS(s, epoch = old_epoch)
receipt := COMMIT_HANDOVER_RECEIPT(sink_set, controller_B, new_epoch)
ENABLE_CONTROLLER(controller_B, sink_set, new_epoch, HASH(receipt))
RETURN new_epoch
FUNCTION FINALIZE_CONTROL_COMMAND(cmd, sink):
state := READ_PROTECTED_AUTHORITY_STATE(sink)
REQUIRE cmd.controller_id == state.current_controller_id
REQUIRE cmd.authority_epoch == state.authority_epoch
REQUIRE CMD_WITHIN_ENVELOPE(cmd, state.current_envelope_digest)
REQUIRE FRESH_AND_NOT_REPLAYED(cmd)
COMMIT_COMMAND_RECEIPT(cmd, sink, state.authority_epoch)
RELEASE_TO_SINK(cmd)
```

## 4.8 Multi-Sink and Hierarchical Variants

A vehicle may separate steering, propulsion, braking, payload, sensor, route admission, or flight-mode authority. A handover may transfer only a subset. For example, a remote assistance operator may temporarily obtain route-selection authority without direct steering authority, while the local autonomy controller retains low-level stabilization. A DAA safety controller may hold only the power to constrain or veto the current trajectory envelope rather than ordinary piloting authority. The protected state therefore may encode authority as a lattice or set of non-overlapping sink scopes, provided that conflicting ordinary authority for the same sink and epoch is prevented.

## 4.9 Security and Design-Around Closure

The embodiment is not avoided by using leases, sessions, tokens, heartbeats, controller priorities, mutexes, leader election, safety-driver takeover, remote-pilot takeover, arbitration tables, or control-mode flags. Such mechanisms may

Page 13

form evidence or inputs. The execution-finality property exists when the effectuation boundary verifies a protected current-controller/epoch state and stale authority cannot actuate merely because a prior session or credential remains valid. The handover is itself finalized as a protected state transition before the new controller can produce ordinary effects.

# 5. COMMON THREAT MODEL AND IMPLEMENTATION NOTES

## 5.1 Threats Addressed

- Stale but authentic DAA maneuver replay after the traffic picture changes.
- Multi-intruder omission in which a resolution solves one encounter while creating another.
- DAA-source split brain in which multiple individually authorized resolvers issue conflicting maneuvers.
- Replay or theft of a first-responder credential outside the incident scene or after incident closure.
- Expansion of a responder instruction into broader remote-control authority than the specific emergency maneuver.
- Perception-only emergency-scene classification being mistaken for authority to violate ordinary traffic policy.
- Dual-controller actuation during remote takeover, failover, or recovery.
- Queued commands from a prior authority epoch reaching the actuator after a handover.
- Partial transaction, reset, rollback, or power failure leaving authority state ambiguous.
- Upstream software substituting a different trajectory, lane, path, sink, or actuator value after authorization.

## 5.2 Representative Protected Implementations

The protected domains may be implemented using a safety microcontroller, secure microcontroller, lock-step safety processor, FPGA, vehicle domain controller with isolated safety partition, TEE coupled to a hardware security module, secure gateway, autopilot safety core, protected motion-admission controller, or equivalent non-bypassable execution boundary. Cryptographic mechanisms may include HMAC, digital signatures, authenticated encryption, deterministic CBOR or fixed binary commitments, monotonic counters, secure boot measurements, attestation, hash-linked receipts, and protected freshness stores. The disclosed inventions do not require a particular primitive; the relevant property is that the finality sink cannot be made to accept a stale, substituted, over-broad, wrong-epoch, or wrong-context act through ordinary software bypass.

## 5.3 Latency Profiles

High-rate motion control need not perform public-key verification for every actuator sample. A slower path may validate authority, conflict state, responder identity, or controller handover and derive a short-lived symmetric capability or protected envelope. The hot path may then verify a fixed-size MAC, epoch, nonce/sequence value, envelope bound, and current safety state. The protected domain should force revalidation at material state transitions such as conflict-set changes, scene changes, policy epoch changes, controller handover, boundary proximity, or expiry.

Page 14

## CLAIMS

1. **A cyber-physical execution-control system comprising a command-generating component**

configured to generate a proposed operation capable of producing a physical, operational, communicative, persistent, or other externally consequential effect; a Protected Execution Domain configured to represent the proposed operation as a Candidate Act maintained in a Non-Effective State, deterministically represent the Candidate Act, generate a cryptographic binding commitment that binds at least the Candidate Act, a Finality Sink associated with an effectuation boundary, and freshness information, and generate a constrained Beacon Proof Capsule carrying or referencing a compact representation of the cryptographic binding commitment; a constrained communication interface configured to communicate the Beacon Proof Capsule; and the Finality Sink configured independently to reconstruct an actual Candidate Act presented for effectuation, derive an expected binding value from the actual Candidate Act, compare the expected binding value with the Beacon Proof Capsule, and prevent effectuation unless the comparison and required authorization and freshness checks succeed.

2. **The system of claim 1, wherein the cryptographic binding commitment is generated under a**

Binding Key held by the Protected Execution Domain and the Finality Sink and unavailable to a mission computer, transmitter, autonomy component, planner, or other component proposing or forwarding the Candidate Act.

3. **The system of claim 1, wherein the Beacon Proof Capsule comprises an Authority Reference**

identifying or cryptographically referencing an Authority Object that is not transmitted in full within the Beacon Proof Capsule, and wherein the Authority Reference alone is insufficient to authorize effectuation.

4. **The system of claim 3, wherein the Authority Reference is resolved from protected local storage,**

an authenticated cache, a gateway, or a trusted resolver, while the Finality Sink retains the final determination whether effectuation is permitted.

5. **The system of claim 1, wherein the binding commitment further binds at least one of a policy**

epoch, revocation epoch, Context Commitment, geographic region, geofence version, road-zone version, operational corridor, mission phase, flight mode, driving mode, payload state, radio state, device identity, expiry value, altitude band, lane group, or safety-state reference.

6. **The system of claim 1, wherein the freshness information comprises at least one of a nonce,**

sequence number, monotonic counter, time slot, validity interval, rolling session value, challenge, or expiry value, and the Finality Sink rejects a Beacon Proof Capsule associated with freshness information previously consumed.

7. **The system of claim 6, wherein protected replay state is updated atomically with a deciding read**

of current policy state and current revocation state and with commitment of an execution capability.

8. **The system of claim 7, wherein a Finality Receipt recording at least an allow, deny, or safe-state**

decision is committed before the execution capability becomes usable.

9. **The system of claim 1, wherein the compact representation comprises a truncated cryptographic**

commitment having a retained bit length selected according to at least a collision-risk criterion and, for an unkeyed commitment, an attacker offline-work criterion.

10. **The system of claim 9, wherein detection that two or more full commitments correspond to the**

same truncated representation causes denial, escalation to a longer commitment profile, or both.

Page

115

11. **The system of claim 1, wherein the Beacon Proof Capsule is transmitted within, adjacent to,**

contemporaneously with, or through a communication channel associated with a remoteidentification, V2X, telemetry, discovery, advertisement, sidelink, mesh, on-board bus, or other constrained message, and identification of a device by said message does not itself authorize the Candidate Act.

12. **The system of claim 1, wherein the Finality Sink comprises or controls at least one of a flight**

controller, electronic speed controller, motor controller, motor gate driver, drive-by-wire controller, secure bus gateway, actuator controller, payload-release controller, servo controller, RF transmitenable controller, baseband controller, camera controller, sensor controller, motion-admission gate, secure microcontroller, safety processor, FPGA, or protected software partition.

13. **A method for controlling effectuation of a cyber-physical operation over a constrained**

communication channel, the method comprising generating or receiving a proposed operation; representing the proposed operation as a Candidate Act; maintaining the Candidate Act in a Non- Effective State; deterministically representing the Candidate Act; generating a cryptographic binding commitment that binds at least the Candidate Act, a designated Finality Sink, and freshness information; encoding a compact representation of the cryptographic binding commitment in a Beacon Proof Capsule; communicating the Beacon Proof Capsule; independently reconstructing, at or adjacent to the designated Finality Sink, an actual Candidate Act presented for effectuation; generating an expected binding value from the reconstructed actual Candidate Act; verifying the expected binding value against information carried or referenced by the Beacon Proof Capsule; and permitting effectuation only when said verification and required authority, freshness, currentness, and context conditions succeed.

14. **The method of claim 13, further comprising generating the binding commitment under a**

Binding Key unavailable to a component generating, proposing, transmitting, or forwarding the Candidate Act.

15. **The method of claim 13, further comprising resolving a compact Authority Reference to a fuller**

Authority Object and preventing effectuation when the Authority Reference cannot be resolved or the Authority Object is invalid, expired, revoked, or incompatible with the reconstructed actual Candidate Act.

16. **The method of claim 13, further comprising reading current policy state and current revocation**

state inside the same atomic finality commit in which freshness state is consumed and effectuation authority is committed.

17. **The method of claim 16, further comprising committing a Finality Receipt before a bounded**

execution capability becomes usable at the Finality Sink.

18. **The method of claim 13, wherein failure of authentication, freshness, replay, policy-currentness,**

revocation-currentness, context, sink, act, fragmentation, authority-resolution, or ambiguity verification causes the Candidate Act to remain in the Non-Effective State.

19. **A control apparatus for installation at or adjacent to an effectuation boundary of a cyber-**

physical system, comprising a protected processor; protected state storage; a communication interface configured to receive a Beacon Proof Capsule; an act input configured to obtain information representing an operation presented for effectuation; and an effectuation-control output; wherein the protected processor is configured to reconstruct an actual Candidate Act from the operation presented for effectuation, generate a cryptographic representation thereof, verify that the Beacon Proof Capsule is cryptographically bound to the actual Candidate Act and to the apparatus

Page 116

or a downstream effectuation component, verify freshness and anti-replay state, and assert the effectuation-control output only when said verification succeeds.

20. **The apparatus of claim 19, wherein the effectuation-control output controls at least one of an**

ESC enable, motor-driver enable, PWM envelope, propulsion-enable path, steering or braking permission envelope, actuator enable, payload-latch enable, solenoid power, RF transmit enable, sensor enable, camera enable, secure-bus authorization, mode-transition register, or motionadmission gate.

21. **The apparatus of claim 19, wherein the protected processor independently obtains current**

operational context comprising at least one of geofence state, zone state, corridor state, location, altitude, lane group, mission phase, flight mode, driving mode, payload state, radio state, or safety state and rejects effectuation when the current operational context does not correspond to context cryptographically bound to the Beacon Proof Capsule.

22. **The apparatus of claim 19, wherein a verified Authority Object is cached locally such that**

verification of the Candidate Act does not require remote network access in the hot path.

23. **The apparatus of claim 19, wherein successful verification causes generation of a sink-local**

bounded execution capability distinct from the Beacon Proof Capsule and restricted by at least one of act, sink, time, counter, parameter, actuator envelope, or single-use condition.

24. **A constrained-beacon fragmentation system comprising an encoder configured to divide**

execution-finality evidence associated with a Candidate Act into a plurality of beacon fragments, each fragment carrying at least a fragment identifier or index, a fragment-set or session identifier, a common root commitment, and integrity or authentication evidence; and a verifier configured to authenticate the fragments, determine whether a sufficient fragment set has been received, reconstruct the execution-finality evidence only from an authenticated sufficient fragment set, verify the common root commitment, and prevent the Candidate Act from becoming effective when the required evidence has not been successfully reconstructed.

#### 25. The system of claim 24, wherein the common root commitment is derived from an

unfragmented Beacon Proof Capsule and each fragment authenticator cryptographically binds at least the session identifier, root commitment, fragment index, fragment count, and fragment payload.

26. **The system of claim 24, wherein fragments associated with different session identifiers, root**

commitments, freshness values, policy epochs, devices, or Candidate Acts cannot be combined to produce valid reconstructed execution-finality evidence.

27. **The system of claim 24, wherein receipt of an incomplete, corrupt, mixed, duplicate, or**

otherwise insufficient fragment set cannot authorize effectuation and instead maintains the Candidate Act in a Non-Effective State.

28. **The system of claim 24, wherein reconstructed execution-finality evidence is subsequently**

verified by a Finality Sink against an independently reconstructed actual Candidate Act before effectuation.

29. **The system of claim 1, wherein a cold-path process performs at least one of certificate-chain**

verification, Authority Object validation, policy parsing, geofence or zone validation, key establishment, resolver synchronization, or authority-cache population, and a hot-path process at the Finality Sink performs at least Beacon Proof Capsule parsing, authority-reference lookup, freshness

Page 117

verification, replay verification, act-binding verification, and release or withholding of effectuation authority.

30. **A system for observer-verifiable evidence of execution decisions in a constrained cyber-**

physical device, comprising a Protected Execution Domain configured to generate a sequence of one-way-related evidence keys from secret state unavailable to an identification transmitter, mission computer, autonomy component, or radio forwarder; generate, for an allow, deny, or safe-action decision associated with a Candidate Act, a compact Act Evidence Record containing decision information and an authentication tag produced from an evidence key associated with a time interval; disclose the evidence key only after a predetermined delay; and publish or cause publication of an Evidence Anchor cryptographically binding the evidence-key chain, timing parameters, and the Protected Execution Domain to a device identity; wherein a third-party observer accepts the Act Evidence Record only when the record was received before the associated evidence key could validly have been disclosed.

31. **The system of claim 30, wherein the evidence keys are generated as a reverse one-way chain**

such that disclosure of an evidence key permits derivation or verification of earlier keys but does not reveal a later undisclosed key.

32. **The system of claim 30, wherein the Act Evidence Record comprises at least an interval**

identifier, decision value, sink class, act class or privacy-preserving act-class value, monotonic receipt counter, and truncated message-authentication tag.

33. **The system of claim 30, wherein the Evidence Anchor is signed once for an evidence epoch and**

comprises at least a device identifier, epoch identifier, Protected Execution Domain key identifier, chain commitment, timing interval, disclosure lag, and starting receipt-counter information.

34. **The system of claim 30, wherein a corresponding Finality Receipt contains at least a header or**

counter matching the Act Evidence Record, thereby permitting a later auditor to associate broadcast act-decision evidence with a protected receipt chain.

35. **The system of claim 30, wherein an Act Evidence Record, Key Disclosure Record, Evidence**

Anchor, or Finality Receipt is evidence only and is not accepted by a Finality Sink as authority to perform a Candidate Act.

36. **The system of claim 30, wherein loss of one or more key-disclosure messages does not**

permanently prevent verification because a subsequently disclosed key permits verification of an earlier key according to the one-way relationship.

37. **A method for controlling spatially scoped authority of an autonomous or remotely operated**

system, comprising determining a current distance to a boundary of a permitted spatial region or corridor; determining a position-uncertainty bound, permitted speed, enforcement-to-actuator reaction latency, and guaranteed deceleration; determining a stopping-distance term from the permitted speed, reaction latency, and guaranteed deceleration; determining a maximum revalidation interval from the distance to the boundary reduced by the position-uncertainty bound and stopping-distance term and divided by the permitted speed; revalidating authority at or before expiry of said maximum interval; and withholding further outward motion, reducing permitted speed, or selecting a protected safe action when the resulting interval is non-positive.

38. **The method of claim 37, wherein the stopping-distance term is determined according to**

sstop=vτ+v2/(2a)s\_{stop}=v\\tau+v^2/(2a), and the revalidation interval satisfies Δr≤(d-ϵpos-sstop)/v\\Delta\_r\\le(d-\\epsilon\_{pos}-s\_{stop})/v.

Page 118

39. **The method of claim 37, further comprising obtaining position estimates from a plurality of**

independent or partially independent sources and removing authority for spatially scoped outward motion when fewer than a required number of sources agree within an uncertainty-dependent consistency bound.

40. **The method of claim 37, wherein revalidation frequency automatically increases as the**

autonomous or remotely operated system approaches the permitted boundary.

41. **An autonomous ground-vehicle execution-control system comprising a Protected Execution**

Domain, a motion-admission or mode-transition Finality Sink, and a protected Safe-Action Set; wherein the Protected Execution Domain gates at least permission-expanding or consequential nonsafety Candidate Acts and the Safe-Action Set remains available irrespective of failure of fresh authorization verification, the Safe-Action Set being fixed or bounded by protected firmware, protected logic, attested state, or equivalent protected configuration and not widenable by an untrusted planning component.

42. **The system of claim 41, wherein the gated Candidate Acts include at least one of an increased**

speed envelope, entry into a restricted road zone, activation of a higher automation mode, operation outside a designated operational domain, acceptance of a cooperative manoeuvre, execution of a remotely approved path, fleet-issued movement of an unoccupied vehicle, protected-area sensor recording, or high-power radio transmission.

43. **The system of claim 41, wherein the Safe-Action Set comprises at least one of braking, lane**

keeping, speed reduction, controlled stop, minimal-risk manoeuvre, hazard signalling, or another safety-increasing or state-preserving action.

44. **The system of claim 41, wherein a cooperative manoeuvre is represented as a Candidate Act**

bound to at least a manoeuvre identifier, trajectory envelope or digest, lane or lane-group identifier, speed envelope, time slot, device or participant identifier, and motion-admission Finality Sink.

45. **The system of claim 41, wherein a path, trajectory, or instruction supplied by a remote**

assistance or remote operation service remains non-effective until verified by the vehicle-side Finality Sink against the actual path or trajectory presented to the vehicle motion controller.

46. **The system of claim 1, wherein the cyber-physical system is an unmanned aircraft system and**

the Candidate Act comprises at least one of a flight-mode transition, waypoint transition, thrust command, propulsion envelope, payload release, sensor activation, radio transmission, landing, takeoff, geofence-sensitive movement, or airspace-corridor transition.

47. **The system of claim 46, wherein the Finality Sink comprises or controls an electronic speed**

controller and a verified Beacon Proof Capsule authorizes a bounded PWM, thrust, motor, velocityvector, or propulsion envelope, individual commands within said envelope being admitted without requiring a new Beacon Proof Capsule for every control-cycle setpoint.

#### 48. The system of claim 46, wherein the Candidate Act comprises a payload operation

cryptographically bound to at least a payload identifier and payload-effectuation component and optionally to one or more of a permitted release zone, altitude, aircraft attitude, mission phase, operator authorization, customer authorization, airspace authorization, or payload state, and a payload latch, actuator, or associated power-enable path remains disabled unless verification succeeds.

49. **The system of claim 1, wherein a common high-level operation directed to a plurality of**

autonomous devices produces a respective act-binding value or Beacon Proof Capsule for each

Page 119

device such that authority associated with a first device or first Finality Sink is insufficient to authorize effectuation by a second device or second Finality Sink.

50. **The system of claim 1, wherein at least two fields selected from action class, sink class,**

Authority Reference, policy epoch, revocation epoch, freshness information, Context Commitment, binding commitment, expiry information, or authenticator are represented using dictionary indexing, bit packing, fixed-width encoding, deterministic variable-length encoding, delta encoding, truncated cryptographic representation, implicit session state, or a combination thereof, while the Finality Sink preserves the same exact-act verification semantics independently of the underlying constrained transport.

# ADDITIONAL AUTOMATED-VEHICLE CLAIMS

51. **An automated or autonomous vehicle execution-control system comprising an automated-**

driving, motion-planning, or artificial-intelligence component configured to generate a proposed trajectory or manoeuvre; a Protected Execution Domain configured to form a Candidate Act representing the proposed trajectory or manoeuvre and generate an act-bound cryptographic commitment; and a vehicle-side Finality Sink positioned between the automated-driving or motionplanning component and at least one steering, braking, propulsion, torque, drive-by-wire, or vehicle-motion controller, wherein the Finality Sink independently derives a trajectory, manoeuvre, or control envelope actually presented for vehicle effectuation and prevents admission thereof to vehicle control unless the derived trajectory, manoeuvre, or control envelope corresponds to the actbound cryptographic commitment.

52. **The system of claim 51, wherein the Candidate Act comprises at least one of a lane change, lane**

merge, highway entry, highway exit, intersection traversal, turn, overtaking manoeuvre, roundabout traversal, parking manoeuvre, summoned vehicle movement, road-zone transition, speed-envelope change, automated-driving-mode transition, or execution of a navigation-derived route segment.

53. **The system of claim 51, wherein the Candidate Act is represented as a bounded trajectory**

envelope comprising at least two of a path, lane or lane group, longitudinal-speed envelope, lateralmotion envelope, acceleration envelope, braking envelope, steering envelope, geographic scope, time interval, or operational-design-domain state, and wherein lower-level vehicle-control commands are admitted without separate full authorization while remaining within the verified bounded trajectory envelope.

54. **The system of claim 51, wherein the Finality Sink comprises a motion-admission gate upstream**

of a vehicle motion controller and prevents an output of an automated-driving neural network, planner, or policy component from directly constituting authority to actuate steering, braking, propulsion, or torque.

55. **The system of claim 51, wherein a change in at least one of road-zone state, operational-design-**

domain state, driving mode, geographic scope, policy epoch, revocation epoch, participant state, or vehicle safety state occurring after generation of the Candidate Act invalidates or causes revalidation of the Candidate Act before vehicle effectuation.

56. **The system of claim 51, wherein an over-the-air software, model, policy, map, driving-rule, or**

configuration update causes advancement or modification of a policy or configuration epoch such that an execution authorization associated with an earlier epoch is not automatically usable after said update.

Page

120

57. **The system of claim 51, wherein a remote-assistance instruction, remotely selected route,**

remotely initiated vehicle movement, fleet-issued command, or application-originated movement request remains non-effective until a vehicle-local Finality Sink independently verifies the concrete trajectory or control envelope that will be admitted to vehicle control.

58. **The system of claim 57, wherein the vehicle is unoccupied or lacks continuous local driver**

control and the remotely initiated movement is cryptographically bound to at least a vehicle identity, movement scope, geographic region, time interval, and vehicle motion-admission Finality Sink.

59. **The system of claim 51, wherein failure of execution-finality verification prevents a permission-**

expanding Candidate Act while preserving availability of a protected Safe-Action Set comprising at least one of braking, controlled deceleration, lane keeping, maintaining a presently safe trajectory, controlled stop, minimal-risk manoeuvre, hazard signalling, or transition to a reduced automation mode.

60. **The system of claim 51, wherein a cooperative manoeuvre received through vehicle-to-vehicle,**

vehicle-to-infrastructure, vehicle-to-network, or other V2X communication is represented as a Candidate Act bound to at least a manoeuvre identifier, participant or vehicle reference, trajectory or trajectory digest, lane or lane group, timing window, speed envelope, and motion-admission Finality Sink before acceptance by the vehicle motion controller.

61. **The system of claim 51, wherein a cryptographic Binding Commitment is generated under**

secret material unavailable to the automated-driving neural network, motion planner, application processor, remote-assistance source, or network transmitter, such that said component cannot generate a different trajectory or manoeuvre having a valid binding merely by controlling Candidate Act inputs.

62. **The system of claim 51, wherein a Finality Receipt cryptographically identifying at least the**

admitted trajectory or manoeuvre, decision, current policy state, freshness state, and vehicle Finality Sink is committed before a corresponding bounded vehicle-control capability becomes usable.

# ADDITIONAL SATELLITE / NON-TERRESTRIAL NETWORK CLAIMS

63. **A satellite or non-terrestrial communication execution-control system comprising a**

communication controller configured to generate a proposed communication operation; a Protected Execution Domain configured to represent the proposed communication operation as a Candidate Act and generate an act-bound cryptographic commitment; and a Finality Sink associated with a baseband processor, beamformer, phased-array controller, RF chain, modem, inter-satellite communication interface, gateway-selection function, or transmit-enable path, wherein the Finality Sink independently determines an actual communication operation presented for effectuation and prevents said operation from becoming effective unless it corresponds to the act-bound cryptographic commitment.

64. **The system of claim 63, wherein the Candidate Act identifies or constrains at least two of a**

target satellite, target terminal, communication beam, beam identifier, frequency band, polarization, channel, transmit-power class, geographic service region, traffic class, time interval, gateway, routing destination, link type, or Finality Sink.

65. **The system of claim 63, wherein the satellite or non-terrestrial communication system**

comprises an electronically steered phased-array antenna and the Candidate Act defines or constrains activation, selection, steering, reassignment, or use of a communication beam before the corresponding beamformer or RF path becomes effective.

Page 121

66. **The system of claim 63, wherein a user terminal has communication visibility to a plurality of**

satellites and a transition from a first satellite or beam to a second satellite or beam is represented as a Candidate Act bound to at least the destination satellite or beam, freshness state, communication context, and applicable Finality Sink.

67. **The system of claim 66, wherein a handover candidate selected by link-quality, obstruction,**

mobility, latency, availability, network-load, routing, or predicted-link information remains noneffective until execution-finality verification is completed for the concrete handover presented to the modem, phased-array controller, baseband processor, or RF path.

68. **The system of claim 66, wherein a cached, predicted, or previously valid handover authorization**

is invalidated or revalidated when at least one of satellite visibility, obstruction state, service region, frequency authorization, policy epoch, revocation epoch, device state, or communication context changes before handover effectuation.

69. **The system of claim 63, wherein the Candidate Act comprises activation or modification of an**

RF transmission and binds at least a frequency or frequency class, transmit-power or power class, duration or validity interval, traffic class, geographic or jurisdictional scope, communication sink, and freshness value.

70. **The system of claim 69, wherein the RF transmission remains blocked at an RF transmit-enable,**

baseband, beamformer, power-amplifier control, modem, secure gateway, or equivalent enforcement boundary until verification of the Candidate Act succeeds.

71. **The system of claim 63, wherein communication authorization is represented by a compact**

Beacon Proof Capsule or compact execution-finality representation transported over a satellite, nonterrestrial, telemetry, control, management, feeder-link, service-link, or inter-satellite communication path, and possession of the representation does not by itself authorize a different beam, terminal, satellite, RF path, routing destination, or time interval.

72. **The system of claim 63, wherein the Finality Sink resolves an Authority Reference to authority**

governing at least one of satellite service, geographic service area, beam use, spectrum use, gateway use, inter-satellite routing, terminal operation, traffic class, or transmission power and independently verifies the actual impending communication operation against said authority.

73. **The system of claim 63, wherein a communication-path change from a first communication path**

to a second communication path is cryptographically bound to a path-specific or destinationspecific commitment such that authority applicable to the first communication path is insufficient by itself to effectuate the second communication path.

74. **The system of claim 73, wherein the first and second communication paths comprise respective**

satellite beams, respective satellites, terrestrial and satellite paths, respective gateways, respective RF bands, or respective inter-satellite links.

75. **The system of claim 63, wherein an inter-satellite routing operation is represented as a**

Candidate Act comprising at least a destination or next-hop reference, link identifier, path scope, traffic class, validity interval, and routing Finality Sink, and wherein the routing operation remains non-effective until independently verified at or adjacent to a switching, forwarding, optical-link, or routing boundary.

76. **The system of claim 63, wherein the satellite or non-terrestrial communication system maintains**

a Safe-Action Set comprising at least one of continuation of an existing verified link, reduction of transmit power, receive-only operation, use of a previously verified fallback link, bounded

Page 122

reacquisition, or communication shutdown, and failure of verification of a permission-expanding Candidate Act does not prevent use of said Safe-Action Set.

77. **A non-terrestrial-network terminal comprising a phased-array antenna, modem or baseband**

processor, Protected Execution Domain, and RF or beam-control Finality Sink, wherein the Protected Execution Domain cryptographically binds a proposed satellite-selection, beam-selection, handover, frequency, power, or routing operation to a Candidate Act and the RF or beam-control Finality Sink permits the operation only when an actual operation presented to the phased-array antenna, modem, baseband processor, or RF chain matches the Candidate Act and satisfies freshness and current-authority conditions.

78. **The terminal of claim 77, wherein satellite-selection or beam-selection decisions may be**

generated repeatedly at a rate greater than a rate at which full Authority Objects are validated, verified Authority Objects being cached in a cold path while compact Candidate-Act binding, freshness verification, replay checking, and exact-operation comparison are performed in a lowerlatency hot path.

79. **A satellite-network control method comprising selecting a candidate satellite, communication**

beam, gateway, routing path, or RF configuration; forming a Candidate Act identifying the selected communication operation; cryptographically binding the Candidate Act to a designated communication Finality Sink and freshness state; maintaining the communication operation in a Non-Effective State; independently determining at the Finality Sink the communication operation actually presented for activation; and activating the communication operation only when the actually presented operation corresponds to the cryptographically bound Candidate Act.

80. **The method of claim 79, wherein a subsequent selection of another satellite, beam, gateway,**

route, RF configuration, or terrestrial-versus-satellite path constitutes a different Candidate Act requiring a different binding or successful revalidation before effectuation.

---

Page 123

# 6. DRAFT CLAIMS

The following claims continue from claim 79 of the preceding provisional specification. They are illustrative drafting language for the additional embodiments disclosed above and may be reorganized, broadened, narrowed, divided, or adapted to applicable jurisdictional practice after prior-art and formal claim analysis.

## Claim Set A - Conflict-Set-Bound Detect-and-Avoid Finality

80. An autonomous aircraft control system comprising: one or more traffic-state inputs configured to provide intruderstate information; an ownship-state input; a detect-and-avoid computation engine configured to generate a proposed resolution maneuver; a protected execution-finality domain configured to form a canonical conflict-set representation comprising a plurality of policy-relevant intruder descriptors and to form a conflict-set commitment from the canonical conflict-set representation; and a motion-admission finality sink configured to prevent the proposed resolution maneuver from becoming motion-effective unless a resolution descriptor binds the proposed resolution maneuver to at least the conflict-set commitment, an ownship-state commitment, a validity condition, an authority epoch, and the motionadmission finality sink; wherein, before motion admission, the protected execution-finality domain obtains a current conflict-set state and causes the proposed resolution maneuver to remain non-effective when the current conflict-set state fails a predetermined equivalence or safety predicate relative to the conflict-set state to which the proposed resolution maneuver was bound.
81. The system of claim 80, wherein the canonical conflict-set representation is deterministically sorted and the conflictset commitment comprises a cryptographic hash or Merkle root of the sorted representation.
82. The system of claim 80, wherein each intruder descriptor comprises at least a track reference, relative state, freshness value, and uncertainty value.
83. The system of claim 80, wherein the protected execution-finality domain denies the proposed resolution maneuver when a newly appearing intruder becomes policy-relevant before motion admission.
84. The system of claim 80, wherein the protected execution-finality domain evaluates the proposed resolution maneuver against each of a plurality of relevant intruders and denies the proposed resolution maneuver when the maneuver resolves a first conflict while causing a safety-margin failure with respect to a second intruder.
85. The system of claim 80, further comprising a protected resolution-epoch register, wherein the motion-admission finality sink rejects a maneuver capability associated with an epoch other than a current resolution epoch.
86. The system of claim 85, wherein a new resolution selected from a different detect-and-avoid source advances the resolution epoch and thereby invalidates an earlier resolution capability without requiring revocation of the source credential that generated the earlier resolution.
87. The system of claim 80, wherein the proposed resolution maneuver is represented as a bounded trajectory tube and the motion-admission finality sink reconstructs an actual planner trajectory and admits the actual planner trajectory only when it remains within the bounded trajectory tube.
88. The system of claim 80, wherein loss or staleness of a required surveillance source causes shrinkage of an authorized maneuver envelope or transition to a pre-authorized safe-action set.
89. The system of claim 80, wherein a committed finality receipt records at least a resolution-descriptor digest, a current conflict-set commitment, a decision, a resolution epoch, and a motion-admission sink identifier.
90. A method for execution-finality control of a detect-and-avoid maneuver, the method comprising: receiving a traffic state and an ownship state; identifying a set of conflict-relevant intruders; deterministically representing the conflictrelevant intruders and computing a commitment to the set; receiving or generating a candidate avoidance maneuver; binding the candidate avoidance maneuver to the commitment, the ownship state, a resolution epoch, and a target motion-admission boundary; holding the candidate avoidance maneuver in a non-effective state; obtaining a later conflict state before admission at the target motion-admission boundary; evaluating whether the later conflict state satisfies an equivalence predicate relative to the set to which the candidate avoidance maneuver was bound; and, only when the equivalence predicate and a current maneuver-safety predicate succeed, committing protected finality state and permitting the candidate avoidance maneuver to become motion-effective.

Page 15

91. The method of claim 90, further comprising computing, for each relevant intruder, a separation margin over a maneuver horizon and requiring a minimum of the separation margins to satisfy a non-negative or standards-defined safety threshold.
92. The method of claim 90, wherein the later conflict state causes recomputation when a track is added, removed without a validated termination condition, becomes stale, or experiences uncertainty expansion beyond a predetermined bound.
93. The method of claim 90, further comprising atomically consuming a freshness value or nonce and committing a finality receipt before releasing a sink-verifiable trajectory capability.
94. The method of claim 90, wherein a compact observer-verifiable evidence record identifies a decision, resolution epoch, or conflict-set commitment but is not accepted by the motion-admission boundary as authority for motion.

## Claim Set B - Emergency-Scene Temporary Authority Finality

95. An autonomous road-vehicle control system comprising: a responder-authority verification component; a local scene-state component configured to derive protected evidence of a physical emergency scene; a protected motionfinality domain; and a motion-admission finality sink; wherein the protected motion-finality domain is configured to receive or form an emergency-scene authority object that binds at least a vehicle, an incident, a scene, an instruction or exception class, a bounded motion envelope, and an expiry condition; wherein the protected motion-finality domain independently reconstructs an actual vehicle motion responsive to the instruction and validates the actual vehicle motion against the bounded motion envelope and the local protected evidence of the physical emergency scene; and wherein the motion-admission finality sink withholds effectuation when responder authority is valid but the incident, scene, actual vehicle motion, expiry condition, or required hard-safety predicate does not match the emergency-scene authority object.
96. The system of claim 95, wherein the emergency-scene authority object expressly identifies a temporary traffic-rule exception and does not provide unrestricted remote-driving authority.
97. The system of claim 95, wherein the local scene-state component forms a scene commitment from at least an incident identifier, a scene-zone representation, and local sensor or infrastructure evidence.
98. The system of claim 97, wherein the protected motion-finality domain requires corroboration from at least two independent evidence classes before admitting a higher-risk temporary traffic-rule exception.
99. The system of claim 95, wherein the bounded motion envelope includes one or more of a path corridor, maximum speed, maximum acceleration, reverse-distance bound, permitted lane, permitted direction, stop location, or temporal window.
100. The system of claim 95, wherein a temporary emergency-motion capability is automatically invalidated upon completion, expiry, incident closure, scene exit, authority revocation, loss of required scene corroboration, policyepoch change, or consumption of a single-use nonce.
101. The system of claim 95, wherein a perceived non-verbal responder instruction is treated as evidence and does not become motion authority unless the protected motion-finality domain associates the perceived instruction with an independently verified responder or scene-authority reference.
102. The system of claim 95, wherein the emergency-scene authority object is scene-bound such that replay of a valid responder credential at a different scene does not satisfy the motion-admission finality sink.
103. The system of claim 95, wherein denial of the temporary exception preserves a pre-authorized safe-action set comprising at least braking, lane keeping, speed reduction, hazard signaling, or a minimal-risk stop.

## Claim Set C - Atomic Control-Authority Handover

104. An autonomous motion-control system comprising: a plurality of potential controllers; at least one governed motion or actuator finality sink; and a protected authority-state store maintaining, for the governed finality sink, a current controller identifier and a monotonic authority epoch; wherein each ordinary control act presented to the governed finality sink is bound to at least a controller identifier and an authority epoch; wherein the system is configured to perform a control-authority handover by preparing a proposed new controller, validating an authority scope for the proposed new controller, atomically advancing the monotonic authority epoch and changing the current controller identifier, and enabling ordinary effectuation by the proposed new controller only after the advanced authority epoch is Page 16

committed; and wherein the governed finality sink rejects an otherwise authenticated ordinary control act when the controller identifier or authority epoch of the ordinary control act does not match the protected authority-state store.

105. The system of claim 104, wherein the protected authority-state store is maintained separately for a plurality of finality sinks or actuator classes.
106. The system of claim 104, wherein a prepare phase freezes expansion of authority by an old controller while allowing the old controller to maintain a bounded continuity envelope until commit.
107. The system of claim 104, wherein a commit phase invalidates queued or precomputed ordinary commands associated with the prior authority epoch.
108. The system of claim 104, wherein failure after prepare and before commit does not grant ordinary effectuation authority to the proposed new controller.
109. The system of claim 104, wherein, after commit, inability to establish readiness of the proposed new controller causes transition to a separately authorized safe-action set rather than restoration of the prior authority epoch.
110. The system of claim 104, wherein the plurality of potential controllers comprises two or more of an onboard autonomy controller, remote pilot, remote-assistance service, fleet controller, detect-and-avoid safety controller, emergency controller, or minimal-risk controller.
111. The system of claim 104, wherein a handover capability is bound to a sink identifier, controller identifier, authority epoch, control-envelope digest, expiry, and freshness value.
112. The system of claim 104, wherein the protected authority-state store enforces, for each governed sink and authority epoch, that no more than one ordinary controller has effectuation authority, while a separately defined safe-action controller remains permitted to issue only stabilizing or risk-reducing actions.
113. The system of claim 104, wherein recovery after crash, rollback, reset, or failover completes or aborts an incomplete handover transaction before admitting a new ordinary control command.

#### END OF DOCUMENT

Page 17