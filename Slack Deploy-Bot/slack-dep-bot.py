#!/usr/bin/env python

import os
import time
import logging
import logging.handlers
import subprocess
import shutil
import sys

from slackclient import SlackClient


BOT_USER = 'U9RD6GS5C'
BOT_MENTION = '<@%s>' % BOT_USER
BOT_NAME = 'deploybot'
SLACK_CHANNEL = 'infra'
try:
    SLACK_TOKEN = os.environ['SLACK_TOKEN']
except KeyError:
    LOGGER.error("No Slack token found in environment variable")
    print "Please export the Slack auth token."
    print "export SLACK_TOKEN='xxxxxxxxxxxxxxxxxxxxxxxxxxxx'"
    sys.exit(1)

# C9A4P9LLR - infra
SLACK_CHANNEL_ID = ['C9A4P9LLR']
SUPPORTED_APPS = [ 'node-app' ]
SUPPORTED_ENVS = [ 'dev' ]
LOG_FILE = '/tmp/deploybot.log'
TMP_PATH = '/tmp/deploy/'


APP_INFO = {
                'node-app': {
                            'git_url': 'git@github.com:nitinprabhakaran/<Repo_Name_that_Contains_dockerFile_and_k8s_Manifests>',
                            'app_path': 'demo_app',
                            'image_tag': 'gcr.io/my-gcp-project/dummy-node-test',
                            'k8s_deployment_name': 'node-demo',
                            'k8s_container_name': 'nodejs',
                            'k8s_cluster_name': 'my-test-cluster',
                            'gcp_zone': 'asia-south1-a',
                            'project': 'my-gcp-project',
                },
        }

HELP_TEXT = '''
```
Usage: @deploy <action> <app name> <envionment> <branch name>
Supported Commands:
    help     - Show this help message
    deploy   - Perform a deploy of a supported app
    rollback - Rollback a previous deploy
Example:
    @deploybot deploy node-app dev feature-1
    @deploybot rollback node-app dev
```
'''

slack =  SlackClient(SLACK_TOKEN)

def get_logger(log_file, tag):
    try:
        logger = logging.getLogger(tag)
        logger.setLevel(logging.DEBUG)
        ch = logging.handlers.RotatingFileHandler(
            log_file, maxBytes=250000000, backupCount=1)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    except Exception, e:
        logging.critical("Failed to configure logging handler: %s" % str(e))
        sys.exit(1)
    return logger



def shell_exec(cmd, output=False):
    try:
        LOGGER.info("Executing: `%s`" % cmd)
        print cmd
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        if proc.returncode != 0:
            LOGGER.error("Command `%s` returned non zero exit code" % cmd)
            if err != '':
                LOGGER.error(err)
            return False

        # if the caller asked for the stdout and if stdout is not empty, send it back
        if output and out:
            return out
        return True
    except Exception, e:
        LOGGER.error("Something went wrong while executing the command")
        LOGGER.error("Command : `%s`" % cmd)
        LOGGER.error(str(e))
        return False


def build_docker_image(path, tag):
    ''' Build the docker image from the cloned repo's Dockerfile '''

    LOGGER.info("Building the docker image : `%s`" % tag)
    send_message("Building the docker image : `%s`" % tag)

    cmd = "docker build -t %s %s >> /tmp/deploy/docker-build.log" % (tag, path)
    if shell_exec(cmd):
        LOGGER.info("Docker image build completed")
        send_message("Docker image build completed")
        return
    else:
        LOGGER.error("Failed to build the docker image")
        send_message("Failed to build the docker image")
        return

def push_to_gcr(tag):
    ''' Push the docker image to GCR '''

    cmd = "gcloud docker -- push %s" % tag
    LOGGER.info("Pushing the image to GCR")
    send_message("Pushing the docker image to the registry")
    if shell_exec(cmd):
        LOGGER.info("Successfully pushed the image to GCR")
        send_message("Successfully pushed the image to the registry")
        return
    else:
        send_message("Failed to upload the image to registry. Aborting")
        return

def get_cluster_creds(app_name):
    ''' Get GKE cluster credentials so that we can rollout k8s deployments'''

    cluster_name = APP_INFO[app_name]['k8s_cluster_name']
    zone = APP_INFO[app_name]['asia-south1-a']
    project = APP_INFO[app_name]['project']
    cmd = "gcloud container clusters get-credentials %s --zone %s --project %s" % (cluster_name, zone, project)
    LOGGER.info("Retrieving cluster credentials")
    send_message("Retrieving cluster credentials")
    if shell_exec(cmd):
        LOGGER.info("Successfully retrieved the credentials")
        send_message("Successfully retrieved the credentials")
        return
    else:
        LOGGER.error("Failed to fetch cluster credentials")
        send_message("Failed to fetch cluster credentials. Aborting")
        return

def rollout_k8s(app_name, tag):
    ''' Rollout the image to k8s '''

    deployment_name = APP_INFO[app_name]['k8s_deployment_name']
    container_name = APP_INFO[app_name]['k8s_container_name']
    cmd = "kubectl set image deployment/%s %s=%s" % (deployment_name, container_name, tag)
    LOGGER.info("Rolling out the deployment `%s`, New image: `%s`" % (deployment_name, tag))
    send_message("Rolling out the deployment `%s`, New image: `%s`" % (deployment_name, tag))
    if shell_exec(cmd):
        LOGGER.info("Rollout succeeded")
        send_message("Successfully rolled out")
    else:
        LOGGER.error("Rollout failed")
        send_message("Rollout failed")
    return


