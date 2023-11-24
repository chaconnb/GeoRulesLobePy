# Git Guide


Clone the repository to local. 
```console
git clone git@github.com:chaconnb/georules.git
```

To add a file or a change to a file. 
```console
git add <path/to/file>
```

To commit those changes, and add a comment: 
```console
git commit -m "my commit message" 
```

To push changes from local to remote: 
```console
git push
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