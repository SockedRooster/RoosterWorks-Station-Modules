using System;
using System.Collections.Generic;
using UnityEngine;

public sealed class ModuleRWStationWiring : PartModule
{
    [KSPField(isPersistant = true)] public bool mirrored = false;
    [KSPField] public string elbowModel = "";
    [KSPField] public bool hub = false;

    private readonly List<MeshFilter> routes = new List<MeshFilter>();
    private Dictionary<string, Mesh> originalElbow;
    private Dictionary<string, Mesh> mirroredElbow;

    public override void OnStartFinished(StartState state)
    {
        base.OnStartFinished(state);
        routes.Clear();
        foreach (MeshFilter filter in part.FindModelComponents<MeshFilter>())
        {
            string name = filter.transform.name;
            if ((name.StartsWith("RW_04_Stack_", StringComparison.Ordinal) ||
                 name.StartsWith("RW_05_", StringComparison.Ordinal)) &&
                (name.Contains("_service_blue") || name.Contains("_service_yellow")))
                routes.Add(filter);
        }
        if (elbowModel.Length > 0)
        {
            originalElbow = ReadMeshes(elbowModel);
            mirroredElbow = ReadMeshes(elbowModel + "_MirroredWiring");
            foreach (MeshFilter route in routes)
                if (!originalElbow.ContainsKey(route.transform.name) || !mirroredElbow.ContainsKey(route.transform.name))
                {
                    Debug.LogError("[RoosterWorks] Missing elbow wire mesh on " + elbowModel);
                    routes.Clear();
                    break;
                }
        }
        ApplyOrientation();
    }

    private static Dictionary<string, Mesh> ReadMeshes(string url)
    {
        var meshes = new Dictionary<string, Mesh>();
        GameObject prefab = GameDatabase.Instance.GetModelPrefab(url);
        if (prefab != null)
            foreach (MeshFilter mf in prefab.GetComponentsInChildren<MeshFilter>(true))
                meshes[mf.transform.name] = mf.sharedMesh;
        return meshes;
    }

    [KSPEvent(guiActiveEditor = true, guiActive = true, guiName = "Mirror wiring")]
    public void ToggleWiring()
    {
        mirrored = !mirrored;
        ApplyOrientation();
    }

    private void ApplyOrientation()
    {
        foreach (MeshFilter route in routes)
        {
            Transform t = route.transform;
            if (elbowModel.Length > 0)
                route.sharedMesh = (mirrored ? mirroredElbow : originalElbow)[t.name];
            else if (hub)
                t.localScale = new Vector3(mirrored ? -1f : 1f, 1f, 1f);
            else
            {
                float offset = t.name.Contains("_service_blue") ? 0.065f : 0.092f;
                t.localRotation = Quaternion.AngleAxis(mirrored ? -2f * offset * Mathf.Rad2Deg : 0f, Vector3.up);
            }
        }
        BaseEvent control = Events["ToggleWiring"];
        control.active = routes.Count > 0;
        control.guiName = mirrored ? "Restore standard wiring" : "Mirror wiring";
    }
}
