param([string]$KspRoot='D:/SteamLibrary/steamapps/common/Kerbal Space Program', [string]$Compiler='C:/Program Files/dotnet/sdk/10.0.401/Roslyn/bincore/csc.dll')
$ErrorActionPreference='Stop'
$kitRoot=Split-Path -Parent $PSScriptRoot
$managedRoot=Join-Path $KspRoot 'KSP_x64_Data/Managed'
$compileArgs=@($Compiler,'/nologo','/target:library','/nostdlib+','/optimize+','/deterministic+','/langversion:7.3')
foreach ($reference in @('mscorlib.dll','System.dll','System.Core.dll','Assembly-CSharp.dll','UnityEngine.dll','UnityEngine.CoreModule.dll')) {$compileArgs+='/reference:'+(Join-Path $managedRoot $reference)}
$compileArgs+='/out:'+(Join-Path $kitRoot 'GameData/RoosterWorksStationModules/Plugins/RoosterWorksEditor.dll')
$compileArgs+=Join-Path $kitRoot 'Source/EditorMenu.cs'
& dotnet @compileArgs
if ($LASTEXITCODE -ne 0) {throw 'Editor runtime compilation failed'}
