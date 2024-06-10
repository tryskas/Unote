from django.forms import ModelForm, Form, FileField
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import CustomUser


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Identifiant"


def generate_unique_username():
    batch_size = 1000
    last_number = -1
    query_set = CustomUser.objects.filter(
        username__regex=r'^\d+$').values_list('username', flat=True)

    for batch in range(0, query_set.count(), batch_size):
        usernames = query_set[batch:batch + batch_size]
        existing_numbers = sorted(int(username) for username in usernames)

        for number in existing_numbers:
            if number != last_number + 1:
                break
            last_number = number

    new_number = last_number + 1
    return str(new_number).zfill(8)


class CustomUserCreationForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "email", "user_type")
        labels = {
            'user_type': 'Type d\'utilisateur',
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = generate_unique_username()
        password = CustomUser.objects.make_random_password(length=15)
        user.set_password(password)
        if commit:
            user.save()
        return user, password


class CSVUploadForm(Form):
    csv_file = FileField()


class UserProfileForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ["username", "first_name", "last_name", "email", "user_type"]
        labels = {
            'username': 'Identifiant',
            'user_type': 'Type d\'utilisateur',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        user = self.instance

        self.fields['username'].initial = user.username
        self.fields['username'].widget.attrs['readonly'] = True
        self.fields['first_name'].initial = user.first_name
        self.fields['last_name'].initial = user.last_name
        self.fields['email'].initial = user.email
