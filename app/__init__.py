import subprocess
import os

from flask import Flask, request, jsonify

application = Flask(__name__)

TUNNEL_SERVER_REGISTRY_PATH = 'sharedcloud/sharedcloud-tunnel-server'
CONTAINER_NAME_PATTERN = 'sharedcloud-tunnel-server-http-{}-tcp-{}'


def _has_invalid_valid_token(request):
    token = request.form.get('proxy_access_token')

    return (not token or token != os.environ.get('ACCESS_TOKEN'))


def _get_data_from_request(request):
    return (
        request.form.get('http_service_port'),
        request.form.get('tcp_port'),
        request.form.get('token'),
        request.form.get('authentication_timeout'),
    )


@application.route("/tunnel-manager/open-tunnel", methods=['POST'])
def open_tunnel():
    """
    Open a tunnel based on the ports provided in the POST request
    :return:
    """
    if _has_invalid_valid_token(request):
        return jsonify({
            'status_code': 401,
            'output': '',
            'error': 'Unauthorized.'
        })

    http_service_port, tcp_port, token, authentication_timeout = _get_data_from_request(request)

    cmd_args = [
        'docker', 'login', '-u', os.environ.get('DOCKERHUB_USERNAME'),
        '-p', os.environ.get('DOCKERHUB_PASSWORD')
    ]

    p = subprocess.Popen(cmd_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.communicate()

    if not all([http_service_port, tcp_port, token, authentication_timeout is not None]):
        return jsonify({
            'status_code': 400,
            'output': '',
            'error': 'Invalid request.'
        })

    p = subprocess.Popen(['docker', 'pull', TUNNEL_SERVER_REGISTRY_PATH], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.communicate()

    cmd_args = [
        'docker', 'run', '--name', CONTAINER_NAME_PATTERN.format(http_service_port, tcp_port),
        '-e', 'HTTP_SERVICE_PORT={}'.format(http_service_port),
        '-e', 'TCP_PORT={}'.format(tcp_port),
        '-e', 'TOKEN={}'.format(token),
        '-e', 'AUTHENTICATION_TIMEOUT={}'.format(authentication_timeout),
        '-p', '{}:{}'.format(http_service_port, http_service_port),
        '-p', '{}:{}'.format(tcp_port, tcp_port),
        TUNNEL_SERVER_REGISTRY_PATH
    ]

    subprocess.Popen(cmd_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    return jsonify({
        'status_code': 200,
        'output': 'Tunnel successfully opened.',
        'error': ''
    })


@application.route("/tunnel-manager/close-tunnel", methods=['POST'])
def close_tunnel():
    """
    Close the tunnel created previously.
    :return:
    """
    if _has_invalid_valid_token(request):
        return jsonify({
            'status_code': 401,
            'output': '',
            'error': 'Unauthorized.'
        })

    http_service_port, tcp_port, _, _ = _get_data_from_request(request)

    if not all([http_service_port, tcp_port]):
        return jsonify({
            'status_code': 400,
            'output': '',
            'error': 'Invalid request.'
        })

    cmd_args = [
        'docker', 'rm', '-f', CONTAINER_NAME_PATTERN.format(http_service_port, tcp_port)]
    p = subprocess.Popen(cmd_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = p.communicate()

    return jsonify({
        'status_code': 200,
        'output': str(output),
        'error': str(error)
    })
