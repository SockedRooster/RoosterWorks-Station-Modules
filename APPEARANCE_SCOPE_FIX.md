# Station Modules appearance scope fix — v0.7.5-dev.5

Fixes the unwanted nonfunctional Surface/Rings controls on Station Support
entirely in Station Modules. No separate Support UI hotfix folder is required.

ExteriorFinish now matches only parts with models in
RoosterWorksStationModules/Models. The menu and B9 swatches require actual
ModuleRWRingColor / ModuleRWStationFinish controllers. Their patch pass moves
from FOR to AFTER RoosterWorksStationModules, ensuring those controllers have
already been added before eligibility is checked.

All 41 current station parts retain their appearance controls. The 12 ground
hot-patch parts already contain matching controllers, so their controls also
remain. The 15 Station Support parts receive none of the extra finish/menu/B9
modules; their stock Open Frame/Armored Panels/Armored Grey and adapter
White/Armored Grey variants remain unchanged. Other RW_* mods are unaffected
unless their parts explicitly have compatible controllers/models.

GameData changes are limited to the two selector headers in ExteriorFinish.cfg
and EditorAppearance.cfg plus version metadata. Subtypes, colors, models,
textures, DLLs, ring-reopen fix, data tiers, EC, fuel, supplies and other gameplay
remain identical to dev4. Builders emit the corrected selectors; regression
guards compare against the retained prior selector files and allow header-only
changes, not arbitrary asset changes.

## Install

Close KSP and replace the RoosterWorksStationModules folder with this TEST
build. Leave Station Support and the ground-module hot patch unchanged.
If you previously installed RoosterWorksSupportUIHotfix, remove that separate
folder from GameData; it is now unnecessary. No game installation/save edits
were performed automatically.

## Live check

With the separate Support hotfix absent, support girders/adapters should have
only their working stock variants. Station/ground Surface and Rings should
still switch, reopen, copy and save correctly. Offline tests cover actual part
families and patch order; live VAB/SPH confirmation remains pending. This is a
local development build, not a release/publication claim.
