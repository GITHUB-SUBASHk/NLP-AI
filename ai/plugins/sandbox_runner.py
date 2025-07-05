# File: ai/plugins/sandbox_runner.py

"""
Safely executes plugin logic in a subprocess.
Accepts plugin name and input text.
Prevents main app from crashing due to plugin failures.
"""

from multiprocessing import Process, Pipe
import importlib
import traceback

def run_plugin_safe(plugin_name: str, input_text: str, timeout=3) -> str:
    def worker(conn):
        try:
            plugin = importlib.import_module(f"ai.plugins.{plugin_name}")
            result = plugin.handle(input_text)
            conn.send(result)
        except Exception as e:
            tb = traceback.format_exc()
            conn.send(f"[PLUGIN ERROR] {e}\n{tb}")
        finally:
            conn.close()

    parent_conn, child_conn = Pipe()
    p = Process(target=worker, args=(child_conn,))
    p.start()
    p.join(timeout)

    if p.is_alive():
        p.terminate()
        return "[PLUGIN TIMEOUT] Plugin execution took too long."

    if parent_conn.poll():
        return parent_conn.recv()

    return "[PLUGIN ERROR] No response from plugin."