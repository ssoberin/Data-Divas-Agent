from rest_framework import viewsets
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator

from src.apps.core.models import Worker
from src.apps.api.serializers.worker_serializer import WorkerSerializer


@method_decorator(
    name='list',
    decorator=swagger_auto_schema(operation_summary="Получение списка записей",
                                  tags=["Сотрудники"])
)
@method_decorator(
    name='create',
    decorator=swagger_auto_schema(operation_summary="Создание записи",
                                  tags=["Сотрудники"])
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(
        operation_summary="Изменение данных записи",
        tags=["Сотрудники"]
    )
)
@method_decorator(
    name='destroy',
    decorator=swagger_auto_schema(operation_summary='Удаление сотрудника',
                                  tags=["Сотрудники"])
)
@method_decorator(
    name='retrieve',
    decorator=swagger_auto_schema(operation_summary='Получение сотрудника по ID',
                                  tags=["Сотрудники"])
)
class WorkerViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch']
    serializer_class = WorkerSerializer
    queryset = Worker.objects.all()
