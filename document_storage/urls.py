from django.urls import re_path

from document_storage.views import FolderInformationViewSet, DigitalDocumentsViewSet, TopicsViewSet

urlpatterns = [
    re_path(r'^$', FolderInformationViewSet.as_view({'get': 'get_folder_list'})),
    re_path(r'^folders/$', FolderInformationViewSet.as_view({'get': 'get_folder_list', 'post': 'create'})),
    re_path(r'^folders/(?P<folder_id>\d+)/$', FolderInformationViewSet.as_view({'get': 'get', 'put': 'update'})),
    re_path(r'^documents/(?P<folder_id>\d+)/$', DigitalDocumentsViewSet.as_view(
        {'get': 'get_document_list', 'post': 'create'}
    )),
    re_path(r'^documents/$', DigitalDocumentsViewSet.as_view(
        {'get': 'list'}
    )),
    re_path(r'^documents/search/$', DigitalDocumentsViewSet.as_view(
        {'get': 'search_document'}
    )),
    re_path(r'^topics/$', TopicsViewSet.as_view(
        {'get': 'get_topic_list', 'post': 'create'}
    )),
    re_path(r'^documents/(?P<document_id>\d+)/topics/$', TopicsViewSet.as_view(
        {'get': 'get_document_topics'}
    )),
    re_path(r'^folders/(?P<folder_id>\d+)/topics/$', TopicsViewSet.as_view(
        {'get': 'get_folder_topics'}
    )),

]
