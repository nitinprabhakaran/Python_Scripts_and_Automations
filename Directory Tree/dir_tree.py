import os

# start point
startpath = '.'

folders = []    # folder store
tuples = []     # folders, subdirs, files


def folder_tree(line, dir):
    one = '|-> V '
    padding = '|   '

    if line == dir:
        # print('V '+line)
        return ('V '+line)

    if line.count(os.sep) == 1:
        line = line.split(os.sep)
        line[0] = one
        # print(''.join(line))
        return (''.join(line))

    if line.count(os.sep) >= 2:
        line = line.split(os.sep)
        line[-2] = one
        for i in range(len(line[:-2])):
            line[i] = padding
        # print(''.join(line))
        return (''.join(line))


def files_tree(dir, *args):
    """

    :param dir: startpath
    :param args: args[0] > tuples, args[1] > folders
    :return: None
    """
    file = '|-> '
    padding = '|   '
    last_file = ''
    tuples = args[0]
    folders_list = args[1]
    for root, subs, files in tuples:
        # no files no worries, skip
        if not files:
            continue

        # will use for padding: padding * sep
        sep = root.count(os.sep)

        # only if root has some files
        if root == dir:
            last_file = [file+str(x) for x in files]
            continue

        if subs:
            # take last elem in subs,
            # use it as value to find the same in folders_list
            # get index + 1 to insert right after
            index = folders_list.index([x for x in folders_list if x.endswith(subs[-1])][0]) + 1

        else:
            # we need name the last of folder in the root
            # to use it to find index
            folder_name = root.split(os.sep)[-1]
            index = folders_list.index([x for x in folders_list if x.endswith(folder_name)][0]) + 1

        # prepare files
        files = [sep * padding + file + x for x in files]

        # now insert files to list
        for i, a in enumerate(range(index, index+len(files))):
            folders_list.insert(a, files[i])

    if last_file:
        # merge files in root dir
        folders_list = folders_list + last_file

    # final print tree
    for elm in folders_list:
        print(elm)


def tree_walk(dir):
    for folder, subs, files in os.walk(dir):
        tuples.append((folder, subs, files))
        folders.append(folder_tree(folder, dir))


tree_walk(startpath)
folder_tree(tuples, startpath)
files_tree(startpath, tuples, folders)