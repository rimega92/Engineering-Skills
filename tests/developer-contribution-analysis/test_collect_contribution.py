"""Tests for developer-contribution-analysis/scripts/collect_contribution.py.

They build a small git repository with known cases (a copy, own code, a template,
a junk file, a weak test, a deletion by someone else, a PR merge, a rename followed
by a fix, an alias, a service account and a generated file) and check what the
script reports. Run from the repository root:

    python3 -m unittest discover -s tests/developer-contribution-analysis -v
"""

import filecmp
import json
import os
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SCRIPT = os.path.join(ROOT, "es", "developer-contribution-analysis", "scripts", "collect_contribution.py")
SCRIPT_EN = os.path.join(ROOT, "en", "developer-contribution-analysis", "scripts", "collect_contribution.py")

ALICE = ("Alice Smith", "alice@example.com")
BOB = ("Bob Jones", "bob@example.com")
BOB_ALIAS = ("Bob Jones", "bob.jones@personal.example")
SVC = ("svc01", "svc01@example.com")

APP = "\n".join(["package app;", "", "public class App {"] +
                ["    public int value%d(int x) { return x * %d + %d; }" % (i, i, i * 3) for i in range(20)] + ["}", ""])
CALC = "\n".join(["package app;", "", "public class Calc {"] +
                 ["    public long op%d(long a, long b) { return (a ^ %d) + (b << %d) - %d; }" % (i, i, i % 7, i * 11) for i in range(15)] +
                 ["}", ""])
CALC_TEST = """package app;

import org.junit.jupiter.api.Test;

class CalcTest {
    @Test
    void opZeroRuns() {
        new Calc().op0(1, 2);
    }

    @Test
    void opOneRuns() {
        new Calc().op1(3, 4);
    }
}
"""
LISTENER = """package app;

public class Listener {
    // TODO: Change operation name
    private final String op = "my-operation";
    // private final SampleUseCase useCase;
    public void process(String message) {
        // return useCase.sample(message);
    }
}
"""
GRADLEW = """#!/bin/sh
#   * For example: a user cannot expect ${Hostname} to be expanded, as it is an environment variable
#   * and will be expanded by the shell before the script starts.
exec java -classpath "$CLASSPATH" org.gradle.wrapper.GradleWrapperMain "$@"
"""
LIMITS = "request-limit: 100\ntimeout-ms: 1500\nretries: 3\n"
CONFIG = "\n".join(["server:", "  port: 8080", "app:"] + ["  key%d: value-%d" % (i, i) for i in range(10)] + [""])


class Repo:
    def __init__(self, path):
        self.path = path
        self.day = 0
        self.git("init", "-q", "-b", "main")
        self.git("config", "user.name", "Test")
        self.git("config", "user.email", "test@example.com")
        self.git("config", "commit.gpgsign", "false")

    def git(self, *args, author=None):
        env = dict(os.environ)
        if author:
            date = "2026-01-%02dT10:00:00+00:00" % (1 + self.day)
            env.update({"GIT_AUTHOR_NAME": author[0], "GIT_AUTHOR_EMAIL": author[1], "GIT_COMMITTER_NAME": author[0],
                        "GIT_COMMITTER_EMAIL": author[1], "GIT_AUTHOR_DATE": date, "GIT_COMMITTER_DATE": date})
        return subprocess.run(["git", "-C", self.path] + list(args), check=True, env=env, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE).stdout.decode()

    def write(self, rel, content):
        full = os.path.join(self.path, rel)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as fh:
            fh.write(content)

    def commit(self, author, message, files=None, remove=None):
        for rel, content in (files or {}).items():
            self.write(rel, content)
        for rel in remove or []:
            self.git("rm", "-q", rel)
        self.git("add", "-A")
        self.git("commit", "-q", "-m", message, author=author)
        self.day += 1


