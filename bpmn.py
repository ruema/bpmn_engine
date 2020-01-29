from xml.etree.ElementTree import ElementTree, tostring

BPMN_NS = "{http://www.omg.org/spec/BPMN/20100524/MODEL}"
TAG_DEFINITIONS = f"{BPMN_NS}definitions"
TAG_MESSAGE = f"{BPMN_NS}message"
TAG_SIGNAL = f"{BPMN_NS}signal"
TAG_ESCALATION = f"{BPMN_NS}escalation"
TAG_ERROR = f"{BPMN_NS}error"
TAG_PROCESS = f"{BPMN_NS}process"
TAG_OUTGOING = f"{BPMN_NS}outgoing"
TAG_INCOMING = f"{BPMN_NS}incoming"
TAG_MESSAGE_EVENT_DEFINITION = f"{BPMN_NS}messageEventDefinition"
TAG_TIMER_EVENT_DEFINITION = f"{BPMN_NS}timerEventDefinition"
TAG_CONDITIONAL_EVENT_DEFINITION = f"{BPMN_NS}conditionalEventDefinition"
TAG_SIGNAL_EVENT_DEFINITION = f"{BPMN_NS}signalEventDefinition"
TAG_ESCALATION_EVENT_DEFINITION = f"{BPMN_NS}escalationEventDefinition"
TAG_ERROR_EVENT_DEFINITION = f"{BPMN_NS}errorEventDefinition"
TAG_COMPENSATE_EVENT_DEFINITION = f"{BPMN_NS}compensateEventDefinition"
TAG_TERMINATE_EVENT_DEFINITION = f"{BPMN_NS}terminateEventDefinition"
TAG_LINK_EVENT_DEFINITION = f"{BPMN_NS}linkEventDefinition"

TAG_TIMEDATE = f"{BPMN_NS}timeDate"
TAG_CONDITION = f"{BPMN_NS}condition"
TAG_CONDITION_EXPRESSION = f"{BPMN_NS}conditionExpression"
TAG_SCRIPT = f"{BPMN_NS}script"
TAG_TEXT = f"{BPMN_NS}text"
TAG_DOCUMENTATION = f"{BPMN_NS}documentation"
TAG_LANE = f"{BPMN_NS}lane"
TAG_FLOW_NODE_REF = f"{BPMN_NS}flowNodeRef"
TAG_CHILD_LANE_SET = f"{BPMN_NS}childLaneSet"


class _BPMNMixin(object):
    _BPMN_ATTRIBUTES = {}
    _BPMN_ELEMENTS = {}

    @classmethod
    def from_bpmn(cls, element):
        attr = dict(element.attrib)
        args = {}
        for key, value in cls._BPMN_ATTRIBUTES.items():
            args[value[0]] = attr.pop(key, value[1:])
        if attr:
            print(f"{cls.__name__}: {attr}")
        for el in element:
            if el.tag in cls._BPMN_ELEMENTS:
                key, mode = cls._BPMN_ELEMENTS[el.tag]
                if mode == "text":
                    if key in args:
                        print(f"{cls.__name__}: dupplicate {key}")
                    if list(el) or el.attrib:
                        print(f"{cls.__name__}: {tostring(el)}")
                    args[key] = el.text
                elif mode == "list":
                    if key not in args:
                        args[key] = []
                    if list(el) or el.attrib:
                        print(f"{cls.__name__}: {tostring(el)}")
                    args[key].append(el.text)
                elif isinstance(mode, type):
                    if key == 'items':
                        if key not in args:
                            args[key] = []
                        args[key].append(mode.from_bpmn(el))
                    elif key in args:
                        print(f"{cls.__name__}: dupplicate {key}")
                    else:
                        args[key] = mode.from_bpmn(el)
                else:
                    raise RuntimeError(mode)
            else:
                print(f"{cls.__name__}: {tostring(el)}")
        return cls(**args)

class MessageEventDefinition(_BPMNMixin):
    _BPMN_ATTRIBUTES = {
        'messageRef': ('message_reference',),
    }

    def __init__(self, message_reference):
        self.message_reference = message_reference


