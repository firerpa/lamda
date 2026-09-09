# Copyright 2025 rev1si0n (lamda.devel@gmail.com). All rights reserved.
#
# Distributed under MIT license.
# See file LICENSE for detail or copy at https://opensource.org/licenses/MIT
#
# ===================================================================
# Official FireRPA MCP extension, turning your phone into an AI AGENT
# ===================================================================
#
import json
import xml.etree.ElementTree as etree

from lamda.mcp import *
from lamda.client import *
from lamda.utils import getprop
from lamda.extensions import BaseMcpExtension, to_json_string
from google.protobuf.json_format import MessageToDict
from xmltodict import parse as xml2dict


prompt = """
# Android Automation Guidelines

You are an expert in Android automation, capable of using specialized tools to accurately complete user-requested operations. You understand and can precisely execute each step in the automation process.

## Quality Assurance
- Prioritize using layout information for identifying operational elements. You should always use non-repeating criteria for judgment.
- Resource-id may be duplicated, and duplicate ids should not be used.
- Each operation should have a certain interval; otherwise, the page may not be fully loaded.
- Never use screenshot to detect coordinates.

## Communication
- Follow the user's language preferences"""


class FireRpaMcpExtension(BaseMcpExtension):
    """Your primary task is to help users automate Android device control using AI through this MCP service."""
    route = "/firerpa/mcp/"
    name = "firerpa"
    version = "1.0"
    @mcp("tool", description="Dumps android window's layout hierarchy as JSON string.")
    def dump_window_hierarchy(self, ctx, compressed: Annotated[bool, "Enables or disables layout hierarchy compression, default true."] = True):
        data = self.device.dump_window_hierarchy(compressed).getvalue()
        return self.remove_attrs_and_empty(data)
    @mcp("tool", description="Perform a click at arbitrary coordinates on the display.")
    def click(self, ctx, pointX: Annotated[int, "X coordinate."], pointY: Annotated[int, "Y coordinate."]):
        result = self.device.click(Point(x=pointX, y=pointY))
        return str(result).lower()
    @mcp("tool", description="Perform a swipe between two points.")
    def swipe(self, ctx, fromX: Annotated[int, "Swipe-from X coordinate."], fromY: Annotated[int, "Swipe-from Y coordinate."], toX: Annotated[int, "Swipe-to X coordinate."], toY: Annotated[int, "Swipe-to Y coordinate."], step: Annotated[int, "Step to inject between two points"] = 32):
        result = self.device.swipe(Point(x=fromX, y=fromY), Point(x=toX, y=toY), step=step)
        return str(result).lower()
    @mcp("tool", description="Perform a drag between two points.")
    def drag(self, ctx, fromX: Annotated[int, "Drag-from X coordinate."], fromY: Annotated[int, "Drag-from Y coordinate."], toX: Annotated[int, "Drag-to X coordinate."], toY: Annotated[int, "Drag-to Y coordinate."]):
        result = self.device.drag(Point(x=fromX, y=fromY), Point(x=toX, y=toY))
        return str(result).lower()
    @mcp("tool", description="Get device information such as screen width, height, brand, etc.")
    def get_deviec_info(self, ctx):
        info = self.device.device_info()
        return to_json_string(MessageToDict(info))
    @mcp("tool", description="Display a toast message on the screen.")
    def show_toast(self, ctx, message: Annotated[str, "The toast message."]):
        result = self.device.show_toast(message)
        return str(result).lower()
    @mcp("tool", description="Execute script in the device's shell foreground.")
    def execute_shell_script_foreground(self, ctx, scrip: Annotated[str, "Shell script content."]):
        result = self.device.execute_script(scrip)
        return to_json_string(MessageToDict(result))
    @mcp("tool", description="Wake up the device.")
    def wake_up(self, ctx):
        result = self.device.wake_up()
        return str(result).lower()
    @mcp("tool", description="Turn off the device screen.")
    def sleep(self, ctx):
        result = self.device.sleep()
        return str(result).lower()
    @mcp("tool", description="Check if the device screen is lit up.")
    def is_screen_on(self, ctx):
        result = self.device.is_screen_on()
        return str(result).lower()
    @mcp("tool", description="Check is the device screen locked.")
    def is_screen_locked(self, ctx):
        result = self.device.is_screen_locked()
        return str(result).lower()
    @mcp("tool", description="Get the device clipboard content.")
    def get_clipboard_text(self, ctx):
        result = self.device.get_clipboard()
        return result
    @mcp("tool", description="Set the device clipboard content.")
    def set_clipboard_text(self, ctx, text: Annotated[str, "The text to set."]):
        result = self.device.set_clipboard(text)
        return str(result).lower()
    @mcp("tool", description="Simulates a short press using a key code.")
    def press_key_code(self, ctx, key_code: Annotated[int, "The Android's KeyEvent keycode."]):
        result = self.device.press_keycode(key_code)
        return str(result).lower()
    @mcp("tool", description="Get the last displayed toast on the system.")
    def get_last_toast(self, ctx):
        result = self.device.get_last_toast()
        return to_json_string(MessageToDict(result))
    @mcp("tool", description="Read android system property by name.")
    def getprop(self, ctx, name: Annotated[str, "Android system property name."]):
        return getprop(name) or ""
    @mcp("tool", description="Use full text matching to click on an element.")
    def click_by_text(self, ctx, text: Annotated[str, "The full text field."]):
        result = self.device(text=text).click_exists()
        return str(result).lower()
    @mcp("tool", description="Use text contains matching to click on an element.")
    def click_by_text_contains(self, ctx, substring: Annotated[str, "The substring to be matched."]):
        result = self.device(textContains=substring).click_exists()
        return str(result).lower()
    @mcp("tool", description="Use text regex matching to click on an element.")
    def click_by_text_matches(self, ctx, regex: Annotated[str, "The string matching the element's text."]):
        result = self.device(textMatches=regex).click_exists()
        return str(result).lower()
    @mcp("tool", description="Use full description matching to click on an element.")
    def click_by_description(self, ctx, text: Annotated[str, "The full description field."]):
        result = self.device(description=text).click_exists()
        return str(result).lower()
    @mcp("tool", description="Use description contains matching to click on an element.")
    def click_by_description_contains(self, ctx, substring: Annotated[str, "The substring to be matched."]):
        result = self.device(descriptionContains=substring).click_exists()
        return str(result).lower()
    @mcp("tool", description="Use description regex matching to click on an element.")
    def click_by_description_matches(self, ctx, regex: Annotated[str, "The string matching the element's description."]):
        result = self.device(descriptionMatches=regex).click_exists()
        return str(result).lower()
    @mcp("tool", description="Use resourceId to click on an element, if the resource-id is duplicated, it cannot be used.")
    def click_by_resource_id(self, ctx, resource_id: Annotated[str, "Elements's resourceId (resourceName)."]):
        result = self.device(resourceId=resource_id).click_exists()
        return str(result).lower()
    @mcp("tool", description="Use resourceId to input text into an input element, if the resource-id is duplicated, it cannot be used.")
    def set_text_by_resource_id(self, ctx, resource_id: Annotated[str, "Input elements's resourceId (resourceName)."], text: Annotated[str, "The input text."]):
        result = self.device(resourceId=resource_id).set_text(text)
        return str(result).lower()
    @mcp("tool", description="Use className to input text into an input element.")
    def set_text_by_class_name(self, ctx, class_name: Annotated[str, "Input elements's className. eg: android.widget.EditText"], text: Annotated[str, "The input text."]):
        result = self.device(className=class_name).set_text(text)
        return str(result).lower()
    @mcp("tool", description="Get information about the currently running foreground application.")
    def current_top_application_info(self, ctx):
        result = self.device.current_application().info()
        return to_json_string(MessageToDict(result))
    @mcp("tool", description="Use the package name to launch an Android app.")
    def start_application_by_id(self, ctx, package_name: Annotated[str, "The package name, such as com.android.settings."]):
        result = self.device.application(package_name).start()
        return str(result).lower()
    @mcp("tool", description="Use the package name to close an Android app.")
    def stop_application_by_id(self, ctx, package_name: Annotated[str, "The package name, such as com.android.settings."]):
        result = self.device.application(package_name).stop()
        return str(result).lower()
    @mcp("tool", description="Use the package name to check if the application is installed.")
    def is_application_installed(self, ctx, package_name: Annotated[str, "The package name, such as com.android.settings."]):
        result = self.device.application(package_name).is_installed()
        return str(result).lower()
    @mcp("tool", description="Check if the application is running in the foreground using the package name.")
    def is_application_running_foreground(self, ctx, package_name: Annotated[str, "The package name, such as com.android.settings."]):
        result = self.device.application(package_name).is_foreground()
        return str(result).lower()
    @mcp("tool", description="Get all manifest permissions of the application using the package name.")
    def list_application_permissions(self, ctx, package_name: Annotated[str, "The package name, such as com.android.settings."]):
        result = self.device.application(package_name).permissions()
        return to_json_string(result)
    @mcp("tool", description="Grant the application runtime permissions.")
    def grant_application_permission(self, ctx, package_name: Annotated[str, "The package name, such as com.android.settings."], permission: Annotated[str, "The android runtime permissions."]):
        result = self.device.application(package_name).grant(permission)
        return str(result).lower()
    @mcp("tool", description="Revoke the application's runtime permissions.")
    def revoke_application_permission(self, ctx, package_name: Annotated[str, "The package name, such as com.android.settings."], permission: Annotated[str, "The android runtime permissions."]):
        result = self.device.application(package_name).revoke(permission)
        return str(result).lower()
    @mcp("tool", description="Check if the application has been granted runtime permissions.")
    def is_permission_granted(self, ctx, package_name: Annotated[str, "The package name, such as com.android.settings."], permission: Annotated[str, "The android runtime permissions."]):
        result = self.device.application(package_name).is_permission_granted(permission)
        return str(result).lower()
    @mcp("prompt")
    def agent(self, ctx):
        return PromptMessage(role="user", content=TextContent(text=prompt))
    def remove_attrs_and_empty(self, xml):
        """ remove unnecessery node info to reduce token usage """
        specified_attrs = {"clickable", "scrollable", "checkable", "enabled",
                        "focusable", "long-clickable", "password", "visible-to-user",
                        "drawing-order", "hint", "display-id", "package", "focused"}
        def clean_element(element, parent=None):
            if element.attrib.get("package") == "com.android.systemui" and parent is not None:
                parent.remove(element)
                return True
            attrs_to_remove = {attr for attr, value in element.attrib.items()
                            if attr in specified_attrs or not value.strip()}
            for attr in attrs_to_remove:
                del element.attrib[attr]
            for i in range(len(element) - 1, -1, -1):
                clean_element(element[i], element)
        root = etree.fromstring(xml)
        clean_element(root)
        return json.dumps(xml2dict(etree.tostring(root, encoding="utf-8").decode(),
                            attr_prefix=""), ensure_ascii=False, separators=(",", ":"))