# django-ecs-deploy

Make config files from Django settings variables and templates.

## Installation

From your Django app, install the module from pip:

	pip install django-ecs-deploy
	
Then make sure it is included in your `INSTALLED_APPS` section:

	INSTALLED_APPS = (
		...
	    'ecs-deploy',
	)

## Usage

This command assumes you're using [jwilder/nginx-proxy](https://github.com/jwilder/nginx-proxy) for your web server setup. It also uses your Django settings as well as environment variables to configure builds. It expects the following variables:

### Settings / Environment Variables

`django-ecs-deploy` looks for the following settings in the `settings` file and from your environment. Environment variables will override `settings`:

* `PROJECT` - The name of your project for use as a basename for tasks and Docker image names. Untested with special characters.
* `TIER` - Used in conjunction with the `BUILD_ID` environment setting for Docker image versioning (`staging125`) and with `PROJECT` to define ECS task names (`myproject-staging`)
* `DOCKER_REPOSITORY` - The name of the docker repo to store images in
* `DOCKER_IMAGE` - The name of the base docker image
* `BUILD_ID` - Used along with `TIER` for the image version (`staging124`)
* `DJANGO_SETTINGS_MODULE` - The tier you use to run this command will also be set in the ECS Task's container
* `VIRTUAL_HOST` (optional) - For use with [jwilder/nginx-proxy](https://github.com/jwilder/nginx-proxy)
* `DOCKER_APT_PACKAGES` (optional) - If set, a list of Debian package names will be installed
* `DOCKER_YUM_PACKAGES` (optional) - If set, a list of Yum package names will be installed
* `COMPRESS_ENABLED` (optional) - If set, `python manage.py compress --force` will be run during image build
* `ECS_CLUSTER` (optional) - Defaults to `default`. If set, override ECS cluster name your services will be deployed to.
* `DOCKER_MAX_MEMORY` (optional) - Defaults to 256. Sets max memory in task definition.

#### Port Mapping

Mapping one port is currently supported using the following settings:

* `DOCKER_HOST_PORT` (optional) - The port to use on the host machine. No mapping will be configured if this is not set.
* `DOCKER_CONTAINER_PORT` (optional) - Defaults to `DOCKER_HOST_PORT`
* `DOCKER_PORT_PROTOCOL` (optional) - Defaults to `tcp`

#### Secure Credential Deployment

The following three keys require `awscli` to be installed via your `requirements.txt`:

* `CREDENTIALS_BUCKET` (optional) - source s3 bucket name to retrieve credentials onto Docker container
* `CREDENTIALS_KEY` (optional) - source s3 key for credentials
* `CREDENTIALS_DEST_PATH` (optional) - path to place credentials file on remote server. `pwd` is `/usr/src/app`

The basic command for the retrieval of the credentials counts on an IAM role with access to your bucket, and looks like this:

	aws s3 sync s3://{{ CREDENTIALS_BUCKET }}/{{ CREDENTIALS_KEY }} {{ CREDENTIALS_DEST_PATH }}

### Execution

Set the appropriate settings and environment variables, then run:

	python manage.py ecsdeploy

## Possible Features

I threw this together to serve a need. It makes a lot of assumptions right now about the way you're using it, like what is required vs. optional, etc. I'm totally open to pull requests that make the system more flexible.

The system assumes you have a service created based on `PROJECT` and `TIER` in your settings, and will not create the service for you or use different names.
