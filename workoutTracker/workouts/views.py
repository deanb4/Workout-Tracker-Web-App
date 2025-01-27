from typing import Any, Dict
from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView, DeleteView, UpdateView, CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy,reverse
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from .forms import CreateUser
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView
from django.db.models import Q
from .forms import *
import json
from django.utils import timezone
from datetime import datetime
# from .forms import Create

def home(request):
    return render(request, 'workouts/home.html')

@login_required(login_url='home-page')
def profile(request):
    user = request.user
    exercise_data = ExerciseList.objects.none()
    search_input = request.GET.get('search-area')
    if search_input:
        workouts = Workout.objects.filter(Q(name__icontains=search_input) | Q(date__icontains=search_input),user = user)
    else:
        workouts = Workout.objects.filter(user=user).order_by('-date')[:5]
    
    exercise_name_list = []
    workout = Workout.objects.filter(user=request.user)
    for ex in workout:
        for exercise_list in ex.exercises.through.objects.filter(workout=ex):
            if exercise_list.exercise.name not in exercise_name_list:
                name = exercise_list.exercise.name
                exercise_name_list.append(name)

    max_rep = {}
    dates = {}
    weighted_reps = {}
    # workout = Workout.objects.filter(user=request.user)
    # for w in workout:
    #     for exercise in w.exercises.through.objects.filter(workout=w).order_by('workout'):
         
    for name in exercise_name_list:
        exercise_data = ExerciseList.objects.filter(
            workout__user=request.user,
            exercise__name=name,
            weight = 0
            ).order_by('workout__date')
        exercise_data2 = ExerciseList.objects.filter(
            workout__user=request.user,
            exercise__name=name,
            weight__gt = 0
            ).order_by('workout__date')
        exercise_dates = ExerciseList.objects.filter(
            workout__user=request.user,
            exercise__name=name,
            ).order_by('workout__date')
        
        # dates[name] = []
        # for exercise in exercise_data:
        #     dates[name].append(exercise)
        
        # for exercise in exercise_data2:
        #     for i in dates[name]:
        #         if i.workout.date not in dates[name]:
        #             dates[name].append(exercise)
          
        # for data in exercise_data:
        #     workout_date = data.workout.date  
        # exercise_data_list = [(d.reps, d.weight, d.workout.date) for d in exercise_data2]

        #add dates for data.1 too but make sure to check if they area already in the list. 
        max_rep[name] = (list(exercise_data), list(exercise_data2)) 
        # max_rep[name] = (sorted(list(exercise_data) + list(exercise_data2), key=lambda x: x.workout.date)) 
        dates[name] =  (sorted(list(exercise_data) + list(exercise_data2), key=lambda x: x.workout.date)) 
    new_dates = {}
    for n, data in dates.items():
        new_dates[n] = []
        for d in data:
            workout_date = datetime.strftime(d.workout.date, "%m-%d-%Y")
            if workout_date not in new_dates[n]:
                new_dates[n].append(workout_date)
                # new_dates[n].sort()

    # dates_sorted = {}
    # for name, exercise_data in dates.items():
    #     sorted_data = sorted(exercise_data, key=lambda d: d.workout.date)
    #     dates_sorted[name] = sorted_data
    # new_dates = {}
    # for name ,i in dates.items():
    #     for j in i:
    #         if j not in new_dates:
    #             new_dates[name] = [j for j in i ]

        
        #  [(d.reps, d.weight) for d in exercise_data2])
        # weighted_reps[name]= exercise_data2

    print(new_dates)
    context = {
        "workouts": workouts,
        'profile':Profile.objects.filter(user=user),
        # 'search_input': search_input,
        'workout': workout,
        'exercise_data': exercise_data,
        'max_rep': max_rep,
        'exercise_name_list': exercise_name_list,
        'dates': dates,
        'new_dates': new_dates,
        
        # 'weighted_reps': exercise_data2
        # "workouts": Workout.objects.all()[:5]
    }
    


    
    
    return render(request, 'workouts/profile.html', context)

