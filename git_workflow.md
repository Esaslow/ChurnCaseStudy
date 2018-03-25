# Git Workflow 

Branch, Pull, Rebase and Merge

### What's the point?

You only add your work to the most updated version of your group project.

---

### To Start:

Everyone either clones or adds the same repository as a remote.

This repository should gave a branch for the group-project. This is either the master branch, or a separate branch.

Everyone should make a branch from the group-project branch.

### On your branch:

1. Add the relevant files
2. Commit them
3. Push to your remote branch (origin or whatever remote you are working on)

As a baseline, **always** have the work on your branch saved, even if you're not sharing it anytime soon. More commits is better

Is all the work on your branch saved and ready to go?

### Sharing your work:

Before you can merge ('share') your work, you need to make sure that you have the most recent version of the group project - that is, any other work that your group-members have merged in.

First, checkout to the group-project branch, `git checkout <your branch>`

Then run `git pull`

This should update your local group-project branch to the latest version.

Then, checkout back to your branch, `git checkout <your branch>`

Rebase your branch: `git rebase <group project branch>`

Rebasing looks scary, and it also looks kinda weird in Atom. Dismiss the 'Use Me' buttons by clicking on the ellipses and then clicking 'Dismiss'.

Rebasing will take you through each commit since your branch was rebased, and make you solve merge conflicts. Just go step by step, and look things up as need be. If you haven't rebased in a while, you will have more steps.

Rebasing sets the base of your branch to the latest version of the group project branch. Your branch now has your latest work (from your branch) *and* everyone else's latest work (from the group-project branch).

Then, checkout back to the group-project branch, and merge in your work. 

## Summary

Create a personal branch from the group-project branch:

```
$ git checkout -b <your_branch>

```

Do work on your branch. Make sure to add and commit all your work.  

Push your local branch to your remote branch:

```
$ git push <remote> <your_branch>
```
  
Before merging your work, get the latest verison of the group-project branch:

```
$ git checkout <group_project_branch>
$ git pull <remote> <group_project_branch> 
```

Checkout back to your branch, and rebase it on the update group-project branch:

```
$ git checkout <your_branch>
$ git rebase <group_project_branch>
```

Commit your local rebased branch, and push it to your remote branch:

```
$ git commit -m 'rebased my branch'
$ git push <remote> <your_branch>
```

Then, switch back into the group project branch. To make sure no one else has pushed to the branch since you last pulled from it, pull again:

```
$ git checkout <group_project_branch>
$ git pull <remote> <group_project_branch>
```

If you pull in another update, rebase again. Otherwise, merge in your branch:

```
$ git merge <your_branch>
```

If the merge is successful, commit the merge and push the group project branch to the remote:

```
$ git commit -m 'merged in my branch'
$ git push <remote> <group_project_branch>
```

---

If something fails, delete you branch, then delete the repo, delete your hard drive, microwave your computer, and move to Alaska.