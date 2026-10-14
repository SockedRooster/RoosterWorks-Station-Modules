$ErrorActionPreference = 'Stop'
$source = (Get-Content (Join-Path $PSScriptRoot '../Source/RingColor.cs') -Raw) + "`n" + (Get-Content (Join-Path $PSScriptRoot '../Source/LogisticsContents.cs') -Raw)
$source = "using System;`nusing System.Collections.Generic;`nusing System.Globalization;`nusing UnityEngine;`n" + [regex]::Replace($source,'(?m)^using [^;]+;\r?\n','')
$doubles = @'
namespace UnityEngine {
 public class Object { public static Object Instantiate(Object x) {return ((Mesh)x).Clone();} public static void Destroy(Object x) {} }
 public class Texture {public string name;public Texture(string n){name=n;}}
 public struct Color {public static Color white = new Color();}
 public class Material : Object {public string name;public Texture mainTexture;public Color color;public Material(Material x){name=x.name;CopyPropertiesFromMaterial(x);}public Material(){}public void CopyPropertiesFromMaterial(Material x){mainTexture=x.mainTexture;color=x.color;}}
 public class Transform {public string name;public Transform parent;}
 public class Mesh : Object {public string name="native";public int vertexCount=6,subMeshCount=1;public double[] vertices={0,1,2,3,4,5},uvs={.1,.2,.3},normals={1,0,0};public Dictionary<int,int[]> sub=new Dictionary<int,int[]>{{0,new[]{0,1,2,3,4,5}}};public int[] GetTriangles(int i){return sub[i];}public void SetTriangles(int[] t,int i){sub[i]=t;}public Mesh Clone(){var m=new Mesh{vertexCount=vertexCount,subMeshCount=subMeshCount,name=name,vertices=(double[])vertices.Clone(),uvs=(double[])uvs.Clone(),normals=(double[])normals.Clone()};m.sub=new Dictionary<int,int[]>();foreach(var kv in sub)m.sub[kv.Key]=(int[])kv.Value.Clone();return m;}}
 public class MeshFilter {public Mesh sharedMesh;}
 public class Renderer {public Material[] materials;public Transform transform;public MeshFilter filter;public T GetComponent<T>(){return (T)(object)filter;}}
 public static class Debug {public static int errors;public static void LogError(string x){errors++;}public static void Log(string x){}}
}
public enum UI_Scene {Editor,Flight,All}
public enum StartState {None}
public sealed class KSPField : Attribute {public bool isPersistant,guiActiveEditor;public string guiName;}
public sealed class UI_ChooseOption : Attribute {public string[] options;public UI_Scene affectSymCounterparts;}
public static class HighLogic {public static bool LoadedSceneIsEditor=true,LoadedSceneIsFlight;}
public class BaseField {public UI_Control uiControlEditor=new UI_Control();}
public class UI_Control {public Action<BaseField,object> onFieldChanged,onSymmetryFieldChanged;}
public class PartModule {public Part part;public Dictionary<string,BaseField> Fields=new Dictionary<string,BaseField>{{"ringColor",new BaseField()},{"contents",new BaseField()}};public virtual void OnStart(StartState s){}public virtual string GetInfo(){return "";}}
public class ConfigNode {public string name;public Dictionary<string,string> values=new Dictionary<string,string>();public List<ConfigNode> nodes=new List<ConfigNode>();public ConfigNode(string n){name=n;}public void AddValue(string k,object v){values[k]=Convert.ToString(v,CultureInfo.InvariantCulture);}public string GetValue(string k){return values.ContainsKey(k)?values[k]:null;}public ConfigNode[] GetNodes(string n){return nodes.FindAll(x=>x.name==n).ToArray();}}
public class GameDatabase {public static GameDatabase Instance=new GameDatabase();public Dictionary<string,UnityEngine.Texture> textures=new Dictionary<string,UnityEngine.Texture>();public List<ConfigNode> nodes=new List<ConfigNode>();public UnityEngine.Texture GetTexture(string p,bool normal){return textures.ContainsKey(p)?textures[p]:null;}public ConfigNode[] GetConfigNodes(string n){return nodes.FindAll(x=>x.name==n).ToArray();}}
public class PartResource {public double amount,maxAmount;}
public class ResourceList {public Dictionary<string,PartResource> data=new Dictionary<string,PartResource>();public PartResource this[string n]{get{return data.ContainsKey(n)?data[n]:null;}}public void Remove(string n){data.Remove(n);}}
public class PartResourceLibrary {public static PartResourceLibrary Instance=new PartResourceLibrary();public HashSet<string> definitions=new HashSet<string>{"Food","Water","Oxygen","Nitrogen","Ammonia","Waste","WasteWater"};public object GetDefinition(string n){return definitions.Contains(n)?this:null;}}
public class Part {public ResourceList Resources=new ResourceList();public UnityEngine.Renderer[] renderers=new UnityEngine.Renderer[0];public object collider=new object();public List<T> FindModelComponents<T>(){var result=new List<T>();foreach(var r in renderers)result.Add((T)(object)r);return result;}public void AddResource(ConfigNode n){Resources.data[n.GetValue("name")]=new PartResource{amount=double.Parse(n.GetValue("amount"),CultureInfo.InvariantCulture),maxAmount=double.Parse(n.GetValue("maxAmount"),CultureInfo.InvariantCulture)};}}
public class Event {public int calls;public void Fire(object p){calls++;}}
public static class GameEvents {public static Event onPartResourceListChange=new Event(),onEditorShipModified=new Event();}
public class EditorLogic {public static EditorLogic fetch=new EditorLogic();public object ship=new object();}
public static class MonoUtilities {public static int refreshes;public static void RefreshContextWindows(object p){refreshes++;}}
public static class CustomizationTest {
 static void Check(bool b,string message){if(!b)throw new Exception(message);}
 static ConfigNode Node(string type,params string[] pairs){var n=new ConfigNode(type);for(int i=0;i<pairs.Length;i+=2)n.AddValue(pairs[i],pairs[i+1]);return n;}
 static void Select(ModuleRWLogisticsContents m,string value){m.contents=value;m.Fields["contents"].uiControlEditor.onFieldChanged(m.Fields["contents"],"");}
 public static void Run(){
  var texture=new UnityEngine.Texture("rwm_bronze");var grey=new UnityEngine.Texture("grey shell");
  foreach(string key in new[]{"steel","white","charcoal","blue","green","red","gold"})GameDatabase.Instance.textures["RoosterWorksStationModules/Models/rwm_ring_rwm_bronze_"+key]=new UnityEngine.Texture(key);
  var map=Node("RW_RING_MAP","model","RW_HAB_250");map.nodes.Add(Node("MESH","path","/RW_HAB_250/RW_Bronze","texture","rwm_bronze","vertices","6","triangles","2","ranges","1:1"));GameDatabase.Instance.nodes.Add(map);
  var material=new UnityEngine.Material{mainTexture=texture,name="RW_bronze"};var native=new UnityEngine.Mesh();var root=new UnityEngine.Transform{name="renamed model root"};var renderer=new UnityEngine.Renderer{materials=new[]{material},filter=new UnityEngine.MeshFilter{sharedMesh=native},transform=new UnityEngine.Transform{name="RW_Bronze",parent=root}};
  var untouched=new UnityEngine.Material{mainTexture=new UnityEngine.Texture("glass/logo/lamp"),name="RW_glass"};var excluded=new UnityEngine.Renderer{materials=new[]{untouched},filter=new UnityEngine.MeshFilter{sharedMesh=new UnityEngine.Mesh()},transform=new UnityEngine.Transform{name="RW_glass",parent=root}};
  var p=new Part{renderers=new[]{renderer,excluded}};object collider=p.collider;var ring=new ModuleRWRingColor{part=p};ring.OnStart(StartState.None);
  Check(renderer.filter.sharedMesh==native&&renderer.materials.Length==1,"Default keeps native visual mesh unmodified");
  foreach(string color in new[]{"Blue","Green","Red","Gold","White","Steel","Charcoal"}){
   ring.ringColor=color;ring.Fields["ringColor"].uiControlEditor.onFieldChanged(ring.Fields["ringColor"],"");
   var split=renderer.filter.sharedMesh;Check(split!=native&&split.subMeshCount==2,"Own visual instance split");Check(split.vertices[5]==native.vertices[5]&&split.uvs[2]==native.uvs[2]&&split.normals[0]==native.normals[0],"Vertex data preserved");
   Check(split.GetTriangles(0)[0]==0&&split.GetTriangles(1)[0]==3,"Only exact selected triangle moves to colored submesh");Check(renderer.materials[1].mainTexture.name==color.ToLowerInvariant(),"Requested color");Check(renderer.materials[0]==material&&p.collider==collider&&excluded.materials[0]==untouched,"Shell/physics/excluded surfaces untouched");
  }
  // A copied/symmetric editor part can inherit an already partitioned mesh.
  // A rebuilt editor/model view may retain the mesh but instantiate materials
  // again. Cached old ring references must not silently color detached objects.
  renderer.materials=new[]{new UnityEngine.Material(renderer.materials[0]),new UnityEngine.Material(renderer.materials[1])};
  ring.ringColor="Blue";ring.Update();Check(renderer.materials[1].mainTexture.name=="blue","Ring changes after menu/model material re-instantiation");
  renderer.filter.sharedMesh=native;renderer.materials=new[]{material};
  ring.ringColor="Green";ring.Update();Check(renderer.filter.sharedMesh.subMeshCount==2&&renderer.materials[1].mainTexture.name=="green","Ring changes after native mesh/material reset");
  renderer.filter.sharedMesh=native;
  ring.ringColor="Gold";ring.Update();Check(renderer.materials[1].mainTexture.name=="gold","Native mesh reset with stale two-material array recovers");
  foreach(string color in new[]{"Blue","Green","Red"}){
   renderer.materials=new[]{new UnityEngine.Material(renderer.materials[0]),new UnityEngine.Material(renderer.materials[1])};
   ring.ringColor=color;ring.Update();Check(renderer.materials[1].mainTexture.name==color.ToLowerInvariant(),"Repeated menu reopen and color reselection");
  }
  ring.ringColor="Charcoal";ring.Update();
  var copyRenderer=new UnityEngine.Renderer{materials=(UnityEngine.Material[])renderer.materials.Clone(),filter=new UnityEngine.MeshFilter{sharedMesh=renderer.filter.sharedMesh},transform=renderer.transform};
  var copy=new ModuleRWRingColor{part=new Part{renderers=new[]{copyRenderer}},ringColor="Red"};copy.OnStart(StartState.None);Check(copyRenderer.materials[1].mainTexture.name=="red"&&renderer.materials[1].mainTexture.name=="charcoal","Copied mesh gets independent materials");
  ring.ringColor="Original";ring.Update();Check(renderer.materials[1].mainTexture==texture,"Original texture restored");renderer.materials[0].mainTexture=grey;ring.Update();Check(renderer.materials[1].mainTexture==grey,"Original follows later exterior finish");
  var originalCopy=new ModuleRWRingColor{part=new Part{renderers=new[]{copyRenderer}},ringColor="Original"};originalCopy.OnStart(StartState.None);Check(copyRenderer.materials[1].mainTexture==grey,"Original repairs copied colored mesh");
  HighLogic.LoadedSceneIsEditor=false;HighLogic.LoadedSceneIsFlight=true;var flight=new ModuleRWRingColor{part=p,ringColor="Blue"};flight.OnStart(StartState.None);Check(renderer.materials[1].mainTexture.name=="blue","Saved flight ring color");
  HighLogic.LoadedSceneIsEditor=true;HighLogic.LoadedSceneIsFlight=false;flight.OnDestroy();ring.OnDestroy();Check(renderer.filter.sharedMesh==native&&renderer.materials.Length==1,"Owned mesh cleanup restores original");
  foreach(double scale in new[]{1.0,3.375,8.0}){
   string profile=scale==1?"RW_LOG_250":scale==3.375?"RW_LOG_375":"RW_LOG_500";var set=Node("RW_LOG_LOADOUTS","name",profile);
   var mixed=Node("LOADOUT","name","Mixed supplies");mixed.nodes.Add(Node("RESOURCE","name","Food","amount",(120*scale).ToString(CultureInfo.InvariantCulture),"maxAmount",(120*scale).ToString(CultureInfo.InvariantCulture)));mixed.nodes.Add(Node("RESOURCE","name","Water","amount",(60*scale).ToString(CultureInfo.InvariantCulture),"maxAmount",(60*scale).ToString(CultureInfo.InvariantCulture)));set.nodes.Add(mixed);
   foreach(string name in new[]{"Food","Water","Oxygen","Nitrogen","Ammonia","Waste","WasteWater"}){double capacity=520*scale*(name=="Oxygen"?200:name=="Nitrogen"?180:name=="Ammonia"?35:1);var c=Node("LOADOUT","name",name);c.nodes.Add(Node("RESOURCE","name",name,"amount",((name=="Waste"||name=="WasteWater")?0:capacity).ToString(CultureInfo.InvariantCulture),"maxAmount",capacity.ToString(CultureInfo.InvariantCulture)));set.nodes.Add(c);}GameDatabase.Instance.nodes.Add(set);
   var cargo=new Part();cargo.Resources.data["ElectricCharge"]=new PartResource{amount=77,maxAmount=100};var log=new ModuleRWLogisticsContents{part=cargo,profileSet=profile};log.OnStart(StartState.None);Check(cargo.Resources["Food"].amount==120*scale,"Default legacy supply");cargo.Resources["Food"].amount=30*scale;
   Select(log,"Food");Check(cargo.Resources["Water"]==null&&cargo.Resources["Food"].amount==130*scale,"Dedicated payload replaces others, preserving fill fraction");
   int events=GameEvents.onPartResourceListChange.calls;for(int i=0;i<100;i++)log.Update();Check(GameEvents.onPartResourceListChange.calls==events,"Idle avoids resource menu/event loop");
   foreach(string name in new[]{"Water","Oxygen","Nitrogen","Ammonia","Waste","WasteWater"}){Select(log,name);Check(cargo.Resources[name]!=null&&cargo.Resources["Food"]==null&&cargo.Resources["ElectricCharge"].amount==77,"Selection changes managed cargo only");if(name.StartsWith("Waste"))Check(cargo.Resources[name].amount==0,"Waste starts empty");}
   Select(log,"Food");cargo.Resources.data["Water"]=new PartResource();cargo.Resources["Food"].maxAmount=1;cargo.Resources["Food"].amount=.5;int modified=GameEvents.onEditorShipModified.calls;for(int i=0;i<30;i++)log.Update();Check(cargo.Resources["Water"]==null&&cargo.Resources["Food"].amount==260*scale&&GameEvents.onEditorShipModified.calls==modified,"External inventory reset repaired without repeated ship modification");
   var loaded=new ModuleRWLogisticsContents{part=cargo,profileSet=profile,contents="Food"};loaded.OnStart(StartState.None);Check(cargo.Resources["Food"].amount==260*scale,"Editor save/reload preserves partial fill");
   PartResourceLibrary.Instance.definitions.Remove("Ammonia");Select(loaded,"Ammonia");Check(cargo.Resources["Food"]!=null&&cargo.Resources["Ammonia"]==null,"Missing resource definition leaves existing loadout intact");PartResourceLibrary.Instance.definitions.Add("Ammonia");
   HighLogic.LoadedSceneIsEditor=false;HighLogic.LoadedSceneIsFlight=true;double amount=cargo.Resources["Food"].amount;var vessel=new ModuleRWLogisticsContents{part=cargo,profileSet=profile,contents="Mixed supplies"};vessel.OnStart(StartState.None);vessel.contents="Water";for(int i=0;i<100;i++)vessel.Update();Check(cargo.Resources["Food"].amount==amount&&cargo.Resources["Water"]==null,"Flight/old-vessel initialization never resizes, switches, refills or migrates");HighLogic.LoadedSceneIsEditor=true;HighLogic.LoadedSceneIsFlight=false;
  }
  var field=(KSPField)Attribute.GetCustomAttribute(typeof(ModuleRWLogisticsContents).GetField("contents"),typeof(KSPField));Check(field.isPersistant&&field.guiActiveEditor,"Persistent editor-only logistics choice");
  var symmetry=(UI_ChooseOption)Attribute.GetCustomAttribute(typeof(ModuleRWRingColor).GetField("ringColor"),typeof(UI_ChooseOption));Check(symmetry.affectSymCounterparts==UI_Scene.Editor,"Ring editor symmetry");Check(UnityEngine.Debug.errors==0,"No missing ring textures");
 }
}
'@
Add-Type -TypeDefinition ($source + "`n" + $doubles)
[CustomizationTest]::Run()
Write-Output 'PASS actual customization source: ring partition/colors/default/finish/renamed-root/editor copies/flight/cleanup; both LOG sizes, payload replacement, empty waste, partial fill, UI refresh, repair loops, missing definitions and no flight migration/refill'
