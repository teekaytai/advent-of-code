from abc import ABC, abstractmethod
from collections import defaultdict
from math import lcm, prod
import sys
from typing import Callable, NamedTuple, Optional

Pulse = bool
HIGH_PULSE = True
LOW_PULSE = False

ON = True
OFF = False

FLIP_FLOP_PREFIX = '%'
CONJUNCTION_PREFIX = '&'

START_MODULE_NAME = 'broadcaster'
START_PULSE = LOW_PULSE
END_MODULE = 'rx'


class Module(ABC):
    def __init__(self) -> None:
        self.src_modules: list[Module] = []
        self.dst_modules: list[Module] = []

    def connect_to(self, module: 'Module') -> None:
        self.dst_modules.append(module)
        module._connect_from(self)

    def _connect_from(self, module: 'Module') -> None:
        self.src_modules.append(module)

    def reset(self) -> None:
        # By default no state that needs to be reset
        pass

    @abstractmethod
    def send_pulse(self, pulse: Pulse, src_module: Optional['Module']) -> Optional[tuple[Pulse, list['Module']]]: ...


class EmptyModule(Module):
    def send_pulse(self, _: Pulse, __: Optional[Module]) -> None:
        return None


class BroadcastModule(Module):
    def send_pulse(self, pulse: Pulse, _: Optional[Module]) -> tuple[Pulse, list[Module]]:
        return pulse, self.dst_modules


class FlipFlopModule(Module):
    def __init__(self) -> None:
        super().__init__()
        self.state = OFF

    def reset(self) -> None:
        self.state = OFF

    def send_pulse(self, pulse: Pulse, _: Optional[Module]) -> Optional[tuple[Pulse, list[Module]]]:
        if pulse == HIGH_PULSE:
            return None
        self.state = not self.state
        out_pulse = HIGH_PULSE if self.state == ON else LOW_PULSE
        return out_pulse, self.dst_modules


class ConjunctionModule(Module):
    def __init__(self) -> None:
        super().__init__()
        self.last_pulses: dict[Module, Pulse] = {}

    def _connect_from(self, module: Module) -> None:
        super()._connect_from(module)
        self.last_pulses[module] = LOW_PULSE

    def reset(self) -> None:
        for module in self.last_pulses:
            self.last_pulses[module] = LOW_PULSE

    def send_pulse(self, pulse: Pulse, src_module: Optional[Module]) -> tuple[Pulse, list[Module]]:
        if src_module is not None:
            self.last_pulses[src_module] = pulse
        out_pulse = LOW_PULSE if all(pulse == HIGH_PULSE for pulse in self.last_pulses.values()) else HIGH_PULSE
        return out_pulse, self.dst_modules


class Transmission(NamedTuple):
    src_module: Optional[Module]
    pulse: Pulse
    dst_module: Module


class Machine:
    def __init__(self, config: str) -> None:
        self.modules: dict[str, Module] = defaultdict(EmptyModule)
        src_names: list[str] = []
        dsts_names: list[list[str]] = []
        for line in config.splitlines():
            src, dsts = line.split(' -> ')
            src, module = self._parse_and_make_module(src)
            self.modules[src] = module
            src_names.append(src)
            dsts_names.append(dsts.split(', '))
        for src, dst_lst in zip(src_names, dsts_names):
            src_module = self.modules[src]
            for dst in dst_lst:
                dst_module = self.modules[dst]
                src_module.connect_to(dst_module)

    def _parse_and_make_module(self, module_str: str) -> tuple[str, Module]:
        if module_str.startswith(FLIP_FLOP_PREFIX):
            return module_str.lstrip(FLIP_FLOP_PREFIX), FlipFlopModule()
        elif module_str.startswith(CONJUNCTION_PREFIX):
            return module_str.lstrip(CONJUNCTION_PREFIX), ConjunctionModule()
        return module_str, BroadcastModule()

    def reset(self) -> None:
        for module in self.modules.values():
            module.reset()

    def get_module_inputs(self, module_name: str) -> list[Module]:
        return self.modules[module_name].src_modules

    def run_once(self, callback: Optional[Callable[[Transmission], None]]) -> None:
        queue: list[Transmission] = [Transmission(None, START_PULSE, self.modules[START_MODULE_NAME])]
        next_queue: list[Transmission] = []
        while queue:
            for transmission in queue:
                if callback is not None:
                    callback(transmission)
                prev_module, pulse, curr_module = transmission
                output = curr_module.send_pulse(pulse, prev_module)
                if output is not None:
                    next_pulse, next_modules = output
                    next_queue.extend(Transmission(curr_module, next_pulse, next_module) for next_module in next_modules)
            queue = next_queue
            next_queue = []

    def count_pulses(self, num_steps: int) -> list[int]:
        pulse_counts: list[int] = [0, 0]

        def pulse_counter(transmission: Transmission) -> None:
            pulse_counts[transmission.pulse] += 1

        for _ in range(num_steps):
            self.run_once(pulse_counter)
        return pulse_counts

    def run_until_pulse_sent(self, target_module: Module, target_pulse: Pulse) -> int:
        target_pulse_sent = False

        def transmission_monitor(transmission: Transmission) -> None:
            nonlocal target_pulse_sent
            if transmission.src_module == target_module and transmission.pulse == target_pulse:
                target_pulse_sent = True

        run_count = 0
        while not target_pulse_sent:
            self.run_once(transmission_monitor)
            run_count += 1
        return run_count


machine = Machine(sys.stdin.read())

# Part 1
print(prod(machine.count_pulses(1000)))

# Part 2
# By investigating the given configuration, we see that the end module is only connected to by one conjunction module,
# and this conjunction module is connected to by conjunction modules that each send a high pulse once every certain
# number of steps. The end module gets activated when these cycles align.
end_module_inputs = machine.get_module_inputs(END_MODULE)
last_conjunction_module = end_module_inputs[0]
assert len(end_module_inputs) == 1 and isinstance(last_conjunction_module, ConjunctionModule)
overall_cycle_length = 1
for module in last_conjunction_module.src_modules:
    assert isinstance(module, ConjunctionModule)
    machine.reset()
    cycle_length = machine.run_until_pulse_sent(module, HIGH_PULSE)
    assert machine.run_until_pulse_sent(module, HIGH_PULSE) == cycle_length
    overall_cycle_length = lcm(overall_cycle_length, cycle_length)
print(overall_cycle_length)