class TimerEventDefinition(_BPMNMixin):
    _BPMN_ELEMENTS = {
        TAG_TIMEDATE: ('timedate', 'text'),
    }

    def __init__(self, timedate=None):
        self.timedate = timedate


class ConditionalEventDefinition(_BPMNMixin):
    _BPMN_ELEMENTS = {
        TAG_CONDITION: ('condition', 'text'),
    }

    def __init__(self, condition):
        self.condition = condition


class SignalEventDefinition(_BPMNMixin):
    _BPMN_ATTRIBUTES = {
        'signalRef': ('signal_reference',),
    }

    def __init__(self, signal_reference):
        self.signal_reference = signal_reference


class EscalationEventDefinition(_BPMNMixin):
    _BPMN_ATTRIBUTES = {
        'escalationRef': ('escalation_reference',),
    }

    def __init__(self, escalation_reference):
        self.escalation_reference = escalation_reference


class ErrorEventDefinition(_BPMNMixin):
    _BPMN_ATTRIBUTES = {
        'errorRef': ('error_reference',),
    }

    def __init__(self, error_reference):
        self.error_reference = error_reference


class CompensateEventDefinition(_BPMNMixin):
    def __init__(self):
        pass


class TerminateEventDefinition(_BPMNMixin):
    def __init__(self):
        pass

class LinkEventDefinition(_BPMNMixin):
    _BPMN_ATTRIBUTES = {
        'name': ('name',),
    }

    def __init__(self, name):
        self.name = name

EVENT_CLASSES = {
    TAG_MESSAGE_EVENT_DEFINITION: ('event', MessageEventDefinition),
    TAG_TIMER_EVENT_DEFINITION: ('event', TimerEventDefinition),
    TAG_CONDITIONAL_EVENT_DEFINITION: ('event', ConditionalEventDefinition),
    TAG_SIGNAL_EVENT_DEFINITION: ('event', SignalEventDefinition),
    TAG_ESCALATION_EVENT_DEFINITION: ('event', EscalationEventDefinition),
    TAG_ERROR_EVENT_DEFINITION: ('event', ErrorEventDefinition),
    TAG_COMPENSATE_EVENT_DEFINITION: ('event', CompensateEventDefinition),
    TAG_TERMINATE_EVENT_DEFINITION: ('event', TerminateEventDefinition),
    TAG_LINK_EVENT_DEFINITION: ('event', LinkEventDefinition),
}

class ConditionExpression(object):
    _BPMN_ATTRIBUTES = {
        '{http://www.w3.org/2001/XMLSchema-instance}type': ('expression_type', None)
    }

    def __init__(self, condition, expression_type=None):
        self.condition = condition
        self.expression_type = expression_type

    @classmethod
    def from_bpmn(cls, element):
        attr = dict(element.attrib)
        args = {}
        for key, value in cls._BPMN_ATTRIBUTES.items():
            args[value[0]] = attr.pop(key, value[1:])
        if attr:
            print(f"{cls.__name__}: {attr}")
        for el in element:
            print(f"{cls.__name__}: {tostring(el)}")
        return cls(element.text, **args)

class Message(object):
    def __init__(self, attrs):
        self.attrs = attrs

class SequenceFlow(_BPMNMixin):
    _BPMN_ATTRIBUTES = {
        'id': ('id', ),
        'name': ('name', None),
        'sourceRef': ('source_reference', None),
        'targetRef': ('target_reference', None),
    }
    _BPMN_ELEMENTS = {
        TAG_DOCUMENTATION: ('documentation', 'text'),
        TAG_CONDITION_EXPRESSION: ('condition', ConditionExpression),
    }

    def __init__(self, id, name=None, documentation=None, source_reference=None, target_reference=None, condition=None):
        self.id = id
        self.name = name
        self.source_reference = source_reference
        self.target_reference = target_reference
        self.condition = condition
        self.documentation = documentation


