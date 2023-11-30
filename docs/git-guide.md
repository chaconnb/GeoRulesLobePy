# Git Guide
Git is a free and open source distributed version control system designed to handle everything from small to very large projects with speed and efficiency. Atlassian has a very good [website](https://www.atlassian.com/git/glossary#commands) to help you learn git

### Setting up a local repo
These steps will copy the current state of the remote repository to your local PC. You can
make changes on your local copy and upload them to the remote repository. More details about
cloning a git repository can be found in the [Git documentation](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository). 

Clone the repository to local. 
```console
git clone git@github.com:chaconnb/georules.git
```
### Branching
A branch represents an independent line of development. Branches serve as an abstraction for the edit/stage/commit process. You can think of them as a way to request a brand new working directory, staging area, and project history. New commits are recorded in the history for the current branch, which results in a fork in the history of the project.

The `git branch` command lets you create, list, rename, and delete branches. It doesn’t let you switch between branches or put a forked history back together again. For this reason, git branch is tightly integrated with the git checkout and git merge commands.

Some branch commands: 
- `git branch` : list all branches in your local repo. The current branch will be indicated
- `git branch -avv` : list all local and remote branches, with rich description and display
- `git branch -D <branch-name` : delete the specified branch
- `git switch <branch-name>`: switch to the target branch

To create a new branch use the `git checkout -b` command. This will create a new branch and switch to the current branch.

IMPORTANT: To create a branch from the main, go first to the main and create the branch. 
           To create a branch from a branch, go to the branch you want to create the branch from and create the branch. 
```console
git checkout -b "my-new-branch" 
```

### Making changes to your code. 
To add a file or a change to a file. 
```console
git add <path/to/file>
```
To add multiple files at the same time
```console 
git add file1 file2 file3 
```
or to add using a wildcard (*)
```console 
git add * 
```
> WARNING: This will add everything, should only use if you know what you are doing. 

To commit those changes, and add a comment: 
```console
git commit -m "my commit message" 
```

To push changes from local to remote: 
```console
git push
```
### Updating your local code
If any changes to the remote code are made (like merging a PR, for example), you might want to 
update your local code to match with the changes in the remote repo. To do so, switch to the 
branch you want to update and perform a `git pull` command. 

To pull changes/ update local branch (go to your project in terminal)
1. Go to main
```console
git switch main
```
2. Pull all files to local from github
```console
git fetch; git pull
```


## Git Workflow
These steps describe a simple git workflow. You can see a visualization of the workflow
in the `./workflow-git.pdf`. 

1. Create a new branch
```console
git checkout -b 'my-new-branch' 
```
2. Switch to the new branch
```console
git switch my-new-branch
```
3. To run code go to folder where the code is:
  ```console
cd directory's name
cd georules
```
Write python and file's name:
  ```console
python file's name
python M_LRB.py
```
4. Make changes/updates to the code (remember to push changes to the remote branch)
5. Create a "Pull Request" (PR)
6. If the PR can be safely merged into the main branch, merge. 
> **PR merge recommendations**  
> Use squash-merge when merging PRs
> Delete the 'my-new-branch' after the merge to keep branches clean

## VSCode Help 
To open VSCode from the terminal, use: 
```console 
code . 
```

Remember to open the from the `georules` folder so that VSCode can recognize that this is a git repo. 
(i.e., a folder with a .git directory)
