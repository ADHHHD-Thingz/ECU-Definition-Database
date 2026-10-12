import importlib.util
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).parents[1] / "tools" / "definition_audit.py"
spec = importlib.util.spec_from_file_location("definition_audit", MODULE_PATH)
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


class DefinitionAuditTests(unittest.TestCase):
    def test_xml_counts_namespaced_elements(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "sample.xml"
            path.write_text(
                '<root xmlns="urn:test"><ecu_struct><map><eattributes /></map>'
                '<map><eattributes /></map></ecu_struct><romid /></root>',
                encoding="utf-8",
            )
            result = audit.audit_xml(path, path.stat().st_size)
            self.assertEqual(result["xml_parse"], "ok")
            self.assertEqual(result["map_count"], 2)
            self.assertEqual(result["eattributes_count"], 2)
            self.assertEqual(result["ecu_struct_count"], 1)
            self.assertEqual(result["romid_count"], 1)

    def test_bad_xml_is_recorded(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "broken.xml"
            path.write_text("<root><map>", encoding="utf-8")
            result = audit.audit_xml(path, path.stat().st_size)
            self.assertEqual(result["xml_parse"], "error")
            self.assertIn("xml_error", result)

    def test_hash_is_deterministic(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "sample.bin"
            path.write_bytes(b"ecu-rom")
            self.assertEqual(audit.sha256_file(path), audit.sha256_file(path))


if __name__ == "__main__":
    unittest.main()
