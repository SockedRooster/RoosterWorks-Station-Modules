param([ValidateSet('RW_ISRU_250','RW_NST_250','RW_CEN_250','RW_NSM_250')][string]$PartID='RW_ISRU_250')
$ErrorActionPreference='Stop'
$kit=Split-Path -Parent $PSScriptRoot
$source="using System.Globalization;`n"+(Get-Content (Join-Path $kit 'Source/RingColor.cs') -Raw)
$doubles=Get-Content (Join-Path $kit 'Tools/GravityColorDoubles.cs') -Raw
$tests=(Get-Content (Join-Path $kit 'Tools/EndcapColorTests.cs') -Raw).Replace('RW_END_250_125',$PartID)
Add-Type -TypeDefinition ($source+"`n"+$doubles+"`n"+$tests)
$fixture=Get-Content (Join-Path $kit 'Reports/ORBITAL_INDUSTRY_COLOR_FIXTURE.json') -Raw | ConvertFrom-Json
foreach($spec in $fixture.$PartID){[EndcapColorTest]::Add($spec.path,$spec.texture,$spec.vertexCount,[int[]]$spec.triangles,$spec.ranges)}
[EndcapColorTest]::Run()
