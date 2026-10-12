$ErrorActionPreference = 'Stop'
# Exercise the actual access method with small state-only doubles. This checks
# transitions, not Unity physics or KSP's live lifecycle; compile the full plugin
# separately with build-runtime.ps1 against the installed game assemblies.
$runtime = Get-Content (Join-Path $PSScriptRoot '../Source/StationHatch.cs') -Raw
$start = $runtime.IndexOf('    private void ApplyAccess()')
$end = $runtime.IndexOf('    private IEnumerator CheckAfterStart()', $start)
$method = $runtime.Substring($start, $end - $start)
$harness = @'
using System;
class Transform { public string name; }
class Collider { public bool enabled; public Transform transform; }
class PartVariant { public string Name; }
class ModulePartVariants { public PartVariant SelectedVariant = new PartVariant(); }
class Part { public Transform airlock; public bool noAutoEVAAny; public bool NoAutoEVA { get { return noAutoEVAAny; } } }
static class HighLogic { public static bool LoadedSceneIsFlight; }
static class Debug { public static void Log(string text) {} }
public class HatchAccessTest {
    const string HatchName = "RW_HAB250_EVA_Airlock";
    Part part = new Part();
    Collider hatchTrigger = new Collider { transform = new Transform {name=HatchName} };
    Collider ladderTrigger = new Collider();
    ModulePartVariants variants = new ModulePartVariants();
    string appliedVariant;
    bool ownsEvaLock, previousEvaLock;
    void Select(string name) { variants.SelectedVariant.Name=name; ApplyAccess(); }
    static void Check(bool pass,string label) { if(!pass)throw new Exception(label); }
    public static void Run() {
        HighLogic.LoadedSceneIsFlight=true;
        foreach(bool restricted in new[]{false,true}) {
            var t=new HatchAccessTest();t.part.noAutoEVAAny=restricted;
            t.part.airlock=t.hatchTrigger.transform;
            t.Select("Standard");
            Check(!t.hatchTrigger.enabled&&!t.ladderTrigger.enabled&&t.part.airlock==null&&t.part.NoAutoEVA,"Standard gate");
            t.Select("Standard");
            t.Select("SideHatch");
            Check(t.hatchTrigger.enabled&&t.ladderTrigger.enabled&&t.part.airlock==t.hatchTrigger.transform&&t.part.NoAutoEVA==restricted,"SideHatch restore original restriction");
            t.Select("Standard");t.Select("SideHatch");
            Check(t.part.NoAutoEVA==restricted,"Repeated transition preserves restriction");
        }
        var direct=new HatchAccessTest(); direct.Select("SideHatch");
        Check(direct.part.airlock==direct.hatchTrigger.transform&&!direct.part.NoAutoEVA,"Direct flight load of SideHatch");
        var absent=new HatchAccessTest();absent.hatchTrigger=null;absent.Select("SideHatch");
        Check(!absent.ladderTrigger.enabled&&absent.part.NoAutoEVA,"Missing hatch fails closed");
        var foreign=new HatchAccessTest();var other=new Transform{name="OtherModAirlock"};foreign.part.airlock=other;
        foreign.Select("SideHatch"); Check(foreign.part.airlock==other,"Preserve other airlock");
        var unknown=new HatchAccessTest();unknown.Select("Unknown");
        Check(unknown.part.airlock==null&&unknown.part.NoAutoEVA,"Unknown variant fails closed");
        HighLogic.LoadedSceneIsFlight=false;
        var editor=new HatchAccessTest();editor.Select("Standard");
        Check(!editor.part.NoAutoEVA,"Editor does not contaminate flight lock");
        editor.Select("SideHatch");Check(editor.ladderTrigger.enabled,"Editor switch enables ladder");
    }
'@
Add-Type -TypeDefinition ($harness + $method + "`n}")
[HatchAccessTest]::Run()
Write-Output 'PASS actual ApplyAccess logic: both variants, repeated switches, original restriction, direct load, absent hatch, foreign airlock, unknown variant, editor lock isolation'
