import tempfile
import unittest
from pathlib import Path
from unittest import mock

from liveproof.config import load_settings
from liveproof.generators import FAMILIES, generate_tasks
from liveproof.io import read_tasks, write_jsonl
from liveproof.schema import stable_hash
from liveproof.verifier import solve, verify


class LiveProofTest(unittest.TestCase):
    def test_generation_is_deterministic(self):
        left = [task.private_record() for task in generate_tasks("seed", 12, profile="easy")]
        right = [task.private_record() for task in generate_tasks("seed", 12, profile="easy")]

        self.assertEqual(stable_hash(left), stable_hash(right))

    def test_all_families_are_generated_and_solved(self):
        tasks = generate_tasks("coverage", len(FAMILIES) * 2)
        self.assertEqual({task.family for task in tasks}, set(FAMILIES))

        for task in tasks:
            ok, note = verify(task, solve(task))
            self.assertTrue(ok, f"{task.id}: {note}")

    def test_extreme_profile_is_auditable(self):
        tasks = generate_tasks("extreme-coverage", len(FAMILIES), profile="extreme")
        self.assertEqual({task.family for task in tasks}, set(FAMILIES))

        for task in tasks:
            ok, note = verify(task, solve(task))
            self.assertTrue(ok, f"{task.id}: {note}")

    def test_wrong_answer_rejected(self):
        task = generate_tasks("wrong", 1)[0]
        ok, _ = verify(task, "definitely wrong")

        self.assertFalse(ok)

    def test_answer_tag_is_extracted(self):
        task = generate_tasks("tagged", 1)[0]
        ok, note = verify(task, f"scratch text <answer>{solve(task)}</answer>")

        self.assertTrue(ok, note)

    def test_jsonl_roundtrip(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "tasks.jsonl"
            tasks = generate_tasks("roundtrip", 4)
            write_jsonl(path, (task.private_record() for task in tasks))

            loaded = read_tasks(path)

        self.assertEqual([task.id for task in loaded], [task.id for task in tasks])
        self.assertEqual([solve(task) for task in loaded], [solve(task) for task in tasks])

    def test_numbered_nvidia_keys_are_loaded(self):
        env = {
            "NVIDIA_API_KEYS": "shared-a,shared-b",
            "NVIDIA_API_KEY_1": "shared-a",
            "NVIDIA_API_KEY_2": "numbered-b",
            "NVIDIA_API_KEY_3": "numbered-c",
        }
        with mock.patch.dict("os.environ", env, clear=True):
            settings = load_settings()

        self.assertEqual(settings.api_keys, ("shared-a", "shared-b", "numbered-b", "numbered-c"))


if __name__ == "__main__":
    unittest.main()
