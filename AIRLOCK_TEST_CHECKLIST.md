Current EC balance: see ELECTRIC_CHARGE_BALANCE.md; older capacity figures below are historical.

# RW-AIR-250 test candidate — KSP 1.12.5 / v0.8.0-dev.1

## Appearance and assembly

- [ ] Locate RW-AIR-250 under Utility. Inspect front/rear/top/bottom in VAB and flight.
- [ ] Badges read outward, rim seams are closed, hardware is seated; check sun/shadow.
- [ ] Attach both size-2 ends to HAB/LAB/CMD/HUB/LOG and verify flush mating.
- [ ] Toggle warm-white porthole lighting; only RW_AirGlass illuminates.
- [ ] Confirm two crew seats/portraits and crew transfer using temporary stock IVA.
- [ ] Load/reload the craft and scene; retain inventory, crew and light state.

## Stock EVA and boarding (essential new checks)

- [ ] On an unobstructed craft with a crewed command module, transfer a Kerbal into AIR.
- [ ] EVA from both occupant portraits. Spawn is at side hatch, outward, clear of hull.
- [ ] Grab the native ladder, climb in both directions, let go and re-grab.
- [ ] Board AIR from the ladder/exit zone. Repeat after quicksave/load and scene change.
- [ ] Check actual neighbouring-part obstructions still block EVA normally.
- [ ] Standard Windows HAB remains gated and Side Hatch HAB still works as previously confirmed.
- [ ] Two inventory slots and 120 L packed limit work for compatible EVA equipment; 400 EC loads.

## Kerbalism

- [ ] With FeatureHabitat, AIR shows a 6 m³ / 20 m² habitat and no duplicate Habitat module.
- [ ] Attach to a provisioned, powered station; check atmosphere/pressure and crew transfer.
- [ ] EVA/boarding respects Kerbalism suit, pressure, atmosphere and resource rules.
- [ ] Depressurization controls, if provided by installed Kerbalism, behave normally; no bespoke cycle advertised.
- [ ] Without Kerbalism, part loads and stock EVA/boarding work without missing-resource warnings.

Record KSP.log, ModuleManager.ConfigCache, craft and screenshots for failures.
Offline trigger/convex-hull checks do not confirm KSP runtime discovery or EVA.
The temporary IVA is borrowed stock layout; custom chamber IVA remains deferred.
