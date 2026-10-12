using System;
using System.Collections;
using UnityEngine;

[assembly: System.Reflection.AssemblyVersion("0.4.6.0")]

// The native model remains authoritative for hatch geometry. Bind only the
// HAB's named, tagged trigger after Part.Awake and PartModule startup finish.
// No new collider, crew teleport, or bypass of KSP/Kerbalism EVA rules.
public sealed class ModuleRWStationHatch : PartModule
{
    private const string HatchName = "RW_HAB250_EVA_Airlock";

    private Collider hatchTrigger;
    private Collider ladderTrigger;
    private ModulePartVariants variants;
    private string appliedVariant;
    private bool ownsEvaLock;
    private bool previousEvaLock;

    public override void OnStart(StartState state)
    {
        base.OnStart(state);
        foreach (Collider candidate in part.GetComponentsInChildren<Collider>(true))
        {
            if (!candidate.isTrigger || candidate.gameObject.layer != 21) continue;
            if (candidate.name == HatchName && candidate.CompareTag("Airlock"))
                hatchTrigger = candidate;
            if (candidate.name == "RW_HAB250_EVA_Ladder" && candidate.CompareTag("Ladder"))
                ladderTrigger = candidate;
        }
        variants = part.FindModuleImplementing<ModulePartVariants>();
        ApplyAccess();
        StartCoroutine(CheckAfterStart());
    }

    public override void OnUpdate()
    {
        base.OnUpdate();
        // Also covers editor symmetry and restored variant selections.
        ApplyAccess();
    }

    private void ApplyAccess()
    {
        if (part == null) return;
        string selected = variants != null && variants.SelectedVariant != null
            ? variants.SelectedVariant.Name : "Standard";
        if (selected == appliedVariant) return;
        appliedVariant = selected;
        bool open = selected == "SideHatch" && hatchTrigger != null;
        if (hatchTrigger != null) hatchTrigger.enabled = open;
        if (ladderTrigger != null) ladderTrigger.enabled = open;
        if (open)
        {
            if (part.airlock == null || part.airlock.name == HatchName)
                part.airlock = hatchTrigger.transform;
        }
        else if (part.airlock != null && part.airlock.name == HatchName)
            part.airlock = null;

        // Portrait EVA checks NoAutoEVA, not airlock != null. Lock it as well
        // as disabling physical boarding. Only own this flag in flight, so
        // editor clones cannot carry a temporary lock into a hatch variant.
        // Preserve any pre-existing restriction instead of blindly clearing it.
        if (HighLogic.LoadedSceneIsFlight)
        {
            if (!open && !ownsEvaLock)
            {
                previousEvaLock = part.noAutoEVAAny;
                part.noAutoEVAAny = true;
                ownsEvaLock = true;
            }
            else if (open && ownsEvaLock)
            {
                part.noAutoEVAAny = previousEvaLock;
                ownsEvaLock = false;
            }
        }
        Debug.Log("[RWStation 0.4.6][Access] variant=" + selected
            + " hatch=" + open + " ladder=" + (ladderTrigger != null && ladderTrigger.enabled)
            + " noAutoEVA=" + part.NoAutoEVA);
    }

    private IEnumerator CheckAfterStart()
    {
        yield return null;
        appliedVariant = null;
        ApplyAccess();
        if (HighLogic.LoadedSceneIsFlight) BindAndReport("after-start");
        yield return new WaitForSeconds(5f);
        if (HighLogic.LoadedSceneIsFlight) BindAndReport("settled");
    }

    private void BindAndReport(string phase)
    {
        if (part == null) return;
        try
        {
            Collider hatch = null;
            foreach (Collider candidate in part.GetComponentsInChildren<Collider>(true))
            {
                if (candidate.name == HatchName && candidate.CompareTag("Airlock")
                    && candidate.isTrigger && candidate.gameObject.layer == 21)
                {
                    hatch = candidate;
                    break;
                }
            }
            string previous = part.airlock == null ? "null" : part.airlock.name;
            bool bound = false;
            if (hatch != null && hatch.enabled && hatch.gameObject.activeInHierarchy
                && part.airlock == null)
            {
                part.airlock = hatch.transform;
                bound = true;
            }
            Debug.Log("[RWStation 0.4.6][Hatch] phase=" + phase
                + " part=" + part.name + " flightID=" + part.flightID
                + " nativeTrigger=" + (hatch != null)
                + " active=" + (hatch != null && hatch.enabled && hatch.gameObject.activeInHierarchy)
                + " previousAirlock=" + previous + " bound=" + bound
                + " airlock=" + (part.airlock == null ? "null" : part.airlock.name)
                + " noAutoEVA=" + part.NoAutoEVA
                + " crew=" + part.protoModuleCrew.Count
                + " vesselType=" + (vessel == null ? "null" : vessel.vesselType.ToString()));
            if (vessel != null && GameVariables.Instance != null)
            {
                bool unlocked = GameVariables.Instance.UnlockedEVA(
                    ScenarioUpgradeableFacilities.GetFacilityLevel(SpaceCenterFacility.AstronautComplex));
                bool possible = GameVariables.Instance.EVAIsPossible(unlocked, vessel);
                foreach (ProtoCrewMember crew in part.protoModuleCrew)
                    Debug.Log("[RWStation 0.4.6][Crew] phase=" + phase
                        + " name=" + crew.name + " evaPossible=" + possible
                        + " type=" + crew.type + " inactive=" + crew.inactive
                        + " roster=" + crew.rosterStatus
                        + " lockedReason=" + (possible && !part.NoAutoEVA && !crew.inactive
                            && crew.type != ProtoCrewMember.KerbalType.Tourist ? "none"
                            : GameVariables.Instance.GetEVALockedReason(vessel, crew)));
            }
            if (part.airlock != null)
            {
                Vector3 direction = (part.airlock.position - part.transform.position).normalized;
                RaycastHit hit;
                bool blocked = Physics.Raycast(part.airlock.position - 0.5f * direction,
                    direction, out hit, part.hatchObstructionCheckOutwardDistance + 0.5f,
                    LayerUtil.DefaultEquivalent | (1 << 15) | (1 << 19) | (1 << 26),
                    QueryTriggerInteraction.Ignore);
                Debug.Log("[RWStation 0.4.6][Exit] phase=" + phase
                    + " blocked=" + FlightEVA.HatchIsObstructedMore(part, part.airlock)
                    + " outwardHit=" + (blocked ? hit.collider.name : "none"));
            }
            if (vessel != null && vessel.connection != null)
                Debug.Log("[RWStation 0.4.6][Comm] phase=" + phase
                    + " vesselType=" + vessel.vesselType
                    + " canComm=" + vessel.connection.CanComm
                    + " connected=" + vessel.connection.IsConnected
                    + " signal=" + vessel.connection.SignalStrength);
            else
                Debug.Log("[RWStation 0.4.6][Comm] phase=" + phase + " connection=null");
        }
        catch (Exception error)
        {
            Debug.LogError("[RWStation 0.4.6][Hatch] " + error);
        }
    }
}
