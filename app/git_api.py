import logging
from contextlib import contextmanager
from pathlib import Path

from git import InvalidGitRepositoryError, Repo

from app import settings
from app.models import TaskSolution

logging.basicConfig(level=logging.DEBUG)

git_ssh_cmd = 'ssh -i %s' % settings.SOLUTIONS_REPO_SSH_KEY


def clone_repo():
    repo = Repo.clone_from(settings.SOLUTIONS_REPO_URI, settings.SOLUTIONS_REPO_PATH, env={"GIT_SSH_COMMAND": git_ssh_cmd})
    return repo


try:
    repo = Repo(settings.SOLUTIONS_REPO_PATH)
except InvalidGitRepositoryError:
    repo = clone_repo()

repo.git.update_environment(GIT_SSH_COMMAND=git_ssh_cmd)


def checkout_main():
    repo.git.clean('-xdf')
    repo.git.checkout('main')


def sync_repo():
    # удаляем все незакомиченные файлы если они есть чтобы при стягивании не было конфликтов
    # и чекаутимся стягиваем свежий main чтоб ветка с решением создавалась от него
    checkout_main()
    repo.git.pull()


def checkout_or_create_branch(branch_name):
    ref_names = {r.name for r in repo.references}
    if branch_name in ref_names:
        # если ветка есть по какой то причине то переходим на нее (практически невозможный кейс)
        repo.git.checkout(branch_name)
    else:
        # создаем ветку и переходим на нее
        repo.git.checkout("-b", branch_name)


@contextmanager
def checkout_branch(branch_name):
    try:
        checkout_or_create_branch(branch_name)
        yield
    finally:
        checkout_main()


def commit_solution(solution: TaskSolution):
    sync_repo()

    with checkout_branch(solution.branch_name):
        dst = Path(f'tasks/{solution.task.code}.py')

        with solution.file.get_store().open(solution.file.path) as f:
            repo_dst = Path(repo.working_dir) / dst
            repo_dst.write_bytes(f.read())

        repo.git.add(str(dst))

        repo.index.commit(f'Решение задачи {solution.task.code} студентом {solution.user.login}')

        # ci.variable нужна чтобы запускать тесты только для нужной нам таски
        repo.git.push(
            "-o", f'ci.variable=CI_TASK_CODE={solution.task.code}',
            "-o", f'ci.variable=CI_TASK_UPDATE_URL={solution.get_update_url()}',
            '--set-upstream', 'origin', solution.branch_name
        )

        return repo.head.object.hexsha
