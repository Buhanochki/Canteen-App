from django.contrib import admin
from django.urls import path

from core.apps.items.views import (
    AdminItemsListView,
    ItemCreateView,
    ItemDetailedView,
    ItemUpdateView,
    item_delete,
)
from core.apps.purchases.views import PurchasesListView, purchase_delete, PurchaseCreateView, purchase_approve, PurchasesAdminListView

from core.apps.users.views import (
    UserLoginView,
    UserProfile,
    UserProfileUpdate,
    UserRegistration,
    logout_user,
    main_page,
)

from core.apps.meals.views import (
    UserDashboard,
    pay_for_day,
    return_day_payment,
    visit_meal,
    AdminDayDetailView,
    MealCreateView,
    delete_meal,
    prepare_meal,
    UserMealListView,
)

from core.apps.reviews.views import (
    MealReviews,
    ReviewCreate,
    delete_review,
)

from core.apps.ingredients.views import (
    IngredientsListView,
    IngredientsCreateView
)

from core.apps.reports.views import (
    MealReportListView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", logout_user, name="logout"),
    path("", main_page, name="main-page"),
    path("dashboard/admin", AdminItemsListView.as_view(), name="admin-dashboard"),
    path("dashboard/user/day/<str:date>", UserDashboard.as_view(), name="user-dashboard"),
    path("meals/buy/<str:category>/<str:date>", pay_for_day, name='pay'),
    path("meals/return/<str:category>/<str:date>", return_day_payment, name='unpay'),
    path("meals/create/<int:day_pk>/<str:category>", MealCreateView.as_view(), name="meals-create"),
    path("meals/visit/<int:pk>", visit_meal, name="meal-visit"),
    path("meals/delete/<int:pk>", delete_meal, name='meal-delete'),
    path("meals/prepare/<int:pk>", prepare_meal, name="meal-prepare"),
    path("register/", UserRegistration.as_view(), name="register"),
    path("user_profile/", UserProfile.as_view(), name="user-profile"),
    path("user_profile/update_profile", UserProfileUpdate.as_view(), name="update_profile"),
    path("items/create", ItemCreateView.as_view(), name="item-create"),
    path("items/update/<int:pk>", ItemUpdateView.as_view(), name="item-update"),
    path("items/delete/<int:pk>", item_delete, name="item-delete"),
    path("items/item/detailed/<int:pk>", ItemDetailedView.as_view(), name="item-detailed"),
    path("purchases/view", PurchasesListView.as_view(), name="purchase-view"),
    path("purchases/delete/<int:pk>", purchase_delete, name="purchase-delete"),
    path("reviews/meal/<int:pk>", MealReviews.as_view(), name="reviews-view"),
    path("reviews/create/meal/<int:pk>", ReviewCreate.as_view(), name="review-create"),
    path("reviews/delete/<int:pk>", delete_review, name='review-delete'),
    path("days/admin/<str:date>", AdminDayDetailView.as_view(), name="admin-day"),
    path("ingredients/all", IngredientsListView.as_view(), name="ingredients-all"),
    path("reports/meal/<str:date>", MealReportListView.as_view(), name="report-meal"),
    path("purchases/create", PurchaseCreateView.as_view(), name='purchase-create'),
    path("purchases/approve/<int:pk>", purchase_approve, name="purchase-approve"),
    path("purchases/admin/view", PurchasesAdminListView.as_view(), name="purchase-admin"),
    path("ingredients/create", IngredientsCreateView.as_view(), name='ingredients-create'),
    path("abons", UserMealListView.as_view(), name='abons')
]
