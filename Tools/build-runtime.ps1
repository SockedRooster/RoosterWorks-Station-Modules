param(
    [string]$KspRoot = 'D:/SteamLibrary/steamapps/common/Kerbal Space Program',
    [string]$Compiler = 'C:/Program Files/dotnet/sdk/10.0.401/Roslyn/bincore/csc.dll'
)
$ErrorActionPreference = 'Stop'
$packageRoot = Split-Path -Parent $PSScriptRoot
$managedRoot = Join-Path $KspRoot 'KSP_x64_Data/Managed'
$pluginRoot = Join-Path $packageRoot 'GameData/RoosterWorksStationModules/Plugins'
New-Item -ItemType Directory -Force -Path $pluginRoot | Out-Null
$compileArgs = @($Compiler, '/nologo', '/target:library', '/nostdlib+', '/optimize+', '/deterministic+', '/langversion:7.3')
foreach ($reference in @('mscorlib.dll','System.dll','System.Core.dll','Assembly-CSharp.dll','UnityEngine.dll','UnityEngine.CoreModule.dll','UnityEngine.PhysicsModule.dll')) {
    $compileArgs += '/reference:' + (Join-Path $managedRoot $reference)
}
$compileArgs += '/out:' + (Join-Path $pluginRoot 'RoosterWorksStationRuntime.dll')
$compileArgs += Join-Path $packageRoot 'Source/StationHatch.cs'
& dotnet @compileArgs
if ($LASTEXITCODE -ne 0) { throw 'Runtime compilation failed' }
