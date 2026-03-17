from typing import Literal

import pydantic

from rendercv.schema.models.base import BaseModelWithoutExtraKeys
from rendercv.schema.models.design.color import Color
from rendercv.schema.models.design.font_family import FontFamily as FontFamilyType
from rendercv.schema.models.design.typst_dimension import TypstDimension

type Bullet = Literal["●", "•", "◦", "-", "◆", "★", "■", "—", "○"]
type BodyAlignment = Literal["left", "justified", "justified-with-no-hyphenation"]
type Alignment = Literal["left", "center", "right"]
type SectionTitleType = Literal[
    "with_partial_line", "with_full_line", "without_line", "moderncv"
]
type PageSize = Literal["a4", "a5", "us-letter", "us-executive"]

length_common_description = (
    "It can be specified with units (cm, in, pt, mm, em). For example, `0.1cm`."
)


class Page(BaseModelWithoutExtraKeys):
    size: PageSize = pydantic.Field(default="a4")
    top_margin: TypstDimension = pydantic.Field(default="1.75cm")
    bottom_margin: TypstDimension = pydantic.Field(default="1.75cm")
    left_margin: TypstDimension = pydantic.Field(default="1.75cm")
    right_margin: TypstDimension = pydantic.Field(default="1.75cm")
    show_footer: bool = pydantic.Field(default=False)
    show_top_note: bool = pydantic.Field(default=True)


color_common_description = (
    "The color can be specified either with their name, hexadecimal value, RGB"
    " value, or HSL value."
)
color_common_examples = ["Black", "7fffd4", "rgb(0,79,144)", "hsl(270, 60%, 70%)"]


class Colors(BaseModelWithoutExtraKeys):
    body: Color = pydantic.Field(
        default=Color("rgb(31, 41, 55)"),
        examples=color_common_examples,
    )
    name: Color = pydantic.Field(
        default=Color("rgb(5, 150, 105)"),
        examples=color_common_examples,
    )
    headline: Color = pydantic.Field(
        default=Color("rgb(5, 150, 105)"),
        examples=color_common_examples,
    )
    connections: Color = pydantic.Field(
        default=Color("rgb(5, 150, 105)"),
        examples=color_common_examples,
    )
    section_titles: Color = pydantic.Field(
        default=Color("rgb(5, 150, 105)"),
        examples=color_common_examples,
    )
    links: Color = pydantic.Field(
        default=Color("rgb(5, 150, 105)"),
        examples=color_common_examples,
    )
    footer: Color = pydantic.Field(
        default=Color("rgb(156, 163, 175)"),
        examples=color_common_examples,
    )
    top_note: Color = pydantic.Field(
        default=Color("rgb(156, 163, 175)"),
        examples=color_common_examples,
    )


class FontFamily(BaseModelWithoutExtraKeys):
    body: FontFamilyType = pydantic.Field(default="Inter")
    name: FontFamilyType = pydantic.Field(default="Datatype")
    headline: FontFamilyType = pydantic.Field(default="Datatype")
    connections: FontFamilyType = pydantic.Field(default="Datatype")
    section_titles: FontFamilyType = pydantic.Field(default="Datatype")


class FontSize(BaseModelWithoutExtraKeys):
    body: TypstDimension = pydantic.Field(default="10pt")
    name: TypstDimension = pydantic.Field(default="30pt")
    headline: TypstDimension = pydantic.Field(default="10pt")
    connections: TypstDimension = pydantic.Field(default="10pt")
    section_titles: TypstDimension = pydantic.Field(default="1.4em")


class SmallCaps(BaseModelWithoutExtraKeys):
    name: bool = pydantic.Field(default=False)
    headline: bool = pydantic.Field(default=False)
    connections: bool = pydantic.Field(default=False)
    section_titles: bool = pydantic.Field(default=False)


class Bold(BaseModelWithoutExtraKeys):
    name: bool = pydantic.Field(default=False)
    headline: bool = pydantic.Field(default=False)
    connections: bool = pydantic.Field(default=False)
    section_titles: bool = pydantic.Field(default=False)


