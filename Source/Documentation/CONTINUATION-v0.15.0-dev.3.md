# v0.15.0-dev.3 — PWR resource-menu refresh

User confirmed that the reactor is now a stock variant, then reported stale EnrichedUranium/DepletedFuel menu entries after switching to Battery and unchanged displayed EC capacity. The installed dev.2 game log records successful Battery/Nuclear transitions and the rounded 5910 EC target. Prior state-double tests did not model KSP's open resource-widget caching.

The variant controller now fires onPartResourceListChange and calls KSP MonoUtilities.RefreshContextWindows after resource changes, rebuilding open slider ranges and removed fuel rows. It also verifies actual EC capacity when the remembered selection is unchanged, correcting a later editor reset, and removes reintroduced fuel tanks in Battery-only editor mode. Notification is change-triggered, not repeated every idle frame. The source test includes capacity-reset and passive fuel-reintroduction cases, with explicit window-refresh assertions. Actual live menu confirmation remains pending.

Rounded values are **3060 / 5910 EC nuclear**, **3500 / 6750 EC Battery only**, unchanged **5.5 / 6 EC/s** generation. Finish, models, other parts, finite fuel/waste and saved running-state behavior remain unchanged. Close KSP and replace the RoosterWorks folder with the dev.3 TEST build. Test a newly placed PWR core while keeping its right-click menu open: nuclear must show reduced maximum and fuel/waste rows; Battery must restore maximum and remove both fuel rows.

## Previous development notes

