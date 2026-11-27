#!/usr/bin/env python3
"""Collect the git evidence of one developer's contribution to a repository.

Read-only: it only runs git commands (and, with --platform, read-only queries
to the repository's hosting platform). Standard library only. Python 3.9+.
Run it with `python3 -I`.

Usage:
  python3 -I collect_contribution.py --repo PATH --list-authors [--mailmap FILE]
  python3 -I collect_contribution.py --repo PATH --author EMAIL_OR_NAME [--author ...] --out DIR
         [--since YYYY-MM-DD] [--until YYYY-MM-DD] [--ref REF] [--mailmap FILE]
         [--role developer|devops|qa|lead|intern] [--exclude GLOB ...] [--lang es|en]
         [--platform none|auto|github|azure|gitlab] [--platform-user LOGIN]
         [--jobs N] [--blame-copies] [--no-team-copy]

Outputs in --out:
  data.json    every metric, for checks and later comparisons
  summary.md   overview: totals, scoring inputs, identities, platform data, signals
  annex.md     full data tables, ready to paste as the report's appendices
  charts.md    Mermaid charts and text bar charts built from the data
"""

import argparse
import collections
import concurrent.futures
import datetime as dt
import fnmatch
import json
import os
import re
import shutil
import statistics
import subprocess
import sys
import threading
import unicodedata
import urllib.parse

EMPTY_TREE = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"
REFS = ["--branches", "--remotes", "--tags"]
VERSION = "2"

# ---------------------------------------------------------------- git helpers


