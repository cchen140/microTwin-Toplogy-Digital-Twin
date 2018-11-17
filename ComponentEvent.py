from enum import Enum, unique


class AbstractEvent(object):
    def __init__(self, eventtype, subject, ssid, time = 0):
        self._eventype = eventtype
        self._subject = subject
        self._ssid = ssid
        self._time = time

    def get_time(self):
        return self._time

    def get_type(self):
        return self._eventype

    def get_subject(self):
        return self._subject

    def get_ssid(self):
        return self._ssid


@unique
class EventType(Enum):
    ADDED = 'add'  # Signifies that a new component is detected

    ERROR = 'error'  # Signifies that the component failure happened,
                       # temporarily delete the component as well as the links

    UPDATED = 'update'  # Signifies that update the information of component
                        # e.g. some variables like location changed

    IDLING = 'idle'   # Signifies that there is no job in the process

    REMOVED = 'remove'  # Signifies that a component is removed from plant permanently

    RECOVER = 'recover' # Signifies that a component is recovered from error
    
    LOADING = 'loading' # Signifies that a component is loading a part

    UNLOADING = 'unloading' # Signifies that a component is unloading a part

    CYCLING = 'cycling' # Signifies that component is working on a part
    
    BLOCKED = 'blocked' # Signifies that a component must stop because there is no space to deposit the item
    #heartbeat > 0 
    
    WAITING = 'waiting'	# Signifies that a component cannot start work because additional conditions must be fulfilled
    #heartbeat > 0, MTTR reached, processingtime = 0
    
    SETUP = 'setup' # Signifies that a component is being setup
    #heartbeat = 0
    
    EMERGENCY STOP = 'emergency_stop' # Signifies that a component aborts operation and is placed into safe condition 
    #heartbeat = 0
    
    REPAIR = 'repair' # Signifies that a component has an intervention 
    #heartbeat = 0, MTBF is reached

    SHUTDOWN = 'shutdown' # Signifies that a component manually goes into shutdown state
    #heartbeat = 0,



class CncEvent(AbstractEvent):
    def __init__(self, eventtype, ssid, time):
        super(CncEvent, self).__init__(eventtype, 'cnc', ssid, time)


class StopperEvent(AbstractEvent):
    def __init__(self, eventtype, ssid, time):
        super(StopperEvent,self).__init__(eventtype, 'stopper', ssid, time)


class RobotEvent(AbstractEvent):
    def __init__(self, eventtype, ssid, time):
        super(RobotEvent,self).__init__(eventtype, 'rebot', ssid, time)
