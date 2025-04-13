## 上手使用

#### 创建 SSH key

[使用GitHub（一）：添加SSHkey - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/34584694)



#### 上传代码

[使用GitHub（二）：配置并使用Git创建版本库 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/34585267)

1. 在 github 上创建一个新的仓库，给它一个合适的名字，比如 your-project。

2. 在本地创建一个文件夹，用来存放你的项目文件，比如 your-project。

3. 进入文件夹，输入 `git init` 命令，初始化一个本地仓库。

4. 将你的项目文件复制或移动到本地文件夹中，然后输入 `git add . ` 命令，将所有文件添加到暂存区。

5. 输入 `git commit -m "first commit"` 命令，将暂存区的文件提交到本地仓库，并添加一个提交信息。

6. 输入 `git remote add origin git@github.com:yourname/yourproject.git` 

    将本地仓库与远程仓库关联起来，其中 yourname 是你的 github 用户名，youproject 是你的 github 仓库名。

    如：`git remote add origin git@github.com:JAILuo/lcthw-for-leanring.git`

7. 输入 `git branch -M main ` 和 `git push -u origin main` 

    你将本地仓库的主分支设置为`main`，

    并将内容推送到远程仓库的`main`分支。保

8. 在 github 上查看你的仓库，应该项目文件已经上传成功了。

 

> 之后使用：
>
> 1. `git add . /git add all`
>
>     > 但注意更新的时候的记录，上面这条命令是对全部文件的：
>     >
>     > 具体对某一个文件：
>     >
>     > To commit a specific file with a specific comment in Git, you need to follow these steps:
>     >
>     > Add the changes to the staging area using the git add command. For example, to add a specific file named “file.txt”, use:
>     >
>     > ```bash
>     > git add file.txt
>     > ```
>     >
>     > Check the status of the files using the git status command to ensure that only the desired file is staged for commit.
>     >
>     > Commit the changes using the git commit command and provide a comment for the specific file. For example, to commit “file.txt” with the comment “Updated file.txt”, use:
>     >
>     > ```bash
>     > git commit -m "Updated file.txt"
>     > ```
>     >
>     > This way, only the specified file will have the given comment associated with it.
>
> 2. `git commit`
>
> 3. `git push`



#### 分支管理

Git 中关于分支（branch）的操作是非常重要的，以下是一些常用的 Git 分支操作：

1. **创建分支**：
   - `git branch <branch_name>`：创建一个新的分支。
   - `git checkout -b <branch_name>`：创建一个新的分支并切换到该分支。

2. **切换分支**：
   - `git checkout <branch_name>`：切换到指定的分支。

3. **查看分支**：
   - `git branch`：列出所有本地分支，当前分支前会有一个 `*` 号。
   - `git branch -a`：列出所有本地和远程分支。

4. **删除分支**：
   - `git branch -d <branch_name>`：删除指定的本地分支。
   - `git branch -D <branch_name>`：强制删除指定的本地分支（未合并的分支）。

5. **合并分支**：
   - `git merge <branch_name>`：将指定分支合并到当前分支。

6. **推送分支**：
   - `git push origin <branch_name>`：推送本地分支到远程仓库。

7. **拉取远程分支**：
   - `git fetch origin <branch_name>`：拉取远程分支到本地，但不会自动合并。

8. **重命名分支**：
   - `git branch -m <new_branch_name>`：重命名当前分支。

9. **查看分支历史**：
   - `git log --oneline --decorate --graph --all`：查看所有分支的提交历史。

以上是一些常用的 Git 分支操作，可以帮助您在项目开发中更好地管理和协作不同的功能和版本。



#### 实际开发

在实际公司开发中，团队通常会使用 Git 进行版本控制和协作，以下是在公司开发中常见的 Git 功能和操作：

1. **分支管理**：
   - 创建新分支用于开发新功能或修复 bug。
   - 合并分支以将新功能或修复的代码合并到主分支。
   - 删除已经合并的分支以保持分支结构清晰。

2. **代码提交**：
   - 提交代码以保存当前工作进度。
   - 编写有意义的提交信息以便他人理解代码变更的目的。

3. **代码审查**：
   - 发起代码审查以确保代码质量和一致性。
   - 回顾他人提交的代码并提出反馈或建议。

4. **解决冲突**：
   - 处理代码合并时可能出现的冲突，解决冲突后提交更改。

5. **版本回退**：
   - 回滚到先前的提交版本以修复错误或恢复之前的状态。

6. **远程仓库同步**：
   - 拉取远程仓库最新代码以保持本地代码同步。
   - 推送本地代码到远程仓库以分享最新更改。

7. **标签管理**：
   - 创建标签以标记重要的版本发布。
   - 查看和共享特定标签对应的代码版本。

