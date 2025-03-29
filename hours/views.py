from datetime import datetime
from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Project, SpentTime
from .serializers import ProjectSerializer
from rest_framework.views import APIView
from django.db.models import Sum


# CRUD для проектов
class ProjectListCreateView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]


# CRUD для списанного времени
class AddSpentTimeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        project_id = request.data.get("project_id")
        hours = request.data.get("hours")
        date_str = request.data.get("date")

        # Проверка наличия обязательных параметров
        if project_id is None or hours is None or date_str is None:
            return Response(
                {"detail": "Параметры project_id, hours и date обязательны."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Преобразование даты
        try:
            date = datetime.strptime(date_str, "%d.%m.%Y").date()
        except ValueError:
            return Response(
                {"detail": "Неверный формат даты. Используйте DD.MM.YYYY."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Проверка существования проекта
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response(
                {"detail": "Проект не найден."}, status=status.HTTP_404_NOT_FOUND
            )

        # Создание записи о затраченном времени
        spent_time = SpentTime(
            user=request.user, project=project, date=date, hours=hours
        )
        spent_time.save()

        return Response(
            {"detail": "Часы успешно добавлены."}, status=status.HTTP_201_CREATED
        )


# Эндпоинт для отчета
class ReportView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, project_id):
        # Получаем данные из тела запроса
        start_date_str = request.data.get("start_date")
        end_date_str = request.data.get("end_date")

        # Проверка прав доступа
        if not request.user.is_staff and not request.user.is_moderator:
            return Response(
                {"detail": "У вас нет прав доступа."}, status=status.HTTP_403_FORBIDDEN
            )

        # Проверка наличия параметров
        if start_date_str is None or end_date_str is None:
            return Response(
                {"detail": "Параметры start_date и end_date обязательны."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Преобразование строковых дат в объекты datetime
        try:
            start_date = datetime.strptime(start_date_str, "%d.%m.%Y")
            end_date = datetime.strptime(end_date_str, "%d.%m.%Y")
            # Устанавливаем время конца на конец дня
            end_date = end_date.replace(hour=23, minute=59, second=59)
        except ValueError:
            return Response(
                {"detail": "Неверный формат даты. Используйте DD.MM.YYYY."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Получаем проект
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response(
                {"detail": "Проект не найден."}, status=status.HTTP_404_NOT_FOUND
            )

        # Получаем данные о списанном времени
        report_data = (
            SpentTime.objects.filter(
                project=project, date__gte=start_date, date__lt=end_date
            )
            .values("user__id")
            .annotate(hours=Sum("hours"))
        )

        # Формируем ответ
        response_data = [
            {"id": item["user__id"], "hours": item["hours"]} for item in report_data
        ]

        return Response(response_data, status=status.HTTP_200_OK)
