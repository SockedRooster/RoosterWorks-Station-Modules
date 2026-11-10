param([string]$KspRoot='D:/SteamLibrary/steamapps/common/Kerbal Space Program')
$ErrorActionPreference='Stop'
$kit=Split-Path -Parent $PSScriptRoot
$managed=Join-Path $KspRoot 'KSP_x64_Data/Managed'
$compileArgs=@('C:/Program Files/dotnet/sdk/10.0.401/Roslyn/bincore/csc.dll','/nologo','/target:library','/nostdlib+','/optimize+','/deterministic+','/langversion:7.3')
foreach($reference in @('mscorlib.dll','System.dll','System.Core.dll','Assembly-CSharp.dll','UnityEngine.dll','UnityEngine.CoreModule.dll')){$compileArgs+='/reference:'+(Join-Path $managed $reference)}
$compileArgs+='/out:'+(Join-Path $kit 'GameData/RoosterWorksStationModules/Plugins/RoosterWorksStationLogistics.dll')
$compileArgs+=Join-Path $kit 'Source/StationLogisticsContents.cs'
& dotnet @compileArgs
if($LASTEXITCODE){throw 'Station logistics compilation failed'}
'PASS station logistics compiled against installed KSP 1.12.5 assemblies'