8. **忽略文件**：
   - 使用 `.gitignore` 文件来忽略不需要版本控制的文件或文件夹。

9. **子模块管理**：
   - 将其他 Git 仓库作为子模块引入主项目中，方便管理依赖。

10. **Hooks 使用**：
    - 使用 Git 钩子（hooks）来触发自定义脚本，在提交、合并等操作时执行特定任务。

以上是在公司开发中常见的 Git 功能和操作，通过合理使用这些功能，团队可以更高效地协作、管理和追踪代码变更。





## 相关工作流

[Git 协作模式 | Notev](https://nyakku.moe/posts/2019/10/26/git-collaboration.html#如何提交-pr)

[A successful Git branching model » nvie.com](https://nvie.com/posts/a-successful-git-branching-model/)





## 相关问题

#### 关于Git提交时的身份信息未配置

```bash
$ git commit
Author identity unknown

*** Please tell me who you are.

Run

  git config --global user.email "you@example.com"
  git config --global user.name "Your Name"

to set your account's default identity.
Omit --global to set the identity only in this repository.

fatal: unable to auto-detect email address (got 'x(none)')
```

这个错误提示表明 Git 在提交时无法确定你的身份信息（用户名和邮箱地址），因此需要你配置这些信息。你可以按照提示中的指引，通过以下命令来设置你的用户名和邮箱地址：

```
git config --global user.email "you@example.com"
git config --global user.name "Your Name"
```

在上面的命令中，将 `you@example.com` 替换为你的邮箱地址，将 `Your Name` 替换为你的用户名。这样设置后，Git 就能正确识别你的身份信息，你就可以成功提交代码了。

如果你只想在当前仓库中设置身份信息而不是全局设置，可以去掉 `--global` 参数，例如：

```
git config user.email "you@example.com"
git config user.name "Your Name"
```

设置完身份信息后，再次尝试提交代码，应该就不会再出现上述错误了。



==解决==



#### 关于 vim-plug 下载时出现的问题：使用/更换镜像站

当使用`https://kkgithub.com`作为镜像站时，您可以按照以下步骤重新配置Git的镜像站设置：

1. 打开终端，并输入以下命令来查看当前Git的镜像站点设置：
   ```
   git config --global --get http.proxy
   git config --global --get https.proxy
   ```

2. 如果上述命令返回了镜像站点地址，您可以使用以下命令来移除镜像站点设置：
   ```
   git config --global --unset http.proxy
   git config --global --unset https.proxy
   ```

3. 然后，您可以设置新的镜像站点地址为`https://kkgithub.com`。请注意，`https://kkgithub.com`可能不是一个有效的Git镜像站点，您可能需要使用其他可靠的镜像站点。但是，如果您仍然希望使用`https://kkgithub.com`，您可以尝试设置如下：
   ```
   git config --global url."https://kkgithub.com/".insteadOf "https://github.com/"
   ```

4. 然后再次尝试克隆`ycmd`子模块，看看是否可以成功。

请注意，镜像站点的可靠性和稳定性对于Git操作非常重要，建议您选择经过验证和可靠的镜像站点。希望这些信息对您有帮助。如果您有任何其他问题，请随时告诉我。





#### 关于Git push问题1

```bash
$ git push -u orign main
fatal: 'orign' does not appear to be a git repository
fatal: Could not read from remote repository.

Please make sure you have the correct access rights
and the repository exists.
```

这个错误提示表明 Git 在尝试推送到远程仓库时遇到了权限问题，可能是因为 SSH 密钥认证失败。以下是可能导致这个问题的一些原因和解决方法：

1. **SSH密钥未正确配置**：请确保你在GitHub账户中添加了正确的公钥。你可以在GitHub的设置中找到 SSH and GPG keys 来添加公钥。

2. **SSH代理问题**：有时候 SSH 代理可能会导致权限问题。你可以尝试在终端中运行以下命令来关闭 SSH 代理，然后再次尝试推送：

    ```
    eval "$(ssh-agent -s)"
    ssh-add ~/.ssh/id_rsa
    ```

3. **检查远程仓库地址**：确保你使用的远程仓库地址是正确的。你可以运行以下命令来检查远程仓库地址：

    ```
    git remote -v
    ```

4. **检查SSH配置**：确保你的SSH配置文件中包含正确的私钥路径。你可以检查 `~/.ssh/config` 文件或者 `~/.ssh/authorized_keys` 文件。

5. **尝试使用HTTPS方式推送**：如果以上方法无法解决问题，你可以尝试使用HTTPS方式推送代码。你可以将远程仓库地址改为HTTPS方式：

    ```
    git remote set-url origin https://github.com/yourusername/your-repo.git
    ```



- 直接使用了`git remote set-url origin https://github.com/yourusername/your-repo.git`解决

    ==解决==





#### ssh登录

在Ubuntu 22.04上，你可以使用以下步骤来生成新的SSH密钥对、将其添加到SSH代理并配置SSH客户端：

1. 生成新的SSH密钥对：
   - 打开终端并输入以下命令来生成新的SSH密钥对：
     ```
     ssh-keygen -t rsa -f ~/.ssh/id_rsa_github -C "your_email@example.com"
     ```
     这里`-t`参数指定密钥类型为RSA，`-f`参数指定生成的密钥文件名为id_rsa_github，`-C`参数用于指定注释，通常可以填写你的邮箱地址。

   - 同样的方式生成Jetson Nano的SSH密钥对：
     ```
     ssh-keygen -t rsa -f ~/.ssh/id_rsa_jetson -C "your_email@example.com"
     ```

2. 将新的SSH密钥添加到SSH代理：
   - 使用以下命令将新生成的SSH密钥添加到SSH代理中：
     ```
     ssh-add ~/.ssh/id_rsa_github
     ssh-add ~/.ssh/id_rsa_jetson
     ```

3. 配置SSH客户端：
   - 使用文本编辑器打开`~/.ssh/config`文件，并添加以下内容：
     ```
     # GitHub
     Host github.com
     HostName github.com
     IdentityFile ~/.ssh/id_rsa_github
     
     # Jetson Nano
     Host jetson
     HostName <jetson_nano_ip>
     IdentityFile ~/.ssh/id_rsa_jetson
     ```

通过以上步骤，你可以在不同的场景下使用不同的SSH密钥对，而无需每次重新生成SSH密钥。同时，确保在GitHub和Jetson Nano上配置相应的公钥以进行授权访问。





#### ! [rejected]          master -> master (fetch first)

```bash
! [rejected]          master -> master (fetch first)
error: failed to push some refs to 'https://github.com/JAILuo/ics2023-ysyx.git&#39;  
hint: Updates were rejected because the remote contains work that you do
hint: not have locally. This is usually caused by another repository pushing
hint: to the same ref. You may want to first integrate the remote changes
hint: (e.g., 'git pull ...') before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.

```

这个错误信息表明你尝试将本地的Git仓库推送到远程仓库时，远程仓库中存在一些你本地没有的更新。这通常是因为其他人已经推送了更改到远程仓库，而你的本地仓库还没有同步这些更改。

要解决这个问题，你可以按照以下步骤操作：

1. **拉取远程仓库的最新更改**：
   使用命令 `git pull origin master` 来拉取远程仓库的最新更改到你的本地仓库。这将会合并远程仓库的更改到你的当前分支。

2. **解决任何潜在的合并冲突**：
   如果在合并过程中出现冲突，Git会提示你解决这些冲突。你需要手动编辑冲突的文件，选择保留哪部分更改，然后提交更改。

3. **再次尝试推送**：
   一旦解决了所有合并冲突并且本地仓库是最新的，你可以使用 `git push origin master` 再次尝试推送你的更改到远程仓库。

如果你希望保留你本地的更改而不是合并远程的更改，你可以使用 `git pull --rebase` 来拉取远程更改，这样可以保持你的提交历史更干净。

请注意，如果你不是仓库的协作者或者没有写入权限，你可能需要先 fork 仓库，然后推送到你的 fork 中。如果你需要进一步的帮助，请提供更多的上下文信息。

> more：`git pull ` 和 `git pull --rebase`
>
> `git pull --rebase` 和 `git pull` 都是用来将远程仓库的更改合并到你的本地仓库中，但它们在合并更改时的策略有所不同，这会影响到你的提交历史。
>
> - `git pull`（默认行为）
>
>     当你使用不带参数的 `git pull` 时，Git 会执行以下步骤：
>
>     1. 首先，它会将远程分支的当前状态保存为一个临时的本地分支。
>     2. 然后，它会将你的当前分支重置为远程分支的当前状态。
>     3. 接着，它会尝试将你的本地更改合并到这个远程状态上。
>     4. 如果合并成功，你会得到一个包含两个父提交的合并提交，表示你的本地更改和远程更改的合并。
>
>     这种方式的优点是简单直接，但缺点是它会在你的提交历史中引入一个额外的合并提交，这可能会使历史变得复杂和难以追踪。
>
> - `git pull --rebase`
>
>     使用 `git pull --rebase` 时，Git 会执行以下步骤：
>
>     1. 它会首先记录下你当前分支上相对于远程分支的提交（即你的本地更改）。
>     2. 然后，它会将远程分支的更改拉取到你的当前分支上，将你的本地分支更新到远程分支的最新状态。
>     3. 接着，它会将你在第一步记录的本地更改重新应用到更新后的分支上，一个接一个地进行。
>     4. 如果过程中没有冲突，你会得到一个线性的提交历史，就像你的本地更改是在远程更改之后直接进行的。
>
>     - 使用 `git pull --rebase` 的好处包括：
>         - **更清晰的提交历史**：避免了不必要的合并提交，使得提交历史更加线性和清晰。
>         - **更容易的回滚**：如果你需要回滚一些更改，线性的提交历史使得这个过程更加简单。
>         - **更好的协作**：在团队中使用 rebase 可以帮助保持一致的提交历史，使得团队成员更容易理解项目的发展。
>     - 然而，`git pull --rebase` 也有潜在的缺点：
>         - 如果团队成员也在使用相同的分支进行工作，使用 rebase 可能会导致冲突，因为 rebase 改变了提交的顺序和哈希值。
>         - 如果不恰当地使用 rebase，可能会不小心丢失他人的工作或者混淆提交历史。
>
> 总的来说，选择使用 `git pull` 还是 `git pull --rebase` 取决于你的团队工作流程和个人偏好。如果你希望保持一个干净、线性的提交历史，`git pull --rebase` 是一个很好的选择。如果你更倾向于保留每次合并的上下文，那么 `git pull` 可能更适合你。





#### fatal: unable to access xxxx: Failed to connect to xxxx : Connection refused

> git clone 拒绝连接，Connection refused 解决方法
> 一、使用env指令查询系统代理并取消对应http代理
> 二、使用git config指令查询代理并取消代理
> 三、直接修改.gitconfig配置文档查询代理并取消代理
>
> git clone经常出现代理错误，报错如下：
> fatal: unable to access 'https://[github](https://so.csdn.net/so/search?q=github&spm=1001.2101.3001.7020).com/xbg/myproject.git/': Failed to connect to 127.0.0.1 port 8888: 拒绝连接
> 1
> 普遍的解决方案都是取消代理，但是本人经常遇到常见的取消代理无效的问题，所以把各种方案都总结如下。
>
> 一、使用env指令查询系统代理并取消对应http代理
> 使用指令：
>
> env | grep -i proxy 
> 1
> 会显示系统所有的代理信息：
>
> NO_PROXY=localhost,127.0.0.0/8,::1
> http_proxy=http://127.0.0.1:8888/
> https_proxy=http://127.0.0.1:8888/
> HTTPS_PROXY=http://127.0.0.1:8888/
> no_proxy=localhost,127.0.0.0/8,::1
> HTTP_PROXY=http://127.0.0.1:8888/
> 1
> 2
> 3
> 4
> 5
> 6
> 使用unset指令取消代理：
>
> unset http_proxy
> unset  https_proxy
> unset  HTTPS_PROXY
> unset  HTTP_PROXY
> 1
> 2
> 3
> 4
> 二、使用git config指令查询代理并取消代理
> 查看代理：
>
> git config --global http.proxy
> 1
> 显示已有的http代理信息：
>
> http://127.0.0.1:8888
> 1
> 取消代理：
>
> git config --global --unset http.proxy
> 1
> 三、直接修改.gitconfig配置文档查询代理并取消代理
> 经常以上两种方式都不能查询到系统代理，但是git clone仍有相同报错，则可以直接查看.gitconfig来查询git使用代理，若有代理则将其删除。
> 1
> 使用指令：
>
> vim ~/.gitconfig
> 1
> .gitconfig如下：
>
> 可以看到有https的代理，将那两行删除。
>
> 此时再git clone问题解决。

[解决使用git时遇到Failed to connect to github.com port 443 after 21090 ms: Couldn‘t connect to server_git couldn't connect to server](https://blog.csdn.net/qq_40296909/article/details/134285451)

改端口，该补充一些计算机网路的知识了。





#### 想要切换到别的分支，但是不想要这次的修改

 如果你在分支上进行了一些改动并进行了测试，但并不想提交这些改动，你可以采取以下几种方法来处理这些未提交的更改：

1. **放弃工作目录中的所有更改**：
   如果你确定不想保留这些更改，可以使用 `git checkout` 或 `git reset` 命令来放弃自上次提交以来的所有更改。
   ```bash
   git reset --hard
   git checkout .
   ```
   这将重置你的工作目录和索引（暂存区）到最后一次提交的状态。

2. **暂存改动**：
   如果你想要保留这些改动，但目前不想提交，你可以使用 `git stash` 命令来暂存这些改动。
   ```bash
   git stash
   ```
   这会将你的改动存储在一个“暂存栈”中，你的工作目录将会被清理干净。

3. **创建一个新的分支**：
   如果你想要保留这些改动并且将来可能会用到，可以创建一个新的分支来保存这些改动。
   
   ```bash
   git checkout -b new-branch-name
   ```
   这样，你的改动将会保存在新的分支上，你可以在任何时候回到这个分支继续工作。
   
4. **使用 `git restore` 命令**：
   在 Git 2.23 版本及以后，你可以使用 `git restore` 命令来放弃工作目录中的特定文件或所有文件的更改。
   ```bash
   git restore .
   ```
   或者放弃特定文件的更改：
   ```bash
   git restore <file-path>
   ```

5. **使用 `git clean` 命令**：
   如果你想要删除未跟踪的文件（例如，那些没有加入到 Git 仓库中的新文件），可以使用 `git clean` 命令。
   ```bash
   git clean -f
   ```
   这个命令会删除所有未跟踪的文件和目录，但不会删除已跟踪的文件。

选择适合你情况的方法来处理你的改动。如果你只是想要回到上次提交的状态并且不保留任何未提交的更改，那么使用 `git reset --hard` 和 `git checkout .` 是最快的方法。如果你想要保留这些更改以备将来使用，那么 `git stash` 或创建一个新的分支会是更好的选择。

​	



#### 关于 vim-plug 管理插件的镜像站

```bash
Plug 'git://github.com/junegunn/fzf', { 'do': { -> fzf#install() } }
Plug 'git://github.com/junegunn/fzf.vim'

Plug 'git://github.com/Shougo/defx.nvim.git'
Plug 'git://github.com/roxma/nvim-yarp.git'
Plug 'git://github.com/roxma/vim-hug-neovim-rpc.git'
Plug 'git://github.com/kristijanhusak/defx-icons.git'

```

直接深入仓库的全称





#### 设置不同的远程仓库

为了避免远程仓库名称冲突，你可以为不同的远程仓库指定不同的名称。以下是如何操作的步骤：

1. **创建新的远程仓库名称**：
   - 当你想要添加一个新的远程仓库时，不要使用默认的 `origin`，而是指定一个新的名字。例如：
     ```bash
     git remote add upstream https://github.com/your-username/your-repo.git
     ```
   - 这里 `upstream` 是你为远程仓库指定的新名称，`https://github.com/your-username/your-repo.git` 是你的远程仓库的URL。

2. **推送到新的远程仓库**：
   - 一旦你添加了一个新的远程仓库，你可以使用这个新的名称来推送代码：
     ```bash
     git push upstream main
     ```
   - 这会将你的 `main` 分支推送到名为 `upstream` 的远程仓库。

3. **查看远程仓库**：
   - 要查看所有远程仓库的名称和URL，可以使用：
     ```bash
     git remote -v
     ```
   - 这将列出所有的远程仓库及其对应的URL。

4. **修改远程仓库URL**：
   - 如果你需要修改远程仓库的URL（例如，从HTTP切换到SSH），可以使用：
     ```bash
     git remote set-url upstream https://github.com/your-username/your-repo.git
     ```
   - 这将更新名为 `github` 的远程仓库的URL。

5. **删除远程仓库**：
   - 如果你不再需要某个远程仓库，可以使用以下命令删除它：
     ```bash
     git remote remove github
     ```
   - 这将删除名为 `github` 的远程仓库。

6. **重命名远程仓库**：
   - 如果你想要改变远程仓库的名称，可以使用以下命令：
     ```bash
     git remote rename old-name new-name
     ```
   - 这将把远程仓库的名称从 `old-name` 改为 `new-name`。

通过使用不同的名称为不同的远程仓库，你可以轻松地管理和推送到多个远程仓库，而不会发生冲突。





#### 提交不同的内容

在 Git 中，如果你想为不同的文件编写不同的提交注释，你可以使用部分提交（partial commits）或者分别对每个文件进行提交。以下是几种方法：

- 方法 1：使用 `git add` 部分提交

    1. **添加文件到暂存区**：

        - 首先，使用 `git add` 将你想要提交的文件添加到暂存区（stage area）。

        - 例如，如果你有两个文件 `file1.txt` 和 `file2.txt`，你只想提交 `file1.txt`，你可以运行：

            ```bash
            git add file1.txt
            ```

        - 然后，编写提交注释并提交：

            ```bash
            git commit -m "提交 file1.txt 的更改"
            ```

        - 接下来，你可以再次运行 `git add` 添加 `file2.txt`：

            ```bash
            git add file2.txt
            ```

        - 编写另一个提交注释并提交：

            ```bash
            git commit -m "提交 file2.txt 的更改"
            ```


- 方法 2：使用 `git commit` 的 `-C` 或 `-c` 选项

    如果你已经将所有更改添加到暂存区，但想要为不同的更改编写不同的提交注释，你可以使用 `-C` 或 `-c` 选项来复制之前的提交信息。

    1. **添加所有更改到暂存区**：

        ```bash
        git add .
        ```

    2. **提交更改**：

        - 首先，提交所有更改：

            ```bash
            git commit -m "Initial commit with all changes"
            ```

        - 然后，你可以使用 `git rebase` 来修改提交信息：

            ```bash
            git rebase -i HEAD~1
            ```

        - 这将打开一个编辑器，列出最近的提交。你可以将提交更改为 `edit`，保存并退出。

        - 然后，你可以修改提交信息：

            ```bash
            git commit --amend -m "提交 file1.txt 的更改"
            ```

        - 重复上述步骤，为 `file2.txt` 修改提交信息。

- 方法 3：使用 `git add -p` 交互式添加

    1. **交互式添加更改**：

        - 运行 `git add -p`，Git 会提示你选择哪些更改要添加到暂存区。

        - 你可以选择只添加 `file1.txt` 的更改，然后提交：

            ```bash
            git commit -m "提交 file1.txt 的更改"
            ```

        - 然后，你可以再次运行 `git add -p` 来添加 `file2.txt` 的更改，并提交：

            ```bash
            git commit -m "提交 file2.txt 的更改"
            ```





#### 提交分支

> 从你提供的错误信息来看，你在尝试将本地的 `L0` 分支推送到远程仓库时遇到了两个问题：
>
> 1. **fatal: 'L0' does not appear to be a git repository**：
>    这个错误表明 `L0` 被误认为是远程仓库的名称，而不是分支名称。你需要确保在 `git push` 命令中正确指定了远程仓库和分支。
>
> 2. **error: src refspec upstream does not match any**：
>    这个错误表明你尝试将本地分支推送到 `upstream` 远程仓库，但是 `upstream` 远程仓库中没有对应的分支可以接收推送。
>
> 针对这些问题，你可以按照以下步骤操作：
>
> - 步骤1：检查远程仓库的分支
>
>     首先，你需要检查远程仓库 `origin` 和 `upstream` 中有哪些分支。使用以下命令：
>
>     ```bash
>     git branch -r
>     ```
>
>     这将列出所有远程分支。
>
> - 步骤2：推送到正确的远程仓库
>
>     根据你的需求，你似乎想要将 `L0` 分支推送到 `origin` 远程仓库。确保使用正确的远程仓库名称和分支名称。使用以下命令：
>
>     ```bash
>     git push origin L0
>     ```
>
>     这个命令将 `L0` 分支推送到 `origin` 远程仓库。
>
> - 步骤3：检查权限和仓库存在性
>
>     如果仍然遇到权限问题或仓库不存在的错误，请确保：
>
>     - 你有正确的访问权限。
>     - 远程仓库URL正确无误。
>
> - 步骤4：解决分支不匹配问题
>
>     如果 `upstream` 远程仓库中没有 `L0` 分支，你可以选择：
>
>     - 在 `upstream` 仓库中创建一个新的分支，然后推送：
>
>         ```bash
>         git push upstream L0
>         ```
>
>     - 或者，如果你只想推送到 `origin` 仓库，确保使用正确的远程仓库名称。



#### 更改仓库名称

当你在远程仓库（比如GitHub、GitLab等）更改了仓库名称后，你需要更新本地仓库的远程URL以匹配新的仓库名称。以下是你可以按照的步骤：

1. **打开命令行工具**：
   打开你的命令行工具（在Windows上是CMD或PowerShell，在macOS或Linux上是Terminal）。

2. **切换到你的本地仓库目录**：
   使用`cd`命令切换到你的本地仓库目录。例如：
   ```bash
   cd path/to/your/local/repo
   ```

3. **查看当前的远程仓库URL**：
   你可以使用以下命令来查看当前配置的远程仓库URL：
   ```bash
   git remote -v
   ```

4. **更改远程仓库的URL**：
   使用`git remote set-url`命令来更改远程仓库的URL。你需要将`origin`（这是默认的远程仓库名称）的URL更改为新的URL。假设你的新仓库URL是`https://github.com/username/ics2024.git`，你可以这样做：
   ```bash
   git remote set-url origin https://github.com/username/ics2024.git
   ```

5. **再次查看远程仓库URL**：
   再次使用`git remote -v`来确认URL已经更改：
   ```bash
   git remote -v
   ```

6. **拉取最新的更改**：
   如果远程仓库中有新的更改，你可以使用以下命令来拉取这些更改：
   ```bash
   git pull origin main
   ```
   这里假设`main`是你的默认分支名称。如果你的仓库使用的是`master`或其他分支名称，请相应地替换。

7. **推送本地更改**：
   如果你有本地更改需要推送到远程仓库，可以使用以下命令：
   ```bash
   git push origin main
   ```

通过这些步骤，你的本地仓库就会同步到新的远程仓库名称。记得在团队协作中通知其他成员也更新他们的远程仓库URL。



#### 更新子模块仓库名称

```bash
git submodule update --remote --merge
```







#### **清理提交历史**：git reabse -i HEAD~n 

起初是因为在做 NJU OS lab的时候往GitHub上提交了很多的垃圾日志（编译记录），就想着有没有什么办法能够去除掉已经提交的日志，我能想到的，别人肯定也想到过，也肯定有相关工具，就 AI 搜到了 rebase。

[Git - git-rebase Documentation](https://git-scm.com/docs/git-rebase)

[git rebase | Atlassian Git Tutorial](https://www.atlassian.com/git/tutorials/rewriting-history/git-rebase)

> 比如，删除本地仓库中 M2 分支的某个特定提交，可以使用 `git rebase -i` 命令进行交互式变基操作。以下是具体步骤：
>
> 1. **切换到 M2 分支**（如果尚未切换）：
>    ```bash
>    git checkout M2
>    ```
>
> 2. **启动交互式变基**：
>    ```bash
>    git rebase -i HEAD~N
>    ```
>    - `N` 是你想要回溯的提交数量。例如，如果你想要回溯到包含垃圾日志的提交，可以将 `N` 设置为包含这些提交的数量。假设你知道垃圾日志是在最近的 5 个提交中，那么可以使用 `HEAD~5`。
>
> 3. **编辑提交历史**：
>    - 执行上述命令后，Git 会打开一个文本编辑器（通常是 Vim 或 Nano），列出最近的 `N` 个提交。
>    - 在编辑器中，你会看到类似以下的内容：
>      ```
>      pick 1234567 Commit message 1
>      pick 2345678 Commit message 2
>      pick 3456789 Commit message 3
>      pick 4567890 Commit message 4
>      pick 5678901 Commit message 5
>      ```
>    - 找到包含垃圾日志的提交，将其前面的 `pick` 改为 `drop`。例如，如果垃圾日志在第三个提交中，修改为：
>      ```
>      pick 1234567 Commit message 1
>      pick 2345678 Commit message 2
>      drop 3456789 Commit message 3
>      pick 4567890 Commit message 4
>      pick 5678901 Commit message 5
>      ```
>    - 保存并退出编辑器。在 Vim 中，可以按 `:wq` 保存并退出；在 Nano 中，可以按 `Ctrl+X`，然后按 `Y` 确认保存，最后按 `Enter` 退出。
>
> 4. **完成变基**：
>    - Git 会根据你的修改重新应用提交，垃圾日志的提交会被删除。
>    - 如果在变基过程中遇到冲突，Git 会提示你解决冲突。解决冲突后，使用 `git add` 添加更改，并继续变基：
>      ```bash
>      git rebase --continue
>      ```
>
> - 注意事项
>
>     - **备份**：在进行交互式变基之前，建议备份你的代码，以防意外丢失重要数据。
>
>     - **强制推送**：如果你已经将 M2 分支推送到远程仓库，删除提交后需要使用 `git push --force` 强制推送到远程仓库：
>
>         ```bash
>         git push --force origin M2
>         ```
>
>         - **注意**：强制推送会覆盖远程仓库的历史，可能会对其他协作者造成影响。在执行强制推送之前，请确保与团队成员沟通，并确保不会丢失重要的提交.
>
> 通过这些步骤，你可以删除 M2 分支中的特定提交，从而清理垃圾日志。



更多操作：

> 在 Git 的交互式变基（Interactive Rebase）中，`pick`、`edit`、`squash` 和 `fixup` 是一些常用的命令，用于在变基过程中对提交进行操作和优化。以下是对这些操作的详细解释：
>
> 1. `pick`
>
> - **作用**：选择一个提交，将其应用到新的基底上。
> - **示例**：
>   ```plaintext
>   pick 1234567 Commit message for the first commit
>   pick 2345678 Commit message for the second commit
>   ```
>   这将按顺序应用这两个提交。
>
> 2. `edit`
>
> - **作用**：选择一个提交，将其应用到新的基底上，并在应用后暂停，允许你编辑该提交。
> - **示例**：
>   ```plaintext
>   pick 1234567 Commit message for the first commit
>   edit 2345678 Commit message for the second commit
>   ```
>   这将首先应用第一个提交，然后在第二个提交应用后暂停，你可以在这个阶段修改文件、添加或删除更改，然后继续变基。
>
> 3. `squash`
>
> - **作用**：将多个提交合并为一个提交。合并后的提交将包含所有被合并提交的更改，但只会保留一个提交记录。
> - **示例**：
>   ```plaintext
>   pick 1234567 Commit message for the first commit
>   squash 2345678 Commit message for the second commit
>   squash 3456789 Commit message for the third commit
>   ```
>   这将把第二个和第三个提交合并到第一个提交中，最终只有一个提交记录。
>
> 4. `fixup`
>
> - **作用**：类似于 `squash`，但 `fixup` 会将多个提交合并为一个提交，并且不会保留被合并提交的提交信息。
> - **示例**：
>   ```plaintext
>   pick 1234567 Commit message for the first commit
>   fixup 2345678 Commit message for the second commit
>   fixup 3456789 Commit message for the third commit
>   ```
>   这将把第二个和第三个提交的更改合并到第一个提交中，但不会保留第二个和第三个提交的提交信息。
>
> 5. `reword`
>
> - **作用**：选择一个提交，将其应用到新的基底上，并在应用后暂停，允许你修改该提交的提交信息。
> - **示例**：
>   ```plaintext
>   pick 1234567 Commit message for the first commit
>   reword 2345678 Commit message for the second commit
>   ```
>   这将首先应用第一个提交，然后在第二个提交应用后暂停，你可以在这个阶段修改提交信息，然后继续变基。
>
> 6. `drop`
>
> - **作用**：删除一个提交，不将其应用到新的基底上。
> - **示例**：
>   ```plaintext
>   pick 1234567 Commit message for the first commit
>   drop 2345678 Commit message for the second commit
>   ```
>   这将应用第一个提交，但不会应用第二个提交，第二个提交将被删除。
>
> - 示例
>
>     假设你有以下提交历史：
>
>     ```
>     A - B - C - D [main]
>          \
>           E - F - G [feature]
>     ```
>
>     你希望将 `feature` 分支变基到 `main` 分支，并优化提交历史。你可以使用以下命令：
>
>     ```sh
>     git checkout feature
>     git rebase -i main
>     ```
>
>     这将打开一个文本编辑器，列出 `feature` 分支上的所有提交：
>
>     ```plaintext
>     pick e123456 Commit message for E
>     pick f234567 Commit message for F
>     pick g345678 Commit message for G
>     ```
>
>     你可以修改这个文件，例如：
>
>     ```plaintext
>     pick e123456 Commit message for E
>     squash f234567 Commit message for F
>     fixup g345678 Commit message for G
>     ```
>
>     保存并关闭编辑器后，Git 将开始变基操作。如果选择 `squash` 或 `fixup`，Git 会暂停并要求你合并提交信息。你可以编辑合并后的提交信息，然后保存并退出编辑器，继续变基。
>
> - 总结
>     - **`pick`**：选择并应用提交。
>     - **`edit`**：选择并应用提交，暂停以便编辑。
>     - **`squash`**：合并多个提交为一个提交，保留提交信息。
>     - **`fixup`**：合并多个提交为一个提交，不保留提交信息。
>     - **`reword`**：选择并应用提交，暂停以便修改提交信息。
>     - **`drop`**：删除提交，不应用。
>
> 通过这些操作，你可以灵活地优化和清理提交历史，使项目的历史更加清晰和易于维护。





#### stash 和 pop

在 Git 中，如果你在当前分支上进行了一些开发但还没有提交，这时有另一个任务需要处理，你可以按照以下步骤来保存当前的工作并创建一个新的分支来处理新任务：

步骤 1：保存当前未提交的更改

使用 `git stash` 命令将当前未提交的更改暂存起来。这会将你的工作现场保存到一个堆栈中，使你可以切换到其他分支而不必提交当前的更改。

```bash
git stash
```



步骤 2：创建并切换到新分支

使用 `git checkout -b` 命令创建一个新的分支并切换到该分支。

```bash
git checkout -b new-feature-branch
```



步骤 3：在新分支上进行开发

现在你可以在新分支上进行新任务的开发工作。



步骤 4：提交新分支的更改

完成新任务的开发后，将更改提交到新分支。

```bash
git add .
git commit -m "完成新任务的开发"
```

步骤 5：切换回原来的分支

完成新任务后，你可以切换回原来的分支，继续之前的工作。

```bash
git checkout original-branch
```



步骤 6：恢复暂存的更改

切换回原来的分支后，使用 `git stash pop` 命令将之前暂存的更改恢复出来，继续进行开发。

```bash
git stash pop
```



总结

通过以上步骤，你可以有效地在 Git 中处理多个任务，而不会互相干扰。以下是完整的流程：

1. **保存当前工作**：`git stash`
2. **创建并切换到新分支**：`git checkout -b new-feature-branch`
3. **在新分支上开发并提交**
4. **切换回原来分支**：`git checkout original-branch`
5. **恢复暂存的工作**：`git stash pop`

这样，你就可以在不同的任务之间灵活切换，同时保持代码的整洁和有序。