def build_repo(path):
    r = Repo(path)
    r.commit(ALICE, "Create app", {"svc-a/src/main/java/app/App.java": APP, "svc-a/deploy/config/app.yaml": CONFIG,
                                   ".gitattributes": "gen/** linguist-generated\n"})
    r.commit(BOB, "Create service b", {"svc-b/src/main/java/app/App.java": APP})                       # copy of Alice's file
    r.commit(BOB, "Add calculator", {"svc-b/src/main/java/app/Calc.java": CALC,                          # own code
                                     "svc-b/src/test/java/app/CalcTest.java": CALC_TEST})                # tests without assertions
    r.commit(BOB, "Add listener", {"svc-b/src/main/java/app/Listener.java": LISTENER,                    # template
                                   "svc-b/app.log": "started\nconnected\nstopped\n"})                    # junk
    r.git("mv", "svc-a/deploy/config", "svc-a/deploy/cfg")
    r.commit(BOB, "Rename config folder")                                                                # rename only
    r.commit(BOB, "fix: port", {"svc-a/deploy/cfg/app.yaml": CONFIG.replace("8080", "9090")})           # not a self-fix
    r.commit(BOB_ALIAS, "Tune calculator", {"svc-b/src/main/java/app/Calc.java": CALC + "// tuned by bob\n"})
    r.commit(SVC, "Bump version", {"version.txt": "1.0.1\n"})
    r.commit(ALICE, "Remove listener", remove=["svc-b/src/main/java/app/Listener.java"])                 # deleted by someone else
    r.commit(BOB, "Add generated client", {"gen/Client.java": "class Client { int a; int b; }\n"})       # linguist-generated
    r.commit(BOB, "Add gradle wrapper", {"svc-b/gradlew": GRADLEW})                                    # boilerplate with "For example"
    r.commit(ALICE, "Add limits", {"svc-b/limits.yaml": LIMITS})
    r.commit(BOB, "Add burst limit", {"svc-b/limits.yaml": LIMITS + "burst-limit: 15\n"})
    r.commit(BOB, "fix: burst limit", {"svc-b/limits.yaml": LIMITS + "burst-limit: 25\n"})           # fixes their own line
    r.commit(BOB, "fix: request limit", {"svc-b/limits.yaml":                                          # same file, Alice's line
                                          LIMITS.replace("request-limit: 100", "request-limit: 120") + "burst-limit: 25\n"})
    r.git("checkout", "-q", "-b", "feature")
    r.commit(BOB, "Add feature", {"svc-b/src/main/java/app/Feature.java":
                                  "package app;\n\npublic class Feature {\n    public boolean enabled(int flags) { return (flags & 0x4) != 0; }\n}\n"})
    r.git("checkout", "-q", "main")
    r.git("merge", "-q", "--no-ff", "-m", "Merged PR 42: Add feature", "feature", author=ALICE)
    return r


class CollectContributionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.repo = os.path.join(cls.tmp.name, "repo")
        os.makedirs(cls.repo)
        build_repo(cls.repo)
        cls.out = {}
        for lang in ("es", "en"):
            out = os.path.join(cls.tmp.name, "out-" + lang)
            subprocess.run([sys.executable, "-I", SCRIPT, "--repo", cls.repo, "--author", BOB[1], "--author", BOB_ALIAS[1],
                            "--lang", lang, "--out", out], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            cls.out[lang] = out
        with open(os.path.join(cls.out["es"], "data.json"), encoding="utf-8") as fh:
            cls.data = json.load(fh)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def file(self, path):
        for c in self.data["commits"]:
            for f in c["files"]:
                if f["path"] == path:
                    return f
        self.fail("file not found: " + path)

    def signals(self, kind):
        return [s for s in self.data["signals"] if s["type"] == kind]

    def test_scripts_are_identical_in_both_languages(self):
        self.assertTrue(filecmp.cmp(SCRIPT, SCRIPT_EN, shallow=False))

    def test_counts_commits_of_all_identities(self):
        self.assertEqual(self.data["totals"]["commits"], 12)
        self.assertEqual({i["email"] for i in self.data["identities"]}, {BOB[1], BOB_ALIAS[1]})

    def test_detects_copy_and_its_source(self):
        f = self.file("svc-b/src/main/java/app/App.java")
        self.assertGreaterEqual(f["copy_score"], 0.99)
        self.assertEqual(f["copy_source"]["author"], ALICE[1])
        self.assertFalse(f["own"])

    def test_own_code_is_own(self):
        self.assertTrue(self.file("svc-b/src/main/java/app/Calc.java")["own"])

    def test_template_is_not_own(self):
        f = self.file("svc-b/src/main/java/app/Listener.java")
        self.assertTrue(f["template_like"])
        self.assertFalse(f["own"])

    def test_junk_and_weak_tests(self):
        self.assertTrue(any(s["path"] == "svc-b/app.log" for s in self.signals("junk_file")))
        weak = [s for s in self.signals("weak_test") if s["path"].endswith("CalcTest.java")]
        self.assertEqual(len(weak), 1)
        self.assertEqual((weak[0]["tests"], weak[0]["assertions"]), (2, 0))

    def subject_of(self, short):
        return next(c["subject"] for c in self.data["commits"] if c["short"] == short)

    def test_self_fix_only_when_it_changes_their_own_lines(self):
        fixes = {self.subject_of(s["commit"]): self.subject_of(s["fixes"]) for s in self.signals("self_fix")}
        self.assertEqual(fixes, {"fix: burst limit": "Add burst limit"})  # not "fix: port" (after a rename) nor "fix: request limit"

    def test_no_template_markers_in_standard_files(self):
        self.assertEqual(self.file("svc-b/gradlew")["template_markers"], 0)
        self.assertFalse(any(s["path"].endswith("gradlew") for s in self.signals("template_markers")))

    def test_deleted_by_someone_else(self):
        row = next(r for r in self.data["file_fate"] if r["path"].endswith("Listener.java"))
        self.assertFalse(row["exists_at_ref"])
        self.assertEqual(row["deleted_by"]["author"], ALICE[0])

    def test_pr_merge_is_detected(self):
        prs = [p for p in self.data["prs"] if p["is_pr"]]
        self.assertEqual([p["pr"] for p in prs], ["42"])
        self.assertEqual(self.data["totals"]["prs_with_target_commits"], 1)

    def test_identity_suggestion_and_service_account(self):
        aliases = [a for s in self.data["identity_suggestions"] for a in [s["canonical_email"]] + s["aliases"]]
        self.assertIn(BOB_ALIAS[1], aliases)
        self.assertIn(BOB[1], aliases)
        self.assertIn(SVC[1], self.data["service_accounts"])

    def test_generated_files_are_excluded_from_blame(self):
        self.assertEqual(self.data["excluded"]["generated_or_vendored"], 1)
        self.assertNotIn("gen/Client.java", dict(self.data["surviving_by_file"]))

    def test_team_copy_detection_is_symmetric(self):
        alice = next(r for r in self.data["team"] if r["email"] == ALICE[1])
        self.assertGreater(alice["own_added"], 0)
        self.assertGreater(alice["surviving_own"], 0)

    def test_scoring_inputs(self):
        s = self.data["scoring_inputs"]
        self.assertEqual(s["d1"]["own_surviving"], self.data["totals"]["own_surviving_lines"])
        self.assertIsNotNone(s["d4"]["durability"])
        self.assertIn(s["d6"]["suggested"], (1, 2, 3, 4, 5))

    def test_outputs_are_localized_and_complete(self):
        for lang, heading in (("es", "### A. Todos los commits"), ("en", "### A. All commits")):
            with open(os.path.join(self.out[lang], "annex.md"), encoding="utf-8") as fh:
                annex = fh.read()
            self.assertIn(heading, annex)
            self.assertIn("<!-- developer-contribution-analysis: ", annex)
            for name in ("data.json", "summary.md", "charts.md"):
                self.assertTrue(os.path.exists(os.path.join(self.out[lang], name)))

    def test_list_authors(self):
        out = subprocess.run([sys.executable, "-I", SCRIPT, "--repo", self.repo, "--list-authors"], check=True,
                             stdout=subprocess.PIPE).stdout.decode()
        self.assertIn("[service account?]", out)
        self.assertIn("<bob", out)


if __name__ == "__main__":
    unittest.main()