class StartEvent(_BPMNMixin):
    _BPMN_ATTRIBUTES = {
        'id': ('id', ),
        'name': ('name', None),
    }
    _BPMN_ELEMENTS = dict({
        TAG_DOCUMENTATION: ('documentation', 'text'),
        TAG_OUTGOING: ('outgoing', 'list'),
    }, **EVENT_CLASSES)

    def __init__(self, id, name=None, documentation=None, outgoing=None, event=None):
        self.id = id
        self.name = name
        self.event = event
        self.documentation = documentation
        self.outgoing = [] if outgoing is None else outgoing

    def execute(self, task):
        resulting_tasks = []
        for flow in self.outgoing:
            flow = task.runtime.process.items[flow]
            if flow.condition:
                raise Runtime("start event flows cannot have conditions")
            element = task.runtime.process.items[flow.target_reference]
            resulting_tasks.append(Task(task.runtime, element))
        return resulting_tasks


class BoundaryEvent(object):
    @classmethod
    def from_bpmn(cls, element):
        print(tostring(element))

class IntermediateCatchEvent(_BPMNMixin):
    _BPMN_ATTRIBUTES = {
        'id': ('id', ),
        'name': ('name', None),
    }
    _BPMN_ELEMENTS = dict({
        TAG_OUTGOING: ('outgoing', 'list'),
        TAG_INCOMING: ('incoming', 'list'),
    }, **EVENT_CLASSES)

    def __init__(self, id, name=None, event=None, incoming=None, outgoing=None):
        self.id = id
        self.name = name
        self.event = event
        self.incoming = [] if incoming is None else incoming
        self.outgoing = [] if outgoing is None else outgoing


class IntermediateThrowEvent(_BPMNMixin):
    _BPMN_ATTRIBUTES = {
        'id': ('id', ),
        'name': ('name', None),
    }
    _BPMN_ELEMENTS = dict({
        TAG_OUTGOING: ('outgoing', 'list'),
        TAG_INCOMING: ('incoming', 'list'),
    }, **EVENT_CLASSES)

    def __init__(self, id, name=None, event=None, incoming=None, outgoing=None):
        self.id = id
        self.name = name
        self.event = event
        self.incoming = [] if incoming is None else incoming
        self.outgoing = [] if outgoing is None else outgoing


class EndEvent(_BPMNMixin):
    _BPMN_ATTRIBUTES = {
        'id': ('id', ),
        'name': ('name', None),
    }
    _BPMN_ELEMENTS = dict({
        TAG_INCOMING: ('incoming', 'list'),
    }, **EVENT_CLASSES)

    def __init__(self, id, name=None, incoming=None, event=None):
        self.id = id
        self.name = name
        self.incoming = [] if incoming is None else incoming
        self.event = event


class ExclusiveGateway(_BPMNMixin):
    _BPMN_ATTRIBUTES = {
        'id': ('id', ),
        'name': ('name', None),
        'default': ('default', None),
    }
    _BPMN_ELEMENTS = {
        TAG_DOCUMENTATION: ('documentation', 'text'),
        TAG_INCOMING: ('incoming', 'list'),
        TAG_OUTGOING: ('outgoing', 'list'),
    }

    def __init__(self, id, name=None, documentation=None, incoming=None, outgoing=None, default=None):
        self.id = id
        self.name = name
        self.incoming = [] if incoming is None else incoming
        self.outgoing = [] if outgoing is None else outgoing
        self.default = default
        self.documentation = documentation

    def execute(self, task):
        outgoing_flows = []
        for flow in self.outgoing:
            if flow == self.default:
                continue
            flow = task.runtime.process.items[flow]
            if not flow.condition or task.runtime.evaluate(flow.condition.condition):
                outgoing_flows.append(flow)
        if not outgoing_flows:
            default_flow = task.runtime.process.items[self.default]
            outgoing_flows.append(default_flow)
        if len(outgoing_flows) > 1:
            raise RuntimeError("more than one outgoing flow")
        return [
            Task(task.runtime, 
                task.runtime.process.items[flow.target_reference]
            )
            for flow in outgoing_flows
        ]


