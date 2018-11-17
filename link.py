class link(object):
    def __init__(self, own_ssid, connected_ssid):
        self._owns_sid = own_ssid
        self._connected_ssid = connected_ssid


class Host_to_Device_Connection(link):
    def __init__(self, hostId, deviceId):
        super(Host_to_Device_Connection, self).__init__(hostId, deviceId)
