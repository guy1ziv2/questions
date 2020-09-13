from typing import Any
from typing import Dict
from typing import List
from typing import Union
from pydantic import BaseModel
from pydantic import Extra
from pydantic import HttpUrl

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

from . import settings


class Base(BaseModel):
    class Config:

        fields = {
            "kind": "type",
            "all_rows_required": "isAllRowRequired",
            "expression_format": "format",
            "max_value": "max",
            "min_value": "min",
        }

        @classmethod
        def fix_name(cls, name):
            words = name.split("_")
            name = ""
            for index, word in enumerate(words):
                if index == 0:
                    name += word
                else:
                    name += word.capitalize()
            return name

        extra = Extra.allow
        alias_generator = fix_name


class Validator(Base):
    kind: str


class Question(Base):
    kind: str
    name: str = ""
    title: str = ""
    description: str = ""
    is_required: bool = False
    visible: bool = True
    default_value: str = ""
    correct_answer: str = ""
    visible_if: str = ""
    enable_if: str = ""
    start_with_new_line: bool = True
    value_name: str = ""
    required_if: str = ""
    required_error_text: str = ""
    hide_number: bool = True
    indent: int = 0
    title_location: Literal[settings.TITLE_LOCATIONS] = "default"
    description_location: Literal[settings.DESCRIPTION_LOCATIONS] = "default"
    width: str = ""
    max_width: str = "initial"
    min_width: str = "300px"
    use_display_values_in_title: bool = True
    validators: List[Validator] = []
    extra_js: List[HttpUrl] = []
    extra_css: List[HttpUrl] = []


class TextQuestion(Question):
    kind: str = "text"
    place_holder: str = ""
    input_type: Literal[settings.TEXT_INPUT_TYPES] = "text"
    max_length: int = -1
    max_value: str = ""
    min_value: str = ""
    size: int = 0
    step: str = ""
    text_update_mode: Literal[settings.TEXT_UPDATE_MODES] = "default"
    input_mask: str = "none"
    input_format: str = ""
    prefix: str = ""
    auto_unmask: bool = True
    extra_js: List[HttpUrl] = [
        "https://unpkg.com/jquery",
        "https://unpkg.com/inputmask@5.0.3/dist/inputmask.js",
    ]


class ChoicesQuestion(Question):
    kind: str = ""
    col_count: int = 4
    choices: List[Union[str, Dict[str, Union[str, HttpUrl]]]] = []
    choices_by_url: Dict[Literal[settings.CHOICES_BY_URL_KEYS], str] = []
    choices_order: Literal[settings.CHOICE_ORDER_VALUES] = "none"
    choices_enable_if: str = ""
    choices_visible_if: str = ""
    hide_if_choices_empty: bool = True
    has_other: bool = False
    other_text: str = "Other"
    other_error_text: str = ""
    other_place_holder: str = ""
    none_text: str = "None"


class RadioGroupQuestion(ChoicesQuestion):
    kind: str = "radiogroup"
    show_clear_button: bool = False


class DropdownQuestion(ChoicesQuestion):
    kind: str = "dropdown"
    choices_max: int = 0
    choices_min: int = 0
    choices_step: int = 1
    options_caption: str = ""
    show_options_caption: bool = True


class CheckboxQuestion(ChoicesQuestion):
    kind: str = "checkbox"
    has_none: bool = False
    has_select_all: bool = False
    select_all_text: str = ""


class ImagePickerQuestion(ChoicesQuestion):
    kind: str = "imagepicker"
    content_mode: Literal[settings.IMAGE_CONTENT_MODE_VALUES] = "image"
    show_label: bool = False
    image_height: int = 200
    image_width: int = 300
    image_fit: Literal[settings.IMAGE_FIT_VALUES] = "none"
    multi_select: bool = False
    has_other: bool = False
    other_text: str = "Other"
    other_error_text: str = ""
    other_place_holder: str = ""


class BooleanQuestion(Question):
    kind: str = "boolean"
    label_true: str = ""
    label_false: str = ""
    show_title: bool = False
    value_true: str = "true"
    value_false: str = "false"


