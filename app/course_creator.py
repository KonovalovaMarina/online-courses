import gitlab
from gitlab import Gitlab
from gitlab.v4 import objects
import typing as t

gl: Gitlab = gitlab.Gitlab('https://gitlab.com/', private_token='zwssJW89vD66DJ2xE2M8')

main_group_id: int = 8345723
main_projects_id: t.Dict[str, int] = {'python': 19477176}

#main_group_id: int = 9409848
#main_projects_id: t.Dict[str, int] = {'python': 21188140}

try:
    projects: t.Dict[str, gitlab.v4.objects.Project] = \
        {project_name: gl.projects.get(project_id) for (project_name, project_id) in main_projects_id.items()}
except gitlab.exceptions.GitlabGetError as e:
    print(e.error_message)


def repository_creator(course, list_login):
    try:
        subgroup_course: gitlab.v4.objects.Group = gl.groups.create({'name': course, 'path': course + '_path',
                                                                     'parent_id': main_group_id, 'visibility': 'private'})
    except gitlab.exceptions.GitlabHttpError as e:
        return e.error_message
    except gitlab.exceptions.GitlabCreateError as e1:
        return e1.error_message

    for login in list_login:
        try:
            subgroup_student: gitlab.v4.objects.Group = gl.groups.create({'name': login, 'path': login+'_path',
                                                                          'parent_id': subgroup_course.id,
                                                                          'visibility': 'private'})
        except gitlab.exceptions.GitlabHttpError as e:
            subgroup_course.delete()
            return e.error_message
        try:
            projects[course].forks.create({'namespace': subgroup_student.id})
        except gitlab.exceptions.GitlabCreateError as e:
            subgroup_course.delete()
            return e.error_message
        user: gitlab.v4.objects.User = gl.users.list(username=login)[0]
        try:
            subgroup_student.members.create({'user_id': user.id,
                                             'access_level': gitlab.DEVELOPER_ACCESS})
        except gitlab.exceptions.GitlabCreateError as e:
            subgroup_course.delete()
            return e.error_message
