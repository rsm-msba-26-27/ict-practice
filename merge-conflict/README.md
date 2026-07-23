# Make (and fix) a merge conflict — on purpose

A merge conflict happens when the same lines change in two places before the
changes meet. Today you create one deliberately, in YOUR practice repo, so the
first real one is boring.

Work inside the repo you created in Practice 02 part A
(`~/rsm-msba/ict-practice-<username>`).

## Step 1 — create the file that will conflict

In your repo, create `favorites.md` with exactly this content:

```markdown
# My San Diego favorites

Best taco: carne asada
Best beach: fill this in
```

Commit and push it (VS Code Source Control, or the terminal):

```bash
git add favorites.md
git commit -m "add favorites"
git push
```

## Step 2 — change it on GitHub (the "someone else" edit)

On github.com, open your repo, click `favorites.md`, then the pencil icon (Edit).
Change the taco line to:

```
Best taco: al pastor
```

Commit directly to `main` from the web page. Your repo on GitHub is now
AHEAD of the copy on your laptop.

## Step 3 — change the SAME line locally, without pulling

Back in VS Code, edit `favorites.md` — change the taco line to:

```
Best taco: fish
```

Save, then commit (do **not** pull first — that is the whole point):

```bash
git add favorites.md
git commit -m "actually fish tacos"
```

## Step 4 — push, and enjoy the rejection

```bash
git push
```

Rejected — GitHub has a commit you do not have. Git tells you to pull first:

```bash
git pull
```

Now git reports a CONFLICT in `favorites.md`. You are exactly where we want you.

## Step 5 — resolve it

Open `favorites.md` in VS Code. You will see conflict markers:

```
<<<<<<< HEAD
Best taco: fish
=======
Best taco: al pastor
>>>>>>> (GitHub's version)
```

VS Code shows buttons above the block: **Accept Current | Accept Incoming |
Accept Both**. Pick whichever taco you actually prefer (or click neither and
just edit the block by hand — it is only text). Make sure every `<<<<<<<`,
`=======`, and `>>>>>>>` line is gone, then:

```bash
git add favorites.md
git commit -m "resolve the great taco conflict"
git push
```

## Step 6 — verify

Refresh your repo on github.com — `favorites.md` shows your resolved version,
and the history shows all three commits plus the merge. Done: you have
survived a merge conflict, on purpose, in under ten minutes.
