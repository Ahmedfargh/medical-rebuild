from django import forms
class RegisterForm(forms.Form):
    doctor_mail=forms.EmailField(label="email",max_length=32,required=True)
    doctor_name=forms.CharField(label="name",max_length=32,required=True)
    doctor_phone=forms.CharField(label="phone",required=True)
    doctor_password=forms.CharField(label="password",widget=forms.PasswordInput,required=True)
    doctor_password_confirm=forms.CharField(label="password",widget=forms.PasswordInput,required=True)
    doctor_certificate=forms.FileField(label="Upload certificate", required=True)
    doctor_personal_image=forms.FileField(label="perosnal image", required=True)
    def clean(self):
        cleaned_data=super().clean()
        password=cleaned_data.get("doctor_password")
        confirm_password=cleaned_data.get("doctor_password_confirm")
        if password and confirm_password and password!=confirm_password:
            raise forms.ValidationError("password don't match")
        return cleaned_data