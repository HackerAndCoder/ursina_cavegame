class NBT:
    def __init__(self, nbt_data = {}):
        self.data = nbt_data
    
    def set_tag(self, tag, data):
        self.data[tag] = data
    
    def remove_tag(self, tag):
        try:
            del self.data[tag]
        except:
            pass
    
    def get(self, tag):
        try:
            return self.data[tag]
        except:
            return None
    
    def get_safe(self, tag, default):
        try:
            return self.data[tag]
        except:
            return default