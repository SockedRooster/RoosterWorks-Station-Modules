Current EC balance: see ELECTRIC_CHARGE_BALANCE.md; older capacity figures below are historical.

# v0.12.0-dev.1 greenhouse inspection-light repair

- [ ] In editor/flight, find stock Lights On/Off; new part defaults to on.
- [ ] At night, confirm real light illuminates crop meshes, beyond bright strips.
- [ ] Toggle off/on and Light action group; save/reload and verify state.
- [ ] With Default, turn crop production off: inspection lights remain available.
- [ ] In sunlight, normal crop emission may dim; manual inspection light still works.
- [ ] Confirm inspection strips and crop strips do not fight over one material.
- [ ] Check GRN-375 independently; four native point lights, scaled 3.3 m ranges.
- [ ] Cosmetic inspection lighting has no additional EC drain; actual grow-lamp
      physics retain Kerbalism's existing EC demand. Check crop production separately.

Previous crop checklist below remains applicable, except the statement that no
point light is provided: v0.12.0-dev.1 adds that native light explicitly.

# RW-GRN-250 — KSP 1.12.5 test checklist

- [ ] Utility listing: dry mass 2.75 t, 16000 funds, 0 crew, 1000 EC; no IVA/EVA.
- [ ] Stack both size-2 ends at ±1.8 m; compare family rims and inspect closed caps.
- [ ] Inspect eight glass bays from all directions: frames overlap, no open slits.
- [ ] See real foliage/trays through glass; check sorting, lighting and far-side panes.
- [ ] Inspect all RoosterWorks badges, growing racks, service panels and irrigation.
- [ ] With Default, inspect ModuleManager.ConfigCache: exactly one Greenhouse;
      crop_size and ec_rate half template values, each input/output half, same
      crop_rate and thresholds; lamps RW_GreenhouseLamps; no animation references.
- [ ] Template kerbalism-greenhouse must remain unchanged. Confirm no MM errors.
- [ ] Confirm one Habitat (when FeatureHabitat) and one pressure controller.
- [ ] Confirm 40 Water, 200 Ammonia, 3000 CO2, 2000 Nitrogen startup; 300 Food
      and 6000 Oxygen capacity initially empty, plus battery. Record loaded mass.
- [ ] Stock cosmetic light module absent when Default Greenhouse was copied;
      greenhouse operation owns warm-white emission with no fighting/flickering.
- [ ] In a supplied pressurized station, enable greenhouse and confirm growth/
      harvest on older versions or continuous output on versions using that model.
- [ ] Verify food/output storage limit, oxygen production and water/nutrient/carbon
      consumption. Compare actual rates with template under the same conditions.
- [ ] In darkness, confirm artificial-light EC draw and emission; in bright sun,
      confirm module reduces lamp intensity/draw. Battery alone is not generation.
- [ ] Remove power in darkness, then each required input; production must stop.
- [ ] Depressurize and test radiation threshold; inspect reported production issue.
- [ ] Test time warp, unload vessel, return and save/load; no duplicated resources.
- [ ] With no Default profile, verify no unknown resources/Greenhouse module;
      manual cosmetic lights work and no food is created. Other profiles need
      their own production patch; stock-only greenhouse is visual equipment.
- [ ] Check prior nine parts, AIR boarding, PWR battery and adapter fit.

Static plants do not track crop progress. No custom IVA, shutter animation, crop
animation or point light is provided. Shader alpha and lamp emission must be
verified in Unity/KSP; CPU preview is not a gameplay or transparency-sorting test.
Record KSP.log, ModuleManager.ConfigCache, version, craft and screenshots on failure.
