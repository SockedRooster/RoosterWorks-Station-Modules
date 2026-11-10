using System;
using UnityEngine;

// Cosmetic rotor on one fixed KSP part. No forces, joints or attached parts
// rotate. Equivalent acceleration is informational, not applied game gravity.
public sealed class ModuleRWGravityRing : PartModule
{
    [KSPField(isPersistant=true)] public float deployment,targetDeployment,phase,actualRpm;
    [KSPField(isPersistant=true)] public bool running;
    [KSPField] public float deployDuration=30f,powerRate=.75f;
    [KSPField(isPersistant=true,guiActive=true,guiActiveEditor=true,guiName="Ring speed")]
    [UI_FloatRange(minValue=1f,maxValue=8f,stepIncrement=.5f)] public float rpm=6f;
    [KSPField(guiActive=true,guiActiveEditor=true,guiName="Gravity ring")] public string status="Stowed";
    [KSPField(guiActive=true,guiActiveEditor=true,guiName="Equivalent acceleration")] public string acceleration="0.00 g (visual only)";
    private Transform rotor;
    private readonly Transform[] hinges=new Transform[8],pods=new Transform[8],spokes=new Transform[8];
    private string warning;
    public override void OnLoad(ConfigNode n){base.OnLoad(n);Bind();Pose();}
    public override void OnStart(StartState s){base.OnStart(s);Bind();Pose();}
    private void Bind()
    {
        if(part==null)return;rotor=part.FindModelTransform("RW_GravityRotor");
        for(int i=0;i<8;i++){hinges[i]=part.FindModelTransform("RW_GravityHinge"+i.ToString("00"));pods[i]=part.FindModelTransform("RW_GravityPod"+i.ToString("00"));spokes[i]=part.FindModelTransform("RW_GravityTelescopic"+i.ToString("00"));}
    }
    private bool Orbit()
    {
        if(HighLogic.LoadedSceneIsEditor)return true;
        return vessel!=null&&(vessel.situation==Vessel.Situations.ORBITING||vessel.situation==Vessel.Situations.SUB_ORBITAL||vessel.situation==Vessel.Situations.ESCAPING);
    }
    private bool Crewed(){return part!=null&&part.protoModuleCrew.Count>0;}
    [KSPEvent(guiActive=true,guiActiveEditor=true,guiName="Deploy Gravity Ring")]
    public void Deploy(){if(!Orbit()){warning="Deploy after reaching space";Pose();return;}warning=null;targetDeployment=1;}
    [KSPEvent(guiActive=true,guiActiveEditor=true,guiName="Fold Gravity Ring")]
    public void Fold()
    {
        if(Crewed()){warning="Transfer crew out before folding";Pose();return;}
        if(running||actualRpm>.01f){warning="Stop the rotor before folding";Pose();return;}
        if(!Orbit()){warning="Fold in space or the editor";Pose();return;}
        warning=null;targetDeployment=0;
    }
    [KSPEvent(guiActive=true,guiActiveEditor=true,guiName="Start Ring Rotation")]
    public void StartRing(){if(deployment<.9999f||targetDeployment<1){warning="Fully deploy before starting rotation";Pose();return;}if(!Orbit()){warning="Start rotation in space";Pose();return;}warning=null;running=true;}
    [KSPEvent(guiActive=true,guiActiveEditor=true,guiName="Stop Ring Rotation")]
    public void StopRing(){warning=null;running=false;}
    [KSPAction("Deploy gravity ring")]public void DeployAction(KSPActionParam p){Deploy();}
    [KSPAction("Fold gravity ring")]public void FoldAction(KSPActionParam p){Fold();}
    [KSPAction("Start ring rotation")]public void StartAction(KSPActionParam p){StartRing();}
    [KSPAction("Stop ring rotation")]public void StopAction(KSPActionParam p){StopRing();}
    public void Update(){if(rotor==null)Bind();if(HighLogic.LoadedSceneIsEditor)Step(Time.deltaTime);}
    public void FixedUpdate()
    {
        if(!HighLogic.LoadedSceneIsFlight||vessel==null||!vessel.loaded||vessel.packed||TimeWarp.CurrentRateIndex!=0)return;
        Step(Time.fixedDeltaTime);
    }
    private static float Safe(float v,float fallback){return float.IsNaN(v)||float.IsInfinity(v)?fallback:v;}
    private void Normalize()
    {
        deployment=Mathf.Clamp01(Safe(deployment,0));targetDeployment=Mathf.Clamp01(Safe(targetDeployment,deployment));
        rpm=Mathf.Clamp(Safe(rpm,6),1,8);actualRpm=Mathf.Clamp(Safe(actualRpm,0),0,8);phase=Safe(phase,0)%360;
        if(phase<0)phase+=360;
        if(deployment<.9999f){running=false;actualRpm=0;}
    }
    private bool Power(float rate,float dt)
    {
        if(HighLogic.LoadedSceneIsEditor)return true;
        double requested=Math.Max(0,rate)*dt;if(requested<=0)return true;
        return part.RequestResource("ElectricCharge",requested)>=requested*.98;
    }
    private void Step(float dt)
    {
        if(part==null||rotor==null)return;Normalize();dt=Mathf.Clamp(Safe(dt,0),0,.1f);
        if(!Orbit()){running=false;actualRpm=0;Pose();return;}
        if(targetDeployment<deployment&&Crewed()){targetDeployment=deployment;warning="Transfer crew out before folding";}
        if(deployment!=targetDeployment)
        {
            running=false;
            if(actualRpm>.01f){warning="Stop the rotor before folding";Pose();return;}
            if(!Power(.25f,dt)){warning="Deployment paused: low electric charge";Pose();return;}
            warning=null;deployment=Mathf.MoveTowards(deployment,targetDeployment,dt/Mathf.Max(1,Safe(deployDuration,30)));
        }
        float target=running&&deployment>=.9999f?rpm:0;
        if((target>0||actualRpm>.01f)&&!Power(Mathf.Max(0,Safe(powerRate,.75f)),dt)){target=0;warning="Low electric charge: rotor coasting down";}
        else if(warning=="Low electric charge: rotor coasting down")warning=null;
        actualRpm=Mathf.MoveTowards(actualRpm,target,dt*.8f);phase=(phase+actualRpm*6*dt)%360;
        Pose();
    }
    private static float Smooth(float t){t=Mathf.Clamp01(t);return t*t*(3-2*t);}
    private void Pose()
    {
        Normalize();if(rotor==null)return;
        rotor.localRotation=Quaternion.Euler(0,phase,0);
        float arm=1-Smooth(deployment/.65f);
        float reach=Smooth(deployment/.55f),inflate=Smooth((deployment-.55f)/.45f);
        float length=.95f+1.8f*reach,root=1.72f-.27f*reach;
        for(int i=0;i<8;i++)
        {
            float folded=i==0||i==4?82:88;
            float angle=(i%2==0?folded:-folded)*arm;
            if(hinges[i]!=null){hinges[i].localRotation=Quaternion.Euler(0,0,angle);hinges[i].localPosition=new Vector3(root,0,0);}
            if(spokes[i]!=null)spokes[i].localScale=new Vector3(length/2.75f,1,1);
            if(pods[i]!=null){pods[i].localPosition=new Vector3(length,0,0);pods[i].localRotation=Quaternion.Euler(0,0,-angle);pods[i].localScale=new Vector3(.5f+.5f*inflate,.85f+.15f*inflate,.7f+.3f*inflate);}
        }
        double omega=actualRpm*Math.PI/30;acceleration=(omega*omega*4.2/9.80665).ToString("0.00",System.Globalization.CultureInfo.InvariantCulture)+" g (visual only)";
        status=warning??(deployment<.0001f?"Stowed":deployment<.9999f?(targetDeployment>deployment?"Unfolding / inflating":targetDeployment<deployment?"Deflating / folding":"Holding deployment"):actualRpm>.01f?(running?"Rotating":"Coasting to stop"):"Deployed / stopped");
    }
    public override string GetInfo(){return "Fixed 2.5 m hub; 9.84 m deployed ring. Four crew. Fold only when empty and stopped. 0.25 EC/s deploying; 0.75 EC/s rotating, loaded realtime only. Equivalent g is informational; no physical artificial gravity. Conservative Kerbalism support counts the fixed hub only.";}
}
