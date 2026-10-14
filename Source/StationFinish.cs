using System;
using UnityEngine;

// Independent of ModulePartVariants: HAB window/hatch choices retain their IDs.
// Only established outer-shell diffuse textures change; shaders, glass, logos,
// copper accents, emissive maps, colliders and gameplay are untouched.
public sealed class ModuleRWStationFinish : PartModule
{
    [KSPField(isPersistant = true, guiActiveEditor = true, guiName = "Exterior finish")]
    [UI_ChooseOption(options = new[] { "White", "Grey metal" }, affectSymCounterparts = UI_Scene.Editor)]
    public string finish = "White";
    private string applied;
    private static readonly string[] surfaces = { "cladding_white", "cladding", "ceramic", "white" };

    public override void OnStart(StartState state)
    {
        base.OnStart(state);
        var control = Fields["finish"].uiControlEditor;
        if (control != null)
        {
            control.onFieldChanged += OnFinishChanged;
            control.onSymmetryFieldChanged += OnFinishChanged;
        }
        if (HighLogic.LoadedSceneIsEditor || HighLogic.LoadedSceneIsFlight) ApplyFinish();
    }
    private void OnFinishChanged(BaseField field, object previousValue)
    {
        ApplyFinish();
    }
    // Unity Update runs in both scenes; PartModule.OnUpdate is flight-driven.
    // Also catches editor symmetry, loading and other scripts changing the field.
    public void Update()
    {
        if (finish != applied && (HighLogic.LoadedSceneIsEditor || HighLogic.LoadedSceneIsFlight)) ApplyFinish();
    }
    private void ApplyFinish()
    {
        if (part == null || GameDatabase.Instance == null) return;
        bool grey = finish == "Grey metal";
        int changed = 0;
        foreach (Renderer renderer in part.FindModelComponents<Renderer>())
        {
            foreach (Material material in renderer.materials)
            {
                string name = material.name.Replace(" (Instance)", "");
                string textureName = material.mainTexture == null ? "" : material.mainTexture.name.Replace(" (Instance)", "");
                foreach (string surface in surfaces)
                {
                    // KSP/visual mods can rename materials. Native texture names
                    // are a fallback without recolouring glass, badges or lamps.
                    if (!name.EndsWith("_" + surface, StringComparison.Ordinal)
                        && textureName != "rwm_" + surface && textureName != "rwm_" + surface + "_grey"
                        && !textureName.EndsWith("/rwm_" + surface, StringComparison.Ordinal)
                        && !textureName.EndsWith("/rwm_" + surface + "_grey", StringComparison.Ordinal)) continue;
                    string path = "RoosterWorksStationModules/Models/rwm_" + surface + (grey ? "_grey" : "");
                    Texture texture = GameDatabase.Instance.GetTexture(path, false);
                    if (texture != null) { material.mainTexture = texture; changed++; }
                    else Debug.LogError("[RoosterWorks] Missing finish texture: " + path);
                    break;
                }
            }
        }
        applied = finish;
        Debug.Log("[RoosterWorks] Exterior finish " + finish + ": " + changed + " shell materials updated.");
    }
    public override string GetInfo() { return "Optional white or grey metal exterior. Choose the finish in the editor."; }
}
