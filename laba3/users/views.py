from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.base import TemplateView
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView

from common.views import TitleMixin
from users.forms import UserLoginForm, UserRegistrationForm


class IndexView(TitleMixin, TemplateView):
    template_name = 'users/index.html'
    title = 'Home'


class UserRegistrationView(TitleMixin, SuccessMessageMixin, CreateView):
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('login')
    success_message = 'Поздравляю! Вы успешно зарегистрировались!'
    title = 'Регистрация'


class UserLoginView(TitleMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'Авторизация'

    def form_valid(self, form):
        # Выполняем аутентификацию пользователя
        login(self.request, form.get_user())

        # Получаем сессию пользователя
        session_key = self.request.session.session_key
        if not session_key:
            # Если сессия пустая, создаем новую
            self.request.session.save()
            session_key = self.request.session.session_key

        # Устанавливаем куки с уникальным значением сессии
        response = super().form_valid(form)
        response.set_cookie('session_token', session_key, secure=True)
        print(session_key)
        return response


class UserLogoutView(LogoutView):

    def dispatch(self, request, *args, **kwargs):
        # Вызываем метод dispatch из базового класса
        response = super().dispatch(request, *args, **kwargs)

        response = HttpResponseRedirect(reverse_lazy('index'))
        response.delete_cookie('session_token')
        # После выхода пользователя перенаправляем на нужный URL
        return response


def user_json_view(request):
    # Получаем текущего пользователя
    user = request.user

    # Проверка наличия cookie "session_token" и аутентификации пользователя
    if ("session_token" in request.COOKIES and user.is_authenticated):
        # Возвращаем данные пользователя в формате JSON
        user_data = {
            "username": user.username,
            "password": user.password,
        }
        return JsonResponse(user_data)
    else:
        # Возвращаем сообщение об ошибке "Unauthorized" в виде JSON
        error_message = {"message": "Unauthorized"}
        return JsonResponse(error_message, status=401)
