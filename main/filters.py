from admin_auto_filters.filters import AutocompleteFilter


class CustomAuthorFilter(AutocompleteFilter):
    title = "Автор"
    field_name = "author"


class CustomPostFilter(AutocompleteFilter):
    title = "Пост"
    field_name = "post"
