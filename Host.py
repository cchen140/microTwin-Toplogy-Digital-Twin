#  Describes end - station host, which is leaf node in the graph
class Host(object):
    def __init__(self,ssid,ipadd,macadd,program,heartbeat,hostlocation,hosttype,cyclingtime):
        self._hostType = hosttype
        self._hostId = ssid
        self._ipAdd = ipadd
        self._macAdd = macadd
        self._program = program
        self._heartBeat = heartbeat
        self._HostLocation = hostlocation
        self._cyclingTime = cyclingtime

    def get_hostid(self):
        return self._hostId

    def get_program(self):
        return self._program

    def get_heartbeat(self):
        return self._heartBeat
        
    def get_cyclingtime(self):
        return self._cyclingTime


class Drive(object):
    def __init__(self, actionstate):
        self.__actionstate = actionstate


class Cnc(Host):
    def __init__(self, ssid, ipadd, macadd, program, heartbeat, hostlocation, drivelist,controlmode, hosttype, cyclingtime = 'cnc'):
        super(Cnc, self).__init__(ssid, ipadd, macadd, program, heartbeat, hostlocation, hosttype, cyclingtime)
        self._driveList = drivelist
        self._controlMode = controlmode

    def set_hostid(self,ssid):
        self._hostId = ssid

    def set_ipadd(self,ipadd):
        self._ipAdd = ipadd

    def set_macadd(self,macadd):
        self._macAdd = macadd

    def set_program(self,program):
        self._program = program

    def set_hearbeat(self,heartbeat):
        self._heartBeat = heartbeat

    def set_hostlocation(self,hostlocation):
        self._HostLocation = hostlocation

    def set_controlmode(self,controlmode):
        self._controlMode = controlmode

    def set_drivelist(self,drivelist):
        self._driveList = drivelist
    
    def set_cyclingtime(self, cyclingtime):
        self._cyclingTime = cyclingtime


# drive1 = Drive('work')
# drive2 = Drive('idle')
# hostlocation = HostLocation('11', 1)
# drivelist = [drive1, drive2]
# cnc = Cnc('11','10.10.10.10','00:00:00:00:00:00/1','slice',True, hostlocation, drivelist,'')





