from re import template
from typing import List
from django.db import models
from django.db.models.fields.related import ForeignKey
from django.db.models.query import QuerySet
from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from django.views.generic.edit import ModelFormMixin, UpdateView
from categorias.models import Categoria
from comentarios.models import Comentario
from posts.models import Post
from django.db.models import Q, Count, Case, When
from comentarios.forms import FormComentario
from comentarios.models import Comentario
from django.contrib import messages


class PostIndex(ListView):
    model = Post
    template_name = 'posts/index.html'
    paginate_by = 6
    context_object_name = 'posts'

    # alterar a query dos posts
    def get_queryset(self):
        qs = super().get_queryset()
        # para ordenar os posts por ordem invertida de ID
        # e filtar só por posts publicados
        qs = qs.order_by('-id').filter(publicado_post=True)

        # consultar numero de comentários por post
        qs = qs.annotate(
            # cria uma variavel para contar comentarios
            numero_comentarios=Count(
                # somente conta caso esteja publicado
                Case(
                    # da tabela comentario o item comentario publicado
                    # se for true, conta 1
                    When(comentario__publicado_comentario=True, then=1)
                )
            )
        )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # cat = Categoria.objects.raw('SELECT * FROM categorias_categoria')

        # recupera primeiros 4
        catFirst = Categoria.objects.all()[:4]
        # recupera o restante se tiver
        catLast = Categoria.objects.all()[4:]

        context["categoriesIni"] = catFirst
        context["categoriesFim"] = catLast
        return context


class PostBusca(PostIndex):
    template_name = 'posts/post_busca.html'

    def get_queryset(self):
        qs = super().get_queryset()

        print(f'Argumentos recebidos do campo busca: {self.request.GET}')
        print(f'Recuperando o campo termo: {self.request.GET.get("termo")}')
        termo = self.request.GET.get("termo")

        if not termo:
            return qs

        qs = qs.filter(
            Q(titulo_post__icontains=termo) |
            Q(autor_post__first_name__iexact=termo) |
            Q(conteudo_post__icontains=termo) |
            Q(excerto_post__icontains=termo) |
            Q(categoria_post__nome_cat__iexact=termo)
        )

        return qs


class PostCategoria(PostIndex):
    template_name = 'posts/post_categoria.html'

    def get_queryset(self):
        # o super abaixo é o PostIndex de qual a classe herdou.
        # isso é feito para nao perder a query feita na classe acima
        qs = super().get_queryset()

        # pega o argumento passado com post_categoria no _nav.html
        categoria = self.kwargs.get('categoria')

        # query abaixo explicada:
        #     - categoria_post é ForeignKey da tabela Categoria
        #     - que tem o campo nome_cat
        #     - iexact = exatamente (i = case sensitive)
        #     - entao pega nome_cat relacionado a categoria_post
        qs = qs.filter(categoria_post__nome_cat__iexact=categoria)

        return qs


class PostDetalhes(UpdateView):
    model = Post
    template_name = 'posts/post_detalhes.html'
    # if form should contain all fields from model
    #fields = '__all__'

    # criado um formulario de comentarios (no comentarios/forms.py) e importado
    form_class = FormComentario
    #context_object_name = 'post'

    # funçao para filrar somente comentarios publicados
    #       e comentarios do post correto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        comentarios = Comentario.objects.filter(publicado_comentario=True,
                                                post_comentario=post.id)

        context['comentarios'] = comentarios
        return context

    # funçao que altera valores a serem salvos na base de dados e salva

    def form_valid(self, form):
        post = self.get_object()
        # coloca todos os valores no formulario na variavel comentario
        comentario = Comentario(**form.cleaned_data)

        # insere outros valores:
        comentario.post_comentario = post
        # se usuario logado usa este usuario. se nao, deixa em branco
        if self.request.user.is_authenticated:
            comentario.usuario_comentario = self.request.user

        comentario.save()
        messages.success(self.request, 'Comentário enviado com suscesso.')
        return redirect('post_detalhes', pk=post.id)


class PostEkbTeste(ListView):
    model = Post
    template_name = 'posts/post_testes.html'