class SignaturePadQuestion(Question):
    kind: str = "signaturepad"
    height: int = 200
    width: int = 300
    allow_clear: bool = False


class MultipleTextQuestion(Question):
    kind: str = "multipletext"
    col_count: int = 2
    items: List[Dict[str, str]] = []
    item_size: int = 0


class CommentQuestion(Question):
    kind: str = "comment"
    rows: int = 3
    cols: int = 50
    max_length: int = -1
    place_holder: str = ""
    text_update_mode: Literal[settings.TEXT_UPDATE_MODES] = "default"


class RatingQuestion(Question):
    kind: str = "rating"
    min_rate_description: str = ""
    max_rate_description: str = ""
    rate_max: int = 5
    rate_min: int = 1
    rate_step: int = 1
    rate_values: List[Union[int, Dict[str, Union[int, str]]]] = []


class FileQuestion(Question):
    kind: str = "file"
    show_preview: bool = True
    allow_multiple: bool = False
    store_data_as_text: bool = True
    image_height: int = 100
    image_width: int = 150
    max_size: int = 0
    accepted_types: str = ""
    allow_images_preview: bool = True
    need_confirm_remove_file: bool = False
    wait_for_upload: bool = True


class MatrixQuestion(Question):
    kind: str = "matrix"
    columns: List[Dict[Union[int, str], str]]
    rows: List[Dict[Union[int, str], str]]
    all_rows_required: bool = False
    cells: Dict[str, Dict[str, str]]
    columns_visible_if: str = ""
    rows_order: Literal[settings.ROW_ORDER_VALUES]
    rows_visible_if: str = ""
    show_header: bool = True


class MatrixDropdownQuestion(Question):
    kind: str = "matrixdropdown"
    columns: List[Dict[Union[int, str], Any]]
    rows: List[Dict[Union[int, str], str]]
    all_rows_required: bool = False
    cells: Dict[str, Dict[str, Any]]
    columns_visible_if: str = ""
    rows_order: Literal[settings.ROW_ORDER_VALUES]
    rows_visible_if: str = ""
    show_header: bool = True
    cell_type: Literal[settings.MATRIX_CELL_TYPES] = "dropdown"
    choices: List[Any] = []
    column_col_count: int = 1
    column_layout: Literal[settings.MATRIX_COLUMN_LAYOUTS] = "horizontal"
    column_min_width: str = ""
    horizontal_scroll: bool = False
    options_caption: str = ""
    row_title_width: str = ""
    total_text: str = ""


class MatrixDynamicQuestion(Question):
    kind: str = "matrixdynamic"
    columns: List[Dict[Union[int, str], Any]]
    rows: List[Dict[Union[int, str], str]]
    all_rows_required: bool = False
    cells: Dict[str, Dict[str, Any]]
    columns_visible_if: str = ""
    rows_order: Literal[settings.ROW_ORDER_VALUES]
    rows_visible_if: str = ""
    show_header: bool = True
    cell_type: Literal[settings.MATRIX_CELL_TYPES] = "dropdown"
    choices: List[Any] = []
    column_col_count: int = 1
    column_layout: Literal[settings.MATRIX_COLUMN_LAYOUTS] = "horizontal"
    column_min_width: str = ""
    horizontal_scroll: bool = False
    options_caption: str = ""
    add_row_location: Literal[settings.MATRIX_ROW_LOCATIONS] = "default"
    add_row_text: str = ""
    allow_add_rows: bool = True
    allow_remove_rows: bool = True
    confirm_delete: bool = False
    confirm_delete_text: str = ""
    default_row_value: Any = ""
    default_value_from_last_row: bool = False
    key_duplication_error: str = ""
    key_name: str = ""
    max_row_count: int = 100
    min_row_count: int = 1
    remove_row_text: str = ""
    row_count: int = 1


class TagBoxQuestion(DropdownQuestion):
    kind: str = "tagbox"
    select2_config: str = ""
    extra_js: List[HttpUrl] = [
        "https://unpkg.com/jquery",
        "https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.4/js/select2.min.js",
    ]
    extra_css: List[HttpUrl] = [
        "https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.4/css/select2.min.css",
    ]