class InclusiveGateway(_BPMNMixin):
    _BPMN_ATTRIBUTES = {
        'id': ('id', ),
        'name': ('name', None),
        'default': ('default', None),
    }
    _BPMN_ELEMENTS = {
        TAG_INCOMING: ('incoming', 'list'),
        TAG_OUTGOING: ('outgoing', 'list'),
    }

    def __init__(self, id, name=None, incoming=None, outgoing=None, default=None):
        self.id = id
        self.name = name
        self.incoming = [] if incoming is None else incoming
        self.outgoing = [] if outgoing is None else outgoing
        self.default = default


class ComplexGateway(_BPMNMixin):
    _BPMN_ATTRIBUTES = {
        'id': ('id', ),
        'name': ('name', None),
        'default': ('default', None),
    }
    _BPMN_ELEMENTS = {
        TAG_INCOMING: ('incoming', 'list'),
        TAG_OUTGOING: ('outgoing', 'list'),
    }

    def __init__(self, id, name=None, incoming=None, outgoing=None, default=None):
        self.id = id
        self.name = name
        self.incoming = [] if incoming is None else incoming
        self.outgoing = [] if outgoing is None else outgoing
        self.default = default


class EventBasedGateway(_BPMNMixin):
    _BPMN_ATTRIBUTES = {
        'id': ('id', ),
        'name': ('name', None),
        'default': ('default', None),
    }
    _BPMN_ELEMENTS = {
        TAG_INCOMING: ('incoming', 'list'),
        TAG_OUTGOING: ('outgoing', 'list'),
    }

    def __init__(self, id, name=None, incoming=None, outgoing=None, default=None):
        self.id = id
        self.name = name
        self.incoming = [] if incoming is None else incoming
        self.outgoing = [] if outgoing is None else outgoing
        self.default = default


class ParallelGateway(_BPMNMixin):
    _BPMN_ATTRIBUTES = {
        'id': ('id', ),
        'name': ('name', None),
    }
    _BPMN_ELEMENTS = {
        TAG_INCOMING: ('incoming', 'list'),
        TAG_OUTGOING: ('outgoing', 'list'),
    }

    def __init__(self, id, name=None, incoming=None, outgoing=None):
        self.id = id
        self.name = name
        self.incoming = [] if incoming is None else incoming
        self.outgoing = [] if outgoing is None else outgoing


class CallActivity(_BPMNMixin):
    _BPMN_ATTRIBUTES = {
        'id': ('id', ),
        'name': ('name', None),
        'default': ('default', None),
    }
    _BPMN_ELEMENTS = {
        TAG_INCOMING: ('incoming', 'list'),
        TAG_OUTGOING: ('outgoing', 'list'),
    }

    def __init__(self, id, name=None, incoming=None, outgoing=None, default=None):
        self.id = id
        self.name = name
        self.incoming = [] if incoming is None else incoming
        self.outgoing = [] if outgoing is None else outgoing
        self.default = default


class ManualTask(_BPMNMixin):
    _BPMN_ATTRIBUTES = {
        'id': ('id', ),
        'name': ('name', None),
        'default': ('default', None),
    }
    _BPMN_ELEMENTS = {
        TAG_INCOMING: ('incoming', 'list'),
        TAG_OUTGOING: ('outgoing', 'list'),
    }

    def __init__(self, id, name=None, incoming=None, outgoing=None, default=None):
        self.id = id
        self.name = name
        self.incoming = [] if incoming is None else incoming
        self.outgoing = [] if outgoing is None else outgoing
        self.default = default


class ServiceTask(_BPMNMixin):
    _BPMN_ATTRIBUTES = {
        'id': ('id', ),
        'name': ('name', None),
        'default': ('default', None),
    }
    _BPMN_ELEMENTS = {
        TAG_INCOMING: ('incoming', 'list'),
        TAG_OUTGOING: ('outgoing', 'list'),
    }

    def __init__(self, id, name=None, incoming=None, outgoing=None, default=None):
        self.id = id
        self.name = name
        self.incoming = [] if incoming is None else incoming
        self.outgoing = [] if outgoing is None else outgoing
        self.default = default


