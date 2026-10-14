$ErrorActionPreference='Stop'
$source=Get-Content (Join-Path $PSScriptRoot '../Source/EditorMenu.cs') -Raw
$doubles=@'
namespace UnityEngine {public static class Debug {public static void LogWarning(string s){}public static void LogError(string s){throw new System.Exception(s);}}}
public class KSPField:System.Attribute {public bool isPersistant;}
public class HighLogic {public static bool LoadedSceneIsEditor=true;}
public class BasePAWGroup {public string name,displayName;public bool startCollapsed;public BasePAWGroup(string n,string d,bool c){name=n;displayName=d;startCollapsed=c;}}
public class UI_Control {public System.Action<BaseField,object> onFieldChanged;}
public class UI_ChooseOption:UI_Control {public string[] options;}
public class BaseField {public bool guiActiveEditor=true;public UI_Control uiControlEditor=new UI_ChooseOption();public BasePAWGroup group;}
public class BaseEvent {public string guiName;public BasePAWGroup group;}
public class FieldList:System.Collections.Generic.List<BaseField> {public System.Collections.Generic.Dictionary<string,BaseField> keyed=new System.Collections.Generic.Dictionary<string,BaseField>();public BaseField this[string n]{get{if(!keyed.ContainsKey(n)){var f=new BaseField();keyed[n]=f;Add(f);}return keyed[n];}}}
public class Part {public System.Collections.Generic.List<PartModule> Modules=new System.Collections.Generic.List<PartModule>();public System.Collections.Generic.List<BaseEvent> Events=new System.Collections.Generic.List<BaseEvent>();}
public class PartModule {public Part part;public FieldList Fields=new FieldList();public System.Collections.Generic.List<BaseEvent> Events=new System.Collections.Generic.List<BaseEvent>();}
public class ModuleRWStationFinish:PartModule {public string finish="Grey metal";public ModuleRWStationFinish(){var f=Fields["finish"];}}
public class ModuleRWRingColor:PartModule {public string ringColor="Green";public ModuleRWRingColor(){var f=Fields["ringColor"];}}
public class ModuleRWPowerVariant:PartModule {public string hardware="Nuclear";}
public class ModulePartVariants:PartModule {public ModulePartVariants(){var f=Fields["selectedVariant"];}}
public class ModuleColorChanger:PartModule {public ModuleColorChanger(){Events.Add(new BaseEvent{guiName="Lights On"});}}
public class ModuleInventoryPart:PartModule {public ModuleInventoryPart(){Events.Add(new BaseEvent{guiName="Inventory"});}}
public class ModuleB9PartSwitch:PartModule {
 public string moduleID;public string CurrentSubtypeName{get;private set;}="White";
 public ModuleB9PartSwitch(){var f=Fields["currentSubtypeIndex"];}
 public void SwitchSubtype(string n){CurrentSubtypeName=n;}
 public void Click(string n){CurrentSubtypeName=n;Fields["currentSubtypeIndex"].uiControlEditor.onFieldChanged?.Invoke(Fields["currentSubtypeIndex"],null);}
}
public class HardDrive:PartModule {
 public int effectiveSampleCapacity=34;public string sampleCapacityUI="34 slots";
 private System.Collections.Generic.List<System.Collections.Generic.KeyValuePair<string,int>> sampleCapacities=new System.Collections.Generic.List<System.Collections.Generic.KeyValuePair<string,int>>();
 public HardDrive(){var f=Fields["sampleCapacityUI"];}
 public void Update(){foreach(var c in sampleCapacities)if(c.Key==sampleCapacityUI)effectiveSampleCapacity=c.Value;}
}
public static class EditorMenuTests {
 static void Check(bool ok,string s){if(!ok)throw new System.Exception(s);}
 public static void Run(){
  var p=new Part();var finish=new ModuleRWStationFinish();var ring=new ModuleRWRingColor();var stock=new ModulePartVariants();var power=new ModuleRWPowerVariant();var light=new ModuleColorChanger();var inventory=new ModuleInventoryPart();
  var surface=new ModuleB9PartSwitch{moduleID="RWFinishSwatch"};var rings=new ModuleB9PartSwitch{moduleID="RWRingSwatch"};
  p.Modules.AddRange(new PartModule[]{finish,ring,stock,power,light,inventory,surface,rings});p.Events.Add(new BaseEvent{guiName="Seat 0 inventory"});
  var menu=new ModuleRWEditorMenu{part=p};menu.LateUpdate();
  Check(surface.CurrentSubtypeName=="Grey_metal"&&rings.CurrentSubtypeName=="Green","Existing saved cosmetic selections restored");
  Check(!finish.Fields["finish"].guiActiveEditor&&!ring.Fields["ringColor"].guiActiveEditor,"No duplicate appearance rows");
  surface.Click("White");rings.Click("Gold");Check(finish.finish=="White"&&ring.ringColor=="Gold","Swatches immediately update persistent native controllers");
  rings.Fields["currentSubtypeIndex"].uiControlEditor.onFieldChanged=null;
  ring.ringColor="Original";menu.LateUpdate();Check(ring.ringColor=="Gold","Reopened menu resynchronizes selector even when choice name has not changed");
  rings.Click("Green");menu.LateUpdate();Check(ring.ringColor=="Green","Ring selector works after UI callbacks are recreated");
  Check(stock.Fields["selectedVariant"].group.name=="RWHardware"&&power.hardware=="Nuclear","Stock reactor hardware remains independent");
  Check(light.Events[0].group.startCollapsed&&inventory.Events[0].group.startCollapsed&&p.Events[0].group.name=="RWInventory","Lighting/seat inventory grouped and collapsed");
  var noB9=new Part();var old=new ModuleRWStationFinish();noB9.Modules.Add(old);new ModuleRWEditorMenu{part=noB9}.LateUpdate();Check(old.Fields["finish"].guiActiveEditor&&old.finish=="Grey metal","No-B9 fallback retains active original choice");
  foreach(double factor in new[]{1d,3.375d,8d}){
   p=new Part();var hd=new HardDrive{effectiveSampleCapacity=ModuleRWScienceTiers.Slots(factor,1)};p.Modules.Add(hd);var tiers=new ModuleRWScienceTiers{part=p,volumeFactor=factor};tiers.LateUpdate();
   var options=((UI_ChooseOption)hd.Fields["sampleCapacityUI"].uiControlEditor).options;Check(options.Length==10,"Ten sample choices");
   for(int i=0;i<10;i++){hd.sampleCapacityUI=options[i];hd.Update();tiers.LateUpdate();Check(hd.effectiveSampleCapacity==ModuleRWScienceTiers.Slots(factor,i+1),"Exact proportional whole-slot choice");}
   int saved=tiers.selectedSamples;hd.effectiveSampleCapacity=ModuleRWScienceTiers.Slots(factor,1);var reload=new ModuleRWScienceTiers{part=p,volumeFactor=factor,selectedSamples=saved};reload.LateUpdate();Check(hd.effectiveSampleCapacity==saved,"Saved rounded maximum survives native HardDrive startup validation");
   HighLogic.LoadedSceneIsEditor=false;hd.effectiveSampleCapacity=100;new ModuleRWScienceTiers{part=p,volumeFactor=factor,selectedSamples=1}.LateUpdate();Check(hd.effectiveSampleCapacity==100,"Flight archives are never resized");HighLogic.LoadedSceneIsEditor=true;
  }
  Check(ModuleRWScienceTiers.Slots(3.375,1)==34&&ModuleRWScienceTiers.Slots(3.375,10)==338,"Fractional volume scaling rounds half up");
 }
}
'@
Add-Type -TypeDefinition ($source+"`n"+$doubles)
[EditorMenuTests]::Run()
Write-Output 'PASS actual menu/tier source: saved colors, swatch changes, independent reactor hardware, grouped lighting/inventory, no-B9 fallback, ten whole-slot tiers, saved rounded selections, no flight resize'
