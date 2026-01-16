# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import copy
import logging
import math
import time

import pydirectinput
import win32api

import src.shape_list as shape_list
from src.config_manager import ConfigManager
from src.controllers.mouse_controller import MouseController
from src.singleton_meta import Singleton

logger = logging.getLogger("Keybinder")

# disable lag
pydirectinput.PAUSE = 0
pydirectinput.FAILSAFE = False


class Keybinder(metaclass=Singleton):

    def __init__(self) -> None:
        logger.info("Intialize Keybinder singleton")
        self.top_count = 0
        self.triggered = False
        self.start_hold_ts = math.inf
        self.holding = False
        self.is_started = False
        self.last_know_keybinds = {}
        self.last_key_press_time = {}  # Track last key press time for throttling

    def start(self):
        if not self.is_started:
            logger.info("Start Keybinder singleton")
            self.init_states()
            self.screen_w, self.screen_h = pydirectinput.size()
            self.monitors = self.get_monitors()
            self.is_started = True

    def init_states(self) -> None:
        """Re initializes the state of the keybinder.
           If new keybinds are added.
        """
        # Preserve existing key states to avoid releasing held keys
        old_key_states = getattr(self, 'key_states', {})
        
        # keep states for all registered keys.
        self.key_states = {}
        for _, v in (ConfigManager().mouse_bindings |
                     ConfigManager().keyboard_bindings).items():
            state_name = v[0] + "_" + v[1]
            # Preserve existing state if it exists, otherwise default to False
            self.key_states[state_name] = old_key_states.get(state_name, False)
        self.key_states["holding"] = old_key_states.get("holding", False)
        
        # Only reset throttle timing if not already initialized
        if not hasattr(self, 'last_key_press_time'):
            self.last_key_press_time = {}
            
        self.last_know_keybinds = copy.deepcopy(
            (ConfigManager().mouse_bindings |
             ConfigManager().keyboard_bindings))

    def get_monitors(self) -> list[dict]:
        out_list = []
        monitors = win32api.EnumDisplayMonitors()
        for i, (_, _, loc) in enumerate(monitors):
            mon_info = {}
            mon_info["id"] = i
            mon_info["x1"] = loc[0]
            mon_info["y1"] = loc[1]
            mon_info["x2"] = loc[2]
            mon_info["y2"] = loc[3]
            mon_info["center_x"] = (loc[0] + loc[2]) // 2
            mon_info["center_y"] = (loc[1] + loc[3]) // 2
            out_list.append(mon_info)

        return out_list

    def get_curr_monitor(self):

        x, y = pydirectinput.position()
        for mon_id, mon in enumerate(self.monitors):
            if x >= mon["x1"] and x <= mon["x2"] and y >= mon[
                    "y1"] and y <= mon["y2"]:
                return mon_id
        #raise Exception("Monitor not found")
        return 0

    def mouse_action(self, val, action, thres, mode) -> None:
        state_name = "mouse_" + action

        mode = "hold" if self.key_states["holding"] else "single"

        if mode == "hold":
            if (val > thres) and (self.key_states[state_name] is False):
                pydirectinput.mouseDown(action)

                self.key_states[state_name] = True

            elif (val < thres) and (self.key_states[state_name] is True):
                pydirectinput.mouseUp(action)
                self.key_states[state_name] = False

        elif mode == "single":
            if (val > thres):
                if not self.key_states[state_name]:
                    pydirectinput.click(button=action)
                    self.start_hold_ts = time.time()

                self.key_states[state_name] = True

                if not self.holding and (
                    ((time.time() - self.start_hold_ts) * 1000) >=
                        ConfigManager().config["hold_trigger_ms"]):

                    pydirectinput.mouseDown(button=action)
                    self.holding = True

            elif (val < thres) and (self.key_states[state_name] is True):

                self.key_states[state_name] = False

                if self.holding:
                    pydirectinput.mouseUp(button=action)
                    self.holding = False
                    self.start_hold_ts = math.inf

    def keyboard_action(self, val, keysym, thres, mode, hold_mode=True, throttle_time_ms=200.0):

        state_name = "keyboard_" + keysym
        current_state = self.key_states.get(state_name, False)
        
        # Ensure hold_mode is a boolean (handle string "True"/"False" from JSON)
        if isinstance(hold_mode, str):
            hold_mode = hold_mode.lower() == "true"
        hold_mode = bool(hold_mode)

        if hold_mode:
            # Hold mode: keep key pressed while gesture is above threshold
            if not current_state and val > thres:
                logger.info(f"HOLD keyDown: {keysym}, val={val:.3f}, thres={thres:.3f}")
                pydirectinput.keyDown(keysym)
                self.key_states[state_name] = True

            elif current_state and val < thres:
                logger.info(f"HOLD keyUp: {keysym}, val={val:.3f}, thres={thres:.3f}")
                pydirectinput.keyUp(keysym)
                self.key_states[state_name] = False
        else:
            # Throttled mode: single press with cooldown between activations
            current_time = time.time() * 1000  # Convert to milliseconds
            
            if val > thres:
                # Gesture is active - check if enough time has passed since last press
                last_press_time = self.last_key_press_time.get(state_name, 0)
                time_since_last_press = current_time - last_press_time
                
                if time_since_last_press >= throttle_time_ms:
                    # Time has passed, trigger key press
                    logger.info(f"THROTTLE press: {keysym}, val={val:.3f}, throttle={throttle_time_ms}ms")
                    pydirectinput.press(keysym)
                    self.last_key_press_time[state_name] = current_time
                    self.key_states[state_name] = True
            else:
                # Gesture is not active
                self.key_states[state_name] = False

    def act(self, blendshape_values) -> dict:
        """Trigger devices action base on blendshape values

        Args:
            blendshape_values (npt.ArrayLike): blendshape values from tflite model

        Returns:
            dict: debug states
        """

        if blendshape_values is None:
            return

        if (ConfigManager().mouse_bindings |
                ConfigManager().keyboard_bindings) != self.last_know_keybinds:
            self.init_states()

        for shape_name, v in (ConfigManager().mouse_bindings |
                              ConfigManager().keyboard_bindings).items():
            if shape_name not in shape_list.blendshape_names:
                continue
            # Handle backward compatibility: old bindings have 4 elements, new ones have 6
            if len(v) >= 6:
                device, action, thres, mode, hold_mode, throttle_time_ms = v[:6]
            else:
                device, action, thres, mode = v
                hold_mode = True  # Default to hold mode for backward compatibility
                throttle_time_ms = 200.0  # Default throttle time

            # Get blendshape value
            idx = shape_list.blendshape_indices[shape_name]
            val = blendshape_values[idx]

            if (device == "mouse") and (action == "pause"):
                state_name = "mouse_" + action

                if (val > thres) and (self.key_states[state_name] is False):
                    mon_id = self.get_curr_monitor()
                    if mon_id is None:
                        return

                    MouseController().toggle_active()

                    self.key_states[state_name] = True
                elif (val < thres) and (self.key_states[state_name] is True):
                    self.key_states[state_name] = False

            elif MouseController().is_active.get():

                if device == "mouse":

                    if action == "reset":
                        state_name = "mouse_" + action
                        if (val > thres) and (self.key_states[state_name] is
                                              False):
                            mon_id = self.get_curr_monitor()
                            if mon_id is None:
                                return

                            pydirectinput.moveTo(
                                self.monitors[mon_id]["center_x"],
                                self.monitors[mon_id]["center_y"])
                            self.key_states[state_name] = True
                        elif (val < thres) and (self.key_states[state_name] is
                                                True):
                            self.key_states[state_name] = False

                    elif action == "cycle":
                        state_name = "mouse_" + action
                        if (val > thres) and (self.key_states[state_name] is
                                              False):
                            mon_id = self.get_curr_monitor()
                            next_mon_id = (mon_id + 1) % len(self.monitors)
                            pydirectinput.moveTo(
                                self.monitors[next_mon_id]["center_x"],
                                self.monitors[next_mon_id]["center_y"])
                            self.key_states[state_name] = True
                        elif (val < thres) and (self.key_states[state_name] is
                                                True):
                            self.key_states[state_name] = False

                    else:
                        self.mouse_action(val, action, thres, mode)

                elif device == "keyboard":
                    self.keyboard_action(val, action, thres, mode, hold_mode, throttle_time_ms)

    def destroy(self):
        """Destroy the keybinder"""
        return