class JQueryUIDatePickerQuestion(TextQuestion):
    kind: str = "datepicker"
    date_format: str = "mm/dd/yy"
    config: str = ""
    max_date: str = ""
    min_date: str = ""
    extra_js: List[HttpUrl] = [
        "https://unpkg.com/jquery",
        "https://code.jquery.com/ui/1.11.4/jquery-ui.min.js",
    ]
    extra_css: List[HttpUrl] = [
        "https://ajax.googleapis.com/ajax/libs/jqueryui/1.8.18/themes/smoothness/jquery-ui.css",
    ]


class BootstrapDatePickerQuestion(TextQuestion):
    kind: str = "bootstrapdatepicker"
    date_format: str = "mm/dd/yy"
    start_date: str = ""
    end_date: str = ""
    today_highlight: bool = True
    week_start: int = 0
    clear_button: bool = False
    auto_close: bool = True
    days_of_week_highlighted: str = ""
    disable_touch_keyboard: bool = True
    extra_js: List[HttpUrl] = [
        "https://unpkg.com/jquery",
        "https://unpkg.com/moment@2.24.0/moment.js",
        "https://cdnjs.cloudflare.com/ajax/libs/bootstrap-datepicker/1.9.0/js/bootstrap-datepicker.js",
    ]
    extra_css: List[HttpUrl] = [
        "https://unpkg.com/bootstrap@3.3.7/dist/css/bootstrap.min.css",
        "https://cdnjs.cloudflare.com/ajax/libs/bootstrap-datepicker/1.9.0/css/bootstrap-datepicker.min.css",
    ]


class Select2Question(DropdownQuestion):
    render_as: "select2"
    select2_config: str = ""
    extra_js: List[HttpUrl] = [
        "https://unpkg.com/jquery",
        "https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.4/js/select2.min.js",
    ]
    extra_css: List[HttpUrl] = [
        "https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.4/css/select2.min.css",
    ]


class BarRatingQuestion(DropdownQuestion):
    kind: str = "barrating"
    rating_theme: Literal[settings.BAR_RATING_THEMES] = "fontawesome-stars"
    show_values: bool = False
    extra_js: List[HttpUrl] = [
        "https://unpkg.com/jquery",
        "https://unpkg.com/jquery-bar-rating",
    ]
    extra_css: List[HttpUrl] = [
        "https://maxcdn.bootstrapcdn.com/font-awesome/latest/css/font-awesome.min.css",
        "https://unpkg.com/jquery-bar-rating@1.2.2/dist/themes/bars-1to10.css",
        "https://unpkg.com/jquery-bar-rating@1.2.2/dist/themes/bars-movie.css",
        "https://unpkg.com/jquery-bar-rating@1.2.2/dist/themes/bars-pill.css",
        "https://unpkg.com/jquery-bar-rating@1.2.2/dist/themes/bars-reversed.css",
        "https://unpkg.com/jquery-bar-rating@1.2.2/dist/themes/bars-horizontal.css",
        "https://unpkg.com/jquery-bar-rating@1.2.2/dist/themes/fontawesome-stars.css",
        "https://unpkg.com/jquery-bar-rating@1.2.2/dist/themes/css-stars.css",
        "https://unpkg.com/jquery-bar-rating@1.2.2/dist/themes/fontawesome-stars-o.css",
    ]


class SortableJSQuestion(CheckboxQuestion):
    kind: str = "sortablelist"
    empty_text: str = ""
    max_answers_count: int = -1
    extra_js: List[HttpUrl] = [
        "https://unpkg.com/jquery",
        "https://unpkg.com/sortablejs@1.7.0/Sortable.js",
    ]


