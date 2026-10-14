$ErrorActionPreference = 'Stop'
$source = Get-Content (Join-Path $PSScriptRoot '../Source/PowerVariant.cs') -Raw
$doubles = @'
namespace UnityEngine { public static class Debug { public static void Log(string x) {} } }
public enum StartState { None }
public sealed class KSPField : Attribute {}
public static class HighLogic { public static bool LoadedSceneIsEditor,LoadedSceneIsFlight; }
public class EditorLogic { public static EditorLogic fetch=new EditorLogic(); public object ship=new object(); }
public static class GameEvents { public static ShipEvent onEditorShipModified=new ShipEvent(); public static ShipEvent onPartResourceListChange=new ShipEvent(); }
public static class MonoUtilities { public static int refreshes; public static void RefreshContextWindows(Part p) {refreshes++;} }
public class ShipEvent { public int calls; public void Fire(object ship) {calls++;} }
public class ConfigNode {
    public System.Collections.Generic.Dictionary<string,object> values=new System.Collections.Generic.Dictionary<string,object>();
    public ConfigNode(string s) {} public void AddValue(string key,object value) {values[key]=value;}
}
public class PartResource { public double amount,maxAmount; public bool flowState=true; }
public class ResourceList {
    public System.Collections.Generic.Dictionary<string,PartResource> data=new System.Collections.Generic.Dictionary<string,PartResource>();
    public PartResource this[string s] { get { return data.ContainsKey(s)?data[s]:null; } }
    public void Remove(string s) {data.Remove(s);}
}
public class BaseEvent { public bool active=true; }
public class BaseAction { public bool active=true; }
public class PartModule {
    public Part part;
    public System.Collections.Generic.Dictionary<string,BaseEvent> Events=new System.Collections.Generic.Dictionary<string,BaseEvent>{{"Toggle",new BaseEvent()}};
    public System.Collections.Generic.Dictionary<string,BaseAction> Actions=new System.Collections.Generic.Dictionary<string,BaseAction>{{"Action",new BaseAction()}};
    public virtual void OnStart(StartState s) {} public virtual string GetInfo() {return "";}
}
public class PartVariant { public string Name="Battery"; }
public class ModulePartVariants : PartModule { public PartVariant SelectedVariant=new PartVariant(); }
public class ProcessController : PartModule {
    public string resource="_RWCompactReactor"; public double capacity; public bool running; public int calls;
    public void SetRunning(bool r) {calls++;running=r;if(part.Resources[resource]!=null)part.Resources[resource].flowState=r;}
    public void Configure(bool enable,int multiplier) {
        if(!enable)part.Resources.Remove(resource);
        else part.Resources.data[resource]=new PartResource {amount=capacity,maxAmount=capacity};
    }
}
public class Part {
    public ResourceList Resources=new ResourceList();
    public System.Collections.Generic.List<PartModule> Modules=new System.Collections.Generic.List<PartModule>();
    public T FindModuleImplementing<T>() where T:PartModule {foreach(var m in Modules)if(m is T)return (T)m;return null;}
    public PartResource AddResource(ConfigNode n) {
        var r=new PartResource {amount=Convert.ToDouble(n.values["amount"]),maxAmount=Convert.ToDouble(n.values["maxAmount"])};
        Resources.data[(string)n.values["name"]]=r;return r;
    }
}
public class PowerTest {
    static void Check(bool b,string s) {if(!b)throw new Exception(s);}
    static bool Close(double a,double b) {return Math.Abs(a-b)<1e-7;}
    public static void Run() {
        foreach(double baseEC in new[]{2980.0,5740.0}) {
            double scale=baseEC==2980?1.1:1.2; double nuclearEC=baseEC==2980?2450:4730;
            HighLogic.LoadedSceneIsEditor=true;HighLogic.LoadedSceneIsFlight=false;
            var p=new Part();p.Resources.data["ElectricCharge"]=new PartResource{amount=baseEC/2,maxAmount=baseEC};
            var v=new ModulePartVariants{part=p};var c=new ProcessController{part=p};p.Modules.Add(v);p.Modules.Add(c);
            var t=new ModuleRWPowerVariant{part=p,batteryCapacity=baseEC,reactorCapacity=nuclearEC,reactorScale=scale};t.OnStart(StartState.None);
            Check(c.capacity==0&&!c.running&&p.Resources[c.resource]==null,"Passive cannot generate");
            Check(!c.Events["Toggle"].active&&!c.Actions["Action"].active,"Passive controls disabled");
            c.Configure(true,1);t.Update();Check(p.Resources[c.resource]==null,"Late Kerbalism Start cannot add passive process");
            int calls=c.calls;int modified=GameEvents.onEditorShipModified.calls;
            for(int i=0;i<25;i++)t.Update();Check(c.calls==calls&&GameEvents.onEditorShipModified.calls==modified,"Idle editor avoids repeated ship-modified events");
            for(int repeat=0;repeat<3;repeat++) {
                v.SelectedVariant.Name="Nuclear";t.Update();
                Check(Close(p.Resources["ElectricCharge"].maxAmount,nuclearEC)&&Close(p.Resources["ElectricCharge"].amount,nuclearEC/2),"Nuclear reduction and editor fill fraction");
                Check(Close(p.Resources["EnrichedUranium"].amount,1.5*scale)&&p.Resources["DepletedFuel"].amount==0,"Editor hardware installs finite fuel/waste");
                Check(!c.running&&!p.Resources[c.resource].flowState&&Close(c.capacity,scale),"Nuclear starts off and pseudo flow off");
                Check(c.Events["Toggle"].active&&c.Actions["Action"].active,"Nuclear start controls active");
                c.SetRunning(true);v.SelectedVariant.Name="Battery";t.Update();
                Check(Close(p.Resources["ElectricCharge"].amount,baseEC/2)&&p.Resources["EnrichedUranium"]==null&&p.Resources["DepletedFuel"]==null,"Passive editor restores battery removes reactor inventory");
                Check(!c.running&&c.capacity==0&&p.Resources[c.resource]==null,"Passive shuts down active reactor");
            }
            v.SelectedVariant.Name="Nuclear";t.Update();
            // Simulate another editor listener restoring the prefab capacity
            // while the selection remains Nuclear. It must be repaired and
            // the open resource controls rebuilt without another variant click.
            int refresh=MonoUtilities.refreshes;
            int shipBeforeRepair=GameEvents.onEditorShipModified.calls;
            p.Resources["ElectricCharge"].maxAmount=baseEC;t.Update();
            Check(Close(p.Resources["ElectricCharge"].maxAmount,nuclearEC)&&MonoUtilities.refreshes==refresh+1,"Capacity reset repaired and resource window rebuilt");
            Check(GameEvents.onEditorShipModified.calls==shipBeforeRepair,"Repair does not retrigger external ship-modified capacity resets");
            // A passive reintroduced fuel tank must also disappear from the
            // underlying inventory, not merely be hidden on the menu.
            v.SelectedVariant.Name="Battery";t.Update();
            p.Resources.data["EnrichedUranium"]=new PartResource{amount=1,maxAmount=1};
            refresh=MonoUtilities.refreshes;t.Update();
            Check(p.Resources["EnrichedUranium"]==null&&MonoUtilities.refreshes==refresh+1,"Passive inventory repair notifies and rebuilds menu");
            v.SelectedVariant.Name="Nuclear";t.Update();
            HighLogic.LoadedSceneIsEditor=false;HighLogic.LoadedSceneIsFlight=true;
            p.Resources["EnrichedUranium"].amount=.15;p.Resources["DepletedFuel"].amount=.33;p.Resources["ElectricCharge"].amount=300;
            c.SetRunning(true);p.Resources.Remove(c.resource);
            var loaded=new ModuleRWPowerVariant{part=p,batteryCapacity=baseEC,reactorCapacity=nuclearEC,reactorScale=scale};loaded.OnStart(StartState.None);
            Check(p.Resources["EnrichedUranium"].amount==.15&&p.Resources["DepletedFuel"].amount==.33&&p.Resources["ElectricCharge"].amount==300,"Flight restore never refuels or resets waste/EC");
            Check(c.running&&p.Resources[c.resource].flowState,"Flight restore preserves running state");
            p.Resources.Remove("EnrichedUranium");p.Resources.Remove("DepletedFuel");
            var absent=new ModuleRWPowerVariant{part=p,batteryCapacity=baseEC,reactorCapacity=nuclearEC,reactorScale=scale};absent.OnStart(StartState.None);
            Check(p.Resources["EnrichedUranium"].amount==0,"Missing flight fuel remains empty");
        }
    }
}
'@
Add-Type -TypeDefinition ($source + "`n" + $doubles)
[PowerTest]::Run()
Write-Output 'PASS actual power variant source: both sizes, repeated editor changes, proportional storage/fill, disabled passive process, delayed Start, reactor-off initialization, saved running state, no flight refill and no editor event loop'
