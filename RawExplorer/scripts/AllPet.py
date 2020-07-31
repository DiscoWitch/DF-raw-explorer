from . import ScriptButton


class AllPet(ScriptButton):
    def __init__(self, **kwargs):
        super(AllPet, self).__init__(**kwargs)
        self.text = "Make all creatures pets"

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
            if obj.has_token(["PET", "PET_EXOTIC", "COPY_TAGS_FROM", "EQUIPMENT_WAGON", "DOES_NOT_EXIST"]):
                return False
            return True

        pets = self.app.raws.filter(
            pred_file=lambda f: f.maintype == "CREATURE",
            pred_obj=pet_filt)

        for f in pets.files.values():
            for c in f.objects:
                if c in civilized:
                    continue
                print(c)
                f.objects[c].add_token(["PET_EXOTIC"], 8)
        return super().on_press()