class BusinessRuleTask(_BPMNMixin):
    _BPMN_ATTRIBUTES = {
        'id': ('id', ),
        'name': ('name', None),
        'default': ('default', None),
    }
    _BPMN_ELEMENTS = {
        TAG_INCOMING: ('incoming', 'list'),
        TAG_OUTGOING: ('outgoing', 'list'),
    }

    def __init__(self, id, name=None, incoming=None, outgoing=None, default=None):
        self.id = id
        self.name = name
        self.incoming = [] if incoming is None else incoming
        self.outgoing = [] if outgoing is None else outgoing
        self.default = default


class ReceiveTask(_BPMNMixin):
    _BPMN_ATTRIBUTES = {
        'id': ('id', ),
        'name': ('name', None),
        'default': ('default', None),
        'messageRef': ('message_reference', None),
    }
    _BPMN_ELEMENTS = {
        TAG_INCOMING: ('incoming', 'list'),
        TAG_OUTGOING: ('outgoing', 'list'),
    }

    def __init__(self, id, name=None, incoming=None, outgoing=None, default=None, message_reference=None):
        self.id = id
        self.name = name
        self.incoming = [] if incoming is None else incoming
        self.outgoing = [] if outgoing is None else outgoing
        self.default = default
        self.message_reference = message_reference


class ScriptTask(_BPMNMixin):
    _BPMN_ATTRIBUTES = {
        'id': ('id', ),
        'name': ('name', None),
        'default': ('default', None),
        'scriptFormat': ('script_format', None),
    }
    _BPMN_ELEMENTS = {
        TAG_INCOMING: ('incoming', 'list'),
        TAG_OUTGOING: ('outgoing', 'list'),
        TAG_SCRIPT: ('script', 'text'),
    }

    def __init__(self, id, name=None, incoming=None, outgoing=None, default=None, script_format=None, script=None):
        self.id = id
        self.name = name
        self.incoming = [] if incoming is None else incoming
        self.outgoing = [] if outgoing is None else outgoing
        self.default = default
        self.script_format = script_format
        self.script = script

    def execute(self, task):
        task.runtime.run_script(self.script)
        outgoing_flows = []
        for flow in self.outgoing:
            if flow == self.default:
                continue
            flow = task.runtime.process.items[flow]
            if not flow.condition or task.runtime.evaluate(flow.condition.condition):
                outgoing_flows.append(flow)
        if not outgoing_flows:
            default_flow = task.runtime.process.items[self.default]
            outgoing_flows.append(default_flow)
        return [
            Task(task.runtime, 
                task.runtime.process.items[flow.target_reference]
            )
            for flow in outgoing_flows
        ]


class SendTask(_BPMNMixin):
    _BPMN_ATTRIBUTES = {
        'id': ('id', ),
        'name': ('name', None),
        'default': ('default', None),
    }
    _BPMN_ELEMENTS = {
        TAG_INCOMING: ('incoming', 'list'),
        TAG_OUTGOING: ('outgoing', 'list'),
    }

    def __init__(self, id, name=None, incoming=None, outgoing=None, default=None):
        self.id = id
        self.name = name
        self.incoming = [] if incoming is None else incoming
        self.outgoing = [] if outgoing is None else outgoing
        self.default = default


class UserTask(_BPMNMixin):
    _BPMN_ATTRIBUTES = {
        'id': ('id', ),
        'name': ('name', None),
        'default': ('default', None),
    }
    _BPMN_ELEMENTS = {
        TAG_INCOMING: ('incoming', 'list'),
        TAG_OUTGOING: ('outgoing', 'list'),
    }

    def __init__(self, id, name=None, incoming=None, outgoing=None, default=None):
        self.id = id
        self.name = name
        self.incoming = [] if incoming is None else incoming
        self.outgoing = [] if outgoing is None else outgoing
        self.default = default


class Task(_BPMNMixin):
    _BPMN_ATTRIBUTES = {
        'id': ('id', ),
        'name': ('name', None),
        'default': ('default', None),
    }
    _BPMN_ELEMENTS = {
        TAG_INCOMING: ('incoming', 'list'),
        TAG_OUTGOING: ('outgoing', 'list'),
    }

    def __init__(self, id, name=None, incoming=None, outgoing=None, default=None):
        self.id = id
        self.name = name
        self.incoming = [] if incoming is None else incoming
        self.outgoing = [] if outgoing is None else outgoing
        self.default = default


