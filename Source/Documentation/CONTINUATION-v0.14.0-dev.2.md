# RoosterWorks v0.14.0-dev.2 — finish and reactor visibility fix

Fixes the reported white-only finish by binding the editor field/symmetry callbacks and using Unity Update in both scenes. Adds texture-name fallback for material renaming. The separate nuclear PWR editions now share the ordinary cores' largeElectrics tier and appear in VABOrganizer's nuclearReactors category. Search nuclear in Electrical; passive cores remain under batteries. Batteries remain 3500/6750 EC, nuclear output 5.5/6 EC/s, with retained fuel/waste and built-in cooling. Original native models and hatch DLL are unchanged.

Installed game log/cache showed both nuclear parts and the finish plugin loaded in dev.1. The prior finish test invoked a callback that did not reproduce editor behavior; updated tests drive actual UI callbacks without PartModule.OnUpdate. DLL compilation uses installed KSP assemblies. Offline validation does not establish live KSP visual/gameplay acceptance. Replace the folder while KSP is closed and retest newly placed parts. Do not claim installation, release, GitHub commit or successful gameplay confirmation.

Inspect this corrected source kit before any future edits. Latest source: rw-v0140dev2. See FINISH_AND_REACTOR_OPTIONS.md for usage, requirements, balance and confirmation checklist.

## Previous development notes

