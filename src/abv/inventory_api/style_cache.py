class StyleCache:

    def __init__(self,filename):
        self.filename = filename
        self.cache_dict = {}

    def look_up(self,beer_name):
        if beer_name in self.cache_dict:
            return str(self.cache_dict[beer_name])
        return None

    def add(self, beer, style):
        self.cache_dict[beer] = style
        with open(self.filename,"a") as myfile:
            myfile.write(beer + ',' + style)
