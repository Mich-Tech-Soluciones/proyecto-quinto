from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.hashers import make_password
from .models import CustomUser

class ManageUsersView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        # Only admins can manage users
        return self.request.user.role == 'ADMIN' or self.request.user.is_superuser

    def get(self, request):
        users = CustomUser.objects.all().order_by('-date_joined')
        roles = CustomUser.ROLE_CHOICES
        context = {
            'users': users,
            'roles': roles,
        }
        return render(request, 'users/list.html', context)
        
    def post(self, request):
        action = request.POST.get('action')
        
        if action == 'add':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            role = request.POST.get('role')
            if username and password:
                CustomUser.objects.create(
                    username=username,
                    email=email,
                    password=make_password(password),
                    role=role
                )
        elif action == 'edit_role':
            user_id = request.POST.get('user_id')
            role = request.POST.get('role')
            user = get_object_or_404(CustomUser, id=user_id)
            user.role = role
            user.save()
        elif action == 'delete':
            user_id = request.POST.get('user_id')
            user = get_object_or_404(CustomUser, id=user_id)
            if not user.is_superuser:
                user.delete()
                
        return redirect('users_manage')