class DataObject(_BPMNMixin):
    _BPMN_ATTRIBUTES = {
        'id': ('id', ),
        'name': ('name', None),
    }

    def __init__(self, id, name=None):
        self.id = id
        self.name = name


class DatastoreReference(_BPMNMixin):
    _BPMN_ATTRIBUTES = {
        'id': ('id', ),
        'name': ('name', None),
    }

    def __init__(self, id, name=None):
        self.id = id
        self.name = name


class DataObjectReference(_BPMNMixin):
    _BPMN_ATTRIBUTES = {
        'id': ('id', ),
        'name': ('name', None),
        'dataObjectRef': ('data_object_reference', None),
    }

    def __init__(self, id, name=None, data_object_reference=None):
        self.id = id
        self.name = name
        self.data_object_reference = data_object_reference


class ChildLaneSet(_BPMNMixin):
    _BPMN_ATTRIBUTES = {
        'id': ('id', ),
        'name': ('name', None),
    }
    def __init__(self, id, name):
        self.id = id
        self.name = name

class Lane(_BPMNMixin):
    _BPMN_ATTRIBUTES = {
        'id': ('id', ),
        'name': ('name', None),
    }
    _BPMN_ELEMENTS = {
        TAG_CHILD_LANE_SET: ('child_lane_set', ChildLaneSet),
        TAG_FLOW_NODE_REF: ('flow_nodes', 'list'),
    }

    def __init__(self, id, name=None, flow_nodes=None, child_lane_set=None):
        self.id = id
        self.name = name
        self.flow_nodes = flow_nodes
        self.child_lane_set = child_lane_set


class LaneSet(_BPMNMixin):
    _BPMN_ATTRIBUTES = {
        'id': ('id', ),
        'name': ('name', None),
    }
    _BPMN_ELEMENTS = {
        TAG_LANE: ('items', Lane),
    }

    def __init__(self, id, name=None, items=None):
        self.id = id
        self.name = name
        self.lanes = items

class SubProcess(_BPMNMixin):
    _BPMN_ATTRIBUTES = {
        'id': ('id', ),
        'name': ('name', None),
        'triggeredByEvent': ('triggered_by_event', None),
    }
    _BPMN_ELEMENTS = {
        TAG_INCOMING: ('incoming', 'list'),
        TAG_OUTGOING: ('outgoing', 'list'),
    }

    def __init__(self, id, name=None, incoming=None, outgoing=None, items=None, triggered_by_event=None):
        self.id = id
        self.name = name
        self.incoming = [] if incoming is None else incoming
        self.outgoing = [] if outgoing is None else outgoing
        self.items = {i.id: i for i in items}
        self.triggered_by_event = triggered_by_event

class Association(_BPMNMixin):
    _BPMN_ATTRIBUTES = {
        'id': ('id', ),
        'name': ('name', None),
        'sourceRef': ('source_reference', None),
        'targetRef': ('target_reference', None),
    }

    def __init__(self, id, name=None, source_reference=None, target_reference=None):
        self.id = id
        self.name = name
        self.source_reference = source_reference
        self.target_reference = target_reference


class TextAnnotation(_BPMNMixin):
    _BPMN_ATTRIBUTES = {
        'id': ('id', ),
        'name': ('name', None),
    }
    _BPMN_ELEMENTS = {
        TAG_TEXT: ('text', 'text'),
        TAG_OUTGOING: ('outgoing', 'list'),
    }

    def __init__(self, id, name=None, text=None):
        self.id = id
        self.name = name
        self.text = text

class Process(_BPMNMixin):
    _BPMN_ATTRIBUTES = {
        'id': ('id', ),
        'name': ('name', None),
        'isExecutable': ('is_executable', None),
    }
    _BPMN_ELEMENTS = {
    }

    def __init__(self, id, name=None, items=None, is_executable=None):
        self.id = id
        self.name = name
        self.items = {i.id: i for i in items}
        self.is_executable = is_executable

    def get_start(self):
        starts = [el for el in self.items.values() if isinstance(el, StartEvent)]
        if len(starts) > 1:
            print("More than one start")
        return starts[0] if starts else None

