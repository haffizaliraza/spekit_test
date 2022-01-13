from rest_framework import serializers

from document_storage.models import Folder, DigitalDocuments, Topics


class FolderSerializer(serializers.Serializer):

    class Meta:
        model = Folder
        fields = ('name', 'id', 'state')
        read_only_fields = ('created', 'modified')

    def create(self, validated_data):
        folder_obj = Folder()
        folder_obj.name = validated_data.get('name')
        folder_obj.state = 1
        folder_obj.save()
        return folder_obj


class DigitalDocumentsSerializer(serializers.Serializer):

    class Meta:
        model = DigitalDocuments
        fields = ('name', 'id', 'folder')
        read_only_fields = ('created', 'modified')

    def create(self, validated_data):
        folder_obj = DigitalDocuments()
        folder_obj.folder_id = validated_data.get('folder_id')
        folder_obj.name = validated_data.get('name')
        folder_obj.state = 1
        folder_obj.save()
        return folder_obj


class TopicsSerializer(serializers.Serializer):

    class Meta:
        model = Topics
        fields = ('id', 'name', 'folder', 'document', 'short_form_descriptors', 'long_form_descriptors')
        read_only_fields = ('created', 'modified')

    def create(self, validated_data):
        topic_obj = Topics()
        topic_obj.name = validated_data.get('name')
        topic_obj.state = 1
        topic_obj.save()
        return topic_obj