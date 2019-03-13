from django import forms


class RegisterForm(forms.Form):
    username = forms.CharField(
        label="用户名 (仅包含字母、数字与下划线，不超过20字符，区分大小写)",
        required=True,
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            "oninput": "value=value.substr(0,20)"
        }))
    passwd = forms.CharField(
        label="密码 (最少6位)",
        min_length=6,
        max_length=128,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    pw2 = forms.CharField(
        label="确认密码",
        max_length=128,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    stu_code = forms.CharField(
        label="学号 (10位数字)",
        min_length=10,
        max_length=10,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                "oninput": "value=value.replace(/[^\d]/g,'').substr(0,10)"
            }))
    name = forms.CharField(
        label="真实姓名",
        required=True,
        max_length=32,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            "oninput": "value=value.substr(0,32)"
        }))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        has_alpha = False
        for c in username.upper():
            if c == '_' or 'A' <= c <= 'Z':
                has_alpha = True
            elif not '0' <= c <= '9':
                raise forms.ValidationError('包含非法字符 "%s"' % c)
        if len(username) == 10 and not has_alpha:
            raise forms.ValidationError('请勿使用学号作为用户名')
        return username

    def clean_stu_code(self):
        code = self.cleaned_data.get('stu_code')
        if len(code) != 10 or not all('0' <= c <= '9' for c in code):
            raise forms.ValidationError('学号非法')
        return code


class LoginForm(forms.Form):
    username = forms.CharField(
        label="用户名/学号",
        required=True,
        widget=forms.TextInput({
            'class': 'form-control'
        }))
    passwd = forms.CharField(
        label="密码",
        required=True,
        widget=forms.PasswordInput({
            'class': 'form-control'
        }))


class ChangePasswdForm(forms.Form):
    old_passwd = forms.CharField(
        label="原密码",
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_passwd = forms.CharField(
        label="新密码 (最少6位)",
        min_length=6,
        max_length=128,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_pw2 = forms.CharField(
        label="确认新密码",
        max_length=128,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))