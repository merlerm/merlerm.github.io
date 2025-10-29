from typing import Literal

import rendercv.themes.options as o


class Page(o.Page):
    # rendercv 2.3 removed the shared FieldInfo objects; set defaults directly
    show_page_numbering: bool = False


class Header(o.Header):
    name_font_family: o.FontFamily = "Raleway"
    name_bold: bool = False
    alignment: o.Alignment = "left"
    connections_font_family: o.FontFamily = "Raleway"


class Links(o.Links):
    use_external_link_icon: bool = False


class Text(o.Text):
    font_family: o.FontFamily = "Raleway"


class SectionTitles(o.SectionTitles):
    font_family: o.FontFamily = "Raleway"
    bold: bool = False


class Highlights(o.Highlights):
    left_margin: o.TypstDimension = "0cm"


class EducationEntry(o.EducationEntryOptions):
    main_column_first_row_template: str = "**INSTITUTION**, AREA -- LOCATION"
    date_and_location_column_template: str = "DATE"


class NormalEntry(o.NormalEntryOptions):
    main_column_first_row_template: str = "**NAME** -- **LOCATION**"
    date_and_location_column_template: str = "DATE"


class ExperienceEntry(o.ExperienceEntryOptions):
    main_column_first_row_template: str = "**POSITION**, COMPANY -- LOCATION"
    date_and_location_column_template: str = "DATE"


class EntryTypes(o.EntryTypes):
    education_entry: EducationEntry = EducationEntry()
    normal_entry: NormalEntry = NormalEntry()
    experience_entry: ExperienceEntry = ExperienceEntry()


class CustomThemeOptions(o.ThemeOptions):
    theme: Literal["custom"] = "custom"
    page: Page = Page()
    header: Header = Header()
    highlights: Highlights = Highlights()
    text: Text = Text()
    links: Links = Links()
    entry_types: EntryTypes = EntryTypes()
    section_titles: SectionTitles = SectionTitles()