@login_required(login_url='home-page')
def workout_log(request):
    user = request.user
    search_input = request.GET.get('search-area')
    if search_input:
        workouts = Workout.objects.filter(Q(name__icontains=search_input) | Q(date__icontains=search_input),user = user)
    else:
        workouts = Workout.objects.filter(user=user).order_by('-date')
    # workouts = Workout.objects.all()
    paginator = Paginator(workouts,10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        # "workouts": Workout.objects.all()
        'workouts':page_obj,
        'search_input': search_input
    }
    return render(request, 'workouts/workout_logn.html', context)


def detail(request,pk):
    workout = Workout.objects.get(id=pk)
    context = {
        'exercises': workout.exerciselist_set.all(),
        'workout': workout
         
    }
    return render(request, 'workouts/workout_detail.html', context)

# def redirect_to_previous(request, pk):
#     previous_page = request.META.get('HTTP_REFERER')
#     return redirect(previous_page + f"?pk={pk}")

class RedirectToPreviousMixin:
    def dispatch(self, request, *args, **kwargs):
        request.session['previous_page'] = request.META.get('HTTP_REFERER')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return self.request.session.get('previous_page', '/accounts/profile/')

    def get(self, request, *args, **kwargs):
        return redirect(self.get_success_url())

    # default_redirect = '/accounts/profile/'

    # def get(self, request, *args, **kwargs):
    #     request.session['previous_page'] = request.META.get('HTTP_REFERER', self.default_redirect)
    #     return super().get(request, *args, **kwargs)

    # def get_success_url(self):
    #     return self.request.session.get('previous_page', self.default_redirect)


class WorkoutDelete(DeleteView, LoginRequiredMixin):
        model = Workout
        success_url = '/accounts/profile/'       


class UpdatedView(UpdateView):
    model = Workout
    fields = ['date', 'name']
    template_name = 'workouts/update.html'
    success_url = '/accounts/profile'


class WorkoutDeleteTwo(DeleteView, LoginRequiredMixin):
    model = ExerciseList 

    def get_success_url(self):
        workout_id = self.object.workout.id
        return reverse_lazy('detailed-view', kwargs={'pk': workout_id})


class UpdatedViewTwo(UpdateView):
    model = ExerciseList
    fields = ['sets', 'reps','weight']
    template_name = 'workouts/update.html'
    
    
    def get_success_url(self):
        workout_id = self.object.workout.id
        return reverse_lazy('detailed-view', kwargs={'pk': workout_id})
    

