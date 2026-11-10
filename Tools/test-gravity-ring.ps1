$ErrorActionPreference='Stop'
$kit=Split-Path -Parent $PSScriptRoot
$source=Get-Content (Join-Path $kit 'Source/GravityRing.cs') -Raw
$tests=Get-Content (Join-Path $kit 'Tools/GravityRingTests.cs') -Raw
Add-Type -TypeDefinition ($source+"`n"+$tests)
[GravityRingTest]::Run()
