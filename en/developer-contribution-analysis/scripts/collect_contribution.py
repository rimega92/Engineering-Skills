#!/usr/bin/env python3
"""Collect the git evidence of one developer's contribution to a repository.

Read-only: it only runs git commands that do not change the repository.
Standard library only. Run it with `python3 -I`.

Usage:
  python3 -I collect_contribution.py --repo PATH --list-authors
  python3 -I collect_contribution.py --repo PATH --author EMAIL_OR_NAME [--author ...]
         [--since YYYY-MM-DD] [--until YYYY-MM-DD] [--ref REF] [--mailmap FILE]
         [--exclude GLOB ...] [--lang es|en] [--blame-copies] --out DIR

Outputs in --out:
  data.json    every metric, for the report and for later checks
  summary.md   the same data as readable tables
  charts.md    ready-to-paste Mermaid charts and text bar charts
"""

import argparse
import collections
import concurrent.futures
import datetime as dt
import fnmatch
import json
import os
import re
import subprocess
import sys

EMPTY_TREE = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"
REFS = ["--branches", "--remotes", "--tags"]

# ---------------------------------------------------------------- git helpers

class Git:
    def __init__(self, repo, mailmap=None):
        self.repo = repo
        self.base = ["git", "-C", repo, "-c", "core.quotepath=off", "-c", "color.ui=false"]
        if mailmap:
            self.base += ["-c", "mailmap.file=" + os.path.abspath(mailmap)]
        self._cat = None
        self._mailmap_cache = {}

    def run(self, *args, check=True):
        p = subprocess.run(self.base + list(args), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if check and p.returncode != 0:
            raise RuntimeError("git %s failed: %s" % (" ".join(args[:3]), p.stderr.decode("utf-8", "replace").strip()))
        return p.stdout.decode("utf-8", "replace")

    def blob(self, sha):
        if self._cat is None:
            self._cat = subprocess.Popen(self.base + ["cat-file", "--batch"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        self._cat.stdin.write((sha + "\n").encode())
        self._cat.stdin.flush()
        header = self._cat.stdout.readline().decode().split()
        if len(header) < 3 or header[1] == "missing":
            return ""
        size = int(header[2])
        data = self._cat.stdout.read(size)
        self._cat.stdout.read(1)
        return data.decode("utf-8", "replace")

    def canonical(self, name, email):
        """Apply .mailmap (or --mailmap) to an identity."""
        key = (name, email)
        if key not in self._mailmap_cache:
            out = self.run("check-mailmap", "%s <%s>" % (name or "x", email), check=False).strip()
            m = re.match(r"^(.*?)\s*<([^>]*)>$", out)
            self._mailmap_cache[key] = (m.group(1), m.group(2).lower()) if m else (name, email.lower())
        return self._mailmap_cache[key]


# ---------------------------------------------------------------- classification

JUNK = [r"(^|/)\.DS_Store$", r"\.log(\.\d+)?$", r"\.lck$", r"\.tmp$", r"\.swp$", r"\.class$", r"\.pyc$",
        r"(^|/)node_modules/", r"(^|/)target/", r"(^|/)dist/", r"(^|/)out/", r"(^|/)bin/(?!.*\.(sh|py)$)",
        r"(^|/)\.idea/", r"\.iml$", r"(^|/)coverage/", r"(^|/)\.gradle/", r"(^|/)build/(?!.*\.(gradle|kts)$)",
        r"(^|/)\.env(\..*)?$", r"\.(jks|p12|pem|key)$", r"(^|/)__pycache__/", r"(^|/)\.vscode/"]
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
DEPLOY = [r"(^|/)Dockerfile", r"(^|/)docker-compose", r"\.tf$", r"\.tfvars$", r"(^|/)(helm|charts|k8s|kubernetes|deploy|deployment|infra|infrastructure-as-code|terraform|ops)/",
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
SECRET_CONFIG_RE = re.compile(_SECRET_KEY + r"[\"']?(?![$#%{<]|\s|$)[^\s\"'`]{6,}")  # config files: quoted or not
SECRET_CODE_RE = re.compile(_SECRET_KEY + r"[\"'](?![$#%{<])[^\s\"'`]{6,}[\"']")      # code: only string literals
PEM_RE = re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")
TRIVIAL = {"{", "}", "};", ");", "(", ")", "]", "[", "*/", "/*", "*", "//", "#", "---", "```", "<?php", "?>", "end", "else", "else {", "} else {"}


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


def significant(line):
    s = line.strip()
    return len(s) > 3 and s not in TRIVIAL


# ---------------------------------------------------------------- parsing helpers

def resolve_rename(path):
    m = re.match(r"^(.*)\{(.*) => (.*)\}(.*)$", path)
    if m:
        return re.sub("//+", "/", m.group(1) + m.group(3) + m.group(4))
    if " => " in path:
        return path.split(" => ", 1)[1]
    return path


def iso_week(date_str):
    d = dt.datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    y, w, _ = d.isocalendar()
    return "%d-W%02d" % (y, w)


def week_start(week):
    y, w = week.split("-W")
    return dt.date.fromisocalendar(int(y), int(w), 1)


def parse_date(s):
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))


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
    out = git.run(*args)
    commits = []
    for chunk in out.split("\x1e")[1:]:
        parts = chunk.split("\x1f")
        sha, parents, name, email, date, subj, body, rest = parts[0], parts[1].split(), parts[2], parts[3], parts[4], parts[5], parts[6], parts[7]
        cname, cemail = git.canonical(name, email)
        files = []
        for ln in rest.strip("\n").splitlines():
            f = ln.split("\t")
            if len(f) != 3:
                continue
            a, d, p = f
            binary = a == "-"
            files.append({"path": resolve_rename(p), "raw": p, "add": 0 if binary else int(a), "del": 0 if binary else int(d), "binary": binary})
        commits.append({"sha": sha, "short": sha[:8], "parents": parents, "name": cname, "email": cemail,
                        "date": date, "subject": subj, "body": body.strip(), "files": files,
                        "add": sum(x["add"] for x in files), "del": sum(x["del"] for x in files)})
    return commits


PR_PATTERNS = [r"Merged PR (\d+)", r"Merge pull request #(\d+)", r"See merge request [^\s]*!(\d+)", r"\(#(\d+)\)\s*$",
               r"Merge branch .* into .*\(!(\d+)\)", r"Pull request #(\d+)"]


def pr_id(text):
    for p in PR_PATTERNS:
        m = re.search(p, text, re.M | re.I)
        if m:
            return m.group(1)
    return None


def list_authors(git):
    out = git.run("log", *REFS, "--format=%aN%x1f%aE")
    c = collections.Counter()
    for ln in out.splitlines():
        if "\x1f" in ln:
            n, e = ln.split("\x1f", 1)
            c[git.canonical(n, e)] += 1
    by_email = collections.defaultdict(list)
    for (n, e), k in c.items():
        by_email[e].append((k, n))
    rows = sorted(((sum(k for k, _ in v), e, sorted(v, reverse=True)) for e, v in by_email.items()), reverse=True)
    print("commits  email  [names]")
    for total, e, names in rows:
        print("%7d  %s  %s" % (total, e, "; ".join("%s (%d)" % (n, k) for k, n in names)))


def matches(commit_or_identity, patterns):
    name, email = commit_or_identity
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
    lines = []
    sha = None
    name = ""
    for ln in out.splitlines():
        if re.match(r"^[0-9a-f]{40} \d+ \d+", ln):
            sha = ln[:40]
        elif ln.startswith("author "):
            name = ln[7:]
        elif ln.startswith("author-mail "):
            lines.append((sha, name, ln[12:].strip("<>").lower()))
    return path, lines


def added_lines_by_file(git, sha):
    out = git.run("show", "--format=", "-U0", "--no-ext-diff", "-M", sha, check=False)
    res = collections.defaultdict(list)
    cur = None
    for ln in out.splitlines():
        if ln.startswith("diff --git "):
            cur = None
        elif ln.startswith("+++ "):
            cur = None if ln.strip() == "+++ /dev/null" else ln[6:] if ln.startswith("+++ b/") else ln[4:]
        elif cur and ln.startswith("+"):
            res[cur].append(ln[1:])
    return res


def build_blob_index(git):
    out = git.run("log", *REFS, "--no-merges", "--format=%x1e%H%x1f%aI%x1f%aN%x1f%aE", "--raw", "--no-abbrev", "--no-renames")
    index = collections.defaultdict(list)
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
    return index


# ---------------------------------------------------------------- analysis

def analyze(args):
    git = Git(args.repo, args.mailmap)
    git.run("rev-parse", "--git-dir")
    ref = args.ref or "HEAD"
    ref_sha = git.run("rev-parse", ref).strip()
    patterns = args.author

    all_commits = load_commits(git, args.since, args.until)
    merges = load_commits(git, args.since, args.until, merges=True)
    is_target = lambda c: matches((c["name"], c["email"]), patterns)
    target = [c for c in all_commits if is_target(c)]
    if not target:
        sys.exit("No non-merge commits match --author %s. Run --list-authors to see the identities." % patterns)
    target_shas = {c["sha"] for c in target}
    identities = sorted({(c["name"], c["email"]) for c in target})
    target_emails = {e for _, e in identities}

    excluded = lambda p: any(fnmatch.fnmatch(p, g) for g in (args.exclude or []))

    # ---- per commit enrichment: categories, copy detection, markers, secrets
    index = build_blob_index(git)
    for c in sorted(target, key=lambda c: c["date"]):
        cdate = parse_date(c["date"])
        added = added_lines_by_file(git, c["sha"])
        cats = collections.Counter()
        for f in c["files"]:
            f["category"] = categorize(f["path"])
            cats[f["category"]] += f["add"]
            lines = added.get(f["path"], [])
            sig = [l.strip() for l in lines if significant(l)]
            f["significant"] = len(sig)
            f["template_markers"] = sum(1 for l in lines if TEMPLATE_MARKERS.search(l))
            sre = SECRET_CODE_RE if f["category"] in ("prod_code", "test_code") else SECRET_CONFIG_RE
            f["secret_suspects"] = sum(1 for l in lines if sre.search(l) or PEM_RE.search(l))
            f["copy_score"], f["copy_source"], f["similar_later"] = 0.0, None, None
            if not sig or f["binary"]:
                continue
            same_name = [x for x in index.get(os.path.basename(f["path"]), []) if x[3] not in target_emails]
            cands = [x for x in same_name if parse_date(x[0]) < cdate]
            later = [x for x in same_name if parse_date(x[0]) >= cdate and x[1] != f["path"]]
            f["similar_later"] = None
            for date, path, blob, email, sha in sorted(later)[:20]:
                content = {l.strip() for l in git.blob(blob).splitlines()}
                score = sum(1 for l in sig if l in content) / len(sig)
                if score >= 0.6 and (not f["similar_later"] or score > f["similar_later"]["score"]):
                    f["similar_later"] = {"score": round(score, 3), "path": path, "commit": sha[:8], "date": date[:10], "author": email}
            seen, best = set(), (0.0, None)
            # closest paths first (same folder structure), then most recent
            for date, path, blob, email, sha in sorted(cands, key=lambda x: (-path_affinity(x[1], f["path"]), -parse_date(x[0]).timestamp())):
                if blob in seen:
                    continue
                seen.add(blob)
                if len(seen) > 40:
                    break
                content = {l.strip() for l in git.blob(blob).splitlines()}
                score = sum(1 for l in sig if l in content) / len(sig)
                if score > best[0]:
                    best = (score, {"path": path, "commit": sha[:8], "date": date[:10], "author": email})
                if score >= 0.999:
                    break
            f["copy_score"], f["copy_source"] = round(best[0], 3), best[1]
        c["category_add"] = dict(cats)
        sig_total = sum(f["significant"] for f in c["files"])
        copied = sum(f["significant"] * f["copy_score"] for f in c["files"])
        c["copy_ratio"] = round(copied / sig_total, 3) if sig_total else 0.0
        c["pr"] = pr_id(c["subject"] + "\n" + c["body"])

    # ---- PRs (merge commits) that contain target commits
    prs = []
    for m in merges:
        if len(m["parents"]) < 2:
            continue
        inside = git.run("rev-list", "--no-merges", "%s..%s" % (m["parents"][0], m["parents"][1]), check=False).split()
        mine = [s for s in inside if s in target_shas]
        if mine:
            pid = pr_id(m["subject"] + "\n" + m["body"])
            is_pr = bool(pid)
            prs.append({"merge": m["short"], "is_pr": is_pr, "date": m["date"][:10], "completed_by": m["name"], "completed_by_target": m["email"] in target_emails,
                        "pr": pid, "title": m["subject"], "target_commits": len(mine), "total_commits": len(inside)})
    squash_prs = [c for c in target if c["pr"]]

    # ---- blame at ref
    numstat = git.run("diff", "--numstat", "-z", "--no-renames", EMPTY_TREE, ref_sha)
    files = []
    for rec in numstat.split("\0"):
        f = rec.split("\t")
        if len(f) == 3 and f[0] != "-" and not excluded(f[2]):
            files.append(f[2])
    blame = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(8, (os.cpu_count() or 4))) as ex:
        for path, lines in ex.map(lambda p: blame_file(git, ref_sha, p, args.blame_copies), files):
            blame[path] = lines

    canon_cache = {}
    def canon(name, email):
        if (name, email) not in canon_cache:
            canon_cache[(name, email)] = git.canonical(name, email)[1]
        return canon_cache[(name, email)]

    total_lines = 0
    by_author = collections.Counter()
    by_author_cat = collections.defaultdict(collections.Counter)
    tgt_by_file = collections.Counter()
    tgt_by_commit = collections.Counter()
    file_authors = {}
    for path, lines in blame.items():
        cat = categorize(path)
        fa = collections.Counter()
        for sha, name, email in lines:
            e = canon(name, email)
            total_lines += 1
            by_author[e] += 1
            by_author_cat[e][cat] += 1
            fa[e] += 1
            if sha in target_shas:
                tgt_by_commit[sha[:8]] += 1
            if e in target_emails:
                tgt_by_file[path] += 1
        file_authors[path] = fa
    tgt_surviving = sum(by_author[e] for e in target_emails)

    # ---- what happened to the files the target touched
    touched = collections.defaultdict(lambda: {"added": 0, "deleted": 0, "commits": 0, "created": False})
    for c in target:
        for f in c["files"]:
            t = touched[f["path"]]
            t["added"] += f["add"]
            t["deleted"] += f["del"]
            t["commits"] += 1
            t["category"] = f["category"]
    created = set()
    for c in target:
        for ln in git.run("show", "--format=", "--diff-filter=A", "--name-only", "-M", c["sha"]).splitlines():
            if ln.strip():
                created.add(ln.strip())
    file_fate = []
    for path, t in touched.items():
        alive = path in blame
        row = {"path": path, "category": t["category"], "added": t["added"], "commits": t["commits"], "created_by_target": path in created,
               "exists_at_ref": alive, "target_lines_now": tgt_by_file.get(path, 0), "total_lines_now": len(blame.get(path, []))}
        if alive:
            others = [(k, v) for k, v in file_authors[path].most_common() if k not in target_emails]
            row["top_other_authors_now"] = others[:3]
        elif path in created:
            out = git.run("log", ref_sha, "--full-history", "--diff-filter=D", "-1", "--format=%h%x1f%aN%x1f%aI%x1f%s", "--", path, check=False).strip()
            if not out:
                out = git.run("log", ref_sha, "-m", "--full-history", "--diff-filter=D", "-1", "--format=%h%x1f%aN%x1f%aI%x1f%s", "--", path, check=False).strip()
            if out:
                h, n, d, s = out.split("\x1f", 3)
                row["deleted_by"] = {"commit": h, "author": n, "date": d[:10], "subject": s}
            else:
                row["deleted_by"] = None
        file_fate.append(row)

    # ---- activity and team comparison
    weeks = collections.defaultdict(lambda: [0, 0])
    team = collections.defaultdict(lambda: {"name": collections.Counter(), "commits": 0, "added": 0, "deleted": 0, "first": None, "last": None})
    for c in all_commits:
        w = iso_week(c["date"])
        weeks[w][0 if c["sha"] in target_shas else 1] += 1
        t = team[c["email"]]
        t["name"][c["name"]] += 1
        t["commits"] += 1
        t["added"] += c["add"]
        t["deleted"] += c["del"]
        d = c["date"][:10]
        t["first"] = min(t["first"] or d, d)
        t["last"] = max(t["last"] or d, d)
    if weeks:
        w0, w1 = week_start(min(weeks)), week_start(max(weeks))
        cur = w0
        while cur <= w1:
            y, wk, _ = cur.isocalendar()
            weeks.setdefault("%d-W%02d" % (y, wk), [0, 0])
            cur += dt.timedelta(days=7)
    team_rows = []
    display = {e: max(t["name"], key=lambda n: (len(n.split()), t["name"][n])) for e, t in team.items()}
    dup = collections.Counter(display.values())
    for e, t in team.items():
        label = display[e] if dup[display[e]] == 1 else "%s <%s>" % (display[e], e)
        team_rows.append({"email": e, "name": label, "is_target": e in target_emails, "commits": t["commits"],
                          "added": t["added"], "deleted": t["deleted"], "first": t["first"], "last": t["last"],
                          "surviving": by_author.get(e, 0), "surviving_prod": by_author_cat[e].get("prod_code", 0),
                          "surviving_test": by_author_cat[e].get("test_code", 0)})
    team_rows.sort(key=lambda r: -r["commits"])

    # ---- signals
    signals = []
    subj_day = collections.Counter((c["date"][:10], c["subject"].strip().lower()) for c in target)
    for (d, s), k in subj_day.items():
        if k > 1:
            signals.append({"type": "repeated_subject_same_day", "date": d, "subject": s, "count": k})
    for c in target:
        if c["add"] >= 1000:
            signals.append({"type": "large_commit", "commit": c["short"], "added": c["add"], "copy_ratio": c["copy_ratio"]})
        for f in c["files"]:
            if f["category"] == "junk":
                signals.append({"type": "junk_file", "commit": c["short"], "path": f["path"], "added": f["add"]})
            if f["secret_suspects"]:
                signals.append({"type": "possible_secret", "commit": c["short"], "path": f["path"], "lines": f["secret_suspects"]})
            if f["template_markers"]:
                signals.append({"type": "template_markers", "commit": c["short"], "path": f["path"], "lines": f["template_markers"]})
    ordered = sorted(target, key=lambda c: c["date"])
    for i, c in enumerate(ordered):
        if not re.search(r"(?i)\b(fix|hotfix|correcci[oó]n|corrige|arregl|revert|bug)", c["subject"]):
            continue
        paths = {f["path"] for f in c["files"]}
        for prev in ordered[max(0, i - 10):i]:
            if (parse_date(c["date"]) - parse_date(prev["date"])).days <= 3 and paths & {f["path"] for f in prev["files"]}:
                signals.append({"type": "self_fix", "commit": c["short"], "fixes": prev["short"], "subject": c["subject"]})
                break
    co_authored = git.run("log", *REFS, "-i", "--format=%h %aN %s", *sum((["--grep", "Co-authored-by:.*" + re.escape(p)] for p in patterns), [])).strip().splitlines()

    repo_dates = sorted(c["date"][:10] for c in all_commits)
    tdates = sorted(c["date"][:10] for c in target)
    active_weeks = sorted(w for w, v in weeks.items() if v[0])
    data = {
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "repo": os.path.abspath(args.repo), "ref": ref, "ref_sha": ref_sha[:8], "since": args.since, "until": args.until,
        "author_patterns": patterns, "identities": [{"name": n, "email": e} for n, e in identities],
        "excluded_globs": args.exclude or [],
        "totals": {
            "commits": len(target), "added": sum(c["add"] for c in target), "deleted": sum(c["del"] for c in target),
            "file_changes": sum(len(c["files"]) for c in target), "merges_by_target": sum(1 for m in merges if m["email"] in target_emails),
            "prs_with_target_commits": sum(1 for p in prs if p["is_pr"]), "prs_completed_by_target": sum(1 for p in prs if p["is_pr"] and p["completed_by_target"]),
            "branch_sync_merges_with_target_commits": sum(1 for p in prs if not p["is_pr"]),
            "squash_pr_commits": len(squash_prs), "co_authored_commits": len(co_authored),
            "first_commit": tdates[0], "last_commit": tdates[-1], "repo_first_commit": repo_dates[0], "repo_last_commit": repo_dates[-1],
            "active_weeks": len(active_weeks), "weeks_in_repo_span": len(weeks),
            "days_since_last_commit_vs_repo_last": (dt.date.fromisoformat(repo_dates[-1]) - dt.date.fromisoformat(tdates[-1])).days,
            "surviving_lines": tgt_surviving, "repo_lines_at_ref": total_lines,
            "surviving_share": round(tgt_surviving / total_lines, 4) if total_lines else 0,
            "copy_weighted_added": round(sum(f["add"] * f["copy_score"] for c in target for f in c["files"])),
        },
        "added_by_category": dict(sum((collections.Counter(c["category_add"]) for c in target), collections.Counter())),
        "surviving_by_category": dict(sum((by_author_cat[e] for e in target_emails), collections.Counter())),
        "commits": [{k: c[k] for k in ("short", "date", "subject", "add", "del", "copy_ratio", "category_add", "pr")} |
                    {"files": c["files"], "surviving_lines": tgt_by_commit.get(c["short"], 0)} for c in sorted(target, key=lambda c: c["date"])],
        "prs": prs, "squash_prs": [{"commit": c["short"], "pr": c["pr"], "subject": c["subject"]} for c in squash_prs],
        "co_authored": co_authored,
        "weekly": [{"week": w, "target": v[0], "team": v[1]} for w, v in sorted(weeks.items())],
        "team": team_rows,
        "file_fate": sorted(file_fate, key=lambda r: -r["added"]),
        "surviving_by_file": tgt_by_file.most_common(),
        "signals": signals,
    }
    return data


# ---------------------------------------------------------------- rendering

LABELS = {
    "es": {"prod_code": "Código de producción", "test_code": "Código de pruebas", "deploy_ci": "Despliegue / CI", "build": "Build",
           "config": "Configuración", "docs": "Documentación", "test_assets": "Plantillas y datos de prueba", "boilerplate": "Archivos estándar / boilerplate",
           "junk": "Archivos que no deberían estar en git", "other": "Otros",
           "pie_added": "Líneas agregadas por categoría", "pie_surv": "Líneas vigentes hoy por categoría",
           "copy_title": "Líneas agregadas: copia de archivos existentes vs. nuevas en el repo", "copied": "Copiadas de archivos existentes (>=80%)",
           "adapted": "Adaptadas (50-80%)", "new": "Nuevas en el repo (<50%)",
           "team_commits": "Commits sin merges por autor", "team_surv": "Líneas vigentes por autor", "team_prod": "Código de producción vigente por autor",
           "weekly": "Commits por semana (barras: equipo, línea: desarrollador)", "commits": "Commits", "lines": "Líneas", "week": "Semana",
           "dev": "Desarrollador", "team": "Resto del equipo"},
    "en": {"prod_code": "Production code", "test_code": "Test code", "deploy_ci": "Deployment / CI", "build": "Build",
           "config": "Configuration", "docs": "Documentation", "test_assets": "Test templates and data", "boilerplate": "Standard files / boilerplate",
           "junk": "Files that should not be in git", "other": "Other",
           "pie_added": "Added lines by category", "pie_surv": "Lines still present by category",
           "copy_title": "Added lines: copied from existing files vs. new to the repo", "copied": "Copied from existing files (>=80%)",
           "adapted": "Adapted (50-80%)", "new": "New to the repo (<50%)",
           "team_commits": "Non-merge commits by author", "team_surv": "Lines still present by author", "team_prod": "Production code still present by author",
           "weekly": "Commits per week (bars: team, line: developer)", "commits": "Commits", "lines": "Lines", "week": "Week",
           "dev": "Developer", "team": "Rest of the team"},
}


def bars(rows, width=40):
    if not rows:
        return ""
    mx = max(v for _, v in rows) or 1
    lw = max(len(k) for k, _ in rows)
    total = sum(v for _, v in rows) or 1
    out = []
    for k, v in rows:
        n = v / mx * width
        bar = "█" * int(n) + ("▌" if n - int(n) >= 0.5 else "")
        out.append("%s  %s %s %6.1f%%" % (k.ljust(lw), bar.ljust(width + 1), str(v).rjust(7), 100 * v / total))
    return "```text\n" + "\n".join(out) + "\n```"


def mq(s):
    return '"%s"' % s.replace('"', "'")


def render_charts(d, lang):
    L = LABELS[lang]
    out = []
    def pie(title, mapping):
        rows = [(L[k], v) for k in CATEGORY_ORDER if (v := mapping.get(k, 0))]
        rows.sort(key=lambda r: -r[1])
        out.append("### " + title + "\n\n```mermaid\npie showData\n    title " + title + "\n" +
                   "\n".join("    %s : %d" % (mq(k), v) for k, v in rows) + "\n```\n\n" + bars(rows) + "\n")
    pie(L["pie_added"], d["added_by_category"])
    pie(L["pie_surv"], d["surviving_by_category"])

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
    rows = [(L["copied"], copied), (L["adapted"], adapted), (L["new"], new)]
    out.append("### " + L["copy_title"] + "\n\n```mermaid\npie showData\n    title " + L["copy_title"] + "\n" +
               "\n".join("    %s : %d" % (mq(k), v) for k, v in rows if v) + "\n```\n\n" + bars(rows) + "\n")

    def team_chart(title, key, top=10):
        rows = sorted(((r["name"] + (" ◀" if r["is_target"] else ""), r[key]) for r in d["team"]), key=lambda x: -x[1])[:top]
        if not any(r["is_target"] and r["name"] + " ◀" in [x[0] for x in rows] for r in d["team"]):
            rows += [(r["name"] + " ◀", r[key]) for r in d["team"] if r["is_target"]]
        names = ", ".join(mq(k.replace(" ◀", "")) for k, _ in rows)
        vals = ", ".join(str(v) for _, v in rows)
        out.append("### %s\n\n```mermaid\nxychart-beta\n    title %s\n    x-axis [%s]\n    y-axis %s 0 --> %d\n    bar [%s]\n```\n\n%s\n"
                   % (title, mq(title), names, mq(L["commits"] if key == "commits" else L["lines"]), max(v for _, v in rows) or 1, vals, bars(rows)))
    team_chart(L["team_commits"], "commits")
    team_chart(L["team_surv"], "surviving")
    team_chart(L["team_prod"], "surviving_prod")

    wk = d["weekly"]
    if wk:
        xs = ", ".join(mq(w["week"][2:]) for w in wk)
        mx = max(max(w["team"], w["target"]) for w in wk) or 1
        out.append("### %s\n\n```mermaid\nxychart-beta\n    title %s\n    x-axis [%s]\n    y-axis %s 0 --> %d\n    bar [%s]\n    line [%s]\n```\n"
                   % (L["weekly"], mq(L["weekly"]), xs, mq(L["commits"]), mx, ", ".join(str(w["team"]) for w in wk), ", ".join(str(w["target"]) for w in wk)))
        out.append("| %s | %s | %s |\n|---|---|---|\n" % (L["week"], L["dev"], L["team"]) +
                   "\n".join("| %s (%s) | %s | %d |" % (w["week"], week_start(w["week"]).isoformat(), ("**0**" if not w["target"] else w["target"]), w["team"]) for w in wk) + "\n")
    return "\n".join(out)


def render_summary(d):
    t = d["totals"]
    o = ["# Contribution data (collect_contribution.py)", "",
         "- Repo: `%s` · ref `%s` (`%s`) · period %s → %s" % (d["repo"], d["ref"], d["ref_sha"], d["since"] or "start", d["until"] or "now"),
         "- Identities: " + ", ".join("%s <%s>" % (i["name"], i["email"]) for i in d["identities"]),
         "- Excluded: " + (", ".join(d["excluded_globs"]) or "none"), "", "## Totals", "", "| Metric | Value |", "|---|---|"]
    o += ["| %s | %s |" % (k, v) for k, v in t.items()]
    o += ["", "## Added lines by category", "", "| Category | Added | Still present |", "|---|---|---|"]
    o += ["| %s | %d | %d |" % (k, d["added_by_category"].get(k, 0), d["surviving_by_category"].get(k, 0)) for k in CATEGORY_ORDER
          if d["added_by_category"].get(k) or d["surviving_by_category"].get(k)]
    o += ["", "## Commits", "", "| Commit | Date | + | − | Copy ratio | Still present | PR | Subject |", "|---|---|---|---|---|---|---|---|"]
    o += ["| `%s` | %s | %d | %d | %d%% | %d | %s | %s |" % (c["short"], c["date"][:10], c["add"], c["del"], round(100 * c["copy_ratio"]),
                                                          c["surviving_lines"], c["pr"] or "", c["subject"].replace("|", "\\|")) for c in d["commits"]]
    o += ["", "## Files per commit (copy detection)", ""]
    for c in d["commits"]:
        o.append("### `%s` %s — %s" % (c["short"], c["date"][:10], c["subject"]))
        o.append("| File | Category | + | − | Copy | Source | Similar file by others later | Markers | Secrets? |\n|---|---|---|---|---|---|---|---|---|")
        for f in c["files"]:
            src = f["copy_source"]
            sl = f.get("similar_later")
            o.append("| `%s` | %s | %s | %s | %d%% | %s | %s | %d | %d |" % (f["path"], f["category"], "bin" if f["binary"] else f["add"], "bin" if f["binary"] else f["del"],
                     round(100 * f["copy_score"]), ("%s `%s` %s `%s`" % (src["author"], src["commit"], src["date"], src["path"])) if src else "",
                     ("%d%% %s `%s` %s `%s`" % (round(100 * sl["score"]), sl["author"], sl["commit"], sl["date"], sl["path"])) if sl else "",
                     f["template_markers"], f["secret_suspects"]))
        o.append("")
    o += ["## Pull requests containing the developer's commits", "", "| Merge | Date | PR | Completed by | Their commits / total | Title |", "|---|---|---|---|---|---|"]
    o += ["| `%s` | %s | %s | %s | %d / %d | %s |" % (p["merge"], p["date"], p["pr"] or "", p["completed_by"], p["target_commits"], p["total_commits"],
                                                   p["title"].replace("|", "\\|")) for p in d["prs"] if p["is_pr"]]
    sync = [p for p in d["prs"] if not p["is_pr"]]
    if sync:
        o += ["", "Other merges that carried their commits (branch syncs or merges without a PR number): " + ", ".join("`%s`" % p["merge"] for p in sync)]
    if d["squash_prs"]:
        o += ["", "Squash-merged PR commits: " + ", ".join("`%s` (PR %s)" % (s["commit"], s["pr"]) for s in d["squash_prs"])]
    o += ["", "## Team", "", "| Author | Email | Commits | + | − | First | Last | Still present | Prod code present | Test code present |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    o += ["| %s%s | %s | %d | %d | %d | %s | %s | %d | %d | %d |" % ("**" if r["is_target"] else "", r["name"] + ("**" if r["is_target"] else ""), r["email"],
                                                                 r["commits"], r["added"], r["deleted"], r["first"], r["last"], r["surviving"],
                                                                 r["surviving_prod"], r["surviving_test"]) for r in d["team"]]
    o += ["", "## What happened to the files the developer touched", "",
          "| File | Category | + by dev | Created by dev | Exists now | Dev lines now / total | Others now / deleted by |", "|---|---|---|---|---|---|---|"]
    for r in d["file_fate"]:
        if r["exists_at_ref"]:
            extra = ", ".join("%s %d" % (k.split("@")[0], v) for k, v in r.get("top_other_authors_now", []))
        else:
            db = r.get("deleted_by")
            extra = ("deleted in `%s` by %s on %s: %s" % (db["commit"], db["author"], db["date"], db["subject"])) if db else ("not found at ref" if r["created_by_target"] else "renamed/removed")
        o.append("| `%s` | %s | %d | %s | %s | %d / %d | %s |" % (r["path"], r["category"], r["added"], "yes" if r["created_by_target"] else "",
                 "yes" if r["exists_at_ref"] else "**no**", r["target_lines_now"], r["total_lines_now"], extra.replace("|", "\\|")))
    o += ["", "## Signals", ""]
    o += ["- " + json.dumps(s, ensure_ascii=False) for s in d["signals"]] or ["- none"]
    if d["co_authored"]:
        o += ["", "## Co-authored commits", ""] + ["- " + x for x in d["co_authored"]]
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
    ap.add_argument("--exclude", action="append", help="glob of paths to leave out of blame (repeatable)")
    ap.add_argument("--blame-copies", action="store_true", help="git blame -C -C: attribute moved/copied lines to their origin (slower)")
    ap.add_argument("--lang", default="es", choices=["es", "en"])
    ap.add_argument("--out")
    a = ap.parse_args()
    git = Git(a.repo, a.mailmap)
    if a.list_authors:
        list_authors(git)
        return
    if not a.author or not a.out:
        ap.error("--author and --out are required")
    data = analyze(a)
    os.makedirs(a.out, exist_ok=True)
    with open(os.path.join(a.out, "data.json"), "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=1)
    with open(os.path.join(a.out, "summary.md"), "w", encoding="utf-8") as fh:
        fh.write(render_summary(data))
    with open(os.path.join(a.out, "charts.md"), "w", encoding="utf-8") as fh:
        fh.write(render_charts(data, a.lang))
    t = data["totals"]
    print("OK %d commits, +%d/-%d, %d lines still present (%.1f%% of %d), %d PRs. Files: data.json, summary.md, charts.md in %s"
          % (t["commits"], t["added"], t["deleted"], t["surviving_lines"], 100 * t["surviving_share"], t["repo_lines_at_ref"], t["prs_with_target_commits"], a.out))


if __name__ == "__main__":
    main()
