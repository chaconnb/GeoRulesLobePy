# Git Guide


Clone the repository to local. 
```console
git clone git@github.com:chaconnb/georules.git
```

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

To pull changes/ update local branch (go to your project in terminal)
```console
git fetch; git pull
```


### Git Workflow
1. Create a new branch
```console
git checkout -b 'my-new-branch' 
```
2. Switch to the new branch
```console
git switch my-new-branch
```
3. Make changes/updates to the code (remember to push changes to the remote branch)
4. Create a "Pull Request" (PR)
5. If the PR can be safely merged into the main branch, merge. 
> **PR merge recommendations**  
> Use squash-merge when merging PRs
> Delete the 'my-new-branch' after the merge to keep branches clean

### VSCode Help 
To open VSCode from the terminal, use: 
```console 
code . 
```

Remember to open the from the `georules` folder so that VSCode can recognize that this is a git repo. 
(i.e., a folder with a .git directory)
