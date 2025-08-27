from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from user_app.forms import UserPermissionsForm
from django.shortcuts import get_object_or_404,render,redirect

User = get_user_model()


@login_required
@permission_required('auth.change_permission', raise_exception=True)
def manage_user_permissions(request):
    users = User.objects.all()
    form = None
    selected_user = None

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        if user_id:
            selected_user = get_object_or_404(User, id = user_id)
            form = UserPermissionsForm(request.POST, user = selected_user)

            if form.is_valid():
                selected_user.user_permissions.set(form.cleaned_data['permissions'])
               # permission = form.cleaned_data['permissions']
               # for permission_id in permission:
               #     permission = Permission.objects.get(id =permission_id)
               #     selected_user.user_permissions.add(permission)
                messages.success(request,f'permission for {selected_user} update')
                return redirect('manage_user_permissions')
        
        else:
            form = UserPermissionsForm(user = None)
    else:
        user_id = request.GET.get('user_id')               
        if user_id:
            selected_user = get_object_or_404(User, id = user_id)
            form = UserPermissionsForm(user = selected_user)
        else:
            form = UserPermissionsForm(user = None)

    context = {
        'users':users,
        'selected_user':selected_user,
        'form':form
    }
    return render(request, 'manage_permission.html', context)




