import os


def rename_frames(emotion):
    file_count = len(os.listdir("./steel/"+emotion+"/"))
    print(file_count)
    frames = []
    for i in range(file_count):
        os.rename("./steel/"+emotion+"/"+str(i)+".gif", "./steel/"+emotion+"/"+str(i)+".png")
    return frames


