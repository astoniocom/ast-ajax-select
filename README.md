# Описание

Набор базовых классов для создания собственных ajax-select-компонентов, а так же django rest-framework поля для работы с ManyToMane и ForeignKey. За основу взята библиотека django-ajax-selects.
Совместима с django.forms и rest-framework.fields.

# Использование в качестве основы для создания своих собственных полей выбора

1. Наследуем AjaxSelectFieldMixin
2. Устанавливаем источник ajax-данных через свойство класса data_url

Пример работы с библиотекой можно посмотреть здесь: 

1. ast_ajax_select\ast_ajax_select\rest_framework\fields\AjaxSelectM2MField
2. ast_ajax_select\ast_ajax_select\rest_framework\fields\AjaxSelectFKField
3. ast-geo-place\ast_geo_place\rest_framework\fields\GooglePlaceIdField

# Использование входящих в стостав полей выбора для Rest Framework

1. Установить и настроить django-ajax-selects
2. В вашем serializer-class добавить поле AjaxSelectFKField или AjaxSelectM2MField с параметрами queryset (определяет доступные значения) и channel_name (определяет имя канала из библиотеки django-ajax-selects)