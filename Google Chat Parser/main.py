from pathlib import Path
import os
import shutil

def loadSettings():
    try:
        with open("settings.txt", "r") as f:
            lst = f.readlines()
        settings = {}
        if lst[1].strip() == "True":
            settings["newline sc"] = True
        else:
            settings["newline sc"] = False
        settings["output"] = lst[3].strip()
    except:
        settings = {"newline sc": True}
    return settings

def getMainPathNew():
    curDir = os.getcwd()
    curP = Path(curDir)
    curDirCont = [x for x in curP.iterdir()]
    return curDirCont

def getGroupsFolder():
    curDirCont = getMainPathNew()
    groupsPathInd = findPath(curDirCont, "Groups")
    p = Path(curDirCont[groupsPathInd])
    grpsPaths = [x for x in p.iterdir() if x.is_dir()]
    grps = []
    for i in range(len(grpsPaths)):
        grps.append([Path(grpsPaths[i])])
        grps[i].append([x for x in grps[i][0].iterdir()])
    return grps

def setupMainPath():
    top = Path('.')
    topCont = [x for x in top.iterdir() if x.is_dir()]
    p = Path(topCont[0])
    grpsPaths = [x for x in p.iterdir() if x.is_dir()]
    grps = []
    for i in range(len(grpsPaths)):
        grps.append([Path(grpsPaths[i])])
        grps[i].append([x for x in grps[i][0].iterdir()])
    return grps

def findPath(dir: list, name: str):
    for i in range(len(dir)):
        if name in str(dir[i]):
            return i
    else:
        return None

def findGroupInfo(p:Path):
    dirLst = [x for x in p.iterdir()]
    for path in dirLst:
        if "group_info.json" in str(path):
            return path
    return None

def identifyUsers(jsonFile):
    if jsonFile == None:
        return False
    with open(jsonFile, "r") as f:
        lst = [f.readlines()]
    mems = []
    for val in lst[0]:
        if "name" in val:
            mems.append(val)
    #clean up strings
    for i in range(len(mems)):
        mems[i] = mems[i].split(':')[1].strip(' "\n')
        mems[i] = mems[i].strip("'")
        mems[i] = mems[i].strip(',"')
    return(mems)



def getNewFileName(userName: str, users: list):
    newName = ""
    for val in users:
        if (userName in val) and len(users) > 1:
            pass
        else:
            if newName == "":
                newName = val
            else:
                newName = newName + ", " + val
    if newName == "":
        newName = userName
    return newName

def renameFolder(path:Path, newName):
    try:
        os.rename(path, newName)
    except OSError as error:
        pass
        #print(f"error: {error}")

def renameChatsFolders(userName: str):
    grps = getGroupsFolder()
    info = []
    for val in grps:
        grpInfoPath = findGroupInfo(val[0])
        users = identifyUsers(grpInfoPath)
        info.append([val[0], grpInfoPath, users])
    for val in info:
        if val[1] != None:
            renameFolder(val[0], getNewFileName(userName, val[2]))



def moveFoldersToGroups():
    curDir = os.getcwd()
    excludes = ["takeout", "notes.txt", "main.py", "test.txt", "test.py", "settings.txt"]
    p = Path(curDir)
    pcontents = [x for x in p.iterdir()]
    i = 0
    while i <= len(pcontents) - 1:
        check = False
        for l in range(len(excludes)):
            if excludes[l] in str(pcontents[i]):
                pcontents.pop(i)
                check = True
                break
        if check == False:
            i += 1
    for val in pcontents:
        try:
            dest = str(curDir) + '\\Groups'
            shutil.move(val, dest)
        except:
            pass

def getDirContents(path: str):
    return [x for x in path.iterdir()]

def scrapeMessages(path: str, users: list, userName: str):
    with open(path, "r", errors="ignore") as f:
        lst = f.readlines()
    #look through text, connecting person to a text
    messages = []
    i = 0
    personFound = False
    while i < len(lst) -1:
        if '"name":' in lst[i]:
            if "Deleted User" in lst[i]:
                offset = 4
            if "quoted_message_metadata" in str(lst[i-2]):
                pass
            else:
                #clean up the text
                person = lst[i].split(":", maxsplit=1)[1]
                person = person.strip(' ",\n')
                offset = 5
                try:
                    txtmsg = [person, lst[i+offset].split(":", maxsplit=1)[1].strip('"\n,').strip(' "')]
                    if txtmsg[1] == "114930099899118428868":
                        txtmsg[1] = f"*google meet initiated by {txtmsg[0]}*"
                    if "\\u0027" in txtmsg[1]:
                        txtmsg[1] = txtmsg[1].replace("\\u0027", "'")
                    if "\\n" in txtmsg[1] and settings["newline sc"] == True:
                        txtmsg[1] = txtmsg[1].replace("\\n", "\n")
                    elif txtmsg[1] == "[":
                        txtmsg[1] = lst[i+offset+2].split(":", maxsplit=1)[1].strip('"\n,').strip(' "')
                    elif txtmsg[1].strip() == "{":
                        print("hit")
                        txtmsg[1] = lst[i+offset+1].split(":", maxsplit=1)[1].strip('"\n').strip(' "')
                    messages.append(txtmsg)
                except:
                    print(path)
                    print(txtmsg[1].strip())
                    print(lst[i+offset-1], i)
                    
            i+=9
        i+=1

    if settings["output"] == "one":
        curDir = os.getcwd()
        dest = curDir + "/Output/" + ""
        with open() as f:
            pass
    if settings["output"] == "home":
        f = list(str(path))[:-13]
        newstr = str()
        for val in f:
            newstr += val
        outputPath = newstr + "output.txt"
        with open(outputPath, "w") as f:
            for val in messages:
                f.write(f"{val[0]}: {val[1]}\n")



settings = loadSettings()
userName = input("please input your google user name: ")
renameChatsFolders(userName)
moveFoldersToGroups()
grps = getGroupsFolder()
for val in grps:
    messagesInd = findPath(val[1], "messages.json")
    grpInfoPath = findGroupInfo(val[0])
    users = identifyUsers(grpInfoPath)
    scrapeMessages(val[1][messagesInd], users, userName)
moveFoldersToGroups()