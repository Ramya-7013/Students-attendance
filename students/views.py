
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from users.models import StudentProfile
from .forms import StudentProfileForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from courses.models import Course



# def student_profile_view(request):
#     profile = StudentProfile.objects.get(user=request.user)

#     if request.method == 'POST':
#         form = StudentProfileForm(request.POST, request.FILES, instance=profile)

#         # 🔒 Prevent assigning blank course
#         if form.is_valid():
#             # Reassign the original course to prevent ValueError
#             form.instance.course = profile.course
#             form.save()
#             # redirect or show success message
#     else:
#         form = StudentProfileForm(instance=profile)

#     return render(request, 'students/studentprofile_list.html', {
#         'form': form,
#         'student_profile': profile,
#         'user': request.user,
#     })

from django.shortcuts import render
from users.models import StudentProfile
from .forms import StudentProfileForm

def student_profile_view(request):
    profile = StudentProfile.objects.get(user=request.user)

    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
    else:
        form = StudentProfileForm(instance=profile)

    return render(request, 'students/studentprofile_list.html', {  # ✅ Fix the template name
        'form': form,
        'student_profile': profile,
        'user': request.user,
    })


@method_decorator(login_required, name='dispatch')
class StudentProfileListView(ListView):
    model = StudentProfile
    template_name = 'students/studentprofile_list.html'
    context_object_name = 'profiles'

@method_decorator(login_required, name='dispatch')
class StudentProfileDetailView(DetailView):
    model = StudentProfile
    template_name = 'students/studentprofile_detail.html'
    context_object_name = 'profile'

@method_decorator(login_required, name='dispatch')
class StudentProfileCreateView(CreateView):
    model = StudentProfile
    form_class = StudentProfileForm
    template_name = 'students/studentprofile_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user  # Set user automatically
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('students/studentprofile_list')

@method_decorator(login_required, name='dispatch')
class StudentProfileUpdateView(UpdateView):
    model = StudentProfile
    form_class = StudentProfileForm
    template_name = 'students/studentprofile_form.html'

    def get_success_url(self):
        return reverse_lazy('students/studentprofile_list')


@method_decorator(login_required, name='dispatch')
class StudentProfileDeleteView(DeleteView):
    model = StudentProfile
    template_name = 'students/studentprofile_confirm_delete.html'
    success_url = reverse_lazy('students:studentprofile_list')  # note namespace 'students:'


class StudentsByCourseView(ListView):
    model = StudentProfile
    template_name = 'Admin/student_list.html'
    context_object_name = 'students'

    def get_queryset(self):
        course_id = self.request.GET.get('course_id')
        if course_id:
            return StudentProfile.objects.filter(course_id=course_id)
        return StudentProfile.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = Course.objects.all()
        return context