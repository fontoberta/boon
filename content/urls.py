from django.conf.urls import url, include

from rest_framework.routers import DefaultRouter
from rest_framework_extensions.routers import NestedRouterMixin

from .views import GroupViewSet
from .views import ProjectViewSet
from .views import SectionViewSet
from .views import ImageContentViewSet

from .views import ValidateToken

class NestedDefaultRouter(NestedRouterMixin, DefaultRouter):
    pass

router = NestedDefaultRouter()
group_router = router.register(r'groups', GroupViewSet, base_name='groups')
projects_router = group_router.register(r'projects', ProjectViewSet,
                                        base_name='groups-projects',
                                        parents_query_lookups=['group'])

sections_router = projects_router.register(r'sections',
                                           SectionViewSet,
                                           base_name='groups-projects-sections',
                                           parents_query_lookups=
                                           ['group__project', 'project'])

sections_router.register(r'images', ImageContentViewSet,
                         base_name='groups-projects-sections-images',
                         parents_query_lookups=['group__project',
                                                'project__section',
                                                'section'])

urlpatterns_content = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url(r'validate-token/', ValidateToken.as_view())
]
