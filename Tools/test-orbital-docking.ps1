$ErrorActionPreference='Stop'
$kit=Split-Path -Parent $PSScriptRoot
$source=Get-Content (Join-Path $kit 'Source/OrbitalIndustryDocking.cs') -Raw
$doubles=Get-Content (Join-Path $kit 'Tools/OrbitalDockingDoubles.cs') -Raw
$tests=Get-Content (Join-Path $kit 'Tools/OrbitalDockingTests.cs') -Raw
Add-Type -TypeDefinition ($source+"`n"+$doubles+"`n"+$tests)
[DockingTest]::Run()
