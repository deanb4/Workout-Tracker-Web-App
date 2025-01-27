from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image

class Exercises(models.Model):
    BW = 'bw'
    WEIGHTED = 'weighted'
    CHOICES = [
        (BW, 'Bodyweight'),
        (WEIGHTED, 'Weighted')
    ]
    PULL = 'pull'
    PUSH_VERT = 'push_v'
    PUSH_HORIZ = 'push_h'
    SQUAT = 'squat'
    DEADLIFT = 'deadlift'
    CORE = 'core'

    MUSLCE_GROUPS = [
        (PULL, 'Back Biceps'),
        (PUSH_VERT, 'shoulders/triceps')
    ]

    LIGHT = '1'
    MODERATE = '2'
    HIGH = '3'
    INTENSITY = [
        (LIGHT,'1'),
        (MODERATE,'2'),
        (HIGH,'3'),
        
    ]
    name = models.CharField(max_length=100)
    muscle_groups = models.CharField(max_length=50, null=True, blank=True)
    type = models.CharField(max_length=50 , choices = CHOICES, default = BW)
    intensity = models.CharField(max_length=1, choices=INTENSITY, default=LIGHT)
    


    def __str__(self):
        return self.name
    
    

class ExerciseList(models.Model):
    workout = models.ForeignKey('Workout', default = None, null= True, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercises, on_delete=models.CASCADE, null=True)
    sets = models.IntegerField(default=1, null=True, blank=True)
    reps = models.IntegerField(default=1, null=True, blank=True)
    weight = models.FloatField(default = 0, null= True, blank = True)

    def __str__(self): 
        if self.weight == 0:
            return f'{self.exercise}- {self.sets} sets X {self.reps} reps'
        else:
            return f'{self.exercise}- {self.sets} sets X {self.reps} reps | weight: {self.weight}kg'


class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercises = models.ManyToManyField(Exercises, through= ExerciseList)
    date = models.DateTimeField(default = timezone.now)
    name = models.CharField(max_length=50, null=True, blank=True)

    # @property
    # def get_user(self):
    #     return self.user
    # @property
    # def get_date(self):
    #     return self.date
    
    def get_name(self):
        if self.name is None:
            name = f'workout- {self.id}'
        else:
            name = self.name

        return name
    
    def __str__(self):
        if self.name is None:
            return f'workout-{self.id} {self.date.strftime("%Y-%m-%d")}'
        else:
            return f'{self.name} {self.date.strftime("%Y-%m-%d")}'



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics', null=True, blank=True)
    # workout = models.ForeignKey('Workout', on_delete=models.SET_NULL, null=True)

    #check what set null actually does
    # workouts = models.ForeignKey(Workout, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
        super().save(*args,**kwargs)
        img = Image.open(self.image.path)
        if img.height >200 or img.width >200:
            output_size = ((200,200))
            img.thumbnail(output_size)
            img.save(self.image.path)