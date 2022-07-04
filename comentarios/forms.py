from django.forms import ModelForm
from .models import Comentario


class FormComentario(ModelForm):
    # Para validar o formulario
    def clean(self):
        # pegar os dados do formulario
        data = self.cleaned_data
        nome = data.get('nome_comentario')
        email = data.get('email_comentario')
        comentario = data.get('comentario')

        if len(nome) < 5:
            self.add_error(
                'nome_comentario',
                'Nome precisa ter mais que 5 caracteres'
            )

    class Meta:
        model = Comentario
        # if form should contain all fields from model
        # fields = '__all__'
        fields = ('nome_comentario', 'email_comentario', 'comentario')