class Git:
    def __init__(self, repo, mailmap=None):
        self.repo = repo
        self.base = ["git", "-C", repo, "-c", "core.quotepath=off", "-c", "color.ui=false"]
        if mailmap:
            self.base += ["-c", "mailmap.file=" + os.path.abspath(mailmap)]
        self._cat = None
        self._cat_lock = threading.Lock()
        self._mailmap = {}

    def run(self, *args, check=True, stdin=None):
        p = subprocess.run(self.base + list(args), input=stdin, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if check and p.returncode != 0:
            raise RuntimeError("git %s failed: %s" % (" ".join(args[:3]), p.stderr.decode("utf-8", "replace").strip()))
        return p.stdout.decode("utf-8", "replace")

    def blob(self, sha):
        with self._cat_lock:
            if self._cat is None:
                self._cat = subprocess.Popen(self.base + ["cat-file", "--batch"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            self._cat.stdin.write((sha + "\n").encode())
            self._cat.stdin.flush()
            header = self._cat.stdout.readline().decode().split()
            if len(header) < 3 or header[1] == "missing":
                return ""
            data = self._cat.stdout.read(int(header[2]))
            self._cat.stdout.read(1)
            return data.decode("utf-8", "replace")

    def canonical(self, name, email):
        """Apply .mailmap (or --mailmap) to an identity. Returns (name, lowercase email)."""
        key = (name, email)
        if key not in self._mailmap:
            out = self.run("check-mailmap", "%s <%s>" % (name or "x", email), check=False).strip()
            m = re.match(r"^(.*?)\s*<([^>]*)>$", out)
            self._mailmap[key] = (m.group(1), m.group(2).lower()) if m else (name, email.lower())
        return self._mailmap[key]


# ---------------------------------------------------------------- classification

JUNK = [r"(^|/)\.DS_Store$", r"\.log(\.\d+)?$", r"\.lck$", r"\.tmp$", r"\.swp$", r"\.class$", r"\.pyc$",
        r"(^|/)node_modules/", r"(^|/)target/", r"(^|/)dist/", r"(^|/)out/", r"(^|/)bin/(?!.*\.(sh|py)$)",
        r"(^|/)\.idea/", r"\.iml$", r"(^|/)coverage/", r"(^|/)\.gradle/", r"(^|/)build/(?!.*\.(gradle|kts)$)",
        r"(^|/)\.env(\..*)?$", r"\.(jks|p12|pem|key)$", r"(^|/)__pycache__/", r"(^|/)\.vscode/",
        r"(^|/)(test|tests|build|gradle|mvn|maven|npm|yarn|console)[_-]?(out|output|log|result|results)\.txt$"]  # tool output dumps
BOILERPLATE = [r"(^|/)gradlew(\.bat)?$", r"(^|/)gradle-wrapper\.(jar|properties)$", r"(^|/)mvnw(\.cmd)?$",
               r"(^|/)\.mvn/", r"(^|/)\.gitignore$", r"(^|/)\.gitattributes$", r"(^|/)\.editorconfig$",
               r"(^|/)LICENSE(\..*)?$", r"(^|/)lombok\.config$", r"(^|/)package-lock\.json$", r"(^|/)yarn\.lock$",
               r"(^|/)pnpm-lock\.yaml$", r"(^|/)Podfile\.lock$", r"(^|/)Gemfile\.lock$", r"(^|/)poetry\.lock$",
               r"(^|/)Cargo\.lock$", r"(^|/)go\.sum$", r"(^|/)composer\.lock$", r"\.xcworkspace/", r"\.pbxproj$",
               r"(^|/)Pods/", r"(^|/)\.dockerignore$", r"(^|/)\.prettierrc", r"(^|/)\.eslintrc", r"(^|/)tsconfig.*\.json$"]
TEST_ASSETS = [r"\.jmx$", r"(^|/)performance-test/", r"(^|/)acceptance-test/", r"(^|/)(fixtures?|__snapshots__|testdata|test-data)/",
               r"\.snap$", r"(^|/)DataSet/", r"\.feature$"]
TEST_CODE = [r"(^|/)(src/)?tests?/", r"(^|/)__tests__/", r"(^|/)spec/", r"Tests?\.[a-zA-Z]+$", r"_test\.[a-zA-Z]+$",
             r"\.(spec|test)\.[a-zA-Z]+$", r"(^|/)test_[^/]+\.py$", r"(^|/)androidTest/", r"(^|/)testFixtures/"]
DEPLOY = [r"(^|/)Dockerfile", r"(^|/)docker-compose", r"\.tf$", r"\.tfvars$",
          r"(^|/)(helm|charts|k8s|kubernetes|deploy|deployment|infra|terraform|ops)/",
          r"(^|/)\.github/workflows/", r"azure-pipelines", r"azure_build", r"(^|/)\.gitlab-ci", r"(^|/)Jenkinsfile",
          r"(^|/)bitbucket-pipelines", r"(^|/)\.circleci/", r"(^|/)Procfile$", r"(^|/)serverless\.ya?ml$", r"(^|/)skaffold"]
BUILD = [r"\.gradle(\.kts)?$", r"(^|/)gradle\.properties$", r"(^|/)pom\.xml$", r"(^|/)package\.json$", r"(^|/)build\.sbt$",
         r"(^|/)Makefile$", r"(^|/)CMakeLists\.txt$", r"\.csproj$", r"\.sln$", r"(^|/)setup\.(py|cfg)$", r"(^|/)pyproject\.toml$",
         r"(^|/)requirements.*\.txt$", r"(^|/)Cargo\.toml$", r"(^|/)go\.mod$", r"(^|/)Podfile$", r"(^|/)Package\.swift$",
         r"(^|/)Gemfile$", r"(^|/)composer\.json$", r"(^|/)pubspec\.yaml$"]
DOCS = [r"\.(md|rst|adoc|txt)$", r"(^|/)docs?/"]
CODE_EXT = {"java", "kt", "kts", "scala", "groovy", "py", "js", "jsx", "ts", "tsx", "mjs", "cjs", "vue", "svelte", "go", "rs", "rb",
            "php", "cs", "fs", "vb", "swift", "m", "mm", "c", "cc", "cpp", "cxx", "h", "hpp", "dart", "sql", "sh", "bash", "ps1",
            "lua", "r", "ex", "exs", "erl", "clj", "elm", "hs", "html", "css", "scss", "sass", "less"}
CONFIG_EXT = {"yaml", "yml", "properties", "json", "xml", "toml", "ini", "conf", "cfg", "env", "plist", "xcconfig", "graphql", "proto"}

CATEGORY_ORDER = ["prod_code", "test_code", "deploy_ci", "build", "config", "docs", "test_assets", "boilerplate", "junk", "other"]

# Categories that count as the person's own main work, by role (references/classification.md)
ROLE_OWN = {
    "developer": {"prod_code", "test_code"},
    "intern": {"prod_code", "test_code"},
    "lead": {"prod_code", "test_code"},
    "devops": {"deploy_ci", "build", "config", "prod_code"},
    "qa": {"test_code", "test_assets"},
}
COPY_THRESHOLD = 0.5  # copy ratio from which lines are not counted as own work


def _any(patterns, path):
    return any(re.search(p, path) for p in patterns)


def categorize(path):
    ext = path.rsplit(".", 1)[-1].lower() if "." in os.path.basename(path) else ""
    if _any(JUNK, path):
        return "junk"
    if _any(BOILERPLATE, path):
        return "boilerplate"
    if _any(TEST_ASSETS, path):
        return "test_assets"
    if ext in CODE_EXT and _any(TEST_CODE, path):
        return "test_code"
    if _any(DEPLOY, path):
        return "deploy_ci"
    if _any(BUILD, path):
        return "build"
    if ext in CODE_EXT:
        return "prod_code"
    if _any(DOCS, path):
        return "docs"
    if ext in CONFIG_EXT:
        return "config"
    return "other"


TEMPLATE_MARKERS = re.compile(r"(TODO|FIXME|XXX|my-operation|[Ss]ample[A-Z_]|\bsample\b|\bexample\b|[Ll]orem ipsum|placeholder|"
                              r"@generated|auto-?generated|DO NOT EDIT|Change (the )?(operation|name|this))")
_SECRET_KEY = r"(?i)(password|passwd|pwd|secret|api[_-]?key|access[_-]?key|token|private[_-]?key)[\"']?\s*[:=]\s*"
SECRET_CONFIG_RE = re.compile(_SECRET_KEY + r"[\"']?(?![$#%{<]|\s|$)[^\s\"'`]{6,}")
SECRET_CODE_RE = re.compile(_SECRET_KEY + r"[\"'](?![$#%{<])[^\s\"'`]{6,}[\"']")
PEM_RE = re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")
EMPTY_TYPE_RE = re.compile(r"\b(class|interface|struct|enum|object)\s+\w+[^{;(]*\{\s*\}", re.S)
TEST_CASE_RE = re.compile(r"(@Test\b|@ParameterizedTest\b|\bdef test_\w+|\bfunc Test\w+|\b(it|test)\s*\(\s*['\"`]|\[Fact\]|\[Test\]|\bfunc test\w+\s*\()")
ASSERT_RE = re.compile(r"([aA]ssert\w*|[eE]xpect\w*\s*\(|[vV]erify\w*\s*\(|\.should\w*|\bXCTAssert\w*|\.to(Be|Equal|Have)\w*|"
                       r"\bthen\(|\bcheck\w*\(|\brequire\.|\bfail\s*\()")
TRIVIAL = {"{", "}", "};", ");", "(", ")", "]", "[", "*/", "/*", "*", "//", "#", "---", "```", "<?php", "?>", "end", "else",
           "else {", "} else {"}
SERVICE_RE = re.compile(r"(\[bot\]|\bbot\b|-bot\b|^bot|jenkins|dependabot|renovate|github-actions|azure-?pipelines|build ?service|"
                        r"project collection|noreply|no-reply|^svc|^srv|^sa[-_.]|service[-_. ]?account|automation|^ci[-_.]|^cicd)", re.I)


def significant(line):
    s = line.strip()
    return len(s) > 3 and s not in TRIVIAL


def path_affinity(a, b):
    """Number of matching path segments, from the end and from the start."""
    pa, pb = a.split("/"), b.split("/")
    tail = 0
    while tail < min(len(pa), len(pb)) and pa[-1 - tail] == pb[-1 - tail]:
        tail += 1
    head = 0
    while head < min(len(pa), len(pb)) - tail and pa[head] == pb[head]:
        head += 1
    return tail * 2 + head


def norm_name(name):
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode().lower()
    return " ".join(re.findall(r"[a-z0-9]+", s))


def is_service(name, email):
    local = email.split("@")[0]
    return bool(SERVICE_RE.search(local) or SERVICE_RE.search(name or "") or re.match(r"^[a-z]{2,6}\d{2,}$", local))


# ---------------------------------------------------------------- parsing helpers

def resolve_rename(path):
    m = re.match(r"^(.*)\{(.*) => (.*)\}(.*)$", path)
    if m:
        return re.sub("//+", "/", m.group(1) + m.group(3) + m.group(4))
    if " => " in path:
        return path.split(" => ", 1)[1]
    return path


def parse_date(s):
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))


def iso_week(date_str):
    y, w, _ = parse_date(date_str).isocalendar()
    return "%d-W%02d" % (y, w)


def week_start(week):
    y, w = week.split("-W")
    return dt.date.fromisocalendar(int(y), int(w), 1)


def week_range(first, last):
    out, cur = [], week_start(first)
    end = week_start(last)
    while cur <= end:
        y, w, _ = cur.isocalendar()
        out.append("%d-W%02d" % (y, w))
        cur += dt.timedelta(days=7)
    return out


def median(values):
    values = list(values)
    return statistics.median(values) if values else None


# ---------------------------------------------------------------- collection

def load_commits(git, since, until, merges=False):
    args = ["log"] + REFS + ["--merges" if merges else "--no-merges", "--date-order",
                             "--format=%x1e%H%x1f%P%x1f%aN%x1f%aE%x1f%aI%x1f%s%x1f%b%x1f"]
    if not merges:
        args.append("--numstat")
    if since:
        args.append("--since=" + since)
    if until:
        args.append("--until=" + until)
    commits = []
    for chunk in git.run(*args).split("\x1e")[1:]:
        p = chunk.split("\x1f")
        cname, cemail = git.canonical(p[2], p[3])
        files = []
        for ln in p[7].strip("\n").splitlines():
            f = ln.split("\t")
            if len(f) != 3:
                continue
            binary = f[0] == "-"
            files.append({"path": resolve_rename(f[2]), "raw": f[2], "add": 0 if binary else int(f[0]),
                          "del": 0 if binary else int(f[1]), "binary": binary})
        commits.append({"sha": p[0], "short": p[0][:8], "parents": p[1].split(), "name": cname, "email": cemail,
                        "date": p[4], "subject": p[5], "body": p[6].strip(), "files": files,
                        "add": sum(x["add"] for x in files), "del": sum(x["del"] for x in files)})
    return commits


PR_PATTERNS = [r"Merged PR (\d+)", r"Merge pull request #(\d+)", r"See merge request [^\s]*!(\d+)", r"\(#(\d+)\)\s*$",
               r"\(!(\d+)\)", r"pull request #(\d+)"]


def pr_id(text):
    for p in PR_PATTERNS:
        m = re.search(p, text, re.M | re.I)
        if m:
            return m.group(1)
    return None


def author_table(git):
    out = git.run("log", *REFS, "--format=%aN%x1f%aE")
    c = collections.Counter()
    for ln in out.splitlines():
        if "\x1f" in ln:
            n, e = ln.split("\x1f", 1)
            c[git.canonical(n, e)] += 1
    by_email = collections.defaultdict(collections.Counter)
    for (n, e), k in c.items():
        by_email[e][n] += k
    return by_email


def suggest_identities(by_email):
    """Groups of emails that probably belong to the same person."""
    keys = {}
    for e, names in by_email.items():
        ks = {"local:" + e.split("@")[0]}
        for n in names:
            nn = norm_name(n)
            if len(nn.split()) >= 2:
                ks.add("name:" + nn)
        keys[e] = ks
    parent = {e: e for e in by_email}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    emails = sorted(by_email)
    for i, a in enumerate(emails):
        na = {norm_name(n) for n in by_email[a]}
        for b in emails[i + 1:]:
            nb = {norm_name(n) for n in by_email[b]}
            contained = any(len(x.split()) >= 2 and len(y.split()) >= 2 and (x in y or y in x) for x in na for y in nb)
            if keys[a] & keys[b] or contained:
                parent[find(a)] = find(b)
    groups = collections.defaultdict(list)
    for e in emails:
        groups[find(e)].append(e)
    out = []
    for g in groups.values():
        if len(g) > 1:
            main = max(g, key=lambda e: sum(by_email[e].values()))
            name = max(by_email[main], key=lambda n: (len(n.split()), by_email[main][n]))
            out.append({"canonical_name": name, "canonical_email": main, "aliases": [e for e in g if e != main],
                        "mailmap": ["%s <%s> <%s>" % (name, main, e) for e in g if e != main]})
    return out


def list_authors(git):
    by_email = author_table(git)
    rows = sorted(((sum(v.values()), e, v) for e, v in by_email.items()), reverse=True)
    print("commits  email  [names]")
    for total, e, names in rows:
        svc = any(is_service(n, e) for n in names)
        print("%7d  %s  %s%s" % (total, e, "; ".join("%s (%d)" % (n, k) for n, k in names.most_common()),
                                 "  [service account?]" if svc else ""))
    sug = suggest_identities(by_email)
    if sug:
        print("\nPossible duplicate identities (review them before using them as a mailmap):")
        for s in sug:
            for line in s["mailmap"]:
                print("  " + line)


def matches(identity, patterns):
    name, email = identity
    for p in patterns:
        pl = p.lower().strip()
        if "@" in pl:
            if email == pl:
                return True
        elif pl == email.split("@")[0] or pl in name.lower():
            return True
    return False


def blame_file(git, ref, path, copies):
    args = ["blame", "-w", "-M", "--line-porcelain"]
    if copies:
        args += ["-C", "-C"]
    out = git.run(*(args + [ref, "--", path]), check=False)
    lines, sha, name, email = [], None, "", ""
    for ln in out.splitlines():
        if re.match(r"^[0-9a-f]{40} \d+ \d+", ln):
            sha = ln[:40]
        elif ln.startswith("author "):
            name = ln[7:]
        elif ln.startswith("author-mail "):
            email = ln[12:].strip("<>").lower()
        elif ln.startswith("filename "):
            lines.append((sha, name, email, ln[9:]))
    return path, lines


def changed_lines_by_file(git, sha):
    """Added and removed lines of a commit, by path after the commit."""
    out = git.run("show", "--format=", "-U0", "--no-ext-diff", "-M", sha, check=False)
    added, removed = collections.defaultdict(list), collections.defaultdict(list)
    old = cur = None
    for ln in out.splitlines():
        if ln.startswith("diff --git "):
            old = cur = None
        elif ln.startswith("--- "):
            old = ln
        elif ln.startswith("+++ "):
            cur = None if ln.strip() == "+++ /dev/null" else (ln[6:] if ln.startswith("+++ b/") else ln[4:])
        elif cur and ln.startswith("+"):
            added[cur].append(ln[1:])
        elif cur and ln.startswith("-") and old is not None:
            removed[cur].append(ln[1:])
    return added, removed


def added_lines_by_file(git, sha):
    return changed_lines_by_file(git, sha)[0]


def build_blob_index(git):
    out = git.run("log", *REFS, "--no-merges", "--format=%x1e%H%x1f%aI%x1f%aN%x1f%aE", "--raw", "--no-abbrev", "--no-renames")
    index = collections.defaultdict(list)
    new_blob = {}
    for chunk in out.split("\x1e")[1:]:
        head, _, raw = chunk.partition("\n")
        sha, date, name, email = head.split("\x1f")
        _, cemail = git.canonical(name, email)
        for ln in raw.splitlines():
            if not ln.startswith(":"):
                continue
            meta, _, path = ln.partition("\t")
            m = meta.split()
            if m[4].startswith("D") or set(m[3]) == {"0"}:
                continue
            index[os.path.basename(path)].append((date, path, m[3], cemail, sha))
            new_blob[(sha, path)] = m[3]
    return index, new_blob


class LineSets:
    """Cache of the stripped line sets of blobs."""

    def __init__(self, git, limit=6000):
        self.git, self.limit, self.cache = git, limit, collections.OrderedDict()
        self.lock = threading.Lock()

    def get(self, blob):
        with self.lock:
            if blob in self.cache:
                self.cache.move_to_end(blob)
                return self.cache[blob]
        s = {l.strip() for l in self.git.blob(blob).splitlines()}
        with self.lock:
            self.cache[blob] = s
            if len(self.cache) > self.limit:
                self.cache.popitem(last=False)
        return s


def copy_analysis(commit, own_emails, index, linesets, added, detail):
    """Fill copy_score (and, with detail, source/similar_later/markers) for each file of a commit."""
    cdate = parse_date(commit["date"])
    for f in commit["files"]:
        f["category"] = categorize(f["path"])
        lines = added.get(f["path"], [])
        sig = [l.strip() for l in lines if significant(l)]
        f["significant"] = len(sig)
        f["copy_score"], f["copy_source"] = 0.0, None
        # standard files (gradlew, lockfiles...) are boilerplate already; their comments are not template markers
        f["template_markers"] = 0 if f["category"] == "boilerplate" else sum(1 for l in lines if TEMPLATE_MARKERS.search(l))
        if detail:
            # by file type, not category: code (also in acceptance-test/ or fixtures) only counts quoted literals
            is_code = f["path"].rsplit(".", 1)[-1].lower() in CODE_EXT if "." in os.path.basename(f["path"]) else False
            sre = SECRET_CODE_RE if is_code else SECRET_CONFIG_RE
            f["secret_suspects"] = sum(1 for l in lines if sre.search(l) or PEM_RE.search(l))
            f["similar_later"], f["replicated_later"] = None, 0
        if not sig or f["binary"]:
            continue
        same_name = [x for x in index.get(os.path.basename(f["path"]), []) if x[3] not in own_emails]
        cands = [x for x in same_name if parse_date(x[0]) < cdate]
        seen, best = set(), (0.0, None)
        for date, path, blob, email, sha in sorted(cands, key=lambda x: (-path_affinity(x[1], f["path"]), -parse_date(x[0]).timestamp())):
            if blob in seen:
                continue
            seen.add(blob)
            if len(seen) > 40:
                break
            content = linesets.get(blob)
            score = sum(1 for l in sig if l in content) / len(sig)
            if score > best[0]:
                best = (score, {"path": path, "commit": sha[:8], "date": date[:10], "author": email})
            if score >= 0.999:
                break
        f["copy_score"], f["copy_source"] = round(best[0], 3), best[1]
        if detail:
            later = [x for x in same_name if parse_date(x[0]) >= cdate and x[1] != f["path"]]
            replicas = set()
            for date, path, blob, email, sha in sorted(later)[:40]:
                content = linesets.get(blob)
                score = sum(1 for l in sig if l in content) / len(sig)
                if score >= 0.9:
                    replicas.add(path)
                if score >= 0.6 and (not f["similar_later"] or score > f["similar_later"]["score"]):
                    f["similar_later"] = {"score": round(score, 3), "path": path, "commit": sha[:8], "date": date[:10], "author": email}
            # the same file showing up later, almost unchanged, in other places by other people: usually a template
            f["replicated_later"] = len(replicas)


def generated_paths(git, paths):
    """Paths marked linguist-generated or linguist-vendored in .gitattributes."""
    if not paths:
        return set()
    out = git.run("check-attr", "--stdin", "-z", "linguist-generated", "linguist-vendored", check=False,
                  stdin="\0".join(paths).encode() + b"\0")
    parts = out.split("\0")
    res = set()
    for i in range(0, len(parts) - 2, 3):
        if parts[i + 2] in ("set", "true"):
            res.add(parts[i])
    return res


# ---------------------------------------------------------------- platform (optional, read-only)

def _run_cli(cmd, timeout=120):
    try:
        p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
    except (OSError, subprocess.TimeoutExpired) as e:
        return None, str(e)
    if p.returncode != 0:
        return None, p.stderr.decode("utf-8", "replace").strip()[:300]
    return p.stdout.decode("utf-8", "replace"), None


def _hours(a, b):
    try:
        return round((parse_date(b) - parse_date(a)).total_seconds() / 3600, 1)
    except (TypeError, ValueError, AttributeError):
        return None


def detect_platform(url):
    if "github.com" in url:
        return "github"
    if "dev.azure.com" in url or "visualstudio.com" in url:
        return "azure"
    if "gitlab" in url:
        return "gitlab"
    return None


def platform_data(git, args, target, emails):
    res = {"platform": args.platform, "status": "not requested"}
    if args.platform == "none":
        return res
    url = git.run("remote", "get-url", "origin", check=False).strip()
    plat = detect_platform(url) if args.platform == "auto" else args.platform
    res["platform"] = plat
    if not plat:
        res["status"] = "unknown platform for the origin remote"
        return res
    try:
        if plat == "github":
            return _github(url, args, target, res)
        if plat == "azure":
            return _azure(url, emails, res)
        return _gitlab(url, args, res)
    except Exception as e:  # the platform must never break the collection
        res["status"] = "error: %s" % e
    return res


def _github(url, args, target, res):
    if not shutil.which("gh"):
        res["status"] = "gh CLI not installed"
        return res
    m = re.search(r"github\.com[:/]([^/]+)/(.+?)(\.git)?$", url)
    repo = "%s/%s" % (m.group(1), m.group(2))
    login = args.platform_user
    if not login:
        for c in target[:5]:
            out, _ = _run_cli(["gh", "api", "repos/%s/commits/%s" % (repo, c["sha"]), "--jq", ".author.login"])
            if out and out.strip() and out.strip() != "null":
                login = out.strip()
                break
    if not login:
        res["status"] = "GitHub login not found; pass --platform-user"
        return res
    fields = "number,title,author,createdAt,mergedAt,state"
    authored, err = _run_cli(["gh", "pr", "list", "-R", repo, "--author", login, "--state", "all", "--limit", "1000", "--json", fields])
    if err:
        res["status"] = "error: " + err
        return res
    reviewed, _ = _run_cli(["gh", "pr", "list", "-R", repo, "--search", "reviewed-by:%s -author:%s" % (login, login), "--state", "all",
                            "--limit", "1000", "--json", fields])
    commented, _ = _run_cli(["gh", "pr", "list", "-R", repo, "--search", "commenter:%s -author:%s" % (login, login), "--state", "all",
                             "--limit", "1000", "--json", "number"])
    a, r, c = json.loads(authored or "[]"), json.loads(reviewed or "[]"), json.loads(commented or "[]")
    res.update({"status": "ok", "repo": repo, "user": login,
                "authored": [{"id": x["number"], "title": x["title"], "state": x["state"], "created": x["createdAt"][:10],
                              "hours_to_merge": _hours(x["createdAt"], x.get("mergedAt"))} for x in a],
                "reviewed": [{"id": x["number"], "title": x["title"], "author": (x.get("author") or {}).get("login"),
                              "created": x["createdAt"][:10]} for x in r],
                "commented_on_others": len(c)})
    return res


def _azure(url, emails, res):
    if not shutil.which("az"):
        res["status"] = "az CLI not installed (needs the azure-devops extension)"
        return res
    u = urllib.parse.urlparse(re.sub(r"//[^@/]+@", "//", url))
    parts = [urllib.parse.unquote(p) for p in u.path.strip("/").split("/")]
    if "dev.azure.com" in u.netloc:
        org, project, repo = "https://dev.azure.com/%s/" % parts[0], parts[1], parts[3]
    else:
        org, project, repo = "https://%s/" % u.netloc, parts[0], parts[2]
    base = ["az", "repos", "pr", "list", "--org", org, "--project", project, "--repository", repo, "--status", "all", "--top", "1000", "-o", "json"]
    authored, reviewed, errors, seen = [], [], [], set()
    for e in sorted(emails):
        out, err = _run_cli(base + ["--creator", e])
        if err:
            errors.append(err)
        for x in json.loads(out or "[]"):
            authored.append({"id": x["pullRequestId"], "title": x["title"], "state": x["status"], "created": x["creationDate"][:10],
                             "hours_to_merge": _hours(x["creationDate"], x.get("closedDate")) if x["status"] == "completed" else None})
        out, err = _run_cli(base + ["--reviewer", e])
        if err:
            errors.append(err)
        for x in json.loads(out or "[]"):
            created_by = ((x.get("createdBy") or {}).get("uniqueName") or "").lower()
            if created_by in emails or x["pullRequestId"] in seen:
                continue
            seen.add(x["pullRequestId"])
            vote = next((rv.get("vote", 0) for rv in x.get("reviewers", []) if (rv.get("uniqueName") or "").lower() in emails), 0)
            reviewed.append({"id": x["pullRequestId"], "title": x["title"], "author": created_by, "created": x["creationDate"][:10], "vote": vote})
    if errors and not authored and not reviewed:
        res["status"] = "error: " + errors[0]
        return res
    res.update({"status": "ok", "repo": "%s/%s" % (project, repo), "user": ", ".join(sorted(emails)), "authored": authored,
                "reviewed": reviewed, "voted_on_others": sum(1 for x in reviewed if x["vote"] != 0)})
    return res


def _gitlab(url, args, res):
    if not shutil.which("glab"):
        res["status"] = "glab CLI not installed"
        return res
    if not args.platform_user:
        res["status"] = "GitLab username required; pass --platform-user"
        return res
    m = re.search(r"gitlab[^/:]*[:/](.+?)(\.git)?$", url)
    repo = m.group(1) if m else ""
    out_a, err = _run_cli(["glab", "mr", "list", "-R", repo, "--author", args.platform_user, "--all", "-P", "100", "-F", "json"])
    if err:
        res["status"] = "error: " + err
        return res
    out_r, _ = _run_cli(["glab", "mr", "list", "-R", repo, "--reviewer", args.platform_user, "--all", "-P", "100", "-F", "json"])
    a, r = json.loads(out_a or "[]"), json.loads(out_r or "[]")
    res.update({"status": "ok", "repo": repo, "user": args.platform_user,
                "authored": [{"id": x["iid"], "title": x["title"], "state": x["state"], "created": x["created_at"][:10],
                              "hours_to_merge": _hours(x["created_at"], x.get("merged_at"))} for x in a],
                "reviewed": [{"id": x["iid"], "title": x["title"], "author": (x.get("author") or {}).get("username"),
                              "created": x["created_at"][:10]} for x in r if (x.get("author") or {}).get("username") != args.platform_user]})
    return res


# ---------------------------------------------------------------- analysis

def _ratio(c):
    sig = sum(f.get("significant", 0) for f in c["files"])
    return round(sum(f.get("significant", 0) * f.get("copy_score", 0) for f in c["files"]) / sig, 3) if sig else 0.0


def _band(v, cuts):
    if v is None:
        return None
    for score, cut in cuts:
        if v >= cut:
            return score
    return 1


def analyze(args):
    git = Git(args.repo, args.mailmap)
    git.run("rev-parse", "--git-dir")
    ref = args.ref or "HEAD"
    ref_sha = git.run("rev-parse", ref).strip()
    patterns = args.author
    own_cats = ROLE_OWN[args.role]

    all_commits = load_commits(git, args.since, args.until)
    merges = load_commits(git, args.since, args.until, merges=True)
    target = [c for c in all_commits if matches((c["name"], c["email"]), patterns)]
    if not target:
        sys.exit("No non-merge commits match --author %s. Run --list-authors to see the identities." % patterns)
    target_shas = {c["sha"] for c in target}
    identities = sorted({(c["name"], c["email"]) for c in target})
    target_emails = {e for _, e in identities}
    by_email = author_table(git)

    # ---- copy detection: full detail for the target, copy ratio for everyone else
    index, new_blob = build_blob_index(git)
    linesets = LineSets(git)
    analyzed = target if args.no_team_copy else all_commits

    def work(c):
        own = target_emails if c["sha"] in target_shas else {c["email"]}
        copy_analysis(c, own, index, linesets, added_lines_by_file(git, c["sha"]), detail=c["sha"] in target_shas)
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as ex:
        list(ex.map(work, analyzed))
    # ---- empty types and test assertions (code files of every analyzed commit)
    def inspect(c):
        for f in c["files"]:
            f["empty_types"], f["test_cases"], f["assertions"] = 0, None, None
            if f["binary"] or not f["add"] or f.get("category") not in ("prod_code", "test_code"):
                continue
            blob = new_blob.get((c["sha"], f["path"]))
            content = git.blob(blob) if blob else ""
            f["empty_types"] = len(EMPTY_TYPE_RE.findall(content))
            if f["category"] == "test_code":
                f["test_cases"] = len(TEST_CASE_RE.findall(content))
                f["assertions"] = len(ASSERT_RE.findall(content))
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as ex:
        list(ex.map(inspect, analyzed))
    for c in all_commits:
        for f in c["files"]:
            f.setdefault("category", categorize(f["path"]))
            f.setdefault("copy_score", 0.0)
            # template-like: scaffold markers, or a small file whose types are empty
            f["template_like"] = bool(f.get("template_markers", 0) >= 2 or (f.get("empty_types") and f.get("significant", 0) <= 15))
            f["own"] = (f["category"] in own_cats and f["copy_score"] < COPY_THRESHOLD and not f["binary"] and not f["template_like"])
        c["copy_ratio"] = _ratio(c)
        c["own_add"] = sum(f["add"] for f in c["files"] if f["own"])
        cat = collections.Counter()
        for f in c["files"]:
            cat[f["category"]] += f["add"]
        c["category_add"] = dict(cat)
        c["pr"] = pr_id(c["subject"] + "\n" + c["body"])
    own_file = {(c["sha"], f["path"]): f["own"] for c in all_commits for f in c["files"]}

    # ---- PRs
    prs = []
    for m in merges:
        if len(m["parents"]) < 2:
            continue
        inside = git.run("rev-list", "--no-merges", "%s..%s" % (m["parents"][0], m["parents"][1]), check=False).split()
        mine = [s for s in inside if s in target_shas]
        if mine:
            pid = pr_id(m["subject"] + "\n" + m["body"])
            prs.append({"merge": m["short"], "is_pr": bool(pid), "date": m["date"][:10], "completed_by": m["name"],
                        "completed_by_target": m["email"] in target_emails, "pr": pid, "title": m["subject"],
                        "target_commits": len(mine), "total_commits": len(inside)})
    squash_prs = [c for c in target if c["pr"]]

    # ---- blame at ref
    numstat = git.run("diff", "--numstat", "-z", "--no-renames", EMPTY_TREE, ref_sha)
    candidates = []
    for rec in numstat.split("\0"):
        f = rec.split("\t")
        if len(f) == 3 and f[0] != "-":
            candidates.append(f[2])
    excluded_glob = {p for p in candidates if any(fnmatch.fnmatch(p, g) for g in (args.exclude or []))}
    generated = generated_paths(git, candidates)
    files = [p for p in candidates if p not in generated and p not in excluded_glob]
    blame = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as ex:
        for path, lines in ex.map(lambda p: blame_file(git, ref_sha, p, args.blame_copies), files):
            blame[path] = lines

    canon = {}
    total_lines = 0
    by_author = collections.Counter()
    by_author_cat = collections.defaultdict(collections.Counter)
    own_surviving = collections.Counter()
    tgt_by_file = collections.Counter()
    tgt_by_commit = collections.Counter()
    file_authors = {}
    for path, lines in blame.items():
        cat = categorize(path)
        fa = collections.Counter()
        for sha, name, email, origname in lines:
            if (name, email) not in canon:
                canon[(name, email)] = git.canonical(name, email)[1]
            e = canon[(name, email)]
            total_lines += 1
            by_author[e] += 1
            by_author_cat[e][cat] += 1
            fa[e] += 1
            if own_file.get((sha, origname), own_file.get((sha, path), False)):
                own_surviving[e] += 1
            if sha in target_shas:
                tgt_by_commit[sha[:8]] += 1
            if e in target_emails:
                tgt_by_file[path] += 1
        file_authors[path] = fa
    tgt_surviving = sum(by_author[e] for e in target_emails)

    # ---- fate of the files the target touched
    touched = collections.defaultdict(lambda: {"added": 0, "commits": 0})
    for c in target:
        for f in c["files"]:
            t = touched[f["path"]]
            t["added"] += f["add"]
            t["commits"] += 1
            t["category"] = f["category"]
    created = set()
    for c in target:
        for ln in git.run("show", "--format=", "--diff-filter=A", "--name-only", "-M", c["sha"]).splitlines():
            if ln.strip():
                created.add(ln.strip())
    file_fate = []
    fmt = "--format=%h%x1f%aN%x1f%aI%x1f%s"
    for path, t in touched.items():
        alive = path in blame
        row = {"path": path, "category": t["category"], "added": t["added"], "commits": t["commits"],
               "created_by_target": path in created, "exists_at_ref": alive, "excluded": path in generated or path in excluded_glob,
               "target_lines_now": tgt_by_file.get(path, 0), "total_lines_now": len(blame.get(path, []))}
        if alive:
            row["top_other_authors_now"] = [(k, v) for k, v in file_authors[path].most_common() if k not in target_emails][:3]
        elif path in created and not row["excluded"]:
            out = git.run("log", ref_sha, "--full-history", "--diff-filter=D", "-1", fmt, "--", path, check=False).strip()
            if not out:
                out = git.run("log", ref_sha, "-m", "--full-history", "--diff-filter=D", "-1", fmt, "--", path, check=False).strip()
            row["deleted_by"] = None
            if out:
                h, n, d, s = out.split("\x1f", 3)
                row["deleted_by"] = {"commit": h, "author": n, "date": d[:10], "subject": s}
        file_fate.append(row)

    # ---- team and activity
    weeks = collections.defaultdict(lambda: [0, 0])
    team = collections.defaultdict(lambda: {"name": collections.Counter(), "commits": 0, "added": 0, "deleted": 0, "own_add": 0,
                                            "first": None, "last": None, "weeks": set()})
    for c in all_commits:
        w = iso_week(c["date"])
        weeks[w][0 if c["sha"] in target_shas else 1] += 1
        t = team[c["email"]]
        t["name"][c["name"]] += 1
        t["commits"] += 1
        t["added"] += c["add"]
        t["deleted"] += c["del"]
        t["own_add"] += c["own_add"]
        t["weeks"].add(w)
        d = c["date"][:10]
        t["first"] = min(t["first"] or d, d)
        t["last"] = max(t["last"] or d, d)
    for w in (week_range(min(weeks), max(weeks)) if weeks else []):
        weeks.setdefault(w, [0, 0])
    display = {e: max(t["name"], key=lambda n: (len(n.split()), t["name"][n])) for e, t in team.items()}
    dup = collections.Counter(display.values())
    team_rows = []
    for e, t in team.items():
        team_rows.append({"email": e, "name": display[e] if dup[display[e]] == 1 else "%s <%s>" % (display[e], e),
                          "is_target": e in target_emails, "is_service": any(is_service(n, e) for n in t["name"]),
                          "commits": t["commits"], "added": t["added"], "deleted": t["deleted"], "own_added": t["own_add"],
                          "first": t["first"], "last": t["last"], "active_weeks": len(t["weeks"]),
                          "surviving": by_author.get(e, 0), "surviving_prod": by_author_cat[e].get("prod_code", 0),
                          "surviving_test": by_author_cat[e].get("test_code", 0), "surviving_own": own_surviving.get(e, 0),
                          "own_durability": round(min(1.0, own_surviving.get(e, 0) / t["own_add"]), 3) if t["own_add"] else None})
    team_rows.sort(key=lambda r: -r["commits"])

    # ---- signals
    signals = []
    subj_day = collections.Counter((c["date"][:10], c["subject"].strip().lower()) for c in target)
    for (d, s), k in sorted(subj_day.items()):
        if k > 1:
            signals.append({"type": "repeated_subject_same_day", "date": d, "subject": s, "count": k})
    ordered = sorted(target, key=lambda c: c["date"])
    for c in ordered:
        if c["add"] >= 1000:
            signals.append({"type": "large_commit", "commit": c["short"], "added": c["add"], "copy_ratio": c["copy_ratio"]})
        for f in c["files"]:
            if f["category"] == "junk" and (c["sha"], f["path"]) in new_blob:  # added or changed, not deleted
                signals.append({"type": "junk_file", "commit": c["short"], "path": f["path"], "added": f["add"]})
            if f.get("secret_suspects"):
                signals.append({"type": "possible_secret", "commit": c["short"], "path": f["path"], "lines": f["secret_suspects"]})
            if f.get("template_markers"):
                signals.append({"type": "template_markers", "commit": c["short"], "path": f["path"], "lines": f["template_markers"]})
            if f.get("own") and f.get("replicated_later", 0) >= 2:
                signals.append({"type": "replicated_later", "commit": c["short"], "path": f["path"], "count": f["replicated_later"],
                                "added": f["add"]})
            if f.get("empty_types"):
                signals.append({"type": "empty_type", "commit": c["short"], "path": f["path"], "count": f["empty_types"]})
            if f.get("test_cases") and f["assertions"] < f["test_cases"]:
                signals.append({"type": "weak_test", "commit": c["short"], "path": f["path"], "tests": f["test_cases"], "assertions": f["assertions"]})
    # a fix commit that removes or changes lines the same person added in the previous 3 days
    fix_re = re.compile(r"(?i)\b(fix|hotfix|correcci[oó]n|corrige|arregl|revert|bug)")
    for i, c in enumerate(ordered):
        if not fix_re.search(c["subject"]):
            continue
        _, removed = changed_lines_by_file(git, c["sha"])
        removed = {p: {l.strip() for l in ls if significant(l)} for p, ls in removed.items()}
        for prev in reversed(ordered[max(0, i - 10):i]):
            if (parse_date(c["date"]) - parse_date(prev["date"])).days > 3:
                continue
            prev_added = changed_lines_by_file(git, prev["sha"])[0]
            hit = [p for p, ls in removed.items() if ls & {l.strip() for l in prev_added.get(p, [])}]
            if hit:
                signals.append({"type": "self_fix", "commit": c["short"], "fixes": prev["short"], "subject": c["subject"], "paths": hit})
                break
    co_authored = []
    for p in patterns:
        co_authored += git.run("log", *REFS, "-i", "--format=%h %aN %s", "--grep", "Co-authored-by:.*" + re.escape(p)).strip().splitlines()

    # ---- scoring inputs (references/scoring.md)
    repo_dates = sorted(c["date"][:10] for c in all_commits)
    tdates = sorted(c["date"][:10] for c in target)
    active = [r for r in team_rows if not r["is_target"] and not r["is_service"] and r["commits"] >= 5]
    med_own = median(r["surviving_own"] for r in active)
    med_dur = median(r["own_durability"] for r in active if r["own_durability"] is not None)
    tgt_own_surv = sum(own_surviving.get(e, 0) for e in target_emails)
    tgt_own_add = sum(c["own_add"] for c in target)
    durability = round(min(1.0, tgt_own_surv / tgt_own_add), 3) if tgt_own_add else None
    span = week_range(iso_week(ordered[0]["date"]), max(weeks)) if weeks else []
    tgt_weeks = {iso_week(c["date"]) for c in target}
    weeks_ratio = round(len(tgt_weeks) / len(span), 3) if span else None
    gap_days = (dt.date.fromisoformat(repo_dates[-1]) - dt.date.fromisoformat(tdates[-1])).days
    team_after = sum(1 for c in all_commits if c["date"][:10] > tdates[-1])
    d1_ratio = round(tgt_own_surv / med_own, 3) if med_own else None
    d6 = _band(weeks_ratio, [(5, 0.8), (4, 0.6), (3, 0.4), (2, 0.2)])
    if d6 and gap_days > 28 and team_after:
        d6 = min(d6, 2)
    scoring = {
        "role": args.role, "own_categories": sorted(own_cats), "copy_threshold": COPY_THRESHOLD,
        "active_people": [r["name"] for r in active],
        "d1": {"own_surviving": tgt_own_surv, "team_median_own_surviving": med_own, "ratio": d1_ratio,
               "suggested": _band(d1_ratio, [(5, 1.0), (4, 0.6), (3, 0.3), (2, 0.1)])},
        "d4": {"own_added": tgt_own_add, "own_surviving": tgt_own_surv, "durability": durability, "team_median_durability": med_dur,
               "suggested": _band(durability, [(5, 0.7), (4, 0.5), (3, 0.3), (2, 0.1)])},
        "d6": {"active_weeks": len(tgt_weeks), "weeks_in_span": len(span), "ratio": weeks_ratio, "days_without_commits_at_end": gap_days,
               "team_commits_after_last": team_after, "suggested": d6},
    }

    data = {
        "tool_version": VERSION, "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "repo": os.path.abspath(args.repo), "ref": ref, "ref_sha": ref_sha[:8], "since": args.since, "until": args.until,
        "lang": args.lang, "author_patterns": patterns, "identities": [{"name": n, "email": e} for n, e in identities],
        "identity_suggestions": suggest_identities(by_email),
        "service_accounts": sorted(r["email"] for r in team_rows if r["is_service"]),
        "excluded": {"globs": args.exclude or [], "by_glob": len(excluded_glob), "generated_or_vendored": len(generated)},
        "totals": {
            "commits": len(target), "added": sum(c["add"] for c in target), "deleted": sum(c["del"] for c in target),
            "own_added": tgt_own_add, "file_changes": sum(len(c["files"]) for c in target),
            "merges_by_target": sum(1 for m in merges if m["email"] in target_emails),
            "prs_with_target_commits": sum(1 for p in prs if p["is_pr"]),
            "prs_completed_by_target": sum(1 for p in prs if p["is_pr"] and p["completed_by_target"]),
            "other_merges_with_target_commits": sum(1 for p in prs if not p["is_pr"]),
            "squash_pr_commits": len(squash_prs), "co_authored_commits": len(co_authored),
            "first_commit": tdates[0], "last_commit": tdates[-1], "repo_first_commit": repo_dates[0], "repo_last_commit": repo_dates[-1],
            "surviving_lines": tgt_surviving, "own_surviving_lines": tgt_own_surv, "repo_lines_at_ref": total_lines,
            "surviving_share": round(tgt_surviving / total_lines, 4) if total_lines else 0,
        },
        "scoring_inputs": scoring,
        "added_by_category": dict(sum((collections.Counter(c["category_add"]) for c in target), collections.Counter())),
        "surviving_by_category": dict(sum((by_author_cat[e] for e in target_emails), collections.Counter())),
        "commits": [dict({k: c[k] for k in ("short", "date", "subject", "add", "del", "copy_ratio", "own_add", "category_add", "pr")},
                         files=c["files"], surviving_lines=tgt_by_commit.get(c["short"], 0)) for c in ordered],
        "prs": prs, "squash_prs": [{"commit": c["short"], "pr": c["pr"], "subject": c["subject"]} for c in squash_prs],
        "co_authored": co_authored, "platform": platform_data(git, args, ordered, target_emails),
        "weekly": [{"week": w, "target": v[0], "team": v[1]} for w, v in sorted(weeks.items())],
        "team": team_rows, "file_fate": sorted(file_fate, key=lambda r: -r["added"]),
        "surviving_by_file": tgt_by_file.most_common(), "signals": signals,
    }
    data["marker"] = {"tool_version": VERSION, "ref_sha": data["ref_sha"], "role": args.role, "commits": len(target),
                      "added": data["totals"]["added"], "own_added": tgt_own_add, "surviving": tgt_surviving,
                      "own_surviving": tgt_own_surv, "last_commit": tdates[-1], "active_weeks": len(tgt_weeks)}
    return data


# ---------------------------------------------------------------- rendering

L = {
    "es": {
        "cat": {"prod_code": "Código de producción", "test_code": "Código de pruebas", "deploy_ci": "Despliegue / CI", "build": "Build",
                "config": "Configuración", "docs": "Documentación", "test_assets": "Plantillas y datos de prueba",
                "boilerplate": "Archivos estándar", "junk": "Archivos que no deberían estar en git", "other": "Otros"},
        "pie_added": "Líneas agregadas por categoría", "pie_surv": "Líneas vigentes hoy por categoría",
        "copy_title": "Líneas agregadas: copia de archivos existentes vs. nuevas en el repo",
        "copied": "Copiadas de archivos existentes (>=80%)", "adapted": "Adaptadas (50-80%)", "new": "Nuevas en el repo (<50%)",
        "team_commits": "Commits sin merges por autor", "team_surv": "Líneas vigentes por autor",
        "team_own": "Trabajo propio vigente por autor (sin plantillas ni copias)",
        "weekly": "Commits por semana (barras: equipo, línea: desarrollador)", "commits": "Commits", "lines": "Líneas", "week": "Semana",
        "dev": "Desarrollador", "team": "Resto del equipo", "tpl": "plantilla", "yes": "sí", "no": "**no**", "renamed": "renombrado o movido",
        "deleted": "borrado en `%s` por %s el %s: %s", "excluded": "excluido del análisis",
        "A": "### A. Todos los commits", "A_h": "| Commit | Fecha | + | − | % copia | Propias | Vigentes hoy | PR | Asunto |",
        "B": "### B. Archivos por commit y su origen",
        "B_note": "«%% copia»: parte de sus líneas significativas que ya existía igual en un archivo anterior de otra persona. "
                  "«Parecido posterior»: archivo de otra persona, creado después en otra ruta, que coincide en más del 60 %%. "
                  "«Propia»: cuenta como trabajo propio para el rol (%s) y tiene menos del 50 %% de copia; «plantilla» si tiene marcadores de plantilla o solo tipos vacíos.",
        "B_h": "| Archivo | Categoría | + | − | % copia | Propia | Origen | Parecido posterior | Plantilla | Tipos vacíos | Pruebas / aserciones | ¿Secreto? |",
        "C": "### C. Destino de los archivos que tocó",
        "C_h": "| Archivo | Categoría | + suyas | Lo creó | Existe hoy | Suyas hoy / total | Otros autores hoy o quién lo borró |",
        "D": "### D. Equipo",
        "D_note": "Trabajo propio: líneas en las categorías propias del rol, con menos del 50 % de copia y sin aspecto de plantilla, medido igual para todos. "
                  "Durabilidad: trabajo propio vigente / trabajo propio agregado. (S): cuenta de servicio, fuera de las medianas.",
        "D_h": "| Autor | Commits | + | Propias + | Semanas activas | Primero | Último | Vigentes | Producción vigente | Pruebas vigente | Propias vigentes | Durabilidad |",
        "E": "### E. Pull requests", "E_h": "| Merge | Fecha | PR | Completado por | Sus commits / total | Título |",
        "E_other": "Otros merges que llevaron sus commits (sincronizaciones de rama o sin número de PR): ",
        "E_plat": "#### PRs en la plataforma (%s)", "E_plat_a": "| PR propio | Fecha | Estado | Horas hasta el merge | Título |",
        "E_plat_r": "| PR de otros que revisó | Fecha | Autor | Voto | Título |", "E_none": "No hay PRs con sus commits.",
        "F": "### F. Señales del script", "F_h": "| Señal | Commit | Detalle | Revisión |", "F_todo": "<por revisar>",
        "G": "### G. Líneas vigentes por archivo", "G_h": "| Líneas | Archivo |", "H": "### H. Cómo reproducir",
        "sig": {"repeated_subject_same_day": "Asunto repetido el mismo día", "large_commit": "Commit grande",
                "junk_file": "Archivo que no debería estar en git", "possible_secret": "Posible secreto (solo ubicación)",
                "template_markers": "Marcadores de plantilla", "empty_type": "Clase o tipo vacío",
                "weak_test": "Prueba con menos aserciones que casos", "self_fix": "Corrige un commit propio",
                "replicated_later": "Propio, pero repetido casi igual después en otros sitios (¿plantilla?)"},
    },
    "en": {
        "cat": {"prod_code": "Production code", "test_code": "Test code", "deploy_ci": "Deployment / CI", "build": "Build",
                "config": "Configuration", "docs": "Documentation", "test_assets": "Test templates and data",
                "boilerplate": "Standard files", "junk": "Files that should not be in git", "other": "Other"},
        "pie_added": "Added lines by category", "pie_surv": "Lines still present by category",
        "copy_title": "Added lines: copied from existing files vs. new to the repo",
        "copied": "Copied from existing files (>=80%)", "adapted": "Adapted (50-80%)", "new": "New to the repo (<50%)",
        "team_commits": "Non-merge commits by author", "team_surv": "Lines still present by author",
        "team_own": "Own work still present by author (no templates or copies)",
        "weekly": "Commits per week (bars: team, line: developer)", "commits": "Commits", "lines": "Lines", "week": "Week",
        "dev": "Developer", "team": "Rest of the team", "tpl": "template", "yes": "yes", "no": "**no**", "renamed": "renamed or moved",
        "deleted": "deleted in `%s` by %s on %s: %s", "excluded": "excluded from the analysis",
        "A": "### A. All commits", "A_h": "| Commit | Date | + | − | % copy | Own | Still present | PR | Subject |",
        "B": "### B. Files per commit and their source",
        "B_note": "\"%% copy\": share of their significant lines that already existed verbatim in an earlier file by someone else. "
                  "\"Similar later\": a file by someone else, created later at another path, matching more than 60%%. "
                  "\"Own\": counts as own work for the role (%s) and has less than 50%% copy; \"template\" if it has template markers or only empty types.",
        "B_h": "| File | Category | + | − | % copy | Own | Source | Similar later | Template | Empty types | Tests / assertions | Secret? |",
        "C": "### C. Fate of the files they touched",
        "C_h": "| File | Category | + theirs | Created by them | Exists today | Theirs today / total | Other authors today or who deleted it |",
        "D": "### D. Team",
        "D_note": "Own work: lines in the role's own categories, with less than 50% copy and not template-like, measured the same way for everyone. "
                  "Durability: own work still present / own work added. (S): service account, left out of the medians.",
        "D_h": "| Author | Commits | + | Own + | Active weeks | First | Last | Still present | Production present | Tests present | Own present | Durability |",
        "E": "### E. Pull requests", "E_h": "| Merge | Date | PR | Completed by | Their commits / total | Title |",
        "E_other": "Other merges that carried their commits (branch syncs or without a PR number): ",
        "E_plat": "#### PRs on the platform (%s)", "E_plat_a": "| Own PR | Date | State | Hours to merge | Title |",
        "E_plat_r": "| Others' PR they reviewed | Date | Author | Vote | Title |", "E_none": "No PRs contain their commits.",
        "F": "### F. Script signals", "F_h": "| Signal | Commit | Detail | Review |", "F_todo": "<to review>",
        "G": "### G. Lines still present per file", "G_h": "| Lines | File |", "H": "### H. How to reproduce",
        "sig": {"repeated_subject_same_day": "Subject repeated on the same day", "large_commit": "Large commit",
                "junk_file": "File that shouldn't be in git", "possible_secret": "Possible secret (location only)",
                "template_markers": "Template markers", "empty_type": "Empty class or type",
                "weak_test": "Test with fewer assertions than cases", "self_fix": "Fixes one of their own commits",
                "replicated_later": "Own, but repeated almost unchanged later elsewhere (template?)"},
    },
}


def esc(s):
    return str(s).replace("|", "\\|")


def fmt_num(n, lang):
    s = "{:,}".format(n)
    return s.replace(",", ".") if lang == "es" else s


def bars(rows, lang, width=40):
    if not rows:
        return ""
    mx = max(v for _, v in rows) or 1
    lw = max(len(k) for k, _ in rows)
    total = sum(v for _, v in rows) or 1
    out = []
    for k, v in rows:
        n = v / mx * width
        bar = "█" * int(n) + ("▌" if n - int(n) >= 0.5 else "")
        pct = "%.1f%%" % (100 * v / total)
        out.append("%s  %s %s %7s" % (k.ljust(lw), bar.ljust(width + 1), fmt_num(v, lang).rjust(8), pct.replace(".", ",") if lang == "es" else pct))
    return "```text\n" + "\n".join(out) + "\n```"


def mq(s):
    return '"%s"' % str(s).replace('"', "'")


def render_charts(d):
    lang, T, out = d["lang"], L[d["lang"]], []

    def pie(title, rows):
        rows = [r for r in rows if r[1]]
        out.append("### %s\n\n```mermaid\npie showData\n    title %s\n%s\n```\n\n%s\n" % (
            title, title, "\n".join("    %s : %d" % (mq(k), v) for k, v in rows), bars(rows, lang)))
    for key, src in (("pie_added", "added_by_category"), ("pie_surv", "surviving_by_category")):
        pie(T[key], sorted(((T["cat"][k], d[src].get(k, 0)) for k in CATEGORY_ORDER), key=lambda r: -r[1]))
    copied = adapted = new = 0
    for c in d["commits"]:
        for f in c["files"]:
            if f["binary"] or not f["add"]:
                continue
            if f["copy_score"] >= 0.8:
                copied += f["add"]
            elif f["copy_score"] >= 0.5:
                adapted += f["add"]
            else:
                new += f["add"]
    pie(T["copy_title"], [(T["copied"], copied), (T["adapted"], adapted), (T["new"], new)])

    def team_chart(title, key, ylabel, top=10):
        people = [r for r in d["team"] if not r["is_service"]]
        rows = sorted(((r["name"] + (" ◀" if r["is_target"] else ""), r[key]) for r in people), key=lambda x: -x[1])[:top]
        if not any(k.endswith(" ◀") for k, _ in rows):
            rows += [(r["name"] + " ◀", r[key]) for r in people if r["is_target"]]
        out.append("### %s\n\n```mermaid\nxychart-beta\n    title %s\n    x-axis [%s]\n    y-axis %s 0 --> %d\n    bar [%s]\n```\n\n%s\n" % (
            title, mq(title), ", ".join(mq(k.replace(" ◀", "")) for k, _ in rows), mq(ylabel), max([v for _, v in rows] + [1]),
            ", ".join(str(v) for _, v in rows), bars(rows, lang)))
    team_chart(T["team_commits"], "commits", T["commits"])
    team_chart(T["team_surv"], "surviving", T["lines"])
    team_chart(T["team_own"], "surviving_own", T["lines"])
    wk = d["weekly"]
    if wk:
        out.append("### %s\n\n```mermaid\nxychart-beta\n    title %s\n    x-axis [%s]\n    y-axis %s 0 --> %d\n    bar [%s]\n    line [%s]\n```\n" % (
            T["weekly"], mq(T["weekly"]), ", ".join(mq(w["week"][2:]) for w in wk), mq(T["commits"]),
            max(max(w["team"], w["target"]) for w in wk) or 1, ", ".join(str(w["team"]) for w in wk), ", ".join(str(w["target"]) for w in wk)))
        out.append("| %s | %s | %s |\n|---|---|---|\n" % (T["week"], T["dev"], T["team"]) + "\n".join(
            "| %s (%s) | %s | %d |" % (w["week"], week_start(w["week"]).isoformat(), "**0**" if not w["target"] else w["target"], w["team"])
            for w in wk) + "\n")
    return "\n".join(out)


def render_annex(d):
    lang, T = d["lang"], L[d["lang"]]
    pct = lambda x: "%d%%" % round(100 * x)
    yes = lambda b: T["yes"] if b else ""
    o = [T["A"], "", T["A_h"], "|---|---|---|---|---|---|---|---|---|"]
    for c in d["commits"]:
        o.append("| `%s` | %s | %d | %d | %s | %d | %d | %s | %s |" % (c["short"], c["date"][:10], c["add"], c["del"], pct(c["copy_ratio"]),
                                                                    c["own_add"], c["surviving_lines"], c["pr"] or "", esc(c["subject"])))
    o += ["", T["B"], "", T["B_note"] % ", ".join(T["cat"][k] for k in d["scoring_inputs"]["own_categories"]), ""]
    for c in d["commits"]:
        if not c["files"]:
            continue
        o += ["**`%s` · %s · %s**" % (c["short"], c["date"][:10], esc(c["subject"])), "", T["B_h"], "|---|---|---|---|---|---|---|---|---|---|---|---|"]
        for f in c["files"]:
            s, l = f["copy_source"], f.get("similar_later")
            tests = "%d / %d" % (f["test_cases"], f["assertions"]) if f.get("test_cases") is not None else ""
            o.append("| `%s` | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |" % (
                f["path"], T["cat"][f["category"]], "bin" if f["binary"] else f["add"], "bin" if f["binary"] else f["del"], pct(f["copy_score"]),
                yes(f["own"]) or (T["tpl"] if f.get("template_like") else ""), ("%s `%s` %s `%s`" % (s["author"].split("@")[0], s["commit"], s["date"], s["path"])) if s else "",
                ("%s %s `%s` %s" % (pct(l["score"]), l["author"].split("@")[0], l["commit"], l["date"])) if l else "",
                f.get("template_markers") or "", f.get("empty_types") or "", tests, f.get("secret_suspects") or ""))
        o.append("")
    o += [T["C"], "", T["C_h"], "|---|---|---|---|---|---|---|"]
    for r in d["file_fate"]:
        if r["exists_at_ref"]:
            x = ", ".join("%s %d" % (k.split("@")[0], v) for k, v in r.get("top_other_authors_now", []))
        elif r.get("excluded"):
            x = T["excluded"]
        else:
            b = r.get("deleted_by")
            x = (T["deleted"] % (b["commit"], esc(b["author"]), b["date"], esc(b["subject"]))) if b else T["renamed"]
        o.append("| `%s` | %s | %d | %s | %s | %d / %d | %s |" % (r["path"], T["cat"][r["category"]], r["added"], yes(r["created_by_target"]),
                                                               T["yes"] if r["exists_at_ref"] else T["no"], r["target_lines_now"], r["total_lines_now"], x))
    o += ["", T["D"], "", T["D_note"], "", T["D_h"], "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in d["team"]:
        b = "**" if r["is_target"] else ""
        o.append("| %s%s%s%s | %d | %d | %d | %d | %s | %s | %d | %d | %d | %d | %s |" % (
            b, esc(r["name"]), b, " (S)" if r["is_service"] else "", r["commits"], r["added"], r["own_added"], r["active_weeks"], r["first"],
            r["last"], r["surviving"], r["surviving_prod"], r["surviving_test"], r["surviving_own"],
            pct(r["own_durability"]) if r["own_durability"] is not None else "—"))
    o += ["", T["E"], ""]
    real = [p for p in d["prs"] if p["is_pr"]]
    if real:
        o += [T["E_h"], "|---|---|---|---|---|---|"]
        o += ["| `%s` | %s | %s | %s | %d / %d | %s |" % (p["merge"], p["date"], p["pr"], esc(p["completed_by"]), p["target_commits"],
                                                       p["total_commits"], esc(p["title"])) for p in real]
    else:
        o.append(T["E_none"])
    other = [p for p in d["prs"] if not p["is_pr"]]
    if other:
        o += ["", T["E_other"] + ", ".join("`%s`" % p["merge"] for p in other) + "."]
    pl = d["platform"]
    if pl.get("status") == "ok":
        o += ["", T["E_plat"] % pl["platform"], "", T["E_plat_a"], "|---|---|---|---|---|"]
        o += ["| %s | %s | %s | %s | %s |" % (x["id"], x["created"], x["state"], x["hours_to_merge"] if x["hours_to_merge"] is not None else "—",
                                             esc(x["title"])) for x in pl["authored"]]
        o += ["", T["E_plat_r"], "|---|---|---|---|---|"]
        o += ["| %s | %s | %s | %s | %s |" % (x["id"], x["created"], esc(x.get("author") or ""), x.get("vote", ""), esc(x["title"])) for x in pl["reviewed"]]
    o += ["", T["F"], "", T["F_h"], "|---|---|---|---|"]
    for s in d["signals"]:
        t = s["type"]
        detail = {
            "repeated_subject_same_day": lambda: "\"%s\" × %d (%s)" % (esc(s["subject"]), s["count"], s["date"]),
            "large_commit": lambda: "+%d, %s" % (s["added"], pct(s["copy_ratio"])),
            "junk_file": lambda: "`%s` (+%d)" % (s["path"], s["added"]),
            "possible_secret": lambda: "`%s` (%d)" % (s["path"], s["lines"]),
            "template_markers": lambda: "`%s` (%d)" % (s["path"], s["lines"]),
            "empty_type": lambda: "`%s` (%d)" % (s["path"], s["count"]),
            "replicated_later": lambda: "`%s` (+%d, %d copias)" % (s["path"], s["added"], s["count"]) if lang == "es"
                                         else "`%s` (+%d, %d copies)" % (s["path"], s["added"], s["count"]),
            "weak_test": lambda: "`%s` (%d / %d)" % (s["path"], s["tests"], s["assertions"]),
            "self_fix": lambda: "→ `%s`: %s" % (s["fixes"], esc(s["subject"])),
        }[t]()
        o.append("| %s | %s | %s | %s |" % (T["sig"][t], ("`%s`" % s["commit"]) if s.get("commit") else "—", detail, T["F_todo"]))
    o += ["", T["G"], "", T["G_h"], "|---|---|"] + ["| %d | `%s` |" % (n, p) for p, n in d["surviving_by_file"]]
    cmd = ["python3 -I <skill>/scripts/collect_contribution.py --repo <repo>"] + ["--author '%s'" % a for a in d["author_patterns"]]
    cmd += ["--ref %s" % d["ref"], "--role %s" % d["scoring_inputs"]["role"], "--lang %s" % lang]
    cmd += (["--since %s" % d["since"]] if d["since"] else []) + (["--until %s" % d["until"]] if d["until"] else [])
    cmd += ["--exclude '%s'" % g for g in d["excluded"]["globs"]]
    cmd += ["--platform %s" % d["platform"]["platform"]] if d["platform"].get("status") == "ok" else []
    cmd += ["--out \"$(mktemp -d)\""]
    o += ["", T["H"], "", "```bash", " \\\n  ".join(cmd), "```", "",
          "<!-- developer-contribution-analysis: %s -->" % json.dumps(d["marker"], ensure_ascii=False)]
    return "\n".join(o) + "\n"


def render_summary(d):
    t, s = d["totals"], d["scoring_inputs"]
    o = ["# Data summary · collect_contribution.py v%s" % VERSION, "",
         "- Repo: `%s` · ref `%s` (`%s`) · %s → %s" % (d["repo"], d["ref"], d["ref_sha"], d["since"] or t["repo_first_commit"],
                                                     d["until"] or t["repo_last_commit"]),
         "- Identities: " + ", ".join("%s <%s>" % (i["name"], i["email"]) for i in d["identities"]),
         "- Role: %s (own categories: %s)" % (s["role"], ", ".join(s["own_categories"])),
         "- Excluded: globs %s (%d files), generated/vendored by .gitattributes: %d files" % (
             ", ".join(d["excluded"]["globs"]) or "none", d["excluded"]["by_glob"], d["excluded"]["generated_or_vendored"]),
         "- Service accounts (left out of team medians): " + (", ".join(d["service_accounts"]) or "none"), "",
         "## Totals", "", "| Metric | Value |", "|---|---|"]
    o += ["| %s | %s |" % (k, v) for k, v in t.items()]
    o += ["", "## Scoring inputs (references/scoring.md)", "", "Active people for the medians: " + (", ".join(s["active_people"]) or "none"), "",
          "| Dimension | Metrics | Suggested score |", "|---|---|---|",
          "| D1 | own work present %s vs. team median %s → ratio %s | %s |" % (
              s["d1"]["own_surviving"], s["d1"]["team_median_own_surviving"], s["d1"]["ratio"], s["d1"]["suggested"]),
          "| D4 | own work present %s / own work added %s → %s (team median %s) | %s |" % (
              s["d4"]["own_surviving"], s["d4"]["own_added"], s["d4"]["durability"], s["d4"]["team_median_durability"], s["d4"]["suggested"]),
          "| D6 | %s active weeks / %s → %s; %s days without commits at the end; %s team commits after their last | %s |" % (
              s["d6"]["active_weeks"], s["d6"]["weeks_in_span"], s["d6"]["ratio"], s["d6"]["days_without_commits_at_end"],
              s["d6"]["team_commits_after_last"], s["d6"]["suggested"]),
          "", "D2, D3 and D5 come from the commit review. The suggested D1, D4 and D6 follow the anchors; adjust them only with a written reason."]
    o += ["", "## Added and present by category", "", "| Category | Added | Still present |", "|---|---|---|"]
    o += ["| %s | %d | %d |" % (k, d["added_by_category"].get(k, 0), d["surviving_by_category"].get(k, 0)) for k in CATEGORY_ORDER
          if d["added_by_category"].get(k) or d["surviving_by_category"].get(k)]
    if d["identity_suggestions"]:
        o += ["", "## Possible duplicate identities", "", "If they are right, save them to a temporary mailmap, pass --mailmap and run again:", "", "```text"]
        o += [line for g in d["identity_suggestions"] for line in g["mailmap"]] + ["```"]
    pl = d["platform"]
    o += ["", "## Platform", "", "- %s · status: %s" % (pl.get("platform"), pl.get("status"))]
    if pl.get("status") == "ok":
        merged = [x["hours_to_merge"] for x in pl["authored"] if x.get("hours_to_merge") is not None]
        o += ["- Authored PRs: %d (median hours to merge: %s)" % (len(pl["authored"]), median(merged)),
              "- Others' PRs they reviewed: %d" % len(pl["reviewed"])]
        for key, label in (("voted_on_others", "With a vote"), ("commented_on_others", "Others' PRs they commented on")):
            if key in pl:
                o.append("- %s: %d" % (label, pl[key]))
    o += ["", "## Signals", ""] + (["- " + json.dumps(x, ensure_ascii=False) for x in d["signals"]] or ["- none"])
    o += ["", "Full tables: annex.md · charts: charts.md"]
    return "\n".join(o) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", default=".")
    ap.add_argument("--list-authors", action="store_true")
    ap.add_argument("--author", action="append", help="email (exact) or name fragment; repeat for aliases")
    ap.add_argument("--since")
    ap.add_argument("--until")
    ap.add_argument("--ref", help="branch or commit for blame (default HEAD)")
    ap.add_argument("--mailmap", help="extra mailmap file to unify identities")
    ap.add_argument("--role", default="developer", choices=sorted(ROLE_OWN))
    ap.add_argument("--exclude", action="append", help="glob of paths to leave out of blame (repeatable)")
    ap.add_argument("--blame-copies", action="store_true", help="git blame -C -C: attribute moved or copied lines to their origin (slower)")
    ap.add_argument("--no-team-copy", action="store_true", help="detect copying only for the analyzed person (faster, less fair)")
    ap.add_argument("--platform", default="none", choices=["none", "auto", "github", "azure", "gitlab"],
                    help="read PRs and reviews from the hosting platform with gh, az or glab (read-only)")
    ap.add_argument("--platform-user", help="login on the platform; on GitHub it is found from the commits if omitted")
    ap.add_argument("--jobs", type=int, default=min(8, os.cpu_count() or 4), help="parallel git processes")
    ap.add_argument("--lang", default="es", choices=["es", "en"])
    ap.add_argument("--out")
    a = ap.parse_args()
    git = Git(a.repo, a.mailmap)
    if a.list_authors:
        list_authors(git)
        return
    if not a.author or not a.out:
        ap.error("--author and --out are required")
    a.jobs = max(1, a.jobs)
    data = analyze(a)
    os.makedirs(a.out, exist_ok=True)
    for name, content in (("data.json", json.dumps(data, ensure_ascii=False, indent=1)), ("summary.md", render_summary(data)),
                          ("annex.md", render_annex(data)), ("charts.md", render_charts(data))):
        with open(os.path.join(a.out, name), "w", encoding="utf-8") as fh:
            fh.write(content)
    t = data["totals"]
    print("OK %d commits, +%d/-%d (own work +%d), %d lines present (%.1f%% of %d), own work present %d, %d PRs, platform: %s. "
          "Files in %s: data.json, summary.md, annex.md, charts.md"
          % (t["commits"], t["added"], t["deleted"], t["own_added"], t["surviving_lines"], 100 * t["surviving_share"], t["repo_lines_at_ref"],
             t["own_surviving_lines"], t["prs_with_target_commits"], data["platform"]["status"], a.out))


if __name__ == "__main__":
    main()
