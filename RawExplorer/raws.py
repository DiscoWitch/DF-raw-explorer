import json
import os
import re


from kivy.event import EventDispatcher
import kivy.properties as kpt

from RawExplorer.spec import specdir


class RawCollection(EventDispatcher):
    path = kpt.StringProperty()
    files = kpt.DictProperty()
    spec = kpt.DictProperty()

    def __init__(self, read_now=True, **kwargs):
        super(RawCollection, self).__init__(**kwargs)
        if read_now:
            self.load_spec()
            self.load_raws()

    def load_spec(self):
        self.spec = {}
        with open(specdir+"/obj_subtypes.json", 'r') as f:
            self.spec["subtypes"] = json.load(f)

    def load_raws(self):
        self.files = {}
        if self.path is None:
            return
        objpath = '{}/objects'.format(self.path)
        filenames = os.listdir(objpath)
        for name in filenames:
            # Only try to open regular files
            if not os.path.isfile("{}/{}".format(objpath, name)):
                continue
            rd = RawFile(path="{}/{}".format(objpath, name), collection=self)
            if rd.maintype != '':
                self.files[name] = rd

    def save_raws(self):
        pass

    def filter(self, pred_file=None, pred_obj=None):
        output = RawCollection(path=self.path, spec=self.spec, read_now=False)
        for kf in self.files:
            f = self.files[kf]
            if pred_file is not None and not pred_file(f):
                continue
            fcopy = RawFile(path=f.path, maintype=f.maintype,
                            collection=f.collection, read_now=False)

            for kobj in f.objects:
                obj = f.objects[kobj]
                if pred_obj is not None and not pred_obj(obj):
                    continue
                fcopy.objects[kobj] = obj
            if fcopy.objects:
                output.files[kf] = fcopy
        return output

    def get_object(self, ttype, name):
        for f in self.files.values():
            if ttype not in f:
                continue
            if name in f[ttype]:
                return RawObject(data=f[ttype][name])
        return None


class RawFile(EventDispatcher):
    path = kpt.StringProperty()
    collection = kpt.ObjectProperty()
    maintype = kpt.StringProperty()
    objects = kpt.DictProperty()

    def __init__(self, read_now=True, **kwargs):
        super(RawFile, self).__init__(**kwargs)
        if read_now:
            self.read_raw(self.path)

    def read_raw(self, path):
        data = {}
        cur_item = None
        # cp850 was chosen because it seems to load language files without crashing
        with open(path, 'r', encoding='cp850') as f:
            text = f.read()
            filetype = re.search(r"\[OBJECT:([^\[\]]+)\]", text)
            if not filetype:
                return None
            self.maintype = filetype[1]
            if self.maintype not in self.collection.spec["subtypes"]:
                self.collection.spec["subtypes"][self.maintype] = self.maintype
            # Clip anything before the object type declaration
            text = text[filetype.end(0):]
            groups = re.findall(r"\[([^\[\]]+)\]", text)
            for group in groups:
                tokens = group.split(':')
                if tokens[0] in self.collection.spec["subtypes"][self.maintype]:
                    cur_item = tokens[1]
                    self.objects[cur_item] = RawObject(
                        maintype=self.maintype, subtype=tokens[0])
                    continue
                self.objects[cur_item].tokens.append(tokens)


class RawObject(EventDispatcher):
    maintype = kpt.StringProperty()
    subtype = kpt.StringProperty()
    tokens = kpt.ListProperty()

    def __init__(self, **kwargs):
        super(RawObject, self).__init__(**kwargs)

    def add_token(self, token, index):
        self.tokens.insert(index, token)

    def get_token_index(self, token):
        if type(token) is str:
            for i in range(len(self.tokens)):
                if self.tokens[i][0] == token:
                    return i
        if type(token) is list:
            for i in range(len(self.tokens)):
                if self.tokens[i][0] in token:
                    return i
        return None

    def get_token(self, token):
        ind = self.get_token_index(token)
        if ind is None:
            return None
        else:
            return self.tokens[ind]

    def has_token(self, token):
        return self.get_token_index(token) is not None

    def get_tokens_indices(self, token):
        output = []
        if type(token) is str:
            for i in range(len(self.tokens)):
                if self.tokens[i][0] == token:
                    output.append(i)
        if type(token) is list:
            for i in range(len(self.tokens)):
                if self.tokens[i][0] in token:
                    output.append(i)
        return output

    def get_tokens(self, token):
        inds = self.get_tokens_indices(token)
        return [self.tokens[i] for i in inds]
