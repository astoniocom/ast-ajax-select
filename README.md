# Description

A set of classes for creating your own select components, as well as django rest-framework fields (for ManyToMany and ForeignKey). Compatible with django.forms and rest-framework.fields.

# Creating your own fields

1. Inherit AjaxSelectFieldMixin
2. Set ajax data source using data_url property

Samples:
ast_ajax_select\ast_ajax_select\rest_framework\fields\AjaxSelectM2MField
ast_ajax_select\ast_ajax_select\rest_framework\fields\AjaxSelectFKField
ast-geo-place\ast_geo_place\rest_framework\fields\GooglePlaceIdField

# Using existing fields for Rest Framework

1. Install and setup django-ajax-selects
2. In your serializer-class, add AjaxSelectFKField or AjaxSelectM2MField with the parameter queryset (which defines possible values) and channel_name (defines the channel name from django-ajax-selects).

---

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