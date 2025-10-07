from pathlib import Path
from time import sleep

import docker
import requests
import pytest
from faker import Faker


fake = Faker()


PORT = 8000
LOCAL_PORT = 12345


@pytest.fixture(scope="session")
def dockerfile_path(project_root) -> Path:
    path = project_root / "Dockerfile"
    if not (path.is_file() and len(path.read_text().splitlines()) > 5):
        pytest.skip("Dockerfile is not ready")
    return path


@pytest.fixture
def docker_client():
    return docker.from_env()


@pytest.fixture
def image_name():
    tag = f"online-store-fastapi-image-{fake.word()}:latest"
    print(f"name for image: {repr(tag)}")
    return tag


@pytest.fixture
def build_image(docker_client, project_root, image_name):
    print("Building in", project_root)
    image_object, build_logs = docker_client.images.build(
        path=str(project_root),
        # dockerfile=str(dockerfile_path),
        tag=image_name,
    )
    yield image_object
    # print logs?


@pytest.fixture
def run_image(docker_client, build_image):
    from docker.models.containers import Container
    container: Container = docker_client.containers.run(build_image, detach=True, ports={PORT: LOCAL_PORT})
    print("running docker container detached")
    # give some time to for the web app to start
    sleep(3)
    yield container
    print("stopping docker container")
    container.stop()
    print("docker container stopped")


def test_build_and_run_app(run_image):
    print("sending request to the image")
    resp: requests.Response = requests.get(f"http://localhost:{LOCAL_PORT}/ping/")
    assert resp.status_code == 200
    assert resp.json() == {"message": "pong"}