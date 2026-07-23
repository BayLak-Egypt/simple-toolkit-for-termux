import os
import json
import re
import importlib.util
def parse_library_links(js_filepath="libraryLinks.js"):
    """قراءة وفك شفرة ملف libraryLinks.js مع التعامل مع module.exports والتعليقات"""
    if not os.path.exists(js_filepath):
        print(f"\033[1;31m[!] Error: '{js_filepath}' not found!\033[0m")
        return []
    with open(js_filepath, "r", encoding="utf-8") as f:
        content = f.read()
    content_clean = re.sub(r'//.*', '', content)
    json_match = re.search(r'\[.*\]', content_clean, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(0))
        except Exception as e:
            print(f"\033[1;31m[!] Failed to parse JSON from {js_filepath}: {e}\033[0m")
    return []
def load_plugin_module(server_id):
    """تحميل السكربت الخاص بـ ID معين من مجلد plugins ديناميكياً"""
    plugin_path = os.path.join("plugins", f"{server_id}.py")
    if not os.path.exists(plugin_path):
        return None
    spec = importlib.util.spec_from_file_location(server_id, plugin_path)
    plugin_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(plugin_module)
    return plugin_module
def get_combined_manifest():
    """جلب شجرة الملفات والهاشات من جميع الإضافات"""
    links_data = parse_library_links()
    full_manifest = {}
    for server in links_data:
        server_id = server.get("id")
        if not server_id:
            continue
        plugin = load_plugin_module(server_id)
        if plugin and hasattr(plugin, "fetch_server_manifest"):
            server_manifest = plugin.fetch_server_manifest(server)
            for file_key, file_data in server_manifest.items():
                file_data["server_id"] = server_id
                full_manifest[file_key] = file_data
    return full_manifest
def execute_custom_download(filename, file_info, output_dir="library"):
    """استدعاء دالة التحميل الخاصة بالإضافة في حالة احتياج السيرفر لمعالجة معينة"""
    server_id = file_info.get("server_id")
    if server_id:
        plugin = load_plugin_module(server_id)
        if plugin and hasattr(plugin, "custom_download"):
            print(f"\033[1;34m[*] Executing custom plugin downloader for '{filename}'...\033[0m")
            return plugin.custom_download(filename, file_info, output_dir)
    return None