class Typography(BaseModelWithoutExtraKeys):
    line_spacing: TypstDimension = pydantic.Field(default="0.6em")
    alignment: BodyAlignment = pydantic.Field(default="justified")
    date_and_location_column_alignment: Alignment = pydantic.Field(default="right")
    font_family: FontFamily | FontFamilyType = pydantic.Field(
        default_factory=FontFamily,
    )
    font_size: FontSize = pydantic.Field(default_factory=FontSize)
    small_caps: SmallCaps = pydantic.Field(default_factory=SmallCaps)
    bold: Bold = pydantic.Field(default_factory=Bold)

    @pydantic.field_validator(
        "font_family", mode="plain", json_schema_input_type=FontFamily | FontFamilyType
    )
    @classmethod
    def validate_font_family(
        cls, font_family: FontFamily | FontFamilyType
    ) -> FontFamily:
        if isinstance(font_family, str):
            return FontFamily(
                body=font_family,
                name=font_family,
                headline=font_family,
                connections=font_family,
                section_titles=font_family,
            )
        return FontFamily.model_validate(font_family)


class Links(BaseModelWithoutExtraKeys):
    underline: bool = pydantic.Field(default=False)
    show_external_link_icon: bool = pydantic.Field(default=True)


class Connections(BaseModelWithoutExtraKeys):
    phone_number_format: Literal["national", "international", "E164"] = pydantic.Field(
        default="national"
    )
    hyperlink: bool = pydantic.Field(default=True)
    show_icons: bool = pydantic.Field(default=True)
    display_urls_instead_of_usernames: bool = pydantic.Field(default=False)
    separator: str = pydantic.Field(default="")
    space_between_connections: TypstDimension = pydantic.Field(default="0.5cm")


class Header(BaseModelWithoutExtraKeys):
    alignment: Alignment = pydantic.Field(default="left")
    photo_width: TypstDimension = pydantic.Field(default="3.5cm")
    photo_position: Literal["left", "right"] = pydantic.Field(default="left")
    photo_space_left: TypstDimension = pydantic.Field(default="0.4cm")
    photo_space_right: TypstDimension = pydantic.Field(default="0.4cm")
    space_below_name: TypstDimension = pydantic.Field(default="0.7cm")
    space_below_headline: TypstDimension = pydantic.Field(default="0.7cm")
    space_below_connections: TypstDimension = pydantic.Field(default="0.7cm")
    connections: Connections = pydantic.Field(default_factory=Connections)


class SectionTitles(BaseModelWithoutExtraKeys):
    type: SectionTitleType = pydantic.Field(default="with_partial_line")
    line_thickness: TypstDimension = pydantic.Field(default="0.5pt")
    space_above: TypstDimension = pydantic.Field(default="0.5cm")
    space_below: TypstDimension = pydantic.Field(default="0.3cm")


class Sections(BaseModelWithoutExtraKeys):
    allow_page_break: bool = pydantic.Field(default=True)
    space_between_regular_entries: TypstDimension = pydantic.Field(default="1.2em")
    space_between_text_based_entries: TypstDimension = pydantic.Field(default="0.3em")
    show_time_spans_in: list[str] = pydantic.Field(default=[])

    @pydantic.field_validator("show_time_spans_in", mode="after")
    @classmethod
    def convert_section_titles_to_snake_case(cls, value: list[str]) -> list[str]:
        return [s.lower().replace(" ", "_") for s in value]


class Summary(BaseModelWithoutExtraKeys):
    space_above: TypstDimension = pydantic.Field(default="0cm")
    space_left: TypstDimension = pydantic.Field(default="0cm")


class Highlights(BaseModelWithoutExtraKeys):
    bullet: Bullet = pydantic.Field(default="•")
    nested_bullet: Bullet = pydantic.Field(default="•")
    space_left: TypstDimension = pydantic.Field(default="0cm")
    space_above: TypstDimension = pydantic.Field(default="0.25cm")
    space_between_items: TypstDimension = pydantic.Field(default="0.25cm")
    space_between_bullet_and_text: TypstDimension = pydantic.Field(default="0.5em")


