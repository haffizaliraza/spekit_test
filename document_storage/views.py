from rest_framework import mixins, viewsets, status
from rest_framework.response import Response

from document_storage.models import Folder, DigitalDocuments, Topics
from document_storage.serializers import FolderSerializer,\
    DigitalDocumentsSerializer, TopicsSerializer


class FolderInformationViewSet(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = FolderSerializer

    def get_queryset(self):
        return Folder.objects.all()

    def get_folder_list(self, request, *args, **kwargs):

        folder_list = []
        for folder in Folder.objects.filter(state=1):
            folder_list.append(
                {
                    'id': folder.id,
                    'folder_name': folder.name,
                    'document_list': [
                        document for document in
                        folder.digital_documents_folder.filter(state=1).values_list(
                            'name',
                            flat=True
                        )]
                }
            )

        return Response(
            {
                'success': True,
                'detail': 'All Folder List',
                'data': folder_list,
            },
            status=status.HTTP_200_OK
        )

    def get(self, request, *args, **kwargs):
        try:
            folder = Folder.objects.filter(
                id=kwargs.get('folder_id')
            ).values_list("name", "id")
            return Response(
                {
                    'success': True,
                    'detail': 'Folder object',
                    'data': folder[0],
                },
                status=status.HTTP_200_OK
            )
        except Exception as IndexError:
            return Response(
                {
                    'success': True,
                    'detail': IndexError,
                },
                status=status.HTTP_200_OK
            )

    def create(self, request, *args, **kwargs):
        request_data = request.data.copy()
        folder_serializer = FolderSerializer(data=request_data)
        if folder_serializer.is_valid():
            folder_obj = folder_serializer.create(request_data)

        else:
            return Response(
                {
                    'success': False,
                    'detail': folder_serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                'success': True,
                'detail': 'Folder information saved successfully',
                'data': folder_obj.id
            },
            status=status.HTTP_201_CREATED
        )


class DigitalDocumentsViewSet(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = DigitalDocumentsSerializer

    def get_queryset(self):
        return DigitalDocuments.objects.filter(state=1)

    def list(self, request, *args, **kwargs):
        digital_document_list = []
        for document in self.get_queryset():
            digital_document_list.append(
                {
                    'id': document.id,
                    'name': document.name
                }
            )
        return Response(
            {
                'success': True,
                'detail': 'All Document List',
                'data': digital_document_list,
            },
            status=status.HTTP_200_OK
        )

    def get_document_list(self, request, *args, **kwargs):
        document_list = []
        folder_id = kwargs.get('folder_id')
        for document in DigitalDocuments.objects.filter(
                state=1,
                folder_id=folder_id
        ).values_list('id', 'name', 'folder_id'):
            document_list.append(
                {
                    'id': document[0],
                    'document_name': document[1],
                    'folder_id': document[2],
                }
            )

        return Response(
            {
                'success': True,
                'detail': 'All Document List',
                'data': document_list,
            },
            status=status.HTTP_200_OK
        )

    def search_document(self, request, *args, **kwargs):

        result = []
        folder_name = request.query_params.get("folder_name")
        topic_name = request.query_params.get("topic")
        for topic in Topics.objects.select_related("folder").filter(
                name=topic_name,
                folder__name=folder_name
        ):
            for document in topic.folder.digital_documents_folder.all():
                result.append({
                    'document_name': document.name,
                    'id': document.id
                })
        return Response(
            {
                'success': True,
                'detail': 'All Document List',
                'data': result,
            },
            status=status.HTTP_200_OK
        )

    def create(self, request, *args, **kwargs):
        request_data = request.data.copy()
        document_serializer = DigitalDocumentsSerializer(data=request_data)
        if document_serializer.is_valid():
            folder_obj = document_serializer.create(request_data)

        else:
            return Response(
                {
                    'success': False,
                    'detail': document_serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                'success': True,
                'detail': 'Document information saved successfully',
                'data': folder_obj.id
            },
            status=status.HTTP_201_CREATED
        )


class TopicsViewSet(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = TopicsSerializer

    def get_queryset(self):
        return Topics.objects.all()

    def get_topic_list(self, request, *args, **kwargs):
        topic_list = []

        for item in Topics.objects.filter(
                state=1
        ).values_list(
            'id',
            'name',
            'folder',
            'document',
            'short_form_descriptors',
            'long_form_descriptors'
        ):
            topic_list.append(
                {
                    'id': item[0],
                    'topic_name': item[1],
                    'folder_id': item[2],
                    'document_id': item[3],
                    'short_form_descriptors': item[4],
                    'long_form_descriptors':  item[5]
                }
            )

        return Response(
            {
                'success': True,
                'detail': 'All Topic List',
                'data': topic_list,
            },
            status=status.HTTP_200_OK
        )

    def create(self, request, *args, **kwargs):
        request_data = request.data.copy()
        parent_id = request_data.get('parent_id')
        parent_type = request_data.get('parent_type')
        topic_serializer = TopicsSerializer(data=request_data)
        parent_flag = True
        if topic_serializer.is_valid():
            topic_obj = topic_serializer.create(request_data)
            if parent_type == "folder":
                try:
                    folder_obj = Folder.objects.get(id=int(parent_id))
                    topic_obj.folder_id = int(parent_id)
                    topic_obj.save()
                except Folder.DoesNotExist:
                    parent_flag = False
            elif parent_type == "document":
                try:
                    folder_obj = DigitalDocuments.objects.get(id=int(parent_id))
                    topic_obj.document = folder_obj
                    topic_obj.save()
                except DigitalDocuments.DoesNotExist:
                    parent_flag = False
            else:
                parent_flag = False
            if not parent_flag:
                topic_obj.delete()
                return Response(
                    {
                        'success': False,
                        'detail': 'Parent Id or Type is not Valid'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        else:
            return Response(
                {
                    'success': False,
                    'detail': topic_serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                'success': True,
                'detail': 'Topic information saved successfully',
                'data': folder_obj.id
            },
            status=status.HTTP_201_CREATED
        )

    def get_folder_topics(self, request, *args, **kwargs):
        folder_id = kwargs.get('folder_id')
        folder_topic_list = []
        for data in Topics.objects.filter(
                state=1,
                folder=folder_id,
                document__isnull=True
        ).values_list('id', 'name', 'folder'):
            folder_topic_list.append(
                {
                    'topic_name': data[1],
                    'folder_id': data[2]

                }
            )
        return Response(
            {
                'success': True,
                'detail': 'All Topic List',
                'data': folder_topic_list,
            },
            status=status.HTTP_200_OK
        )

    def get_document_topics(self, request, *args, **kwargs):
        document_id = kwargs.get('document_id')
        document_topic_list = []
        for data in Topics.objects.filter(
                state=1,
                document=document_id,
                folder__isnull=True
        ).values_list('id', 'name', 'document'):
            document_topic_list.append(
                {
                    'topic_name': data[1],
                    'folder_id': data[2]

                }
            )
        return Response(
            {
                'success': True,
                'detail': 'All Topic List',
                'data': document_topic_list,
            },
            status=status.HTTP_200_OK
        )
