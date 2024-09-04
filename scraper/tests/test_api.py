import logging
import random
import string

import pytest

from app import api_interface


@pytest.mark.asyncio
async def test_status():
    response = await api_interface.Service.get_status()
    print(response)
    assert response.is_success


@pytest.mark.asyncio
async def test_get_data():
    response = await api_interface.Service.get_data()
    print(response)
    assert response.is_success


@pytest.mark.asyncio
async def test_post_data():
    def generate_random_cve():
        return ''.join(random.choice(string.ascii_uppercase) for _ in range(10))

    response = await api_interface.Service.post_data([dict(
        cve_id=f'CVE-{generate_random_cve()}-{_}',
        description='Description',
        title='Title',
        problem_types='TypeOne, TypeTwo, TypeThree',
        published_date='2024-08-28T09:50:36.321Z',
        last_modified_date='2024-08-28T09:50:36.321Z',
    ) for _ in range(10)])
    print(response.text)
    assert response.is_success