class Entries(BaseModelWithoutExtraKeys):
    date_and_location_width: TypstDimension = pydantic.Field(default="4.15cm")
    side_space: TypstDimension = pydantic.Field(default="0.2cm")
    space_between_columns: TypstDimension = pydantic.Field(default="0.1cm")
    allow_page_break: bool = pydantic.Field(default=True)
    short_second_row: bool = pydantic.Field(default=False)
    degree_width: TypstDimension = pydantic.Field(default="1cm")
    summary: Summary = pydantic.Field(default_factory=Summary)
    highlights: Highlights = pydantic.Field(default_factory=Highlights)


class OneLineEntry(BaseModelWithoutExtraKeys):
    main_column: str = pydantic.Field(default="**LABEL:** DETAILS")


class EducationEntry(BaseModelWithoutExtraKeys):
    main_column: str = pydantic.Field(
        default="**INSTITUTION**, AREA -- LOCATION\nSUMMARY\nHIGHLIGHTS"
    )
    degree_column: str | None = pydantic.Field(default="**DEGREE**")
    date_and_location_column: str = pydantic.Field(default="DATE")


class NormalEntry(BaseModelWithoutExtraKeys):
    main_column: str = pydantic.Field(
        default="**NAME** -- **LOCATION**\nSUMMARY\nHIGHLIGHTS"
    )
    date_and_location_column: str = pydantic.Field(default="DATE")


class ExperienceEntry(BaseModelWithoutExtraKeys):
    main_column: str = pydantic.Field(
        default="**POSITION**, COMPANY -- LOCATION\nSUMMARY\nHIGHLIGHTS"
    )
    date_and_location_column: str = pydantic.Field(default="DATE")


class PublicationEntry(BaseModelWithoutExtraKeys):
    main_column: str = pydantic.Field(
        default="**TITLE**\nSUMMARY\nAUTHORS\nURL (JOURNAL)"
    )
    date_and_location_column: str = pydantic.Field(default="DATE")


class Templates(BaseModelWithoutExtraKeys):
    footer: str = pydantic.Field(default="*NAME -- PAGE_NUMBER/TOTAL_PAGES*")
    top_note: str = pydantic.Field(default="*LAST_UPDATED CURRENT_DATE*")
    single_date: str = pydantic.Field(default="MONTH_ABBREVIATION YEAR")
    date_range: str = pydantic.Field(default="START_DATE – END_DATE")
    time_span: str = pydantic.Field(
        default="HOW_MANY_YEARS YEARS HOW_MANY_MONTHS MONTHS"
    )
    one_line_entry: OneLineEntry = pydantic.Field(default_factory=OneLineEntry)
    education_entry: EducationEntry = pydantic.Field(default_factory=EducationEntry)
    normal_entry: NormalEntry = pydantic.Field(default_factory=NormalEntry)
    experience_entry: ExperienceEntry = pydantic.Field(default_factory=ExperienceEntry)
    publication_entry: PublicationEntry = pydantic.Field(
        default_factory=PublicationEntry
    )


class CustomTheme(BaseModelWithoutExtraKeys):
    theme: Literal["custom"] = "custom"
    page: Page = pydantic.Field(default_factory=Page)
    colors: Colors = pydantic.Field(default_factory=Colors)
    typography: Typography = pydantic.Field(default_factory=Typography)
    links: Links = pydantic.Field(default_factory=Links)
    header: Header = pydantic.Field(default_factory=Header)
    section_titles: SectionTitles = pydantic.Field(default_factory=SectionTitles)
    sections: Sections = pydantic.Field(default_factory=Sections)
    entries: Entries = pydantic.Field(default_factory=Entries)
    templates: Templates = pydantic.Field(default_factory=Templates)
