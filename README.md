# django-ecs-deploy

Make config files from Django settings variables and templates.

## Installation

From your Django app, install the module from pip:

	pip install django-ecs-deploy
	
Then make sure it (and `makeconf`) are included in your `INSTALLED_APPS` section:

	INSTALLED_APPS = (
		...
	    'makeconf',
	    'ecs-deploy',
	)

## Usage

This command assumes you're using [jwilder/nginx-proxy](https://github.com/jwilder/nginx-proxy) for your web server setup. It also uses your Django settings as well as environment variables to configure builds. It expects the following variables:

### Settings Variables

* `PROJECT` - The name of your project for use as a basename for tasks and Docker image names. Untested with special characters.
* `TIER` - Used in conjunction with the `BUILD_ID` environment setting for Docker image versioning (`staging125`) and with `PROJECT` to define ECS task names (`myproject-staging`)
* `DOCKER_REPOSITORY` - The name of the docker repo to store images in
* `DOCKER_IMAGE` - The name of the base docker image
* `VIRTUAL_HOST` (optional) - For use with [jwilder/nginx-proxy](https://github.com/jwilder/nginx-proxy)
* `DOCKER_APT_PACKAGES` (optional) - If set, a list of Debian package names will be installed
* `DOCKER_YUM_PACKAGES` (optional) - If set, a list of Yum package names will be installed
* `COMPRESS_ENABLED` (optional) - If set, `python manage.py compress --force` will be run during image build
* `REQUIRES_ECR_LOGIN` (optional) - Set this to `True` if pushing to and deploying from Amazon ECR. It will execute the correct Docker login command based on your AWS credentials.

### Environment Variables

* `BUILD_ID` - Used along with `TIER` for the image version (`staging124`)
* `RDS_PASSWORD` - The `RDS_PASSWORD` environment variable will be configured in the ECS Task's container definition
* `DJANGO_SETTINGS_MODULE` - The tier you use to run this command will also be set in the ECS Task's container

### Execution

Set the appropriate settings and environment variables, then run:

	python manage.py ecsdeploy

## Possible Features

I threw this together to serve a need. It makes a lot of assumptions right now about the way you're using it, like what's in the environment vs. what's in settings, what is required vs. optional, etc. I'm totally open to pull requests that make the system more flexible.

The system assumes you have a service created based on `PROJECT` and `TIER` in your settings, and will not create the service for you or use different names.
