"""
Vistas para la gestión de usuarios del sistema Kaza Stylus.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.contrib import messages
from .models import CustomUser


def _is_admin(user):
    """Verifica si el usuario es Administrador o Superuser."""
    return user.role == 'ADMIN' or user.is_superuser


class ManageUsersView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return _is_admin(self.request.user)

    def get(self, request):
        users = CustomUser.objects.all().order_by('-date_joined')
        roles = CustomUser.ROLE_CHOICES
        # Si viene ?edit=id, cargar datos del usuario a editar
        edit_user = None
        edit_id = request.GET.get('edit')
        if edit_id:
            edit_user = CustomUser.objects.filter(id=edit_id).first()
        context = {
            'users': users,
            'roles': roles,
            'edit_user': edit_user,
        }
        return render(request, 'users/list.html', context)

    def post(self, request):
        action = request.POST.get('action')

        if action == 'add':
            username = request.POST.get('username', '').strip()
            email = request.POST.get('email', '').strip()
            password = request.POST.get('password', '')
            role = request.POST.get('role')
            if username and password:
                CustomUser.objects.create(
                    username=username,
                    email=email,
                    password=make_password(password),
                    role=role
                )
                messages.success(request, f'Usuario "{username}" creado exitosamente.')
            else:
                messages.error(request, 'Usuario y contraseña son obligatorios.')

        elif action == 'edit':
            user_id = request.POST.get('user_id')
            user = get_object_or_404(CustomUser, id=user_id)
            if not user.is_superuser:
                username = request.POST.get('username', '').strip()
                email = request.POST.get('email', '').strip()
                role = request.POST.get('role')
                new_password = request.POST.get('password', '').strip()

                if username:
                    user.username = username
                user.email = email
                user.role = role
                if new_password:
                    user.password = make_password(new_password)
                user.save()
                messages.success(request, f'Usuario "{user.username}" actualizado.')
            else:
                messages.warning(request, 'No se puede editar un superusuario.')

        elif action == 'edit_role':
            user_id = request.POST.get('user_id')
            role = request.POST.get('role')
            user = get_object_or_404(CustomUser, id=user_id)
            user.role = role
            user.save()

        elif action == 'delete':
            user_id = request.POST.get('user_id')
            user = get_object_or_404(CustomUser, id=user_id)
            if not user.is_superuser and user != request.user:
                username = user.username
                user.delete()
                messages.success(request, f'Usuario "{username}" eliminado.')
            else:
                messages.warning(request, 'No se puede eliminar este usuario.')

        return redirect('users_manage')
