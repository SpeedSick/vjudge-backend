from django.urls import reverse_lazy

from authentication.models import Profile


def test_register_student_201(db, client):
    data = {
        'username': 'Alan',
        'password': 'qwerty123',
        'email': 'wtf123@mail.ru',
        'first_name': 'Alan',
        'last_name': 'Amanov',
        'is_student': True,
        'is_teacher': False,
    }

    response = client.post(reverse_lazy('registration'), data)
    assert response.status_code == 201
    assert Profile.objects.count() == 1
    user = Profile.objects.last()
    assert user.username == 'Alan'
    assert user.email == 'wtf123@mail.ru'
    assert not user.is_approved
    assert user.is_student
    assert not user.is_teacher
    assert response.data == (
        {
            'id': user.id,
            'username': 'Alan',
            'email': 'wtf123@mail.ru',
            'first_name': 'Alan',
            'last_name': 'Amanov',
            'is_student': True,
            'is_teacher': False,
        }
    )


def test_register_teacher_201(db, client):
    data = {
        'username': 'Alan',
        'password': 'qwerty123',
        'email': 'wtf123@mail.ru',
        'first_name': 'Alan',
        'last_name': 'Amanov',
        'is_student': False,
        'is_teacher': True,
    }
    response = client.post(reverse_lazy('registration'), data)
    assert response.status_code == 201
    assert Profile.objects.count() == 1
    user = Profile.objects.last()
    assert user.username == 'Alan'
    assert user.email == 'wtf123@mail.ru'
    assert not user.is_approved
    assert user.is_teacher
    assert not user.is_student
    assert response.data == (
        {
            'id': user.id,
            'username': 'Alan',
            'email': 'wtf123@mail.ru',
            'first_name': 'Alan',
            'last_name': 'Amanov',
            'is_student': False,
            'is_teacher': True,
        }
    )


def test_register_teacher_with_approved_201(db, client):
    data = {
        'username': 'Alan',
        'password': 'qwerty123',
        'email': 'wtf123@mail.ru',
        'first_name': 'Alan',
        'last_name': 'Amanov',
        'is_student': False,
        'is_teacher': True,
        'is_approved': True,
    }
    response = client.post(reverse_lazy('registration'), data)
    assert response.status_code == 201
    assert Profile.objects.count() == 1
    user = Profile.objects.last()
    assert user.username == 'Alan'
    assert user.email == 'wtf123@mail.ru'
    assert not user.is_approved
    assert user.is_teacher
    assert not user.is_student
    assert response.data == (
        {
            'id': user.id,
            'username': 'Alan',
            'email': 'wtf123@mail.ru',
            'first_name': 'Alan',
            'last_name': 'Amanov',
            'is_student': False,
            'is_teacher': True,
        }
    )


def test_register_student_with_approved_201(db, client):
    data = {
        'username': 'Alan',
        'password': 'qwerty123',
        'email': 'wtf123@mail.ru',
        'first_name': 'Alan',
        'last_name': 'Amanov',
        'is_student': True,
        'is_teacher': False,
        'is_approved': True,
    }
    response = client.post(reverse_lazy('registration'), data)
    assert response.status_code == 201
    assert Profile.objects.count() == 1
    user = Profile.objects.last()
    assert user.username == 'Alan'
    assert user.email == 'wtf123@mail.ru'
    assert not user.is_approved
    assert user.is_student
    assert not user.is_teacher
    assert response.data == (
        {
            'id': user.id,
            'username': 'Alan',
            'email': 'wtf123@mail.ru',
            'first_name': 'Alan',
            'last_name': 'Amanov',
            'is_student': True,
            'is_teacher': False,
        }
    )


def test_register_empty_400(db, client):
    response = client.post(reverse_lazy('registration'), {})
    assert response.status_code == 400
    assert Profile.objects.count() == 0


def test_register_student_and_teacher(db, client):
    data = {
        'username': 'Alan',
        'password': 'qwerty123',
        'email': 'wtf123@mail.ru',
        'first_name': 'Alan',
        'last_name': 'Amanov',
        'is_student': True,
        'is_teacher': True,
    }
    response = client.post(reverse_lazy('registration'), data)
    assert response.status_code == 400
    assert Profile.objects.count() == 0
    assert str(response.data['non_field_errors'][0]) == 'User must be either student or teacher'
