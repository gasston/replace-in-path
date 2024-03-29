# Python 3
import os, sys, shutil, re
import datetime
import io

file_list = [
]

# must be full path. dir can end with slash or no
INPUT_DIR = "PATH"
MIN_LEVEL = 1 # files and dirs inside INPUT_DIR are level 1.
MAX_LEVEL = 6 # inclusive
FILE_NAME_REGEX = r"\.(html|shtml|htm|js|json?)$"
PRINT_FILENAME_WHEN_NO_CHANGE = False
BACKUP_FNAME_EXT = '~bk~'
DO_BACKUP = False

# a regex string. any full path that match is skipped
DIRPATH_SKIP_REGEX = ''

FIND_REPLACE_LIST = [
(STRING_A,STRING_B)
# more pair here
]

##################################################
# code begin

INPUT_DIR = os.path.normpath(INPUT_DIR)

for x in FIND_REPLACE_LIST:
    if len(x) != 2:
        sys.exit("Error: replacement pair has more than 2 elements. Probably missing a comma.")

def replace_string_in_file(file_path):
    "Replaces find/replace pairs in FIND_REPLACE_LIST in file_path"
    input_file = open(file_path, "r", encoding="utf-8")
    try:
        file_content = input_file.read()
    except UnicodeDecodeError:
        # print("UnicodeDecodeError:{:s}".format(input_file))
        return

    input_file.close()

    num_replaced = 0
    for a_pair in FIND_REPLACE_LIST:
        num_replaced += file_content.count(a_pair[0])
        file_content = file_content.replace(a_pair[0], a_pair[1])

    if num_replaced > 0:
        #print("-", num_replaced, " ", file_path.replace(os.sep, "/"))
        if DO_BACKUP:
            backup_fname = file_path + BACKUP_FNAME_EXT
            os.rename(file_path, backup_fname)
        output_file = open(file_path, "w",encoding="utf-8")
        output_file.write(file_content)
        output_file.close()
    else:
        if PRINT_FILENAME_WHEN_NO_CHANGE == True:
            print("no change:", file_path)

##################################################

print(datetime.datetime.now())
print("Input Dir:", INPUT_DIR)
for x in FIND_REPLACE_LIST:
   print("Find string %s",x[0])
   print("Replace string: %s ",x[1])
   print("\n")

if (len(file_list) != 0):
	#print("test")
	for ff in file_list: replace_string_in_file(os.path.normpath(ff) )
else:
    for dirPath, subdirList, fileList in os.walk(INPUT_DIR):
        curDirLevel = dirPath.count( os.sep) - INPUT_DIR.count( os.sep)
        curFileLevel = curDirLevel + 1

# emacs_manual|\

        if (MIN_LEVEL <= curFileLevel) and (curFileLevel <= MAX_LEVEL) and (not re.search(DIRPATH_SKIP_REGEX, dirPath, re.U)):
            #print (dirPath)
            for fName in fileList:
                if (re.search( FILE_NAME_REGEX, fName, re.U)) and (not (re.search(r"#", fName, re.U))):
                    print(dirPath + os.sep + fName)
                    replace_string_in_file(dirPath + os.sep + fName)
                    print ("level %d,  %s" % (curFileLevel, os.path.join(dirPath, fName)))

print("Done.")