def send_message(text):
    ''' Send a message to the Slack channel '''

    try:
        slack.rtm_send_message(channel=SLACK_CHANNEL, message=text)
    except Exception, e:
        print "Failed to send the message: %s" % str(e)


def action_help():
    ''' Print the help message '''

    send_message(HELP_TEXT)

def action_deploy(action, event):
    ''' Do the deployment '''

    LOGGER.info("Deployment is requested")
    parts = action.split()
    if len(parts) != 4:
        send_message("I think you missed some options")
        action_help()
        return
    send_message("Initiating deployment")
    app_name = parts[1].strip()
    environment = parts[2].strip()
    git_branch = parts[3].strip()
    LOGGER.info("App: %s,  Env: %s,  Branch: %s" % (app_name, environment, git_branch))
    if app_name not in SUPPORTED_APPS:
        LOGGER.info("Unsupported app : %s. Aborting deployment" % app_name)
        send_message("The app `%s` is not supported. Aborting deployment" % app_name)
        supported_apps = ', '.join(SUPPORTED_APPS)
        send_message("Supported apps: %s" % supported_apps)
        return
    if environment not in SUPPORTED_ENVS:
        LOGGER.info("Unsupported env : %s. Aborting deployment" % environment)
        send_message("The environment `%s` is not yet supported. Aborting deployment" %environment)
        supported_envs = ', '.join(SUPPORTED_ENVS)
        send_message("Supported environments: %s" % supported_envs)
        return

    LOGGER.info("Checking if the git branch `%s` exists" % git_branch)

    git_url = APP_INFO[app_name]['git_url']
    app_path = APP_INFO[app_name]['app_path']

    cmd = "git ls-remote --heads %s | grep -w 'refs/heads/%s'" % (git_url, git_branch)

    if not shell_exec(cmd, output=True):
        LOGGER.warning("The branch `%s` is not present on the remote" % git_branch)
        send_message("There is no branch `%s` present in upstream. Aborting" % git_branch)
        return
    LOGGER.info("Found the branch in upstream. Proceeding with deployment")

    if os.path.isdir(TMP_PATH):
        LOGGER.info("Cleaning up `%s`" % TMP_PATH)
        try:
            shutil.rmtree(TMP_PATH, ignore_errors=True)
        except Exception, e:
            LOGGER.error("Failed to cleanup the temp directory: %s" % str(e))

    cmd = "git clone -b %s %s %s" % (git_branch, git_url, TMP_PATH)
    LOGGER.info("Cloning the repository `%s`" % git_url)
    send_message("Cloning the repository `%s`" % git_url)
    if shell_exec(cmd):
        LOGGER.info("Cloned the repository")
        send_message("Cloned the repo")
    else:
        LOGGER.error("Failed to clone the repository. Aborting")
        send_message("Failed to clone the repository. Aborting")

        return

    LOGGER.info("Building the docker image")
    dockerfile_path = TMP_PATH + app_path
    # It's a good idea to use the short commit id as the image tag
    cmd = "cd %s; git rev-parse --short HEAD" % dockerfile_path
    commit_id = shell_exec(cmd, True)
    if not commit_id:
        LOGGER.error("Could not get the commit id from the repo. Aborting")
        send_message("Could not get the commit id from the repo. Aborting")
        return
    # This will be the tag of the Docker image
    image_tag = APP_INFO[app_name]['image_tag'] + ':' + commit_id.strip()

    # Let's build the image
    build_docker_image(dockerfile_path, image_tag)

    # Push the image to the docker registry. As of now, only GCR is supported
    push_to_gcr(image_tag)

    # Roll it out
    rollout_k8s(app_name, image_tag)


def action_rollback(action, event):
    send_message("Rolling back")

def process_events(events):
    for event in events:
        message = event.get('text')
        if message and message.startswith(BOT_MENTION):
            # It's a mention of the bot
            channel = event.get('channel')
            LOGGER.info("BOT is being summoned on channel : %s" % channel)

            if channel not in SLACK_CHANNEL_ID:
                send_message("Hi <@%s>, This channel is not authorized to run the bot" % event['user'])
                LOGGER.info("The channel is not authorized to summon the bot")
                return

            # get the action
            action = message.split(BOT_MENTION)[1].strip()
            LOGGER.info("Action requested: `%s`" % action)
            if action.startswith(('help', '?', 'hi', 'hello')):
                action_help()
            elif action.startswith('deploy '):
                action_deploy(action, event)
            elif action.startswith('rollback '):
                action_rollback(action, event)
            else:
                send_message("Unknown action. `%s`" % action)
                action_help()
        else:
            return



def main():
    global LOGGER
    LOGGER = get_logger(LOG_FILE, 'deploybot')

    try:
        slack.rtm_connect()
        LOGGER.info("Connected to Slack")
        LOGGER.info("Listening for events")
        while True:
            events = slack.rtm_read()
            if events:
                process_events(events)
            time.sleep(1)
    except Exception, e:
        LOGGER.error("Failed to connect to slack API")
        LOGGER.error(str(e))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print "Killed"
        sys.exit(1)
