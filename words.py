from random import randint
acceptable_letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
nums = [4, 5, 6, 7, 8, 9, 10, 11, 12]
linesnum = {num : [] for num in nums}

getmostletters = 0.7
usemostletters = 0.7


def read(sheet):
    lines = []
    with open(sheet, "r") as f:
        lines = f.readlines()
    return lines

def readcsv(sheet):
    lines = read(sheet)
    a = []
    cont = False
    for line in lines:
        line = line[line.find(";")+1:]
        line = line[:line.find(";")]
        
        if cont or line == "the":
            cont = True
            a.append(line)
    return a

def parse(lines):
    acc = []
    for item in lines:
        thisword = True
        for i in item.strip():
            if i.lower() not in acceptable_letters:
                thisword = False
                break
            
        if thisword:
            acc.append(item)
            
    return acc

def split(item):
    return [i for i in item]


def remainder(item):
    let = set({})
    remain = set({})
    alllet = set(acceptable_letters)

    for word in item:
        let = let | set(split(word))
    remain = alllet - let
    if len(remain) == 0:
        return ""
    
    return remain

def remove(word):
    lines = read("AllWords.txt")
    found = ""
    
    for item in lines:
        if word.lower().strip() == item.lower().strip():
            found = item
            break
        
    if found != "":
        lines.remove(found)
        with open("AllWords.txt", "w") as f:
            f.writelines(lines)
        print("Done")
        setup()
    else:
        print("Not found")


def setup():
    global linesnum
    
##    lines = read("wordl words.txt")
##    lines += read("realwords.txt")
##    lines += readcsv("english-word-list-total.csv")
    lines = read("AllWords.txt")
    for item in lines:
        item = item.strip()
        if len(item) in nums:
            linesnum[len(item)].append(item.lower())
    

def find(match, contains, ignore=""):
    length = len(match)

    contains = contains.lower()
    ignore = ignore.lower()
    match = match.lower()

    foundwords = []
    if length in nums:
        for item in linesnum[length]:
            item = item.lower()
            temp = item
            
            found = True
            for i in range(length):
                if match[i] != "*" and match[i] != item[i]:
                    found = False
                    break
            if found:
                for j in contains:
                    if j not in item:
                        found = False
                    else:
                        temp = temp.replace(j, "", 1)
                for k in ignore:
                    if k in temp:
                        found = False
            if found:
                if item not in foundwords:
                    print(item)
                    foundwords.append(item)
        if len(foundwords) == 0:
            print("Failed")
                
def run(num):
    from datetime import datetime
    global linesnum
    print(datetime.now().time())

    bestsofar = {}
    for k in range(10000):
        lettersleft = set(acceptable_letters)
        thislist = []
        
        for j in range(1000):
            item = linesnum[num][randint(1, len(linesnum[num]))-1].strip()

            msg = item
##            thisword = []
##            passed = 0
##            for i in item:
##                if i.lower() in thisword:
##                    passed += 1
##                    if passed >= 2:
##                        break
##                else:
##                    thisword.append(i.lower())
##                    
##            msg += ", " + str(passed) + " repeats"
            if True:#passed < 2:
                msg += ", " + str(len(set(split(item)) & lettersleft)) + " overlap"
                if len(set(split(item)) & lettersleft)>= int(round(len(lettersleft)*getmostletters)) or len(set(split(item)) & lettersleft) >= int(round(num*usemostletters)): #If it gets 60% the lettersleft, free pass or If all but 40% of the letters are in, sure

                        
                    thislist.append(item.lower())
                    msg += ", added to list."
                    for i in item:
                        if i.lower() in lettersleft:
                            lettersleft.remove(i.lower())
                    msg += "  Lettersleft:" + str(len(acceptable_letters) - len(lettersleft)) + "   LengthOfList:" + str(len(thislist))
            #print(msg)
            
            if len(lettersleft) == 0:
                break
            if len(thislist) >= 5:
                lettersleft = set(acceptable_letters)
                thislist = []
                break

        if thislist != []:
            if len(lettersleft) not in bestsofar:
                bestsofar[len(lettersleft)] = []
            bestsofar[len(lettersleft)].append(thislist)

    print(datetime.now().time())

    if len(bestsofar) == 0:
        print("Failed")

    best = 99
    for num in bestsofar:
        print(num)
        if num < best:
            best = num

    if best != 99 and best <= 6:
        for i in range(10, 0, -1):
            if i in bestsofar:
                print("")
                print(f"Lists with {i} number of letters remaining.")

                min1 = 99
                for item in bestsofar[i]:
                    if len(item) < min1:
                        min1 = len(item)
                
                count = 0
                for item in bestsofar[i]:
                    if len(item) <= min1+1:
                        print(item, len(item), remainder(item))
                        count += 1
                        if count >= 20 and i != best:
                            break
                        
    elif best != 99:
        print("Failed")

setup()