class NoUISliderQuestion(Question):
    kind: str = "nouislider"
    step: int = 1
    range_min: int = 0
    range_max: int = 100
    pips_mode: str = "positions"
    pips_values: List[int] = [0, 25, 50, 75, 100]
    pips_text: List[Union[int, str]] = [0, 25, 50, 75, 100]
    pips_density: int = 5
    orientation: str = "horizontal"
    direction: str = "ltr"
    tooltips: bool = True
    extra_js: List[HttpUrl] = [
        "https://unpkg.com/jquery",
        "https://unpkg.com/nouislider@9.2.0/distribute/nouislider.js",
        "https://unpkg.com/wnumb@1.1.0",
    ]
    extra_css: List[HttpUrl] = [
        "https://unpkg.com/nouislider@9.2.0/distribute/nouislider.min.css",
    ]


class CKEditorQuestion(Question):
    kind: str = "editor"
    height: str = "300px"
    extra_js: List[HttpUrl] = [
        "https://unpkg.com/jquery",
        "https://cdn.ckeditor.com/4.14.1/standard/ckeditor.js",
    ]


class BootstrapSliderQuestion(Question):
    kind: str = "bootstrpslider"
    step: int = 1
    range_min: int = 0
    range_max: int = 100
    extra_js: List[HttpUrl] = [
        "https://unpkg.com/jquery",
        "https://cdnjs.cloudflare.com/ajax/libs/bootstrap-slider/10.0.0/bootstrap-slider.js",
    ]
    extra_css: List[HttpUrl] = [
        "https://unpkg.com/bootstrap@3.3.7/dist/css/bootstrap.min.css",
        "https://cdnjs.cloudflare.com/ajax/libs/bootstrap-slider/10.0.0/css/bootstrap-slider.css",
    ]


class EmotionsRatingQuestion(DropdownQuestion):
    kind: str = "emotionsratings"
    emotions: List[str] = ["angry", "disappointed", "meh", "happy", "inLove"]
    emotion_size: int = 30
    emotions_count: int = 5
    bg_emotion: str = "happy"
    emotion_color: str = "FF0066"
    extra_js: List[HttpUrl] = [
        "https://unpkg.com/jquery",
        "https://unpkg.com/emotion-ratings@2.0.1/dist/emotion-ratings.js",
    ]


class MicrophoneQuestion(Question):
    kind: str = "microphone"
    extra_js: List[HttpUrl] = [
        "https://www.WebRTC-Experiment.com/RecordRTC.js",
    ]

class HtmlBlock(Question):
    kind: str = "html"
    html: str = ""


class ImageBlock(Question):
    kind: str = "image"
    image_height: int = 200
    image_width: int = 300
    image_fit: Literal[settings.IMAGE_FIT_VALUES] = "none"
    image_link: HttpUrl
    content_mode: Literal[settings.IMAGE_CONTENT_MODE_VALUES] = "image"


class ExpressionBlock(Question):
    kind: str = "expression"
    expression: str
    currency: str = "USD"
    display_style: Literal[settings.EXPRESSION_DISPLAY_STYLES] = "none"
    expression_format: str = ""
    maximum_fraction_digits: int = -1
    minimum_fraction_digits: int = -1
    use_grouping: bool = True


class PanelBlock(Question):
    kind: str = "panel"
    inner_indent: int = 1
    elements: List[Question] = []
    question_start_index: str = ""
    question_title_location: Literal[settings.TITLE_LOCATIONS] = "default"
    show_number: bool = False
    show_question_numbers: Literal[settings.SHOW_QUESTION_NUMBERS_VALUES] = "default"
    state: Literal[settings.PANEL_STATES] = "default"


class PanelDynamicBlock(Question):
    kind: str = "paneldynamic"
    inner_indent: int = 1
    render_mode: Literal[settings.PANEL_RENDER_MODES] = "list"
    panel_count: int = 1
    panel_add_text: str = ""
    panel_remove_text: str = ""
    template_title: str = ""
    template_elements: List[Question] = []
    allow_add_panel: bool = True
    allow_remove_panel: bool = True
    confirm_delete: bool = False
    confirm_delete_text: str = ""
    default_value_from_last_panel: bool = False
    key_duplication_error: str = ""
    key_name: str = ""
    max_panel_count: int = 100
    min_panel_count: int = 1
    panel_add_text: str = ""
    panel_next_text: str = ""
    panel_prev_text: str = ""
    panel_remove_text: str = ""
    panels_state: Literal[settings.PANEL_STATES] = "default"
    show_question_numbers: Literal[settings.SHOW_QUESTION_NUMBERS_VALUES] = "default"
    show_range_in_progress: bool = True
    template_description: str = ""
    template_title_location: Literal[settings.TITLE_LOCATIONS] = "default"


