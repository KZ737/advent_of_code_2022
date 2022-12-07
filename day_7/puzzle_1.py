inputfile = open("./day_7/input.txt", "r")
inputfile.readline()

'''
We are using 2 classes.
One is a file which simply has a name, a size, and a parent.
The other is a folder which has a name, a parent, and a list of its files and subfolders.
Both classes have a getSize() function which in the case of a file obviously returns its size, and in the case of a folder it returns the sum of the getSize() function of its elements.
'''

class File:
    def __init__(self, name: str, size: int, parent):
        self.name = name
        self.size = size
        self.parent = parent
    def getSize(self):
        return self.size

class Folder:
    def __init__(self, name: str, parent):
        self.name = name
        self.parent = parent
        self.files = []
    def addFileOrFolder(self, file):
        self.files.append(file)
    def getSize(self):
        size = 0
        for file in self.files:
            size += file.getSize()
        return size

'''
We declare the root folder (having no parent), and name it as the first parent, and we also add it to a list of our folders.
'''
root = Folder("/", None)
parent = root
folders = [root]

'''
Parsing of the input lines, it's pretty self-explanatory.
If a line is "$ ls", we ignore it.
If a line is "$ cd <foldername>", we create a folder with this name, add that folder to the current parent's folder/file list as well as the list of all folders, then make that folder the new parent folder.
If a line is "$ cd ..", we make the current folder's parent the new parent.
If a line starts with "dir", we ignore it (we create a new folder instance when cd-ing, not at this point).
And lastly, if none of the above is the case, then we have a file, in which case we create a new file with the given name and size, then add it to the current parent's folder/file list.
'''
for line in inputfile:
    cmd = line.strip().split(" ")
    if cmd[0] == "$":
        if cmd[1] == "ls":
            continue
        elif cmd[1] == "cd":
            if cmd[2] == "..":
                parent = parent.parent
            else:
                newFolder = Folder(cmd[2], parent)
                parent.addFileOrFolder(newFolder)
                folders.append(newFolder)
                parent = newFolder
            continue
    elif cmd[0] == "dir":
        continue
    else:
        newFile = File(cmd[1], int(cmd[0]), parent)
        parent.addFileOrFolder(newFile)

'''
Look through our list of all folders and if a given folder's size is less than the given value, add it to the sum.
'''
sumOfSizes = 0
for folder in folders:
    folderSize = folder.getSize()
    if folderSize <= 100000:
        sumOfSizes += folderSize

print(sumOfSizes)

inputfile.close()