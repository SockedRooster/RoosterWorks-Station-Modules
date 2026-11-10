using System.Collections.Generic;

// Stock FlagDecal owns mission artwork and saves the visibility of each renderer.
public sealed class ModuleRWStationFlags : PartModule
{
    private readonly List<FlagDecal> decals = new List<FlagDecal>();

    public override void OnStartFinished(StartState state)
    {
        base.OnStartFinished(state);
        decals.Clear();
        foreach (PartModule module in part.Modules)
        {
            FlagDecal decal = module as FlagDecal;
            if (decal == null) continue;
            decals.Add(decal);
            decal.Events["ToggleFlag"].active = false;
        }
        UpdateLabel();
    }

    [KSPEvent(guiActive = true, guiActiveEditor = true, guiName = "Hide mission flag")]
    public void ToggleMissionFlag()
    {
        if (decals.Count == 0) return;
        bool show = !decals[0].flagDisplayed;
        foreach (FlagDecal decal in decals)
        {
            decal.flagDisplayed = show;
            decal.UpdateDisplay();
        }
        UpdateLabel();
    }

    private void UpdateLabel()
    {
        BaseEvent toggle = Events["ToggleMissionFlag"];
        toggle.active = decals.Count > 0;
        if (toggle.active)
            toggle.guiName = decals[0].flagDisplayed ? "Hide mission flag" : "Show mission flag";
    }
}
