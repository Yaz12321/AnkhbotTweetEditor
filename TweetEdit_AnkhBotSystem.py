#---------------------------------------
#	Import Libraries
#---------------------------------------
import clr, sys, json, os, codecs
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")
import time

#---------------------------------------
#	[Required]	Script Information
#---------------------------------------
ScriptName = "tweet"
Website = "https://www.AnkhBot.com"
Creator = "Yaz12321"
Version = "1.0"
Description = "Send Tweet messages "

settingsFile = os.path.join(os.path.dirname(__file__), "settings.json")

#---------------------------------------
#   Version Information
#---------------------------------------

# Version:
# > 1.1.0.1 <
    # fixed cost setting
    # removed enable/disable button in config

# > 1.1.0.0 <
    # Cleaned up code
    # fixed missing permission check
    # added "only live mode"

# > 1.0.1.0 < 
    # Cleaned up code 
    # fixed missing info in textboxes 

# > 1.0.0.0 < 
    # Official Release

class Settings:
    # Tries to load settings from file if given 
    # The 'default' variable names need to match UI_Config
    def __init__(self, settingsFile = None):
        if settingsFile is not None and os.path.isfile(settingsFile):
            with codecs.open(settingsFile, encoding='utf-8-sig',mode='r') as f:
                self.__dict__ = json.load(f, encoding='utf-8-sig') 
        else: #set variables if no settings file
            self.OnlyLive = False
            self.Command = "!tweet"
            self.EndCommand = "!edittweet"
            self.Permission = "Caster"
            self.PermissionInfo = ""
            self.UseCD = True
            self.Cooldown = 0
            self.OnCooldown = "{0} the command is still on cooldown for {1} seconds!"
            self.UserCooldown = 10
            self.OnUserCooldown = "{0} the command is still on user cooldown for {1} seconds!"
            self.TweetMessage = "You can help the stream by retweeting/liking the tweet saying we went live! Every multiple of 10 RTs gives 25 Coins to the rest of the stream! || "
            self.timer = 600
            
            
    # Reload settings on save through UI
    def ReloadSettings(self, data):
        self.__dict__ = json.loads(data, encoding='utf-8-sig')
        return

    # Save settings to files (json and js)
    def SaveSettings(self, settingsFile):
        with codecs.open(settingsFile,  encoding='utf-8-sig',mode='w+') as f:
            json.dump(self.__dict__, f, encoding='utf-8-sig')
        with codecs.open(settingsFile.replace("json", "js"), encoding='utf-8-sig',mode='w+') as f:
            f.write("var settings = {0};".format(json.dumps(self.__dict__, encoding='utf-8-sig')))
        return


#---------------------------------------
# Initialize Data on Load
#---------------------------------------
def Init():
    # Globals
    global MySettings

    # Load in saved settings
    MySettings = Settings(settingsFile)
    global t
    t = time.time()

    # End of Init
    return

#---------------------------------------
# Reload Settings on Save
#---------------------------------------
def ReloadSettings(jsonData):
    # Globals
    global MySettings

    # Reload saved settings
    MySettings.ReloadSettings(jsonData)

    # End of ReloadSettings
    return

def sendtweet():
    path = os.path.dirname(os.path.abspath(__file__))
    f = open("{}/tweeturl.txt".format(path),"r+")
    tweetlink = f.read()
    f.close()
    Parent.SendTwitchMessage("{} {}".format(MySettings.TweetMessage,tweetlink))
    global t
    t = time.time()
    return

def Execute(data):
    if data.IsChatMessage() and data.GetParam(0).lower() == MySettings.EditCommand:
        if Parent.HasPermission(data.User, MySettings.Permission, MySettings.PermissionInfo):
            tweeturl1 = data.Message
            tweeturl = tweeturl1.replace(MySettings.EditCommand,"")
            path = os.path.dirname(os.path.abspath(__file__))
            f = open("{}/tweeturl.txt".format(path),"w+")
            f.write(tweeturl)
            f.close()
            Parent.SendTwitchMessage("Tweet link has been updated")
        

    
    if data.IsChatMessage() and data.GetParam(0).lower() == MySettings.Command:
        
       

        
        #check if user has permission
        if True:
            
            #check if command is on cooldown
            if Parent.IsOnCooldown(ScriptName,MySettings.Command) or Parent.IsOnUserCooldown(ScriptName,MySettings.Command,data.User):
               
                #check if cooldown message is enabled
                if MySettings.UseCD: 
                    
                    #set variables for cooldown
                    cooldownDuration = Parent.GetCooldownDuration(ScriptName,MySettings.Command)
                    usercooldownDuration = Parent.GetUserCooldownDuration(ScriptName,MySettings.Command,data.User)
                    
                    #check for the longest CD!
                    if cooldownDuration > usercooldownDuration:
                    
                        #set cd remaining
                        m_CooldownRemaining = cooldownDuration
                        
                        #send cooldown message
                        Parent.SendTwitchMessage(MySettings.OnCooldown.format(data.User,m_CooldownRemaining))
                        
                        
                    else: #set cd remaining
                        m_CooldownRemaining = Parent.GetUserCooldownDuration(ScriptName,MySettings.Command,data.User)
                        
                        #send usercooldown message
                        Parent.SendTwitchMessage(MySettings.OnUserCooldown.format(data.User,m_CooldownRemaining))
            
            else:
                sendtweet()

                
                

    return

def Tick():
    
    if time.time() > t + MySettings.timer and Parent.IsLive():
        if MySettings.timer != 0:
            sendtweet()
    
    return

def UpdateSettings():
    with open(m_ConfigFile) as ConfigFile:
        MySettings.__dict__ = json.load(ConfigFile)
    return
