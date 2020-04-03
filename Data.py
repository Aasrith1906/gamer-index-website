




class User():

    def __init__(self , Name , userName , username_type , Game , data_dict):

        self.index = data_dict.getIndex()+1
        self.name = Name
        self.username = userName
        self.username_type = username_type
        self.game = Game
        self.data = data_dict
        self.data.AddUser(self)
    
    

class DataStorage():

    def __init__(self):

        self.dict = self.CreateDict()


    def CreateDict(self):

        return dict()

    def AddUser(self,user):

        self.dict[user.index] = user
    
    def getIndex(self):

        max_index = 0

        for user in self.dict.values():

            if user.index > max_index:

                max_index = user.index

        return max_index

    def getUser(self,name="",index=0):

        if name:

            for user in self.dict:

                if user.name == name:

                    return user
        
        elif index:

            for user in self.data:

                if user.index == index:

                    return user

        else:

            return None

    
    def CheckUsername(self , username,game):

        for user in self.dict.values():

            if user.username == username and user.game == game:

                return True

        return False


    def UpdateJSON(self):

        pass

    def CreateJSON(self):

        pass


class GameSort():

    def __init__(self,data_dict):

        self.game_dict = dict()
        self.data = data_dict

        self.__init_gameslist()

    def __init_gameslist(self):

        list_ = ['Destiny2' ,'Fortnite','Call Of Duty Warzone','PUBG' , 'Apex Legends','Clash Royale','Clash of Clans','Houseparty']

        for game in list_:

            self.game_dict[game] = 0

    def Count(self):

        for user in self.data.values():

            if user.game in self.game_dict.keys():

                self.game_dict[user.game]+=1

            else:

                self.game_dict[user.game] = 1
    
    def CheckGame(self , game):

        if game in self.game_dict.keys():

            self.game_dict[game]+=1

        else:

            self.game_dict[game]=1



    def GetList(self):

        self.Count()

        return self.game_dict.keys()