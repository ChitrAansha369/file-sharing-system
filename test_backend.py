
import pytest
from app import create_app, db
from app.models import User, File
from flask import json
import io

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['UPLOAD_FOLDER'] = 'uploads_test'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_signup(client):
    response = client.post('/auth/signup', json={
        "email": "client@example.com",
        "password": "client123"
    })
    assert response.status_code == 201

def test_duplicate_signup(client):
    client.post('/auth/signup', json={
        "email": "client@example.com",
        "password": "client123"
    })
    response = client.post('/auth/signup', json={
        "email": "client@example.com",
        "password": "client123"
    })
    assert response.status_code == 409

def test_login(client):
    client.post('/auth/signup', json={
        "email": "ops@example.com",
        "password": "ops123"
    })
    with client.application.app_context():
        user = User.query.filter_by(email="ops@example.com").first()
        user.role = "ops"
        db.session.commit()
    response = client.post('/auth/login', json={
        "email": "ops@example.com",
        "password": "ops123"
    })
    assert response.status_code == 200
    assert "access_token" in json.loads(response.data)

def test_upload_file_as_ops(client):
    client.post('/auth/signup', json={
        "email": "ops@example.com",
        "password": "ops123"
    })
    with client.application.app_context():
        user = User.query.filter_by(email="ops@example.com").first()
        user.role = "ops"
        db.session.commit()
    login_res = client.post('/auth/login', json={
        "email": "ops@example.com",
        "password": "ops123"
    })
    token = json.loads(login_res.data)['access_token']

    data = {
        'file': (io.BytesIO(b"dummy content"), 'test.docx')
    }
    res = client.post('/ops/upload',
                      headers={"Authorization": f"Bearer {token}"},
                      data=data,
                      content_type='multipart/form-data')
    assert res.status_code == 201

def test_list_files_as_client(client):
    client.post('/auth/signup', json={
        "email": "ops@example.com",
        "password": "ops123"
    })
    with client.application.app_context():
        user = User.query.filter_by(email="ops@example.com").first()
        user.role = "ops"
        db.session.commit()
    login_res = client.post('/auth/login', json={
        "email": "ops@example.com",
        "password": "ops123"
    })
    token_ops = json.loads(login_res.data)['access_token']
    client.post('/ops/upload',
                headers={"Authorization": f"Bearer {token_ops}"},
                data={'file': (io.BytesIO(b"content"), 'demo.docx')},
                content_type='multipart/form-data')

    client.post('/auth/signup', json={
        "email": "client@example.com",
        "password": "client123"
    })
    login_client = client.post('/auth/login', json={
        "email": "client@example.com",
        "password": "client123"
    })
    token_client = json.loads(login_client.data)['access_token']

    res = client.get('/client/files', headers={"Authorization": f"Bearer {token_client}"})
    assert res.status_code == 200
    assert "download_url" in json.loads(res.data)[0]