class CreateWorkout(CreateView):
    model =  Workout
    fields = ['date','name']
    # success_url = '/accounts/profile'

    def form_valid(self,form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('detailed-view', kwargs={'pk': self.object.id})

# class CreateExerciseList(CreateView):
#     model =  ExerciseList
#     fields = ['exercise','sets','reps','weight']
#     success_url = '/accounts/profile'

#     def form_valid(self,form):
#         workout_id = self.kwargs['pk']
#         print(workout_id)
#         workout = get_object_or_404(Workout, id=workout_id)

#         form.instance.workout = workout

#         return super().form_valid(form)
    
class CreateExerciseList(CreateView):
    model = ExerciseList
    fields = ['exercise', 'sets', 'reps', 'weight']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        workout_id = self.kwargs['pk']
        context["pk"] = workout_id
        return context
    

    def get_initial(self):
        initial = super().get_initial()
        workout_id = self.kwargs['pk']
        workout = get_object_or_404(Workout, id=workout_id)
        initial['workout'] = workout
        return initial

    def form_valid(self, form):
        form.instance.workout = form.initial['workout']
        return super().form_valid(form)
    

    def get_success_url(self): 
        workout_id = self.kwargs['pk']
        return reverse_lazy('detailed-view', kwargs={'pk': workout_id})
    

def register(request):
    if request.method == 'POST':
        form = CreateUser(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'You have successfully created an account. You can now log in.')
            return redirect('login')
    else:
        form = CreateUser()

    return render(request, 'workouts/register.html', {'form':form})


class CreateBaseExercise(CreateView):
    model = Exercises
    # fields = ['name', 'type']
    form_class = ExerciseForm
    # success_url = '/accounts/profile/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        context['pk'] = pk
        return context
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        exercise_type = self.request.POST.get('type')
        if exercise_type == Exercises.BW:
            form.fields['intensity'].required = True
        else:
            form.fields['intensity'].required = False
        return form

    def get_success_url(self):
         workout = self.kwargs['pk']
         return reverse_lazy('create-exercise', kwargs={'pk': workout})


def updateUser(request):
    user = request.user
    if request.method == 'POST':
        u_form = UserUpdate(request.POST, instance=user)
        p_form = ProfileUpdate(request.POST, request.FILES, instance=user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated')
            return redirect('profile')
        
    else:
        u_form = UserUpdate(instance = user)
        p_form = ProfileUpdate( instance = user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'workouts/update_user.html', context )


class EditorChartView(TemplateView):
    template_name = 'workouts/graph.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Query the exercise data for the logged-in user
        workout = Workout.objects.filter(user=self.request.user)
        exercise_name_list = []
        for ex in workout:
            for exercise_list in ex.exercises.through.objects.filter(workout=ex):
                if exercise_list.exercise.name not in exercise_name_list:
                    name = exercise_list.exercise.name
                    exercise_name_list.append(name)
        
        #workout volume for progress graph( add intensity now )
        workout_volume = []
        for w in workout:
            volume = 0
            for exercise in w.exercises.through.objects.filter(workout=w).order_by('workout'):
                # print(f'sets{exercise.sets} reps {exercise.reps}')
                volume += exercise.sets * exercise.reps
            workout_volume.append(volume)
                        
        #add intensity for bw exercises in db and then add calculation
        workout_intensity = []
        for w in workout:
            intensity = 1
            for exercise in w.exercises.through.objects.filter(workout=w):
                intensity += exercise.weight
            workout_intensity.append(intensity) 
        
        #total_progress list but need to change algorithm
        total_progress = [ workout_intensity[index]*i for index, i in enumerate(workout_volume)]
   
        #add intensity factor to equation
        workout_progress = {}
        for w in workout:
            progress = 0
            for exercise in w.exercises.through.objects.filter(workout=w).order_by('workout'):
                # print(f'sets{exercise.sets} reps {exercise.reps} weight {exercise.weight}')
                if exercise.exercise.type is 'weighted':
                    progress += (exercise.sets * exercise.reps * exercise.weight)/10
                else:
                    if exercise.weight != 0:
                        progress += (exercise.sets * exercise.reps * exercise.weight * int(exercise.exercise.intensity))/10
                    else:
                        progress += exercise.sets * exercise.reps * exercise.weight * int(exercise.exercise.intensity)

                # if exercise.weight != 0:
                #     progress += (exercise.sets * exercise.reps * exercise.weight)/10
                # else:
                #     progress += exercise.sets * exercise.reps
            
            workout_progress[w.date] = progress

        # print(total_progress)
        # add another graph to display reps with weight
        exercise_data_list = {}
        for i in exercise_name_list:
            exercise_data= ExerciseList.objects.filter(
            workout__user=self.request.user,
            exercise__name= i,
            ).order_by('workout__date')

            # data for weighted exercises
            # exercise_data2= ExerciseList.objects.filter(
            # workout__user=self.request.user,
            # exercise__name= i,
            # weight__gt = 0,
            # ).order_by('workout__date')
    
            exercise_data_list[i] = exercise_data
                
        
        print(workout_progress)

        context['exercise_data'] = exercise_data_list
        context['workout']= workout
        context['exercise_name_list']= exercise_name_list
        context['workout_progress'] = workout_progress
        
        return context
    

class ExercisesListView(ListView):
    model = Exercises
    context_object_name = 'exercises'
    template_name = 'workouts/exercises_listview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk']= self.kwargs['pk']
        return context
    

class UpdateExercises(UpdateView):
    model = Exercises
    fields = ['name', 'type']
    template_name = 'workouts/updateExercise.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('exercises-listview', kwargs={'pk': pk})
    

    

class WorkoutDelThree(DeleteView, LoginRequiredMixin):
    model = Exercises

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk']= self.kwargs['pk']
        return context
    

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('exercises-listview', kwargs={'pk': pk})