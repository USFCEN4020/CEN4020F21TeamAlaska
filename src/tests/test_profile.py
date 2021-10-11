import pytest
from Profile.Profile import *


@pytest.fixture(scope='module')
def data():
    db = database_access('epic4.sqlite3')
    p = Profile('djirudi', 'dev', 'CS', 'USF', "I'm cool", 'bachelors')
    data = {'profile': p, 'db': db}
    db.execute('''INSERT INTO profile VALUES (?,?,?,?,?,?)''', [
               p.username, p.title, p.major, p.university_name, p.about_me, p.education])
    yield data

    db.delete_profile_table()
    db.close()


def test_get_profile_not_exist(data):
    # data['db'].delete_profile_table()
    unkown_username = 'foo'
    new_profile = getProfile(unkown_username, data['db'])
    match = (
        new_profile.username == unkown_username
        and not new_profile.title
        and not new_profile.major
        and not new_profile.university_name
        and not new_profile.about_me
        and not new_profile.education
    )
    assert match


def test_get_profile_exists(data):
    p = data['profile']
    existing_profile = getProfile(p.username, data['db'])
    match = (
        existing_profile.username == p.username
        and existing_profile.title == p.title
        and existing_profile.major == p.major
        and existing_profile.university_name == p.university_name
        and existing_profile.about_me == p.about_me
        and existing_profile.education == p.education
    )
    assert match


def test_set_title(data):
    p = data['profile']
    p.title = 'woho'
    p.set_title(p.title, data['db'])

    updated_title = data['db'].execute(
        '''SELECT title FROM profile WHERE username = ?''', [p.username])
    match = (
        updated_title[0][0] == p.title
    )
    assert match


def test_set_major(data):
    p = data['profile']
    p.major = 'philosophy'
    p.set_major(p.major, data['db'])

    updated_title = data['db'].execute(
        '''SELECT major FROM profile WHERE username = ?''', [p.username])
    match = (
        updated_title[0][0] == p.major
    )
    assert match


def test_set_university_name(data):
    p = data['profile']
    p.university_name = 'UT'
    p.set_university_name(p.university_name, data['db'])

    updated_title = data['db'].execute(
        '''SELECT university_name FROM profile WHERE username = ?''', [p.username])
    match = (
        updated_title[0][0] == p.university_name
    )
    assert match


def test_set_about_me(data):
    p = data['profile']
    p.about_me = "I'm great!"
    p.set_about_me(p.about_me, data['db'])

    updated_title = data['db'].execute(
        '''SELECT about_me FROM profile WHERE username = ?''', [p.username])
    match = (
        updated_title[0][0] == p.about_me
    )
    assert match


def test_set_education(data):
    p = data['profile']
    p.education = 'phd'
    p.set_education(p.education, data['db'])

    updated_title = data['db'].execute(
        '''SELECT education FROM profile WHERE username = ?''', [p.username])
    match = (
        updated_title[0][0] == p.education
    )
    assert match


def test_isComplete_true(data):
    p = data['profile']
    complete = p.isComplete()
    assert complete


def test_isComplete_false(data):
    p = data['profile']
    p.education = None
    complete = p.isComplete()
    assert not complete
