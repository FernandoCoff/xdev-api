from django.urls import path, include
from rest_framework_nested import routers
from .views import PostViewSet, CommentViewSet

# Cria um roteador padrão.
router = routers.DefaultRouter()
# Registra o ViewSet de Posts no roteador. 
# Isso cria automaticamente as URLs para:
# - /posts/ (GET para listar, POST para criar)
# - /posts/{id}/ (GET para detalhes, PUT/PATCH para atualizar, DELETE para apagar)
# - /posts/{id}/like_toggle/ (Nossa ação customizada)
router.register(r'posts', PostViewSet, basename='post')

# Cria um roteador aninhado para os comentários, baseado no roteador principal.
# Isso garante que os comentários sempre estarão associados a um post.
# Ex: /posts/1/comments/
comments_router = routers.NestedSimpleRouter(router, r'posts', lookup='post')
comments_router.register(r'comments', CommentViewSet, basename='post-comments')

# Agrupa todas as URLs geradas pelos roteadores.
urlpatterns = [
    path('', include(router.urls)),
    path('', include(comments_router.urls)),
]
