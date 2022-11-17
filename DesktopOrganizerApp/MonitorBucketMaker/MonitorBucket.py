import os
from TKWidget import BucketWidget


class __MonitorBucket(object):
    def __init__(self):
        self.lines = None
        self.newLines = []

    def display(self, widget):
        # formatting for export
        self.lines = widget.lines
        for line in self.lines:
            line = line.split(",")
            print(line, "line")
            line[0] = line[0].upper() + ":"
            line[1] = "\"" + line[1] + "\""
            line[2] = ":: Due:" + line[2]
            line = " ".join(line)
            line = line + "\n"
            self.newLines.append(line)

    def update(self):
        """ UNUSED """
        file = open("/Users/lan/Desktop/MonitorBucketMaker/MonitorBucketContents.txt", "w+")
        for line in self.lines:
            line = line + "\n"
            file.write(line)
        file.close()

    def export(self):
        file = open("/Users/lan/Desktop/output.txt", "w+")
        for line in self.newLines:
            file.write(line)
        file.close()


with open("/Users/lan/Desktop/MonitorBucketMaker/MonitorBucketContents.txt") as f:
    contents = f.readlines()
    contents = [row[:-1] for row in contents]

monitorBucket = __MonitorBucket()
widget = BucketWidget(contents)

monitorBucket.display(widget)
monitorBucket.export()