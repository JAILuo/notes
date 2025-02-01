import os
import subprocess
import logging

# 配置日志
logging.basicConfig(filename="deploy.log", level=logging.INFO, format="%(asctime)s - %(message)s")


def run_command(command):
    """运行系统命令并捕获输出"""
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logging.info(f"命令成功：{command}")
        print(result.stdout)
        return result.stdout
    except subprocess.CalledProcessError as e:
        logging.error(f"命令失败：{command}\n错误信息：{e.stderr}")
        print(f"命令执行失败：{e.stderr}")
        exit(1)


def main():
    # 检查当前分支是否为 main
    current_branch = run_command("git rev-parse --abbrev-ref HEAD").strip()
    if current_branch != "main":
        print(f"当前不在 main 分支，当前分支为：{current_branch}")
        print("正在切换到 main 分支...")
        run_command("git checkout main")

    # 提示用户输入提交信息
    commit_message = input("请输入提交信息：").strip()
    if not commit_message:
        print("提交信息不能为空！")
        exit(1)

    # 添加更改并提交到 main 分支
    print("正在提交更改到 main 分支...")
    run_command("git add .")
    run_command(f'git commit -m "{commit_message}"')
    run_command("git push origin main")

    # 部署到 gh-pages 分支
    print("正在部署到 gh-pages 分支...")
    run_command("mkdocs gh-deploy --clean")

    print("文档已更新并部署完成！")


if __name__ == "__main__":
    main()
