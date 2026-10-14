$ErrorActionPreference = 'Stop'
# Actual source with state-only doubles. Checks selection/mapping/persistence,
# not Unity rendering. Full DLL compilation separately uses installed KSP APIs.
$source = Get-Content (Join-Path $PSScriptRoot '../Source/StationFinish.cs') -Raw
$doubles = @'
namespace UnityEngine {
    public class Texture { public string name; public Texture(string n) {name=n;} }
    public class Material { public string name; public Texture mainTexture; }
    public class Renderer { public Material[] materials; }
    public static class Debug { public static int errors; public static void LogError(string x) {errors++;} public static void Log(string x) {} }
}
public enum UI_Scene { Editor, Flight, All }
public enum StartState { None }
public sealed class KSPField : Attribute { public bool isPersistant,guiActiveEditor; public string guiName; }
public sealed class UI_ChooseOption : Attribute { public string[] options; public UI_Scene affectSymCounterparts; }
public static class HighLogic { public static bool LoadedSceneIsEditor, LoadedSceneIsFlight; }
public class Part {
    public UnityEngine.Renderer[] renderers;
    public System.Collections.Generic.List<T> FindModelComponents<T>() {
        var results = new System.Collections.Generic.List<T>();
        foreach(var r in renderers) results.Add((T)(object)r);
        return results;
    }
}
public class PartModule {
    public Part part;
    public System.Collections.Generic.Dictionary<string,BaseField> Fields = new System.Collections.Generic.Dictionary<string,BaseField> { {"finish",new BaseField()} };
    public virtual void OnStart(StartState s) {}
    public virtual void OnUpdate() {}
    public virtual string GetInfo() {return "";}
}
public class BaseField { public UI_Control uiControlEditor = new UI_Control(); }
public class UI_Control {
    public Action<BaseField,object> onFieldChanged, onSymmetryFieldChanged;
}
public class GameDatabase {
    public static GameDatabase Instance=new GameDatabase();
    public System.Collections.Generic.Dictionary<string,UnityEngine.Texture> textures=new System.Collections.Generic.Dictionary<string,UnityEngine.Texture>();
    public UnityEngine.Texture GetTexture(string name,bool normal) {return textures.ContainsKey(name)?textures[name]:null;}
}
public class FinishTest {
    static void Check(bool b,string reason) {if(!b)throw new Exception(reason);}
    public static void Run() {
        var materials=new System.Collections.Generic.List<UnityEngine.Material>();
        foreach(string suffix in new[]{"ceramic","white","cladding","cladding_white"}) {
            foreach(string prefix in new[]{"RW_","RW_Hub_","RW_Power_"}) {
                materials.Add(new UnityEngine.Material {name=prefix+suffix+" (Instance)"});
            }
            foreach(string grey in new[]{"","_grey"}) {
                string path="RoosterWorksStationModules/Models/rwm_"+suffix+grey;
                GameDatabase.Instance.textures.Add(path,new UnityEngine.Texture(path));
            }
        }
        var glass=new UnityEngine.Texture("original glass");
        var logo=new UnityEngine.Texture("original rooster");
        var glow=new UnityEngine.Texture("original warm-white light");
        materials.Add(new UnityEngine.Material{name="RW_glass",mainTexture=glass});
        materials.Add(new UnityEngine.Material{name="RW_crest",mainTexture=logo});
        materials.Add(new UnityEngine.Material{name="RW_Greenhouse_grninspection",mainTexture=glow});
        var t=new ModuleRWStationFinish {part=new Part {renderers=new[]{new UnityEngine.Renderer{materials=materials.ToArray()}}}};
        HighLogic.LoadedSceneIsEditor=true;t.OnStart(StartState.None);
        for(int i=0;i<12;i++) Check(materials[i].mainTexture!=null&&!materials[i].mainTexture.name.EndsWith("_grey"),"Default white");
        for(int repeat=0;repeat<4;repeat++) {
            t.finish="Grey metal";
            // Drive the actual editor callback, without PartModule.OnUpdate.
            t.Fields["finish"].uiControlEditor.onFieldChanged(t.Fields["finish"],"White");
            for(int i=0;i<12;i++) Check(materials[i].mainTexture.name.EndsWith("_grey"),"Grey mapping including overlapping _white suffix");
            t.finish="White";t.Update();
            for(int i=0;i<12;i++) Check(!materials[i].mainTexture.name.EndsWith("_grey"),"White restoration");
        }
        HighLogic.LoadedSceneIsEditor=false;HighLogic.LoadedSceneIsFlight=true;
        var loaded=new ModuleRWStationFinish {part=t.part,finish="Grey metal"};loaded.OnStart(StartState.None);
        for(int i=0;i<12;i++) Check(materials[i].mainTexture.name.EndsWith("_grey"),"Direct flight load of saved grey choice");
        Check(materials[12].mainTexture==glass&&materials[13].mainTexture==logo&&materials[14].mainTexture==glow,"Glass, crest, warm lighting preserved");
        var persistence=(KSPField)Attribute.GetCustomAttribute(typeof(ModuleRWStationFinish).GetField("finish"),typeof(KSPField));
        Check(persistence.isPersistant&&persistence.guiActiveEditor,"Persistent editor choice");
        var choice=(UI_ChooseOption)Attribute.GetCustomAttribute(typeof(ModuleRWStationFinish).GetField("finish"),typeof(UI_ChooseOption));
        Check(choice.affectSymCounterparts==UI_Scene.Editor,"Editor symmetry propagation");
        Check(t.Fields["finish"].uiControlEditor.onSymmetryFieldChanged!=null,"Symmetry change callback installed");
        // Simulate a visual mod renaming the material while retaining its map.
        for(int i=0;i<12;i++) materials[i].name="Renamed material "+i;
        loaded.finish="White";loaded.Update();
        for(int i=0;i<12;i++) Check(!materials[i].mainTexture.name.EndsWith("_grey"),"Texture-name fallback after material rename");
        loaded.finish="Grey metal";
        loaded.Fields["finish"].uiControlEditor.onSymmetryFieldChanged(loaded.Fields["finish"],"White");
        for(int i=0;i<12;i++) Check(materials[i].mainTexture.name.EndsWith("_grey"),"Symmetry callback with renamed materials");
        Check(UnityEngine.Debug.errors==0,"No missing texture paths");
    }
}
'@
Add-Type -TypeDefinition ($source + "`n" + $doubles)
[FinishTest]::Run()
Write-Output 'PASS actual finish source: default white, grey, white restore, overlapping names, repeated switches, saved flight choice, glass/logo/lamp preservation and symmetry setting'
