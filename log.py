import datetime


class Log:
    """Contain information for logs and resume"""

    def __init__(self, path, name):
        self.name = name
        self.log_location = path + 'logs/'
        self.dt = datetime.datetime.now()

        # date will be used to get the daily log name
        self.date = str(self.dt.year)
        self.date += ("0" if self.dt.month < 10 else "") + str(self.dt.month)
        self.date += ("0" if self.dt.day < 10 else "") + str(self.dt.day)

        self.old = 0
        self.actual = 0
        self.new = 0

    def save(self, status):
        """Appends a report. """
        file = self.log_location + 'reports.txt'
        with open(file, 'a+') as f:
            f.write("[%s] %d:%d:%d (%s): %d, %d, %d, %s\n" % (self.date, self.dt.hour, self.dt.minute, self.dt.second,
                                                              self.name, self.old, self.actual, self.new, status))
        return

    def error(self, e):
        """Creates an crash report. """
        file = self.log_location + 'CRASH_' + self.date + "_%d-%d-%d" % (
            self.dt.hour, self.dt.minute, self.dt.second) + '.txt'

        with open(file, 'w+') as f:
            s = "Hour: %d:%d:%d, running %s. Error: %s" % (self.dt.hour, self.dt.minute, self.dt.second, self.name, e)
            s += "\nResults: old-actual-new = %d/%d/%d" % (self.old, self.actual, self.new)
            f.write(s)
        return
