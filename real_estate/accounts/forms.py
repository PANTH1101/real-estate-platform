from django import forms

from .models import Seller


class SellerSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = Seller
        fields = ["name", "email", "phone", "password"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
        }

    def clean(self):
        cleaned = super().clean()
        pwd = cleaned.get("password")
        cpwd = cleaned.get("confirm_password")
        if pwd and cpwd and pwd != cpwd:
            self.add_error("confirm_password", "Passwords do not match.")
        return cleaned


class SellerLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))


class SellerProfileForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = ["name", "phone"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
        }


