# deploy/management/commands/build.py

import os
import sys

from django.conf import settings
from django.core.management.base import BaseCommand
from django.template import loader, Context


class Command(BaseCommand):
    help = 'Build Dockerfile and .ebextensions/ files'

    def render_template(self, source, dest, context):
        template = loader.get_template(source)
        output = template.render(context)
        self.stdout.write('Writing {0}'.format(dest))
        self.write_file(dest, output)

    def write_file(self, dest, output):
        if os.path.splitext(dest)[1] in self.executable_extensions:
            mode = int('0755', 8)
        else:
            mode = int('0644', 8)
        with os.fdopen(
                os.open(dest, os.O_TRUNC | os.O_WRONLY | os.O_CREAT, mode),
                'w') as file_:
            file_.write(output)

    def handle(self, *args, **options):
        settings.TEMPLATE_DEBUG = True
        self.executable_extensions = ('.sh',)
        context = Context({'settings': settings, 'environ': os.environ})

        template_map = {
            'Dockerfile': 'dockerfile.tmpl',
            'start_app.sh': 'gunicorn.tmpl',
            'ecs-task-definition.json': 'ecstask.tmpl',
        }

        for path, template in sorted(template_map.items()):
            self.render_template(template, path, context)

        task_family = '{0.PROJECT}-{0.TIER}'.format(settings)
        docker_version_tag = '{0.TIER}{1}'.format(settings,
                                                  os.environ.get('BUILD_ID'))
        docker_tag_url = '{0.DOCKER_REPOSITORY}/{0.PROJECT}:{1}'.format(
            settings, docker_version_tag)

        if hasattr(settings,
                   'REQUIRES_ECS_LOGIN') and settings.REQUIRES_ECS_LOGIN:
            if os.system('`aws ecr get-login --region us-east-1`') > 0:
                sys.exit(1)

        # TODO: replace all of these commands with boto and py-docker commands
        commands = (
            'docker build -t {0.PROJECT} .'.format(settings),
            'docker tag -f {0.PROJECT} {1}'.format(settings, docker_tag_url),
            'docker push {0}'.format(docker_tag_url),
            'aws ecs register-task-definition --family {0} --cli-input-json '
            'file://ecs-task-definition.json'.format(task_family),
            'aws ecs update-service --cluster default --service {0} '
            '--task-definition'.format(task_family),
        )

        for command in commands:
            result = os.system(command)
            if result != 0:
                print(
                    'Error executing command "{0}". Exiting.'.format(command))
                sys.exit(1)
