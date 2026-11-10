$ErrorActionPreference='Stop'
$kit=Split-Path -Parent $PSScriptRoot
$managed='D:/SteamLibrary/steamapps/common/Kerbal Space Program/KSP_x64_Data/Managed'
$taskArgs=@('C:/Program Files/dotnet/sdk/10.0.401/Roslyn/bincore/csc.dll','/nologo','/target:library','/nostdlib+','/optimize+','/deterministic+','/langversion:7.3')
foreach($ref in @('mscorlib.dll','System.dll','System.Core.dll','Assembly-CSharp.dll','UnityEngine.dll','UnityEngine.CoreModule.dll','UnityEngine.PhysicsModule.dll')){$taskArgs+='/reference:'+(Join-Path $managed $ref)}
$taskArgs+='/out:'+(Join-Path $kit 'GameData/RoosterWorksStationModules/Plugins/RoosterWorksOrbitalIndustry.dll')
$taskArgs+=Join-Path $kit 'Source/OrbitalIndustryDocking.cs'
& dotnet @taskArgs
if($LASTEXITCODE -ne 0){throw 'Orbital runtime compilation failed'}
Write-Output 'PASS orbital docking policy compiled against KSP 1.12.5; no Ground Modules reference'
