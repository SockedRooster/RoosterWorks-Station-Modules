$ErrorActionPreference='Stop'
$kit=Split-Path -Parent $PSScriptRoot
$source="using System.Globalization;`n"+(Get-Content (Join-Path $kit 'Source/RingColor.cs') -Raw)
$doubles=Get-Content (Join-Path $kit 'Tools/GravityColorDoubles.cs') -Raw
$tests=Get-Content (Join-Path $kit 'Tools/GravityColorTests.cs') -Raw
Add-Type -TypeDefinition ($source+"`n"+$doubles+"`n"+$tests)
$fixture=Get-Content (Join-Path $kit 'Reports/GRAVITY_COLOR_FIXTURE.json') -Raw | ConvertFrom-Json
foreach($spec in $fixture){[GravityColorTest]::Add($spec.path,$spec.texture,$spec.vertexCount,[int[]]$spec.triangles,$spec.ranges)}
[GravityColorTest]::Run()
