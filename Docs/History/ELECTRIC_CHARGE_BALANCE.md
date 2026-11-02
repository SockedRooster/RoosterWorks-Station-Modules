# RoosterWorks Station Modules — v0.16.0-dev.1

Four new crewless passage models: straight tubes and 90-degree elbows in **2.5 m / 3.75 m**, with pressure/conditional CLS support and accepted White/Grey finishes. HAB batteries cut 30%, PWR Battery only 15%, PWR Nuclear 20%, rounded base EC to tens. CMD/LAB archive limits are **2.5 GB**; LAB sample storage is **100 slots**. Requested **Ground-base modules** and **Adjustable legs** are added to ROADMAP.md.

Latest stats, source, guards and in-game checks: CREW_TUBES_AND_BALANCE.md. The existing 19 native models, glass, lighting, hatch and finish remain preserved. 23 current native/catalogue parts plus hidden legacy reactor IDs. Offline checks are build evidence; new model/gameplay confirmation remains pending. Close KSP before replacing the TEST folder. No installation, save modification, GitHub action or release was performed.

## Previous development history — old capacity figures superseded

# v0.14 PWR overrides

PWR-250 is now **3500 EC**, PWR-375 **6750 EC**. These explicit user values replace the previous 12600/42525 EC proxy values below. They also apply to the optional nuclear editions. All other capacities and crewed Kerbalism expectations are unchanged. The current frozen policy includes `override_base_ec` for PWR and retains reference +5% elsewhere. See FINISH_AND_REACTOR_OPTIONS.md for the optional reactor's separate generation rates.

## Historical v0.13 balance rationale

# v0.13.0-dev.1 — ElectricCharge balance: reference base + 5%

User requested applying comparable-part battery balance across all parts with
5% above base. This pass changes only initial/max integrated EC storage across
the current 19-part station family. It does not rebalance electrical consumption,
generation, light behavior, greenhouse output, other supplies, crew, dry mass,
price, technology, geometry, attachment or physics. No installed game files edited.

Reference capacities were read from installed, unpatched configs and frozen as
numbers, source IDs and SHA256 in Source/Balancing/electric_charge_policy.json.
No comparator mod is required to build or use these capacities. Rules:
matching stock/SSPXr function and size when available; +5% once on base; no
integrated comparator battery remains zero, rather than creating a battery.
HAB-375 uses the 750 EC six-seat compact SSPXr habitat (-375-3), with HAB-250
using 400 EC SSPXr habitat. CMD uses SSPXr 200/450; CUP stock 200 / SSPXr 500.
LAB stock MPL-LG-2 / SSPXr lab have no top-level battery; their nested EC entries
are consumption, not storage. AIR, cargo LOG and greenhouses also have no
integrated comparator storage. HUB and adapter remain passive with zero EC.
PWR uses installed Near Future Electrical battery-25, 12000 EC, as a dedicated
battery comparator; absent 3.75 counterpart uses 3.375 volume proxy, then +5%.
This avoids comparing a battery core with a crew pod and retains bulk station storage.

| Role | 2.5 m base EC | 3.75 m base EC | Reference |
|---|---:|---:|---|
| HAB | 420 | 787.5 | sspx-habitation-25-1 / sspx-habitation-375-3 |
| LAB | 0 | 0 | Large_Crewed_Lab / sspx-lab-375-1 |
| CMD | 210 | 472.5 | sspx-core-25-1 / sspx-core-375-1 |
| HUB | 0 | 0 | passive structural junction/adapter / passive structural junction/adapter |
| CUP | 210 | 525 | cupola / sspx-cupola-375-1 |
| LOG | 0 | 0 | sspx-cargo-25-1 / sspx-cargo-25-1 |
| AIR | 0 | 0 | sspx-airlock-25-1 / sspx-airlock-25-1 |
| PWR | 12600 | 42525 | battery-25 / battery-25 |
| GRN | 0 | 0 | sspx-greenhouse-25-1 / sspx-greenhouse-375-1 |

Adapter EC remains zero. These are base values, BEFORE Kerbalism. Under the
current Default crewed-part x2.8 patch: CMD-250 588; CMD-375 1323; CUP-250 588;
CUP-375 1470; HAB-250 1176; HAB-375 2205. PWR is crewless: 12600 / 42525 EC.
Do not write boosted values into base configs or apply the +5% again in a patch.
LAB/AIR/LOG/GRN now rely on connected vessel batteries/generation. In particular,
greenhouse production needs connected power; manual cosmetic inspection lights
retain their zero added draw. Food/water/gas startup buffers and rates unchanged.

Source/electric_charge_balance.py applies the explicit policy; build_family375.py
overrides its generic resource scaling for EC. Tools/build_ec_balance.py performs
the config-only balance and refreshes metadata/manifest. Canonical family build
and individual builder wrappers apply the policy before manifest output.
No blind cubic scaling for ordinary integrated batteries, no double 5% bonus.

Every pre-balance GameData file hash from v0.12 is recorded. Original own CFGs
are frozen in Source/Balancing/v012-before; check_preserved verifies historical
hashes and reconstructs prior EC values to prove that only those values changed.
All 19 native models, textures, point lights, runtime DLL and compatibility patches
are byte-identical. Existing historical regression checks use this constrained
EC-only exception, not new arbitrary golden hashes. A large config-only rebuild
must reproduce identical balanced CFGs. Offline suite passed.

KSP actual cache and runtime checks remain pending. Verify new parts in VAB after
reloading configs, inspect ModuleManager.ConfigCache, test electrical loads and
supplied greenhouse operation. Existing craft/save snapshots may retain prior
resource capacities: compare newly placed parts before attributing mismatches
to the new configs. No saves were modified. No install, commit, tag or release.

Build: python Tools/build_ec_balance.py. Validate: python Tools/validate.py.
Package: python Tools/package_appearance.py. Models/previews do not need rebuilding
for this balance pass. Previous lighting and large-family checklists still apply,
with their old EC figures superseded by this document.