ELEMENT_CLASSES = {
    f"{BPMN_NS}sequenceFlow": SequenceFlow,
    f"{BPMN_NS}startEvent": StartEvent,
    f"{BPMN_NS}boundaryEvent": BoundaryEvent,
    f"{BPMN_NS}intermediateCatchEvent": IntermediateCatchEvent,
    f"{BPMN_NS}intermediateThrowEvent": IntermediateThrowEvent,
    f"{BPMN_NS}endEvent": EndEvent,

    f"{BPMN_NS}dataStoreReference": DatastoreReference,
    f"{BPMN_NS}exclusiveGateway": ExclusiveGateway,
    f"{BPMN_NS}inclusiveGateway": InclusiveGateway,
    f"{BPMN_NS}complexGateway": ComplexGateway,
    f"{BPMN_NS}eventBasedGateway": EventBasedGateway,
    f"{BPMN_NS}parallelGateway": ParallelGateway,
    f"{BPMN_NS}callActivity": CallActivity,
    f"{BPMN_NS}manualTask": ManualTask,
    f"{BPMN_NS}serviceTask": ServiceTask,
    f"{BPMN_NS}businessRuleTask": BusinessRuleTask,
    f"{BPMN_NS}receiveTask": ReceiveTask,
    f"{BPMN_NS}scriptTask": ScriptTask,
    f"{BPMN_NS}sendTask": SendTask,
    f"{BPMN_NS}userTask": UserTask,
    f"{BPMN_NS}task": Task,
    f"{BPMN_NS}subProcess": SubProcess,

    f"{BPMN_NS}dataObject": DataObject,
    f"{BPMN_NS}dataObjectReference": DataObjectReference,
    f"{BPMN_NS}association": Association,
    f"{BPMN_NS}textAnnotation": TextAnnotation,
    f"{BPMN_NS}laneSet": LaneSet,
}

SubProcess._BPMN_ELEMENTS.update(
    (key, ('items', cls)) for key, cls in ELEMENT_CLASSES.items()
)

Process._BPMN_ELEMENTS.update(
    (key, ('items', cls)) for key, cls in ELEMENT_CLASSES.items()
)


class ProcessDefinition(object):
    def __init__(self):
        self.processes = {}
        self.messages = {}
        self.signals = {}
        self.escalations = {}
        self.errors = {}

    @classmethod
    def read_bpmn(cls, filename):
        result = cls()
        tree = ElementTree(file=filename)
        root = tree.getroot()
        if root.tag != TAG_DEFINITIONS:
            raise RuntimeError(f"{TAG_DEFINITIONS} expected")
        for element in root:
            if element.tag == TAG_MESSAGE:
                result.messages[element.attrib['id']] = Message(element.attrib)
            elif element.tag == TAG_SIGNAL:
                result.signals[element.attrib['id']] = Message(element.attrib)
            elif element.tag == TAG_ESCALATION:
                result.escalations[element.attrib['id']] = Message(element.attrib)
            elif element.tag == TAG_ERROR:
                result.errors[element.attrib['id']] = Message(element.attrib)
            elif element.tag == TAG_PROCESS:
                result.processes[element.attrib['id']] = Process.from_bpmn(element)
        return result

class Task(object):
    def __init__(self, runtime, element):
        self.runtime = runtime
        self.element = element


class Runtime(object):
    def __init__(self, process, data):
        self.process = process
        self.data = data
        self.tasks = []
        self.tasks.append(Task(self, process.get_start()))

    def evaluate(self, expression):
        print("eval", expression)
        return True

    def run_script(self, script):
        print("run", script)

    def execute(self):
        while self.tasks:
            new_tasks = []
            for task in self.tasks:
                new_tasks.extend(task.element.execute(task))
            self.tasks = new_tasks


if __name__ == '__main__':
    import sys
    process_definition = ProcessDefinition.read_bpmn(sys.argv[1])
    process = list(process_definition.processes.values())[0]
    runtime = Runtime(process, {})
    runtime.execute()