class Page(Base):
    name: str = ""
    title: str = ""
    questions: List[Question] = []
    description: str = ""
    max_time_to_finish: int = 0
    navigation_buttons_visibility: Literal[settings.NAV_BUTTONS_VISIBILITY] = "inherit"
    question_title_location: Literal[settings.TITLE_LOCATIONS] = "default"
    questions_order: Literal[settings.QUESTION_ORDER_VALUES] = "default"


class Survey(Base):
    title: str
    pages: List[Page] = []
    calculated_values: List[Any] = []
    check_errors_mode: Literal[settings.CHECK_ERRORS_MODES] = "onNextPage"
    clear_invisible_values: Literal[settings.CLEAR_INVISIBLE_VALUES] = "onComplete"
    completed_before_html: str = ""
    completed_html: str = ""
    completed_html_on_condition: List[Dict[str, str]] = []
    complete_text: str = ""
    cookie_name: str = ""
    description: str = ""
    edit_text: str = ""
    first_page_is_started: bool = False
    focus_first_question_automatic: bool = True
    focus_on_first_error: bool = True
    go_next_page_automatic: bool = False
    loading_html: str = ""
    locale: Literal[settings.LOCALES] = ""
    logo: HttpUrl = ""
    logo_fit: Literal[settings.IMAGE_FIT_VALUES] = "contain"
    logo_height: int = 200
    logo_position: Literal[settings.LOGO_POSITIONS] = "left"
    logo_width: int = 300
    max_others_length: int = 0
    max_text_length: int = 0
    max_time_to_finish: int = 0
    mode: Literal[settings.SURVEY_MODES] = "edit"
    navigate_to_url: HttpUrl = ""
    navigate_to_url_on_condition: List[Dict[str, HttpUrl]] = []
    page_next_text: str = ""
    page_prev_text: str = ""
    preview_text: str = ""
    progress_bar_type: Literal[settings.PROGRESS_BAR_TYPES] = "pages"
    question_description_location: Literal[
        settings.QUESTION_DESCRIPTION_LOCATIONS
    ] = "underTitle"
    question_error_location: Literal[settings.QUESTION_ERROR_LOCATIONS] = "top"
    questions_on_page_mode: Literal[settings.QUESTION_PAGE_MODES] = "standard"
    questions_order: Literal[settings.QUESTION_ORDER_VALUES] = "initial"
    question_start_index: str = ""
    question_title_location: Literal[settings.TITLE_LOCATIONS] = "top"
    question_title_pattern: str = "numTitleRequire"
    question_title_template: str = ""
    required_text: str = "*"
    send_result_on_page_next: bool = False
    show_completed_page: bool = False
    show_navigation_buttons: Literal[settings.NAV_BUTTONS_POSITIONS] = "bottom"
    show_page_numbers: bool = True
    show_page_titles: bool = True
    show_prev_button: bool = True
    show_preview_before_complete: Literal[settings.SHOW_PREVIEW_VALUES] = "noPreview"
    show_progress_bar: Literal[settings.SHOW_PROGRESS_BAR_OPTIONS] = "off"
    show_question_numbers: Literal[settings.PAGE_SHOW_QUESTION_NUMBERS_VALUES] = "on"
    show_timer_panel: Literal[settings.SHOW_TIMER_VALUES] = "none"
    show_timer_panel_mode: Literal[settings.SHOW_TIMER_MODES] = "all"
    show_title: bool = True
    start_survey_text: str = ""
    store_others_as_comment: bool = True
    survey_id: str = ""
    survey_post_id: str = ""
    survey_show_data_saving: bool = True
    text_update_mode: Literal[settings.TEXT_UPDATE_MODES] = "onBlur"
    triggers: List[Any] = []
