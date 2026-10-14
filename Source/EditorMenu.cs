using System;
using System.Reflection;
using System.Collections.Generic;
using UnityEngine;

// No B9 or Kerbalism assembly dependency. Existing persistent selections and
// native material controllers remain authoritative; optional B9 provides UI only.
public static class RWMenuApi
{
    public static object Read(object obj, string name)
    {
        if (obj == null) return null;
        var t = obj.GetType(); var f = t.GetField(name, BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance);
        if (f != null) return f.GetValue(obj);
        var p = t.GetProperty(name, BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance);
        return p == null ? null : p.GetValue(obj, null);
    }
    public static void Write(object obj, string name, object value)
    { obj.GetType().GetField(name, BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance).SetValue(obj, value); }
    public static PartModule Find(Part part, string type)
    { foreach (PartModule m in part.Modules) if (m.GetType().Name == type) return m; return null; }
}

public sealed class ModuleRWEditorMenu : PartModule
{
    private sealed class Swatch
    {
        public PartModule selector, target; public string field, last;
        public MethodInfo switchMethod; public PropertyInfo nameProperty;
        public bool Bind(Part part, string moduleID, string type, string member)
        {
            target = RWMenuApi.Find(part, type); field = member;
            if (target == null) return false;
            foreach (PartModule m in part.Modules)
                if (m.GetType().Name == "ModuleB9PartSwitch" && (string)RWMenuApi.Read(m,"moduleID") == moduleID) selector = m;
            if (selector == null) return false;
            switchMethod = selector.GetType().GetMethod("SwitchSubtype", new[] { typeof(string) });
            nameProperty = selector.GetType().GetProperty("CurrentSubtypeName");
            if (switchMethod == null || nameProperty == null) return false;
            // Recover pre-swatch craft choices, including editor copies. Never
            // reset the established White/Grey or ring persistence to B9 defaults.
            string saved = (string)RWMenuApi.Read(target, field);
            switchMethod.Invoke(selector, new object[] { saved.Replace(' ', '_') });
            last = (string)nameProperty.GetValue(selector, null);
            target.Fields[field].guiActiveEditor = false;
            if (selector.Fields["currentSubtypeIndex"].uiControlEditor != null)
                selector.Fields["currentSubtypeIndex"].uiControlEditor.onFieldChanged += Changed;
            return true;
        }
        private void Changed(BaseField f, object old) { Tick(); }
        public void Tick()
        {
            if (selector == null || nameProperty == null) return;
            string choice = (string)nameProperty.GetValue(selector, null);
            // PAW/model rebuilds can restore a target field without changing
            // B9's subtype name. Compare live state too; polling also survives
            // recreated UI controls replacing the initial callback delegate.
            if (!String.IsNullOrEmpty(choice))
            {
                string value = choice.Replace('_', ' ');
                if (choice != last || (string)RWMenuApi.Read(target, field) != value)
                    RWMenuApi.Write(target, field, value);
                last = choice;
            }
        }
    }
    private readonly Swatch finish = new Swatch(), rings = new Swatch();
    private bool ready;
    public void LateUpdate()
    {
        if (!HighLogic.LoadedSceneIsEditor || part == null) return;
        if (!ready)
        {
            ready = true;
            GroupControls();
            try { finish.Bind(part, "RWFinishSwatch", "ModuleRWStationFinish", "finish"); }
            catch (Exception e) { Debug.LogWarning("[RoosterWorks] Surface swatches unavailable: " + e.Message); }
            try { rings.Bind(part, "RWRingSwatch", "ModuleRWRingColor", "ringColor"); }
            catch (Exception e) { Debug.LogWarning("[RoosterWorks] Ring swatches unavailable: " + e.Message); }
        }
        finish.Tick(); rings.Tick();
    }
    private void GroupControls()
    {
        var appearance = new BasePAWGroup("RWAppearance", "Appearance", false);
        var lighting = new BasePAWGroup("RWLighting", "Lighting", true);
        var inventory = new BasePAWGroup("RWInventory", "Inventory", true);
        var payload = new BasePAWGroup("RWPayload", "Supply loadout", false);
        var hardware = new BasePAWGroup("RWHardware", "Hardware", false);
        foreach (PartModule m in part.Modules)
        {
            string type = m.GetType().Name;
            BasePAWGroup group = null;
            if (type == "ModuleRWStationFinish" || type == "ModuleRWRingColor") group = appearance;
            if (type == "ModulePartVariants") group = RWMenuApi.Find(part,"ModuleRWPowerVariant") != null ? hardware : appearance;
            if (type == "ModuleLight" || type == "ModuleColorChanger" || type == "ModuleRWLighting" || type.Contains("CabinLight")) group = lighting;
            if (type == "ModuleInventoryPart") group = inventory;
            if (type == "ModuleRWLogisticsContents") group = payload;
            if (group == null) continue;
            foreach (BaseField f in m.Fields) f.group = group;
            foreach (BaseEvent e in m.Events) e.group = group;
        }
        // Stock seat-inventory events live on Part rather than a PartModule.
        foreach (BaseEvent e in part.Events)
            if ((e.guiName ?? "").IndexOf("inventory", StringComparison.OrdinalIgnoreCase) >= 0) e.group = inventory;
    }
}

// Kerbalism's native editor drive controls retain their behaviour and mass/cost
// integration. Only rounded whole-slot choices need an adapter at 3.75 m.
public sealed class ModuleRWScienceTiers : PartModule
{
    [KSPField] public double volumeFactor = 1;
    [KSPField(isPersistant = true)] public int selectedSamples = -1;
    private PartModule drive; private bool ready;
    public static int Slots(double factor, int step)
    { return (int)Math.Round(10 * factor * step, MidpointRounding.AwayFromZero); }
    public void LateUpdate()
    {
        // Flight archives, stored files/samples, and drive persistence are untouched.
        if (!HighLogic.LoadedSceneIsEditor || part == null) return;
        if (!ready)
        {
            drive = RWMenuApi.Find(part, "HardDrive");
            if (drive == null) return;
            ready = true;
            try { Configure(); }
            catch (Exception e) { Debug.LogError("[RoosterWorks] Science tier initialization failed: " + e); }
        }
        if (drive != null) selectedSamples = (int)RWMenuApi.Read(drive, "effectiveSampleCapacity");
    }
    private void Configure()
    {
        // Ten independently selectable data and sample steps. A saved custom
        // whole-slot tier is restored after HardDrive's startup size validation.
        var capacities = new List<KeyValuePair<string, int>>();
        var labels = new string[10];
        int effective = selectedSamples > 0 ? selectedSamples : (int)RWMenuApi.Read(drive, "effectiveSampleCapacity");
        int best = 0, distance = Int32.MaxValue;
        for (int i = 1; i <= 10; i++)
        {
            int n = Slots(volumeFactor, i); string label = n + " slots";
            labels[i-1] = label; capacities.Add(new KeyValuePair<string,int>(label,n));
            int d = Math.Abs(effective - n); if (d < distance) { distance = d; best = i-1; }
        }
        RWMenuApi.Write(drive,"sampleCapacities",capacities);
        ((UI_ChooseOption)drive.Fields["sampleCapacityUI"].uiControlEditor).options = labels;
        RWMenuApi.Write(drive,"sampleCapacityUI",labels[best]);
        RWMenuApi.Write(drive,"effectiveSampleCapacity",capacities[best].Value);
        selectedSamples = capacities[best].Value;
    }
}
