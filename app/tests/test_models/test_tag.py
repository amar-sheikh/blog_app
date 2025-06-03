import pytest
from django.core.exceptions import ValidationError
from app.models import Tag

@pytest.mark.django_db
class TestTag:

    def test_creation_with_valid_data(self):
        assert Tag.objects.count() == 0

        tag = Tag.objects.create(
            name='Tag name',
            description='Tag description'
        )
        tag.full_clean()
        assert Tag.objects.count() == 1
        assert (
            tag.name,
            tag.description
        ) == (
            'Tag name',
            'Tag description'
        )

    def test_creation_with_invalid_data(self):
        with pytest.raises(ValidationError) as exception_info:
            tag = Tag.objects.create(
                name='T' * 65,
                description='D' * 256
            )
            tag.full_clean()

        assert 'Ensure this value has at most 64 characters (it has 65).' in exception_info.value.message_dict['name']
        assert 'Ensure this value has at most 255 characters (it has 256).' in exception_info.value.message_dict['description']
