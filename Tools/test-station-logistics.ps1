param([int]$Size=250)
$ErrorActionPreference='Stop'
$kit=Split-Path -Parent $PSScriptRoot
$source=Get-Content (Join-Path $kit 'Source/StationLogisticsContents.cs') -Raw
$tests=Get-Content (Join-Path $kit 'Tools/StationLogisticsTests.cs') -Raw
Add-Type -TypeDefinition ($source+"`n"+$tests)
$profiles=Get-Content (Join-Path $kit 'Reports/STATION_LOG_CAPACITIES.json') -Raw | ConvertFrom-Json
$key="RW_LOG_$Size"
[GroundLogisticsTest]::Profile=$key
foreach($choice in $profiles.$key.loadouts.PSObject.Properties){
 $resources=@($choice.Value)
 [GroundLogisticsTest]::AddChoice($choice.Name,[string[]]@($resources | ForEach-Object {$_.name}),[double[]]@($resources | ForEach-Object {$_.amount}),[double[]]@($resources | ForEach-Object {$_.maxAmount}))
}
[GroundLogisticsTest]::Run()
