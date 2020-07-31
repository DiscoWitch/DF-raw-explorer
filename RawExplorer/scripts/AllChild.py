from . import ScriptButton


class AllChild(ScriptButton):
    def __init__(self, **kwargs):
        super(AllChild, self).__init__(**kwargs)
        self.text = "Give all creatures child forms"

    def on_press(self):
        entities = self.app.raws.filter(
            pred_file=lambda f: f.maintype == "ENTITY")

        civilized = []
        for f in entities.files.values():
            for civ in f.objects.values():
                if civ.get_token("ALL_MAIN_POPS_CONTROLLABLE"):
                    creatures = civ.get_tokens("CREATURE")
                    for c in creatures:
                        civilized.append(c[1])

        def pet_filt(obj):
            if obj.has_token(["CHILD", "COPY_TAGS_FROM", "EQUIPMENT_WAGON", "DOES_NOT_EXIST"]):
                return False
            return True

        pets = self.app.raws.filter(
            pred_file=lambda f: f.maintype == "CREATURE",
            pred_obj=pet_filt)

        for kf in pets.files:
            print(kf)
            f = pets.files[kf]
            for c in f.objects:
                if c in civilized:
                    continue
                print(c)
                maxage = f.objects[c].get_token("MAXAGE")
                if maxage is None:
                    f.objects[c].add_token(["CHILD", "10"], 8)
                else:
                    childage = int(maxage[1])//5
                    if childage == 0:
                        childage = 1
                    if childage > 10:
                        childage = 10
                    f.objects[c].add_token(["CHILD", str(childage)], 8)
        return super().on_press()
